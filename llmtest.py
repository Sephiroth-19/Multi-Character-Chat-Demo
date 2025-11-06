from llm_service import chat

# 构造一个简单的对话消息
messages = [
    {"role": "user", "content": "你好！请用一句话介绍一下你自己。"}
]

# 调用 chat 函数
try:
    reply = chat(messages)
    print("✅ 模型返回：")
    print(reply)
except Exception as e:
    print("❌ 出错啦：", e)

from llm_service import _client_once

client = _client_once()
resp = client.chat.completions.create(
    model="gpt-4o-mini",
    messages=[{"role": "user", "content": "你好！"}]
)
print(resp)
