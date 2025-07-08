from fastapi import APIRouter, Request, Header, HTTPException
import httpx

from core.config import settings

router = APIRouter()


@router.post("/")
async def telegram_webhook(
        request: Request,
        x_telegram_bot_api_secret_token: str = Header(None),
):
    if x_telegram_bot_api_secret_token != settings.SECRET_TOKEN:
        raise HTTPException(status_code=403, detail="Token mismatch")

    body = await request.json()

    message = body.get("message", {}).get("text")
    chat_id = body.get("message", {}).get("chat", {}).get("id")

    if chat_id and message:
        async with httpx.AsyncClient() as client:
            response = await client.post(
                f"https://api.telegram.org/bot{settings.BOT_TOKEN}/sendMessage",
                json={"chat_id": chat_id, "text": f"Ваше сообщение: {message}"},
            )
            print(response.status_code, response.text)
            response.raise_for_status()

    return {"ok": True}
