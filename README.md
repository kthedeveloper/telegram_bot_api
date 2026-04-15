# 🎙️ Telegram Voice-to-Text Bot (FastAPI)

Backend service for a Telegram bot that receives voice messages, processes audio, and converts speech to text using ASR engines.

---

## 🚀 Features

- ⚡ FastAPI async backend  
- 🤖 Telegram webhook
- 👤 Automatic user registration (`/start`)  
- 🎧 Voice processing pipeline:
  - download from Telegram Bot API  
  - convert `.ogg` → `.wav`  
  - send to ASR engine
  - response to user in chat
- 🧠 Pluggable ASR system:
  - base recognizer abstraction  
  - Vosk (WebSocket) integration  
  - Whisper integration  
- 🗄️ PostgreSQL (async SQLAlchemy)  
- 📦 Dockerized deployment  
- 🧪 Automated tests (pytest + testcontainers)  

---

```text
Telegram → Webhook → FastAPI → Background Task
                         ↓
                  Audio Processing
                         ↓
                    ASR Engine
                         ↓
                  Response to User
```
