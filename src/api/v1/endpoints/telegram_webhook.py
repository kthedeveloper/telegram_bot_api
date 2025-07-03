from fastapi import APIRouter, Request, Header, HTTPException
import httpx
import os

router = APIRouter()

BOT_TOKEN = os.getenv("BOT_TOKEN")
SECRET_TOKEN = os.getenv("TELEGRAM_SECRET_TOKEN")

@router.post("/")
async def telegram_webhook(
        request: Request,
        x_telegram_bot_api_secret_token: str = Header(None),
):
    if x_telegram_bot_api_secret_token != SECRET_TOKEN:
        raise HTTPException(status_code=403, detail="Token mismatch")

    body = await request.json()

    message = body.get("message", {}).get("text")
    chat_id = body.get("message", {}).get("chat", {}).get("id")

    if chat_id and message:
        async with httpx.AsyncClient() as client:
            await client.post(
                f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage",
                json={"chat_id": chat_id, "text": f" Ваше сообщение: {message}"},
            )

    return {"ok": True}
