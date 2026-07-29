"""
State Reducer 语义详解（LangGraph）
=====================================
对比两种更新语义：覆盖（默认）vs 追加（reducer）

场景：多轮对话机器人
- messages：对话历史（需要累积，不能覆盖）
- current_topic：当前话题（可以覆盖）
"""

import os
import sys
import io
from typing import TypedDict, Annotated
import operator
from dotenv import load_dotenv
from langgraph.graph import StateGraph, START, END
from openai import OpenAI

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8')

load_dotenv()

client = OpenAI(
    api_key=os.getenv("OPENAI_API_KEY"),
    base_url=os.getenv("OPENAI_API_BASE")
)
MODEL = "gpt-5.6-sol"


# ============ State 定义：对比两种语义 ============
class DialogState(TypedDict):
    # 【覆盖语义】：当前话题，新值直接替换旧值
    current_topic: str

    # 【追加语义】：对话历史，新消息追加到列表末尾
    # Annotated[list, operator.add] 的含义：
    #   - list：这是个列表类型
    #   - operator.add：用 + 运算符合并新旧值
    #     对列表来说：[1,2] + [3] = [1,2,3]（追加）
    messages: Annotated[list[dict], operator.add]

    # 【追加语义】：轮数计数（整数累加）
    # 如果没有 reducer，每次返回 {"round": 1} 会覆盖成 1
    # 有了 operator.add，就变成 old + new（累加）
    round: Annotated[int, operator.add]


# ============ 节点1：用户输入 ============
def user_input(state: DialogState) -> dict:
    """模拟用户输入。注意返回值如何被合并进 state。"""
    print("\n[节点] 👤 用户输入")

    # 返回的 dict 会被"合并"进全局 state
    # - current_topic：会覆盖旧值（默认语义）
    # - messages：会追加到旧列表末尾（operator.add 语义）
    # - round：会累加（operator.add 语义）
    return {
        "current_topic": "天气",
        "messages": [{"role": "user", "content": "今天天气怎么样？"}],
        "round": 1,  # 第1轮，累加：0 + 1 = 1
    }


# ============ 节点2：AI 回复 ============
def ai_response(state: DialogState) -> dict:
    print("\n[节点] 🤖 AI回复")
    user_msg = state["messages"][-1]["content"]

    # 调用 LLM
    resp = client.chat.completions.create(
        model=MODEL,
        messages=[{"role": "user", "content": f"简短回答（一句话）：{user_msg}"}],
    )
    ai_msg = resp.choices[0].message.content.strip()

    print(f"   用户：{user_msg}")
    print(f"   AI：{ai_msg}")

    # 返回新消息，会追加到 messages 列表
    return {
        "messages": [{"role": "assistant", "content": ai_msg}],
    }


# ============ 节点3：话题切换 ============
def change_topic(state: DialogState) -> dict:
    print("\n[节点] 🔄 话题切换")

    # current_topic 是覆盖语义，会直接替换
    return {
        "current_topic": "美食",  # 覆盖：旧值"天气" → 新值"美食"
        "messages": [{"role": "user", "content": "推荐一道川菜"}],
        "round": 1,  # 累加：1 + 1 = 2
    }


# ============ 组装图 ============
def build_graph():
    g = StateGraph(DialogState)

    g.add_node("user_input", user_input)
    g.add_node("ai_response", ai_response)
    g.add_node("change_topic", change_topic)
    g.add_node("ai_response2", ai_response)  # 复用同一个函数

    g.add_edge(START, "user_input")
    g.add_edge("user_input", "ai_response")
    g.add_edge("ai_response", "change_topic")
    g.add_edge("change_topic", "ai_response2")
    g.add_edge("ai_response2", END)

    return g.compile()


def main():
    print("=" * 60)
    print("  📖 State Reducer 语义演示")
    print("=" * 60)

    app = build_graph()

    # 初始状态
    init_state = {
        "current_topic": "",
        "messages": [],
        "round": 0,
    }

    result = app.invoke(init_state)

    print("\n" + "=" * 60)
    print("【最终 State】")
    print("=" * 60)
    print(f"当前话题（覆盖语义）: {result['current_topic']}")
    print(f"   → 从 '天气' 被覆盖成 '美食'")
    print(f"\n轮数（累加语义）: {result['round']}")
    print(f"   → 0 + 1 + 1 = {result['round']}")
    print(f"\n对话历史（追加语义）: 共 {len(result['messages'])} 条")
    for i, msg in enumerate(result["messages"], 1):
        print(f"   {i}. [{msg['role']}] {msg['content'][:40]}...")

    print("\n" + "=" * 60)
    print("核心理解：")
    print("  • current_topic 没有 Annotated，用覆盖")
    print("  • messages 有 Annotated[list, operator.add]，用追加")
    print("  • round 有 Annotated[int, operator.add]，用累加")
    print("=" * 60)


if __name__ == "__main__":
    main()
