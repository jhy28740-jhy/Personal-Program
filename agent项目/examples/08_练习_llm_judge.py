"""
【动手练习】LLM-as-Judge 质量评分 Agent
=====================================
场景：AI测试部常用技能 —— 用一个 AI(裁判) 去评估另一个 AI(答题者) 的回答质量。
如果回答不合格，就打回去重答，直到合格或达到最大次数。

图结构（带环，和审稿助手同款套路）：

    START → answer → judge → ⟨route⟩ ┬ score>=8      → END
                       ↑              └ score<8 & 未超次数 → answer(重答)
                       └──────────────┘

===========================================================
  你的任务：填 3 个 TODO（难度递增）。写完告诉我，我来 review。
  框架、LLM封装、图的组装 我都写好了，你只管填空。
===========================================================
"""

import os
import sys
import io
import re
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


# 配置
PASS_SCORE = 8       # 及格线
MAX_ATTEMPTS = 3     # 最多重答几次


# ============================================================
#  TODO 1（简单）：定义状态字段
# ------------------------------------------------------------
#  这个 Agent 的"记忆"需要装哪些东西？想一想流程里传递了什么。
#  提示：需要 4 个字段 —— 问题、当前回答、裁判打的分、已经答了几次。
#  参考 06 号示例的 TriageState 写法（注意类型标注）。
# ============================================================
class JudgeState(TypedDict):
    question: str    # 示范：用户的问题（这个我帮你写好了）
    # TODO: 在下面补齐另外 3 个字段（answer / score / attempts）
    answer: str
    score: int
    attempts: int

# ============ 节点1：答题者（已写好，你参考它的写法）============
def answer(state: JudgeState) -> dict:
    attempts = state["attempts"] + 1
    print(f"\n[节点] 🖊️  答题者作答中... (第 {attempts} 次尝试)")

    # 如果是重答，把上次的低分反馈带上，让它改进
    if state.get("score", 0) > 0:
        prompt = (
            f"你上次的回答得分不够（{state['score']}分）。请针对这个问题重新回答，答得更完整准确：\n\n"
            f"问题：{state['question']}"
        )
    else:
        prompt = f"请简洁准确地回答这个问题（3-5句话）：\n\n{state['question']}"

    result = llm(prompt)
    print(f"   回答：{result[:60]}...")
    return {"answer": result, "attempts": attempts}


# ============================================================
#  TODO 2（中等）：写"裁判"节点
# ------------------------------------------------------------
#  让 LLM 给 state["answer"] 打分（1-10 的整数），提取出数字存进 score。
#  步骤：
#    1. 写 prompt：要求 LLM 评估回答质量，【只输出一个 1-10 的数字】
#    2. 调 llm(prompt) 拿到结果
#    3. 从结果里提取数字（提示：用 re.search(r'\d+', 文本) 防止 LLM 多嘴）
#    4. return {"score": 那个数字}
#  参考：06示例里 classify 节点是怎么提取关键词的。
# ============================================================
def judge(state: JudgeState) -> dict:
    print(f"\n[节点] ⚖️  裁判评分中...")
    prompt = (
        f"你是一个严格的评分裁判，请评估下面的问题的质量。"
        f"从准确性，完整性，清晰度三个层面评判。"
        f"对于评分你只需要回答一个整数，评分范围为1~10，分数越高越好。"
        f"问题：{state['question']}"
        f"回答：{state['answer']}"
        f"分数："
    )
    result = llm(prompt)
    match = re.search(r'\d+', result)
    score = int(match.group()) if match else 0
    print(f" 裁判打分: {score}/10)")
    return {"score":score}
    # TODO: 在这里写你的代码
    # prompt = ...
    # result = llm(prompt)
    # score = ...  (从 result 里提取 1-10 的整数)
    # print(f"   裁判打分：{score}/10")
    # return {"score": score}
    pass


# ============================================================
#  TODO 3（较难）：写路由函数
# ------------------------------------------------------------
#  这是图论里的 δ 函数：根据当前状态，决定下一个去哪个节点。
#  规则：
#    - 如果 score >= PASS_SCORE（合格）           → 返回 "pass"
#    - 如果 score < PASS_SCORE 但 attempts 已达上限 → 返回 "pass"（不再重答，止损）
#    - 否则（不合格且还有机会）                    → 返回 "retry"
#  参考：05示例(审稿助手)的 route 函数，逻辑几乎一样。
# ============================================================
def route(state: JudgeState) -> str:
    # TODO: 在这里写路由逻辑，返回 "pass" 或 "retry"
    if state['score'] >= PASS_SCORE:
        print("达标")
        return "pass"
    elif state['score'] <PASS_SCORE and state["attempts"] == MAX_ATTEMPTS:
        print("已达尝试上限")
        return "pass" 
    else:
        return "retry"


# ============ 组装图（已写好，你看懂就行）============
def build_graph():
    g = StateGraph(JudgeState)

    g.add_node("answer", answer)
    g.add_node("judge", judge)

    g.add_edge(START, "answer")     # 开始 → 答题
    g.add_edge("answer", "judge")   # 答完 → 评分

    # 条件边：评分后，根据 route 的返回值决定去向
    g.add_conditional_edges(
        "judge",
        route,
        {
            "pass": END,        # 合格（或止损）→ 结束
            "retry": "answer",  # 不合格 → 回到答题节点（形成环！）
        }
    )

    return g.compile()


def main():
    print("=" * 60)
    print("  ⚖️  LLM-as-Judge 质量评分 Agent（动手练习）")
    print("=" * 60)

    app = build_graph()

    question = "什么是软件测试里的'边界值分析'？"
    print(f"\n【测试问题】{question}")

    # 初始状态：注意 4 个字段都要给初值
    init_state = {"question": question, "answer": "", "score": 0, "attempts": 0}
    result = app.invoke(init_state)

    print("\n" + "=" * 60)
    print(f"✅ 最终回答（尝试了 {result['attempts']} 次，得分 {result['score']}）：")
    print(result["answer"])
    print("=" * 60)


if __name__ == "__main__":
    main()
