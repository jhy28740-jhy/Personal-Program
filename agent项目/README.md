# 🤖 AI Agent 学习项目

个人学习 AI Agent 的代码与资料仓库。

## 📁 目录结构

```
agent项目/
├── README.md                 # 本文件，项目导航
├── 学习进度跟踪.md            # 每日学习进度
├── 使用指南.md               # 快速使用说明
├── .env                      # API密钥配置（不提交Git）
│
├── apps/                     # 🔧 实用工具
│   ├── my_agent.py           # 交互式Agent（日常聊天使用）
│   └── 04_weekly_report.py   # 周报自动生成器
│
├── examples/                 # 📚 学习示例（按顺序学习）
│   ├── 01_first_agent.py         # 单Agent问答
│   ├── 02_agent_with_tools.py    # Agent+工具（计算器）
│   ├── 03_multi_agent.py         # 多Agent协作（研究员+写手）
│   ├── 05_langgraph_reviewer.py  # LangGraph: 环状工作流（审稿助手）
│   └── 06_langgraph_triage.py    # LangGraph: 三分支路由（客服分诊）
│
├── docs/                     # 📖 学习文档
│   ├── AI_Agent_架构总结.md
│   ├── AI_Agent_学习计划.md
│   └── GitHub热门Agent项目清单.md
│
├── tools/                    # 🛠️ 辅助脚本
│   ├── list_models.py        # 列出API网关支持的模型
│   └── test_models.py        # 测试模型可用性
│
├── 周报输出/                  # 📊 周报生成结果
├── website/                  # 🌐 网页版架构总结
├── _archive/                 # 🗄️ 归档的旧文件
└── agent_env/                # 🐍 Python虚拟环境
```

## 🚀 快速开始

### 方式1：双击运行（最简单）
- `运行交互式Agent.bat` — 聊天式使用
- `运行周报生成器.bat` — 自动生成本周周报

### 方式2：VSCode（推荐）
按 `Ctrl+Shift+P`，输入 `Tasks: Run Task`，选择：
- 🤖 运行交互式Agent
- 📊 生成本周周报
- 🧪/🔧/👥 运行示例1-5

### 方式3：命令行
```bash
cd "C:\Users\hyji11\Desktop\个人小项目\agent项目"
agent_env\Scripts\activate
python apps/my_agent.py          # 交互式Agent
python apps/04_weekly_report.py  # 周报生成器
```

## ⚙️ 环境配置

- Python 3.13 + CrewAI 1.15.5 + LangGraph
- API网关：公司内部 iflytek 网关
- 常用模型：`openai/gpt-5.6-sol`（最强）
- 模型名前缀必须加 `openai/`

## 📌 学习路线

1. ✅ 单Agent问答（01）
2. ✅ Agent + 工具调用（02）
3. ✅ 多Agent协作（03）
4. ✅ 实战：周报自动生成器（04）
5. ✅ LangGraph：环状工作流（05）
6. ✅ LangGraph：多分支路由（06）
7. ⬜ State reducer语义（进行中）
8. ⬜ 更复杂的实战项目
