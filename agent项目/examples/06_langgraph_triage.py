"""
智能客服分诊 Agent（LangGraph 三分支路由实战）
=====================================
一个带【三分支条件路由】的有向图：

        START -> classify -> ⟨route⟩ ┬ "tech"    -> tech_support ┐
                                     ├ "billing" -> billing      ┤-> END
                                     └ "other"   -> general      ┘

图论视角：
- classify 是分类顶点，出度=3 的条件边（δ 值域大小=3）
- tech_support / billing / general 是三个处理顶点
- 三条路径都可达汇点 END（树状分叉，无环）
- 对比审稿助手：那个是带环，这个是多路分叉
"""

import os
import sys
import io
from typing import TypedDict
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


def llm(prompt: str) -> str:
    resp = client.chat.completions.create(
        model=MODEL,
        messages=[{"role": "user", "content": prompt}],
    )
    return resp.choices[0].message.content.strip()


# ============ 全局状态 ============
class TriageState(TypedDict):
    question: str      # 用户的问题
    category: str      # 分类结果：tech / billing / other
    answer: str        # 最终回复


# ============ 节点1：分类 ============
def classify(state: TriageState) -> dict:
    print("\n[节点] 🔍 问题分类中...")
    prompt = (
        "你是客服分诊员。用户问题如下，请判断属于哪一类，只输出一个单词：\n"
        "- tech：技术问题（如无法登录、功能报错、系统故障）\n"
        "- billing：账单/付费问题（如扣费、退款、订阅）\n"
        "- other：其他问题（如咨询功能、产品介绍、建议反馈）\n\n"
        f"用户问题：{state['question']}\n\n"
        "分类（只输出 tech / billing / other 之一）："
    )
    result = llm(prompt).strip().lower()
    # 提取关键词（防止LLM多说话）
    if "tech" in result:
        category = "tech"
    elif "billing" in result:
        category = "billing"
    else:
        category = "other"
    print(f"   分类结果：{category}")
    return {"category": category}


# ============ 节点2：技术支持 ============
def tech_support(state: TriageState) -> dict:
    print("\n[节点] 🔧 技术支持处理中...")
    prompt = (
        "你是技术支持专员。用户遇到以下技术问题，请给出专业的排查建议（2-3句话）：\n\n"
        f"{state['question']}"
    )
    answer = llm(prompt)
    print(f"   技术支持回复：{answer[:60]}...")
    return {"answer": answer}


# ============ 节点3：账单处理 ============
def billing(state: TriageState) -> dict:
    print("\n[节点] 💳 账单问题处理中...")
    prompt = (
        "你是财务客服。用户有以下账单疑问，请给出清晰的解释和处理方案（2-3句话）：\n\n"
        f"{state['question']}"
    )
    answer = llm(prompt)
    print(f"   账单处理回复：{answer[:60]}...")
    return {"answer": answer}


# ============ 节点4：通用咨询 ============
def general(state: TriageState) -> dict:
    print("\n[节点] 💬 通用咨询处理中...")
    prompt = (
        "你是客服助手。用户有以下咨询，请给出友好、简洁的回复（2-3句话）：\n\n"
        f"{state['question']}"
    )
    answer = llm(prompt)
    print(f"   通用咨询回复：{answer[:60]}...")
    return {"answer": answer}


# ============ 路由函数：三分支（δ 值域=3）============
def route_by_category(state: TriageState) -> str:
    """根据分类结果，返回下一个节点名。值域 = {"tech", "billing", "other"}。"""
    category = state["category"]
    print(f"   🚦 路由：{category} → 对应处理节点")
    return category  # 直接返回分类名，因为我们会在 add_conditional_edges 里把它映射到节点


# ============ 组装图（三分支拓扑）============
def build_graph():
    g = StateGraph(TriageState)

    # 添加顶点
    g.add_node("classify", classify)
    g.add_node("tech_support", tech_support)
    g.add_node("billing", billing)
    g.add_node("general", general)

    # START -> 分类
    g.add_edge(START, "classify")

    # 三分支条件边：从 classify 根据分类结果分流
    g.add_conditional_edges(
        "classify",
        route_by_category,
        {
            "tech": "tech_support",   # 路径1：技术问题 → 技术支持节点
            "billing": "billing",     # 路径2：账单问题 → 账单处理节点
            "other": "general",       # 路径3：其他问题 → 通用咨询节点
        }
    )

    # 三个处理节点都连向 END（树状分叉，最终汇入）
    g.add_edge("tech_support", END)
    g.add_edge("billing", END)
    g.add_edge("general", END)

    return g.compile()


def main():
    print("=" * 60)
    print("  🤖 智能客服分诊 Agent (三分支路由)")
    print("=" * 60)

    # 准备三个不同类型的测试问题
    test_cases = [
        "我的账户被多扣了50元，怎么申请退款？",           # 应该走 billing
        "登录时提示密码错误，但密码肯定是对的",           # 应该走 tech
        "你们的产品有没有学生优惠？",                    # 应该走 other
    ]

    app = build_graph()

    for i, question in enumerate(test_cases, 1):
        print(f"\n{'='*60}")
        print(f"【测试用例 {i}】{question}")
        print("=" * 60)

        init_state = {"question": question, "category": "", "answer": ""}
        result = app.invoke(init_state)

        print(f"\n✅ 最终回复：")
        print(result["answer"])

    print("\n" + "=" * 60)
    print("  三个问题分别走了三条不同的路径，都成功到达 END")
    print("=" * 60)


if __name__ == "__main__":
    main()
