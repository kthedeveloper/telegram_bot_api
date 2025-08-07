from fastapi import APIRouter, Request, Header, HTTPException
import httpx
import os

from core.config import settings
from schemas import telegram

router = APIRouter()

SAVE_DIR = "/opt/voice_messages"
os.makedirs(SAVE_DIR, exist_ok=True)


@router.post("/")
async def telegram_webhook(
        telegram_update: telegram.TelegramUpdate,
        x_telegram_bot_api_secret_token: str = Header(None),
):
    if x_telegram_bot_api_secret_token != settings.TELEGRAM_SECRET_TOKEN:
        raise HTTPException(status_code=403, detail="Token mismatch")

    message = telegram_update.message.text
    chat_id = telegram_update.message.chat.id
    voice = telegram_update.message.voice
    async with httpx.AsyncClient() as client:
        if chat_id and message:
                response = await client.post(
                    f"https://api.telegram.org/bot{settings.TELEGRAM_BOT_TOKEN}/sendMessage",
                    json={"chat_id": chat_id, "text": f"Ваше сообщение: {message}"},
                )
                print(response.status_code, response.text)
                response.raise_for_status()

        elif chat_id and voice:
            file_id = voice.file_id

            file_info_resp = await client.get(
                f"https://api.telegram.org/bot{settings.TELEGRAM_BOT_TOKEN}/getFile", params={"file_id": file_id}
            )
            file_info_resp.raise_for_status()
            file_path = file_info_resp.json()["result"]["file_path"]

            file_url = f"https://api.telegram.org/file/bot{settings.TELEGRAM_BOT_TOKEN}/{file_path}"
            voice_response = await client.get(file_url)
            voice_response.raise_for_status()

            file_name = f"{chat_id}_{telegram_update.message.message_id}.ogg"
            file_save_path = os.path.join(SAVE_DIR, file_name)
            with open(file_save_path, "wb") as f:
                f.write(voice_response.content)

            await client.post(
                f"https://api.telegram.org/bot{settings.TELEGRAM_BOT_TOKEN}/sendMessage",
                json={"chat_id": chat_id, "text": "Сообщение принято в обработку"}
            )

        return {"ok": True}
