from typing import Dict, List
from characters import get_character
from llm_service import chat as llm_chat

class ConversationManager:
    """
    管理多个角色的对话历史。
    每个角色都有自己独立的 messages 记录。
    """
    def __init__(self, max_rounds: int = 12):
        self.histories: Dict[str, List[Dict[str, str]]] = {}
        self.max_rounds = max_rounds

    def _ensure_history(self, char_key: str):
        """如果角色历史不存在，就创建并注入 system prompt"""
        character = get_character(char_key)
        if char_key not in self.histories:
            self.histories[char_key] = [{
                "role": "system",
                "content": character.system_prompt
            }]
        return self.histories[char_key]

    def _trim(self, history: List[Dict[str, str]]):
        """只保留最近 N 轮对话，防止太长"""
        system_msg = history[0]
        rest = history[1:]
        keep = self.max_rounds * 2  # 每轮=用户+回答
        if len(rest) > keep:
            rest = rest[-keep:]
        history[:] = [system_msg] + rest

    def ask(self, char_key: str, user_text: str, temperature: float = 0.6) -> str:
        """让某角色回答问题"""
        history = self._ensure_history(char_key)
        history.append({"role": "user", "content": user_text})
        self._trim(history)
        reply = llm_chat(history, temperature=temperature)
        history.append({"role": "assistant", "content": reply})
        return reply

    def reset(self, char_key: str):
        """重置某角色的聊天历史"""
        character = get_character(char_key)
        self.histories[char_key] = [{
            "role": "system",
            "content": character.system_prompt
        }]

    def export(self, char_key: str):
        """导出该角色当前的聊天历史"""
        return list(self._ensure_history(char_key))
