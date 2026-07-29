"""
第一个CrewAI Agent示例
功能：使用GPT API创建一个简单的研究助手
"""

import os
import sys
import io
from dotenv import load_dotenv
from crewai import Agent, Task, Crew, LLM

# 修复Windows终端中文编码问题
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8')

# 加载环境变量
load_dotenv()

# 配置GPT模型 - 使用CrewAI的LLM类
# base_url 指向公司内部API网关
# gpt-5.6-sol 是网关支持的最强模型
llm = LLM(
    model="openai/gpt-5.6-sol",
    api_key=os.getenv("OPENAI_API_KEY"),
    base_url=os.getenv("OPENAI_API_BASE")
)

# 创建一个研究员Agent
researcher = Agent(
    role='AI技术研究员',
    goal='研究和总结AI Agent相关的技术知识',
    backstory='你是一位经验丰富的AI研究员，擅长将复杂的技术概念解释清楚。',
    verbose=True,  # 显示详细执行过程
    llm=llm
)

# 创建任务
task = Task(
    description='请用3句话总结：什么是AI Agent？',
    expected_output='3句话的清晰总结',
    agent=researcher
)

# 组建Crew并执行
crew = Crew(
    agents=[researcher],
    tasks=[task],
    verbose=True
)

# 运行
if __name__ == "__main__":
    print("=" * 50)
    print("开始运行你的第一个AI Agent！")
    print("=" * 50)

    result = crew.kickoff()

    print("\n" + "=" * 50)
    print("Agent执行结果：")
    print("=" * 50)
    print(result)
