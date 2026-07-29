"""
智能审稿助手（LangGraph 实战）
=====================================
一个带【条件分支 + 环】的有向图工作流：

    START -> grammar_check -> content_review -> ⟨route⟩
                                  ↑               ├─ score>=7 -> END
                                  └── revise ─────┘ (score<7 且 轮数<3)

图论视角：
- 顶点(Node)：grammar_check / content_review / revise，每个是 state->state 的函数
- 有向边：固定边用 add_edge，分支用 add_conditional_edges
- 环：content_review <-> revise 构成有向环
- 终止：score>=7 可达 END；轮数上限做为环的"离开条件"，保证 END 可达
- State：全局共享的 TypedDict，节点返回的 dict 合并进去
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

# 直接用 OpenAI SDK 调公司网关（比封装更透明，方便你看清每次LLM调用）
client = OpenAI(
    api_key=os.getenv("OPENAI_API_KEY"),
    base_url=os.getenv("OPENAI_API_BASE")
)
MODEL = "gpt-5.6-sol"

MAX_REVISIONS = 3          # 环的最大循环次数（防止不可达END）
PASS_SCORE = 7             # 评分阈值


def llm(prompt: str) -> str:
    """一次简单的LLM调用，返回文本。"""
    resp = client.chat.completions.create(
        model=MODEL,
        messages=[{"role": "user", "content": prompt}],
    )
    return resp.choices[0].message.content.strip()


# ============ 全局状态（图的顶点数据）============
class ReviewState(TypedDict):
    article: str        # 当前文章（会被修正/重写覆盖）
    score: int          # 内容评审得分 1-10
    feedback: str       # 评审反馈
    revisions: int      # 已重写次数（环的计数器）


# ============ 节点1：语法检查 ============
def grammar_check(state: ReviewState) -> dict:
    print("\n[节点] 🔤 语法检查中...")
    prompt = (
        "请检查并修正下面文章的语法、错别字、标点问题。"
        "只输出修正后的完整文章，不要解释。\n\n" + state["article"]
    )
    fixed = llm(prompt)
    print("   语法检查完成")
    return {"article": fixed}


# ============ 节点2：内容评审（打分）============
def content_review(state: ReviewState) -> dict:
    print("\n[节点] 📊 内容评审中...")
    prompt = (
        "你是严格的编辑。请给下面文章的内容质量打分（1-10的整数），"
        "并给出一句改进建议。严格按格式输出：\n"
        "分数: <数字>\n建议: <一句话>\n\n" + state["article"]
    )
    result = llm(prompt)
    # 解析分数
    score = 5
    feedback = result
    for line in result.splitlines():
        if "分数" in line or "分数:" in line.lower():
            digits = "".join(c for c in line if c.isdigit())
            if digits:
                score = int(digits[:2]) if len(digits) >= 2 and digits.startswith("10") else int(digits[0])
        if "建议" in line:
            feedback = line.split("建议", 1)[-1].lstrip(":：").strip()
    print(f"   评分: {score}/10 | 建议: {feedback}")
    return {"score": score, "feedback": feedback}


# ============ 节点3：修改重写 ============
def revise(state: ReviewState) -> dict:
    n = state["revisions"] + 1
    print(f"\n[节点] ✍️  第 {n} 次重写（根据评审建议）...")
    prompt = (
        f"请根据以下改进建议重写文章，使其更好。\n"
        f"改进建议：{state['feedback']}\n\n"
        f"原文章：\n{state['article']}\n\n"
        f"只输出重写后的完整文章。"
    )
    rewritten = llm(prompt)
    return {"article": rewritten, "revisions": n}


# ============ 路由函数：内容评审后往哪走？============
def route_after_review(state: ReviewState) -> str:
    """返回下一个节点名。这是条件边的核心。"""
    if state["score"] >= PASS_SCORE:
        print(f"   ✅ 达标（{state['score']}>={PASS_SCORE}），走向 END")
        return "pass"
    if state["revisions"] >= MAX_REVISIONS:
        print(f"   ⚠️ 已重写{MAX_REVISIONS}次仍未达标，强制结束")
        return "pass"
    print(f"   🔄 未达标（{state['score']}<{PASS_SCORE}），进入重写循环")
    return "revise"


# ============ 组装图 ============
def build_graph():
    g = StateGraph(ReviewState)

    # 添加顶点
    g.add_node("grammar_check", grammar_check)
    g.add_node("content_review", content_review)
    g.add_node("revise", revise)

    # 添加边
    g.add_edge(START, "grammar_check")            # 源点 -> 语法检查
    g.add_edge("grammar_check", "content_review") # 语法 -> 评审

    # 条件边：评审后根据分数分流
    g.add_conditional_edges(
        "content_review",
        route_after_review,
        {
            "pass": END,        # 达标 -> 汇点
            "revise": "revise", # 未达标 -> 重写
        }
    )
    g.add_edge("revise", "content_review")         # 重写 -> 回到评审（形成环）

    return g.compile()


def main():
    print("=" * 55)
    print("  🔍 智能审稿助手 (LangGraph)")
    print("=" * 55)

    # 一篇故意写得比较差的文章，观察它如何被迭代改进
    draft = (
        "AI agent是一个很厉害的东西它可以做很多事情。"
        "比如说他能帮你干活，还能自己思考。总之非常有用，大家都应该用。"
    )

    app = build_graph()
    init_state = {"article": draft, "score": 0, "feedback": "", "revisions": 0}

    print(f"\n【原始草稿】\n{draft}")
    print("\n" + "=" * 55)

    # 执行图。recursion_limit 防止环无限循环（图论：限制路径长度）
    final = app.invoke(init_state, config={"recursion_limit": 20})

    print("\n" + "=" * 55)
    print(f"【最终稿】(评分 {final['score']}/10, 重写 {final['revisions']} 次)")
    print("=" * 55)
    print(final["article"])


if __name__ == "__main__":
    main()
