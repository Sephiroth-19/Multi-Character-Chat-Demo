# app.py
import gradio as gr
from conversation import ConversationManager
from characters import list_characters, get_default_character_key

# 1) 初始化：会话管理器 + 角色下拉选项
cm = ConversationManager(max_rounds=10)
CHAR_OPTS = list_characters()  # {'robin': '妮可·罗宾（仿写风格）', ...}
DEFAULT_KEY = get_default_character_key()  # 'robin'

def _export_as_chat_pairs(char_key: str):
    """
    把 export 的 messages（包含 system/user/assistant）
    转成 Chatbot 需要的 [(user, assistant), ...] 结构。
    """
    history = cm.export(char_key)
    pairs = []
    for msg in history[1:]:  # 跳过 system
        if msg["role"] == "user":
            pairs.append([msg["content"], None])
        elif msg["role"] == "assistant":
            if pairs and pairs[-1][1] is None:
                pairs[-1][1] = msg["content"]
            else:
                pairs.append([None, msg["content"]])
    return pairs

def on_send(user_text: str, char_key: str, temperature: float):
    """点击发送：让该角色回答，并刷新对话气泡"""
    if not user_text.strip():
        return gr.update(), _export_as_chat_pairs(char_key), gr.update(value="请输入消息再发送。")
    try:
        _ = cm.ask(char_key, user_text.strip(), temperature=temperature)
        return gr.update(value=""), _export_as_chat_pairs(char_key), gr.update(value="✅ 已回复")
    except Exception as e:
        # llm_service.py 里已经做过异常包装，这里友好提示
        return gr.update(), _export_as_chat_pairs(char_key), gr.update(value=f"❌ 出错：{e}")

def on_reset(char_key: str):
    """点击重置：清空该角色历史（只保留 system）"""
    cm.reset(char_key)
    return _export_as_chat_pairs(char_key), gr.update(value="🔄 已重置该角色的对话")

with gr.Blocks(title="Multi-Character Chat Demo") as demo:
    gr.Markdown("## 🧱 多角色对话 Demo\n选择一个角色，输入你的问题，看看不同人格的回答风格。")

    with gr.Row():
        # 下拉：展示“名字”，返回“key”
        char_dd = gr.Dropdown(
            choices=[(v, k) for k, v in CHAR_OPTS.items()],
            value=DEFAULT_KEY,
            label="选择角色",
            info="每个角色有独立的‘记忆’与说话风格",
        )
        temp = gr.Slider(0.0, 1.2, value=0.6, step=0.1, label="Temperature（创造力）", info="越高越发散，越低越稳定")

    chatbot = gr.Chatbot(height=460, label="对话")
    status = gr.Markdown("")  # 用来显示“已回复/报错/已重置”等状态

    with gr.Row():
        txt = gr.Textbox(placeholder="输入你的问题（回车或点发送）", label="消息")
    with gr.Row():
        send_btn = gr.Button("发送", variant="primary")
        reset_btn = gr.Button("重置该角色对话", variant="secondary")

    # 交互：发送
    send_btn.click(
        on_send,
        inputs=[txt, char_dd, temp],
        outputs=[txt, chatbot, status],
    )
    txt.submit(
        on_send,
        inputs=[txt, char_dd, temp],
        outputs=[txt, chatbot, status],
    )

    # 交互：重置
    reset_btn.click(
        on_reset,
        inputs=[char_dd],
        outputs=[chatbot, status],
    )

if __name__ == "__main__":
    demo.launch()
