"""
电商竞品价格监控系统 - Demo版
功能：自动抓取竞品信息并生成Excel对比报表
作者：数据服务工作室
"""

import pandas as pd
from datetime import datetime
import json
import os

class CompetitorMonitor:
    def __init__(self, config_file='config.json'):
        """初始化监控系统"""
        self.config_file = config_file
        self.load_config()

    def load_config(self):
        """加载配置文件"""
        if os.path.exists(self.config_file):
            with open(self.config_file, 'r', encoding='utf-8') as f:
                self.config = json.load(f)
        else:
            # 默认配置（Demo数据）
            self.config = {
                "products": [
                    {
                        "name": "竞品A - 无线蓝牙耳机",
                        "url": "https://example.com/product-a",
                        "price": 299.00,
                        "sales": 2850,
                        "rating": 4.8
                    },
                    {
                        "name": "竞品B - 无线蓝牙耳机",
                        "url": "https://example.com/product-b",
                        "price": 259.00,
                        "sales": 3200,
                        "rating": 4.6
                    },
                    {
                        "name": "竞品C - 无线蓝牙耳机",
                        "url": "https://example.com/product-c",
                        "price": 399.00,
                        "sales": 1500,
                        "rating": 4.9
                    }
                ],
                "alert_price_change": 10  # 价格变动超过10%时提醒
            }
            self.save_config()

    def save_config(self):
        """保存配置文件"""
        with open(self.config_file, 'w', encoding='utf-8') as f:
            json.dump(self.config, f, ensure_ascii=False, indent=2)

    def fetch_prices(self):
        """
        抓取竞品价格
        注：真实版本会调用爬虫API，Demo版使用模拟数据
        """
        print("正在抓取竞品数据...")

        # Demo: 模拟价格波动
        import random
        data = []
        for product in self.config['products']:
            # 模拟小幅价格变动
            price_change = random.uniform(-0.05, 0.05)
            new_price = round(product['price'] * (1 + price_change), 2)

            # 模拟销量增长
            sales_change = random.randint(-50, 200)
            new_sales = max(0, product['sales'] + sales_change)

            data.append({
                '商品名称': product['name'],
                '当前价格': new_price,
                '原价格': product['price'],
                '价格变动': f"{((new_price - product['price']) / product['price'] * 100):.2f}%",
                '销量': new_sales,
                '评分': product['rating'],
                '链接': product['url'],
                '更新时间': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            })

            # 检查价格变动预警
            price_change_pct = abs((new_price - product['price']) / product['price'] * 100)
            if price_change_pct > self.config['alert_price_change']:
                print(f"[!] 价格预警: {product['name']} 价格变动 {price_change_pct:.1f}%")

        print(f"[OK] 成功抓取 {len(data)} 个竞品数据")
        return data

    def generate_report(self, data, output_file='竞品价格报表.xlsx'):
        """生成Excel报表"""
        print(f"正在生成报表: {output_file}")

        df = pd.DataFrame(data)

        # 创建Excel writer
        with pd.ExcelWriter(output_file, engine='openpyxl') as writer:
            df.to_excel(writer, sheet_name='价格监控', index=False)

            # 获取工作表
            worksheet = writer.sheets['价格监控']

            # 调整列宽
            for idx, col in enumerate(df.columns, 1):
                max_length = max(
                    df[col].astype(str).map(len).max(),
                    len(col)
                ) + 2
                worksheet.column_dimensions[chr(64 + idx)].width = min(max_length, 50)

        print(f"[OK] 报表已生成: {output_file}")
        return output_file

    def add_history(self, data):
        """追加历史数据"""
        history_file = '价格历史.xlsx'

        df_new = pd.DataFrame(data)

        if os.path.exists(history_file):
            df_old = pd.read_excel(history_file)
            df_combined = pd.concat([df_old, df_new], ignore_index=True)
        else:
            df_combined = df_new

        df_combined.to_excel(history_file, index=False)
        print(f"[OK] 历史数据已更新: {history_file}")

    def run(self):
        """执行监控任务"""
        print("=" * 50)
        print("竞品价格监控系统 v1.0")
        print("=" * 50)

        # 1. 抓取数据
        data = self.fetch_prices()

        # 2. 生成报表
        report_file = self.generate_report(data)

        # 3. 追加历史
        self.add_history(data)

        print("\n" + "=" * 50)
        print("[OK] 监控任务完成！")
        print(f"查看报表: {report_file}")
        print("=" * 50)


if __name__ == "__main__":
    monitor = CompetitorMonitor()
    monitor.run()
