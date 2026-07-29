# 快速上手指南

## 📦 本地使用(无需配置)

1. 双击 `latex-assistant.html` 文件,浏览器会自动打开
2. 或者右键文件 → 打开方式 → 选择浏览器(Chrome/Edge)
3. 选择功能标签,输入内容,点击按钮即可

**注意**: 当前为演示模式,会返回预设的示例结果。要使用完整 AI 功能,请按下方说明配置 API。

---

## 🔌 配置 AI API(完整功能)

### 推荐方案:科大讯飞星火

1. 访问 [讯飞开放平台](https://console.xfyun.cn/)
2. 注册并创建应用,获取 API Key
3. 打开 `latex-assistant.html`,找到第 162 行左右的 `API_CONFIG`:

```javascript
const API_CONFIG = {
  mode: 'api',  // 改为 'api'
  endpoint: 'https://spark-api.xf-yun.com/v1/chat',  // 讯飞 API 地址
  apiKey: '你的API密钥'
};
```

4. 同时修改 `callAI` 函数以适配讯飞的请求格式(代码模板见下方)

### 其他可选方案

**阿里通义千问**:
- 注册地址: https://dashscope.aliyun.com/
- 文档: https://help.aliyun.com/document_detail/2400395.html

**百度文心一言**:
- 注册地址: https://console.bce.baidu.com/qianfan/
- 文档: https://cloud.baidu.com/doc/WENXINWORKSHOP/index.html

---

## 🚀 部署到 GitHub Pages

### 1. 创建 GitHub 仓库

```bash
# 在项目目录执行
git remote add origin https://github.com/jhy28740-jhy/latex-math-assistant.git
git branch -M main
git push -u origin main
```

### 2. 开启 GitHub Pages

1. 进入仓库页面: `https://github.com/jhy28740-jhy/latex-math-assistant`
2. 点击 `Settings` → 左侧 `Pages`
3. Source 选 `Deploy from a branch`
4. Branch 选 `main`,目录选 `/ (root)`
5. 点击 `Save`

等待 1-2 分钟,访问: `https://jhy28740-jhy.github.io/latex-math-assistant/latex-assistant.html`

---

## 🛠️ 自定义开发

### 添加新功能

在 `latex-assistant.html` 中:
1. 在 `<div class="tabs">` 添加新标签按钮
2. 添加对应的 `<div class="panel">` 内容
3. 在 `<script>` 区域添加处理函数

### 修改样式

所有样式在 `<style>` 标签内,使用 CSS 变量方便全局修改:
- `--accent`: 主题色(默认蓝色)
- `--bg`: 背景色
- `--text`: 文字颜色

### 接入不同的 AI 模型

修改 `callAI` 函数的请求格式以适配不同 API:

```javascript
async function callAI(prompt, systemPrompt) {
  const response = await fetch(API_CONFIG.endpoint, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
      'Authorization': `Bearer ${API_CONFIG.apiKey}`
    },
    body: JSON.stringify({
      // 根据你使用的 API 调整请求格式
      model: 'spark-3.5',
      messages: [
        { role: 'system', content: systemPrompt },
        { role: 'user', content: prompt }
      ],
      temperature: 0.7
    })
  });
  
  const data = await response.json();
  // 根据 API 响应格式提取结果
  return data.choices[0].message.content;
}
```

---

## ❓ 常见问题

**Q: 演示模式和 API 模式有什么区别?**
A: 演示模式返回预设的示例结果,适合体验功能;API 模式调用真实大模型,能处理任意输入。

**Q: 如何获取免费的 API 额度?**
A: 国内主流大模型(讯飞/通义/文心)都提供免费试用额度,注册即可领取。

**Q: 可以离线使用吗?**
A: 演示模式可以完全离线使用。API 模式需要网络连接。数学渲染库(KaTeX)使用 CDN,首次加载需要联网,之后会缓存。

**Q: 如何报告 Bug 或提建议?**
A: 在 GitHub 仓库提交 Issue: https://github.com/jhy28740-jhy/latex-math-assistant/issues

---

## 📚 相关资源

- [LaTeX 数学符号速查](https://katex.org/docs/supported.html)
- [KaTeX 官方文档](https://katex.org/)
- [科大讯飞星火文档](https://www.xfyun.cn/doc/spark/Web.html)
- [GitHub Pages 部署指南](https://docs.github.com/zh/pages)

---

有问题欢迎联系作者: jhy28740@gmail.com
