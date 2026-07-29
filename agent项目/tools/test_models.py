"""
测试公司API网关支持哪些模型
"""
import os
import sys
import io
from dotenv import load_dotenv
from openai import OpenAI

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

load_dotenv()

client = OpenAI(
    api_key=os.getenv("OPENAI_API_KEY"),
    base_url=os.getenv("OPENAI_API_BASE")
)

# 常见的模型名候选列表
candidates = [
    "gpt-4o",
    "gpt-4o-mini",
    "gpt-4-turbo",
    "gpt-4.1",
    "gpt-4.1-mini",
    "gpt-3.5-turbo",
    "gpt-5",
    "o1",
    "o3",
    "claude-3-5-sonnet",
    "deepseek-chat",
]

print("=" * 50)
print("开始测试可用模型...")
print("=" * 50)

available = []
for model in candidates:
    try:
        resp = client.chat.completions.create(
            model=model,
            messages=[{"role": "user", "content": "hi"}],
            max_tokens=5
        )
        print(f"✅ 可用: {model}")
        available.append(model)
    except Exception as e:
        msg = str(e)
        # 只显示简短错误
        if "model_not_found" in msg or "无可用渠道" in msg:
            print(f"❌ 不可用: {model} (模型未配置)")
        else:
            print(f"⚠️  {model}: {msg[:80]}")

print("=" * 50)
print(f"可用模型列表: {available}")
print("=" * 50)
