from __future__ import annotations
import os
from typing import List, Dict
from config import get_openai_client

_client = None

def _client_once():
    global _client
    if _client is None:
        _client = get_openai_client()
    return _client

def chat(
        messages: List[Dict[str, str]],
        model: str | None = None,
        temperature: float = 0.6,
) -> str:
    if not messages or not isinstance(messages, list):
        raise RuntimeError('messages 不能为空，且必须是 List[Dict[str, str]]')

    model = model or os.getenv('OPENAI_CHAT_MODEL', 'gpt-4o-mini')
    client = _client_once()

    try:
        resp = client.chat.completions.create(
            model=model,
            messages=messages,
            temperature=temperature,
        )
        content = (resp.choices[0].message.content or '').strip()
        if not content:
            raise RuntimeError('模型返回空内容。')
        return content
    except Exception as e:
        raise RuntimeError(f'调用模型失败: {e}') from e
