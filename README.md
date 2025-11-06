# Multi-Character Chat Demo (OpenAI + Gradio)

A tiny demo that lets multiple “personas” answer the same question with distinct styles — great for learning, showcasing, and quick prototyping.

## ✨ Features
- **Multiple personas** (Robin/Kaori/Tifa/Aerith), each with its own system prompt and tone
- **Per-persona conversation memory** with automatic context trimming
- **Clean Gradio UI**: choose a persona, chat, reset, adjust temperature
- **Config via `.env`**; API key never committed

## 🧱 Tech Stack
- Python 3.10+
- [OpenAI Python SDK](https://platform.openai.com/docs/)
- [Gradio](https://www.gradio.app/)
- python-dotenv

## 📁 Project Structure
