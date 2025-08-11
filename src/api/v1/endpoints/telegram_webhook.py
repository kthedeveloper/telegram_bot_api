from fastapi import APIRouter, BackgroundTasks, Header, HTTPException
import os

from core.config import settings
from schemas import telegram
from service.worker import process_request

router = APIRouter()


@router.post("/")
async def telegram_webhook(
        telegram_update: telegram.TelegramUpdate,
        background_tasks: BackgroundTasks,
        x_telegram_bot_api_secret_token: str = Header(None),
):
    if x_telegram_bot_api_secret_token != settings.TELEGRAM_SECRET_TOKEN:
        raise HTTPException(status_code=403, detail="Token mismatch")

    background_tasks.add_task(process_request, telegram_update)
    return {"ok": True}
