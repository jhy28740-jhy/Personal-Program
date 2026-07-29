"""
第二个Agent示例：给Agent添加工具
功能：Agent通过调用"计算器工具"完成精确计算

学习重点：
- 理解什么是"工具（Tool）"
- 观察Agent如何"决定使用工具 -> 调用 -> 拿到结果"
- 对比：没有工具时LLM可能算错，有工具时结果精确
"""

import os
import sys
import io
from dotenv import load_dotenv
from crewai import Agent, Task, Crew, LLM
from crewai.tools import tool

# 修复Windows终端中文编码问题
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8')

load_dotenv()

# 配置LLM
llm = LLM(
    model="openai/gpt-5.6-sol",
    api_key=os.getenv("OPENAI_API_KEY"),
    base_url=os.getenv("OPENAI_API_BASE")
)


# ============ 定义工具 ============
# 用 @tool 装饰器把一个普通Python函数变成Agent可以调用的工具
# 注意：工具名必须用英文（CrewAI会过滤非字母数字字符，中文名会变空导致报错）
@tool("Calculator")
def calculator(expression: str) -> str:
    """
    执行数学计算。
    输入一个数学表达式字符串（如 "1234 * 5678"），返回精确的计算结果。
    支持 + - * / ** % 等运算。
    """
    try:
        # 安全地计算表达式（只允许数字和基本运算符）
        allowed = set("0123456789+-*/(). %")
        if not all(c in allowed for c in expression):
            return "错误：表达式包含不允许的字符"
        result = eval(expression)
        return f"{expression} = {result}"
    except Exception as e:
        return f"计算错误：{e}"


# ============ 创建带工具的Agent ============
math_agent = Agent(
    role='数学助手',
    goal='准确回答用户的数学计算问题',
    backstory='你是一个严谨的数学助手。遇到计算时，你必须使用"计算器"工具来保证结果精确，绝不靠自己心算。',
    tools=[calculator],   # 把工具交给Agent
    verbose=True,
    llm=llm
)

# ============ 创建任务 ============
task = Task(
    description='请计算 1234 × 5678 加上 98765 等于多少？请使用计算器工具确保精确。',
    expected_output='一句话说明最终的精确计算结果',
    agent=math_agent
)

# ============ 组建Crew并执行 ============
crew = Crew(
    agents=[math_agent],
    tasks=[task],
    verbose=True
)

if __name__ == "__main__":
    print("=" * 50)
    print("运行带【工具】的Agent")
    print("=" * 50)

    result = crew.kickoff()

    print("\n" + "=" * 50)
    print("最终结果：")
    print("=" * 50)
    print(result)

    # 验证：正确答案应该是 1234*5678+98765 = 7006652+98765 = 7105417
    print("\n[人工核对] 1234*5678+98765 =", 1234 * 5678 + 98765)
