from fastapi import APIRouter, Request, Header, HTTPException
import httpx

from core.config import settings
from schemas import telegram

router = APIRouter()


@router.post("/")
async def telegram_webhook(
        telegram_update: telegram.TelegramUpdate,
        x_telegram_bot_api_secret_token: str = Header(None),
):
    if x_telegram_bot_api_secret_token != settings.TELEGRAM_SECRET_TOKEN:
        raise HTTPException(status_code=403, detail="Token mismatch")

    message = telegram_update.message.text
    chat_id = telegram_update.message.chat.id

    if chat_id and message:
        async with httpx.AsyncClient() as client:
            response = await client.post(
                f"https://api.telegram.org/bot{settings.TELEGRAM_BOT_TOKEN}/sendMessage",
                json={"chat_id": chat_id, "text": f"Ваше сообщение: {message}"},
            )
            print(response.status_code, response.text)
            response.raise_for_status()

    return {"ok": True}
