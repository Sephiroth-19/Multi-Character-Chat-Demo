# test_config.py
from config import get_openai_client

def main():
    try:
        client = get_openai_client()   # 调用我们刚写的函数
        print("✅ 成功获取 OpenAI 客户端:", client)
    except Exception as e:
        print("❌ 出错了:", e)

if __name__ == "__main__":
    main()
client = get_openai_client()

# 用这个 client 去跟 ChatGPT 说一句话
response = client.chat.completions.create(
    model="gpt-4o-mini",
    messages=[{"role": "user", "content": "你好，帮我说一句英文问候"}]
)

print(response.choices[0].message.content)
