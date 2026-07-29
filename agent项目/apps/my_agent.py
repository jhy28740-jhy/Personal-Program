"""
我的交互式 Agent —— 日常使用的主力脚本
运行后直接打字输入任务，像聊天一样使用，输入 quit / exit / 退出 结束。

用法：
    cd "C:\\Users\\hyji11\\Desktop\\个人小项目\\agent项目"
    agent_env\\Scripts\\activate
    python my_agent.py
"""

import os
import sys
import io
from pathlib import Path
from dotenv import load_dotenv
from crewai import Agent, Task, Crew
from crewai.tools import tool

# 修复 Windows 终端中文编码问题
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8')

load_dotenv()

from crewai import LLM

# 配置 LLM（公司网关 + 最强模型）
llm = LLM(
    model="openai/gpt-5.6-sol",
    api_key=os.getenv("OPENAI_API_KEY"),
    base_url=os.getenv("OPENAI_API_BASE")
)


# ============ 工具：计算器 ============
@tool("Calculator")
def calculator(expression: str) -> str:
    """执行数学计算。输入数学表达式（如 "12 * 34 + 5"），返回精确结果。"""
    try:
        allowed = set("0123456789+-*/(). %")
        if not all(c in allowed for c in expression):
            return "错误：表达式包含不允许的字符"
        return f"{expression} = {eval(expression)}"
    except Exception as e:
        return f"计算错误：{e}"


# ============ 工具：读取文本文件 ============
@tool("ReadTextFile")
def read_text_file(file_path: str) -> str:
    """
    读取文本类文件的内容（.txt/.md/.csv/.py/.json/.log 等）。
    输入文件的完整路径，返回文件内容（最多前 8000 字符）。
    """
    try:
        p = Path(file_path)
        if not p.exists():
            return f"文件不存在：{file_path}"
        if not p.is_file():
            return f"这不是一个文件：{file_path}"
        text = p.read_text(encoding="utf-8", errors="ignore")
        if len(text) > 8000:
            text = text[:8000] + "\n...（内容过长，已截断）"
        return text
    except Exception as e:
        return f"读取失败：{e}"


# ============ 工具：读取 Excel 文件 ============
@tool("ReadExcel")
def read_excel(file_path: str) -> str:
    """
    读取 Excel 文件（.xlsx）的内容。
    输入文件的完整路径，返回各工作表的数据（每个表最多前 50 行）。
    """
    try:
        import openpyxl
        p = Path(file_path)
        if not p.exists():
            return f"文件不存在：{file_path}"
        wb = openpyxl.load_workbook(p, read_only=True, data_only=True)
        result = []
        for ws in wb.worksheets:
            result.append(f"=== 工作表：{ws.title} ===")
            for i, row in enumerate(ws.iter_rows(values_only=True)):
                if i >= 50:
                    result.append("...（超过50行，已截断）")
                    break
                cells = [str(c) if c is not None else "" for c in row]
                result.append(" | ".join(cells))
        wb.close()
        return "\n".join(result) if result else "（Excel为空）"
    except Exception as e:
        return f"读取Excel失败：{e}"


# ============ 工具：列出文件夹内容 ============
@tool("ListDirectory")
def list_directory(dir_path: str) -> str:
    """
    列出一个文件夹下的所有文件和子文件夹。
    输入文件夹的完整路径，返回其中的文件/文件夹名称列表。
    """
    try:
        p = Path(dir_path)
        if not p.exists():
            return f"文件夹不存在：{dir_path}"
        if not p.is_dir():
            return f"这不是一个文件夹：{dir_path}"
        items = []
        for item in sorted(p.iterdir()):
            tag = "[文件夹]" if item.is_dir() else "[文件]"
            items.append(f"{tag} {item.name}")
        return "\n".join(items) if items else "（空文件夹）"
    except Exception as e:
        return f"列出失败：{e}"


# ============ 创建一个通用助手 Agent ============
assistant = Agent(
    role='全能助手',
    goal='准确、高质量地完成用户交给的各种任务（写作、翻译、总结、计算、读取文件、答疑等）',
    backstory=(
        '你是一位聪明、细致、乐于助人的AI助手。'
        '你会认真理解用户的需求，给出清晰有条理的回答。'
        '遇到数学计算时，使用 Calculator 工具确保精确。'
        '需要查看文件内容时，使用 ReadTextFile（文本）或 ReadExcel（表格）工具。'
        '需要查看某个文件夹里有什么时，使用 ListDirectory 工具。'
        '用户给出文件路径后，你应主动调用相应工具读取，而不是凭空猜测内容。'
    ),
    tools=[calculator, read_text_file, read_excel, list_directory],
    verbose=False,   # 设为False让界面更清爽；想看Agent思考过程可改成True
    llm=llm
)


def run_task(user_input: str) -> str:
    """把用户输入包装成任务，交给Agent执行，返回结果。"""
    task = Task(
        description=user_input,
        expected_output='针对用户需求的、清晰完整的回答',
        agent=assistant
    )
    crew = Crew(agents=[assistant], tasks=[task], verbose=False)
    return str(crew.kickoff())


def main():
    print("=" * 55)
    print("  🤖 我的交互式 Agent 已启动")
    print("  直接输入你想让我做的事，回车执行")
    print("  输入 quit / exit / 退出  结束程序")
    print("=" * 55)

    while True:
        try:
            user_input = input("\n👤 你想让我做什么？> ").strip()
        except (EOFError, KeyboardInterrupt):
            print("\n👋 再见！")
            break

        if not user_input:
            continue
        if user_input.lower() in ("quit", "exit", "退出", "q"):
            print("👋 再见！")
            break

        print("\n🤖 正在思考并执行...\n")
        try:
            answer = run_task(user_input)
            print("-" * 55)
            print(answer)
            print("-" * 55)
        except Exception as e:
            print(f"⚠️ 执行出错：{e}")


if __name__ == "__main__":
    main()
