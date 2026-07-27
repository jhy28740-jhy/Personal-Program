"""
批量文件处理工具 - Demo版
功能：批量处理图片（压缩、裁剪、加水印、格式转换）
作者：数据服务工作室
"""

import os
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont
import json


class BatchImageProcessor:
    def __init__(self, config_file='config.json'):
        """初始化批量处理器"""
        self.config_file = config_file
        self.load_config()

    def load_config(self):
        """加载配置"""
        default_config = {
            "input_folder": "输入图片",
            "output_folder": "输出图片",
            "operations": {
                "compress": True,
                "quality": 85,
                "resize": False,
                "target_width": 1920,
                "target_height": 1080,
                "watermark": False,
                "watermark_text": "© 2024 我的品牌",
                "convert_format": None
            }
        }

        if os.path.exists(self.config_file):
            with open(self.config_file, 'r', encoding='utf-8') as f:
                self.config = json.load(f)
        else:
            self.config = default_config
            self.save_config()

    def save_config(self):
        """保存配置"""
        with open(self.config_file, 'w', encoding='utf-8') as f:
            json.dump(self.config, f, ensure_ascii=False, indent=2)

    def create_folders(self):
        """创建输入输出文件夹"""
        os.makedirs(self.config['input_folder'], exist_ok=True)
        os.makedirs(self.config['output_folder'], exist_ok=True)

    def get_image_files(self):
        """获取所有图片文件"""
        input_folder = self.config['input_folder']
        extensions = ['.jpg', '.jpeg', '.png', '.bmp', '.gif', '.webp']

        files = []
        for ext in extensions:
            files.extend(Path(input_folder).glob(f'*{ext}'))
            files.extend(Path(input_folder).glob(f'*{ext.upper()}'))

        return files

    def compress_image(self, img, quality):
        """压缩图片"""
        return img, quality

    def resize_image(self, img, target_width, target_height):
        """调整图片尺寸（保持比例）"""
        original_width, original_height = img.size
        ratio = min(target_width / original_width, target_height / original_height)

        if ratio < 1:  # 只缩小，不放大
            new_width = int(original_width * ratio)
            new_height = int(original_height * ratio)
            img = img.resize((new_width, new_height), Image.Resampling.LANCZOS)

        return img

    def add_watermark(self, img, text):
        """添加水印"""
        # 创建透明图层
        watermark = Image.new('RGBA', img.size, (255, 255, 255, 0))
        draw = ImageDraw.Draw(watermark)

        # 使用默认字体
        try:
            # Windows系统
            font_path = "C:/Windows/Fonts/arial.ttf"
            if not os.path.exists(font_path):
                # Mac/Linux系统
                font_path = "/System/Library/Fonts/Supplemental/Arial.ttf"
            font = ImageFont.truetype(font_path, 40)
        except:
            font = ImageFont.load_default()

        # 计算文本位置（右下角）
        bbox = draw.textbbox((0, 0), text, font=font)
        text_width = bbox[2] - bbox[0]
        text_height = bbox[3] - bbox[1]

        margin = 20
        x = img.width - text_width - margin
        y = img.height - text_height - margin

        # 绘制半透明白色背景
        draw.rectangle(
            [x - 10, y - 5, x + text_width + 10, y + text_height + 5],
            fill=(255, 255, 255, 180)
        )

        # 绘制黑色文字
        draw.text((x, y), text, fill=(0, 0, 0, 255), font=font)

        # 合并图层
        if img.mode != 'RGBA':
            img = img.convert('RGBA')
        img = Image.alpha_composite(img, watermark)

        return img

    def process_image(self, file_path):
        """处理单张图片"""
        try:
            # 打开图片
            img = Image.open(file_path)

            # 转换为RGB（处理透明背景）
            if img.mode in ('RGBA', 'LA', 'P'):
                background = Image.new('RGB', img.size, (255, 255, 255))
                if img.mode == 'P':
                    img = img.convert('RGBA')
                background.paste(img, mask=img.split()[-1] if img.mode == 'RGBA' else None)
                img = background

            # 调整尺寸
            if self.config['operations']['resize']:
                img = self.resize_image(
                    img,
                    self.config['operations']['target_width'],
                    self.config['operations']['target_height']
                )

            # 添加水印
            if self.config['operations']['watermark']:
                img = self.add_watermark(img, self.config['operations']['watermark_text'])

            # 确定输出格式
            output_format = self.config['operations'].get('convert_format')
            if output_format:
                output_ext = f'.{output_format.lower()}'
            else:
                output_ext = file_path.suffix

            # 生成输出文件名
            output_filename = file_path.stem + output_ext
            output_path = os.path.join(self.config['output_folder'], output_filename)

            # 保存图片
            save_kwargs = {}
            if self.config['operations']['compress']:
                save_kwargs['quality'] = self.config['operations']['quality']
                save_kwargs['optimize'] = True

            # 转回RGB保存
            if img.mode == 'RGBA' and output_ext.lower() in ['.jpg', '.jpeg']:
                img = img.convert('RGB')

            img.save(output_path, **save_kwargs)

            # 计算文件大小
            original_size = os.path.getsize(file_path)
            processed_size = os.path.getsize(output_path)
            compression_ratio = (1 - processed_size / original_size) * 100

            return {
                'success': True,
                'filename': file_path.name,
                'original_size': original_size,
                'processed_size': processed_size,
                'compression_ratio': compression_ratio
            }

        except Exception as e:
            return {
                'success': False,
                'filename': file_path.name,
                'error': str(e)
            }

    def create_sample_images(self):
        """创建示例图片"""
        print("创建示例图片...")
        input_folder = self.config['input_folder']

        for i in range(3):
            # 创建彩色渐变图片
            img = Image.new('RGB', (1920, 1080), color=(50 + i*50, 100 + i*30, 200 - i*40))
            draw = ImageDraw.Draw(img)

            # 添加文字
            text = f"示例图片 {i+1}"
            font_size = 100
            try:
                font_path = "C:/Windows/Fonts/simhei.ttf"
                if not os.path.exists(font_path):
                    font_path = "C:/Windows/Fonts/arial.ttf"
                font = ImageFont.truetype(font_path, font_size)
            except:
                font = ImageFont.load_default()

            # 居中文字
            bbox = draw.textbbox((0, 0), text, font=font)
            text_width = bbox[2] - bbox[0]
            text_height = bbox[3] - bbox[1]
            x = (1920 - text_width) // 2
            y = (1080 - text_height) // 2

            draw.text((x, y), text, fill=(255, 255, 255), font=font)

            # 保存
            img.save(os.path.join(input_folder, f'示例图片_{i+1}.jpg'), quality=95)

        print(f"[OK] 已创建3张示例图片到 {input_folder}/ 文件夹")

    def process_all(self):
        """批量处理所有图片"""
        print("=" * 60)
        print("批量图片处理工具 v1.0")
        print("=" * 60)

        # 创建文件夹
        self.create_folders()

        # 获取图片列表
        image_files = self.get_image_files()

        if not image_files:
            print(f"\n[!] 未在 {self.config['input_folder']}/ 找到图片文件")
            print("正在创建示例图片...")
            self.create_sample_images()
            image_files = self.get_image_files()

        print(f"\n找到 {len(image_files)} 张图片待处理")
        print(f"输出文件夹: {self.config['output_folder']}/\n")

        # 处理每张图片
        results = []
        for idx, file_path in enumerate(image_files, 1):
            print(f"[{idx}/{len(image_files)}] 处理中: {file_path.name}", end=' ... ')
            result = self.process_image(file_path)

            if result['success']:
                print(f"[OK] 完成 (压缩 {result['compression_ratio']:.1f}%)")
            else:
                print(f"[X] 失败: {result['error']}")

            results.append(result)

        # 统计
        success_count = sum(1 for r in results if r['success'])
        total_original = sum(r.get('original_size', 0) for r in results if r['success'])
        total_processed = sum(r.get('processed_size', 0) for r in results if r['success'])

        print("\n" + "=" * 60)
        print("[OK] 处理完成！")
        print(f"成功: {success_count}/{len(image_files)}")
        if total_original > 0:
            overall_compression = (1 - total_processed / total_original) * 100
            print(f"总大小: {total_original / 1024 / 1024:.2f} MB → {total_processed / 1024 / 1024:.2f} MB")
            print(f"整体压缩率: {overall_compression:.1f}%")
        print("=" * 60)


if __name__ == "__main__":
    processor = BatchImageProcessor()
    processor.process_all()
