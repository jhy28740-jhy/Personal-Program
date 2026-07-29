# 📐 LaTeX 数学公式智能助手

基于 AI 大模型的 LaTeX 公式补全、纠错与生成工具,帮助数学工作者和学生提高 LaTeX 公式编写效率。

![项目状态](https://img.shields.io/badge/状态-开发中-yellow)
![许可证](https://img.shields.io/badge/license-MIT-blue)

## ✨ 功能特性

- **🔮 智能补全**: 自动补全不完整的 LaTeX 公式(缺失的括号、参数等)
- **🔧 语法纠错**: 检测并修正 LaTeX 语法错误,给出修正建议
- **✨自然语言生成**: 输入中文描述,自动生成对应的 LaTeX 代码
- **👁️ 实时预览**: 使用 KaTeX 渲染公式,所见即所得
- **📋 一键复制**: 快速复制生成的 LaTeX 代码

## 🎯 适用场景

- 论文写作中快速生成复杂数学公式
- 学习 LaTeX 时的语法检查与纠错
- 将口语化的数学描述转换为标准 LaTeX 代码
- 修复从 PDF 或图片中提取的不完整公式

## 🚀 快速开始

### 方式一:在线使用(推荐)

直接访问在线版本(部署后填写链接):
```
https://jhy28740-jhy.github.io/latex-assistant
```

### 方式二:本地运行

1. 克隆本仓库:
```bash
git clone https://github.com/jhy28740-jhy/latex-math-assistant.git
cd latex-math-assistant
```

2. 用浏览器打开 `latex-assistant.html` 即可使用

**注意**: 当前为演示模式,要使用完整 AI 功能需要配置 API Key(见下方配置说明)。

## ⚙️ 配置 API

编辑 `latex-assistant.html` 文件中的 `API_CONFIG`:

```javascript
const API_CONFIG = {
  mode: 'api',  // 改为 'api'
  endpoint: 'https://你的API地址',
  apiKey: '你的API密钥'
};
```

支持的 API:
- 科大讯飞星火认知大模型
- 阿里通义千问
- 百度文心一言
- OpenAI / Claude(需科学上网)

## 📸 效果展示

### 公式补全
输入不完整公式:
```latex
\int_0^{\pi} \sin(x)
```
自动补全为:
```latex
\int_0^{\pi} \sin(x) \, dx
```

### 自然语言生成
输入: `贝叶斯公式`

生成:
```latex
P(A|B) = \frac{P(B|A) \cdot P(A)}{P(B)}
```

## 🛠️ 技术栈

- **前端**: HTML5 + CSS3 + JavaScript(原生)
- **数学渲染**: KaTeX
- **AI 后端**: 大语言模型 API
- **部署**: GitHub Pages(静态托管)

## 📂 项目结构

```
latex-math-assistant/
├── latex-assistant.html    # 主文件(单文件应用)
├── README.md               # 项目说明
└── screenshots/            # 效果截图(待添加)
```

## 🎓 作者

**纪浩阳**
- 安徽大学数学硕士(图论与组合方向)
- 研究方向:图极限理论、网络拓扑分析
- 个人主页: [https://jhy28740-jhy.github.io](https://jhy28740-jhy.github.io)
- GitHub: [@jhy28740-jhy](https://github.com/jhy28740-jhy)

## 📝 开发动机

作为数学专业研究生,我每天都需要编写大量的 LaTeX 公式。在论文写作和学术交流中,经常遇到:
- 从草稿或口述转换为规范 LaTeX 的繁琐过程
- 复杂公式的括号匹配、参数补全等机械性工作
- 从 OCR 或 PDF 提取的公式需要大量手动修正

因此开发了这个工具,利用 AI 大模型的语言理解能力,自动化这些重复性工作,提高科研效率。

## 🤝 贡献指南

欢迎提交 Issue 和 Pull Request!

如果你有好的想法或发现了 Bug,请:
1. Fork 本仓库
2. 创建你的特性分支 (`git checkout -b feature/AmazingFeature`)
3. 提交你的改动 (`git commit -m 'Add some AmazingFeature'`)
4. 推送到分支 (`git push origin feature/AmazingFeature`)
5. 开启一个 Pull Request

## 📄 许可证

本项目采用 MIT 许可证 - 详见 [LICENSE](LICENSE) 文件

## 🙏 致谢

- [KaTeX](https://katex.org/) - 快速的数学公式渲染引擎
- 科大讯飞讯飞医疗研究院 - 实习期间的技术支持

---

⭐ 如果这个项目对你有帮助,欢迎 Star!
