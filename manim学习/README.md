# 📐 数学可视化教学视频集

用 [Manim](https://www.manim.community/) 创作的动态数学教学动画。

## 🎬 作品列表

### 1️⃣ 函数的奇偶性
- **内容**：完整讲解偶函数（y轴对称）与奇函数（原点对称）
- **案例**：f(x)=x²（偶函数）、f(x)=x³（奇函数）
- **时长**：约 30 秒
- **适用**：高中数学、函数性质教学

### 2️⃣ 傅里叶级数画心形
- **内容**：用 15 个旋转圆叠加绘制心形曲线
- **原理**：傅里叶级数的几何可视化
- **时长**：约 8 秒
- **适用**：高等数学、复变函数、科普

### 3️⃣ 勾股定理（测试版）
- **内容**：3-4-5 直角三角形演示
- **时长**：约 5 秒
- **适用**：初中数学

## 🛠️ 技术栈

- **Manim Community** v0.20.1
- **Python** 3.13
- **FFmpeg** 视频渲染
- **分辨率**：1080p60fps

## 🚀 本地运行

```bash
# 安装依赖
pip install manim imageio-ffmpeg

# 渲染视频（高清）
python -m manim -qh demo3_函数奇偶性.py FunctionParity

# 渲染视频（预览）
python -m manim -ql demo3_函数奇偶性.py FunctionParity
```

## 📂 项目结构

```
manim学习/
├── demo1_勾股定理.py          # 勾股定理脚本
├── demo2_傅里叶画图.py        # 傅里叶级数脚本
├── demo3_函数奇偶性.py        # 函数奇偶性脚本
├── 成品视频/                  # 渲染完成的视频
│   ├── 00_勾股定理_测试版.mp4
│   ├── 01_傅里叶级数画心形_高清.mp4
│   └── 02_函数奇偶性教学_高清.mp4
├── index.html                 # 在线展示页面
└── README.md                  # 本文档
```

## 🌐 在线观看

访问 [GitHub Pages](https://jhy28740-jhy.github.io/Personal-Program/) 在线观看所有视频。

## 📝 作者

- **GitHub**: [@jhy28740-jhy](https://github.com/jhy28740-jhy)
- **邮箱**: jhy28740@gmail.com

## 📄 许可

本项目仅用于教学演示，欢迎学习交流。

---

⭐ 如果这个项目对你有帮助，欢迎给个 Star！
