"""
第三个Agent示例：多Agent协作（CrewAI的招牌功能）
功能：模拟一个"内容创作小组"，两个Agent分工协作完成一篇科普短文

学习重点：
- 理解多个Agent如何分工（每个Agent有独立的角色和职责）
- 理解任务之间的"上下文传递"：前一个Agent的输出 -> 后一个Agent的输入
- 观察 process=sequential（顺序执行）的协作流程

协作流程：
    研究员(整理要点)  ->  写手(润色成文)
"""

import os
import sys
import io
from dotenv import load_dotenv
from crewai import Agent, Task, Crew, LLM, Process

# 修复Windows终端中文编码问题
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8')

load_dotenv()

# 配置LLM（两个Agent共用同一个大脑，也可以各用不同模型）
llm = LLM(
    model="openai/gpt-5.6-sol",
    api_key=os.getenv("OPENAI_API_KEY"),
    base_url=os.getenv("OPENAI_API_BASE")
)

# ============ Agent 1：研究员 ============
researcher = Agent(
    role='技术研究员',
    goal='整理出关于指定主题的3个最核心、最准确的技术要点',
    backstory='你是一位严谨的技术研究员，擅长抓住一个主题的本质，用精炼的要点列出关键信息。',
    verbose=True,
    llm=llm
)

# ============ Agent 2：写手 ============
writer = Agent(
    role='科普作家',
    goal='把技术要点改写成通俗易懂、生动有趣的科普短文',
    backstory='你是一位受欢迎的科普作家，擅长用比喻和大白话把复杂的技术讲给普通人听。',
    verbose=True,
    llm=llm
)

# ============ 任务 1：研究（交给研究员）============
research_task = Task(
    description='研究主题："AI Agent 是什么"。整理出3个最核心的技术要点，每个要点用一句话概括。',
    expected_output='3个技术要点的列表',
    agent=researcher
)

# ============ 任务 2：写作（交给写手）============
# context=[research_task] 表示这个任务会自动拿到研究任务的输出作为输入
writing_task = Task(
    description='根据研究员提供的技术要点，写一段200字左右的科普短文，要求通俗易懂、有比喻。',
    expected_output='一段约200字的科普短文',
    agent=writer,
    context=[research_task]   # 关键：把研究任务的结果作为上下文传进来
)

# ============ 组建Crew（顺序执行）============
crew = Crew(
    agents=[researcher, writer],
    tasks=[research_task, writing_task],
    process=Process.sequential,   # 按顺序：先研究，再写作
    verbose=True
)

if __name__ == "__main__":
    print("=" * 50)
    print("运行【多Agent协作】：研究员 + 写手")
    print("=" * 50)

    result = crew.kickoff()

    print("\n" + "=" * 50)
    print("最终科普短文：")
    print("=" * 50)
    print(result)
