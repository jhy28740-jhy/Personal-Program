"""
列出公司API网关支持的所有模型
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

print("=" * 50)
print("尝试获取网关支持的模型列表...")
print("=" * 50)

# 方法1：标准的 models.list() 接口
try:
    models = client.models.list()
    print("成功获取模型列表：")
    for m in models.data:
        print(f"  - {m.id}")
except Exception as e:
    print(f"models.list() 失败: {str(e)[:150]}")

print("=" * 50)

# 方法2：测试与 codex 分组相关的模型名
print("测试 codex 分组相关模型...")
candidates = [
    "codex",
    "codex-mini",
    "gpt-4-codex",
    "gpt-5-codex",
    "o4-mini",
    "chatgpt-4o-latest",
]
for model in candidates:
    try:
        resp = client.chat.completions.create(
            model=model,
            messages=[{"role": "user", "content": "hi"}],
            max_tokens=5
        )
        print(f"✅ 可用: {model}")
    except Exception as e:
        msg = str(e)
        if "model_not_found" in msg or "无可用渠道" in msg:
            print(f"❌ 不可用: {model}")
        else:
            print(f"⚠️  {model}: {msg[:80]}")
print("=" * 50)
