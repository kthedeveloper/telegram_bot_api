import asyncio

import httpx

from core.config import settings
from schemas.telegram import TelegramUpdate
# from .voice import handle_voice
# from .video import handle_video
# from .video_note import handle_video_note
from service.user_service import handle_start
# from service.asr.recognizer_factory import create_recognizer
from service.rpc.client import RpcClient


async def process_request(update: TelegramUpdate):
    if update.message and update.message.text == "/start":
        return await handle_start(
            update.message.chat.username, update.message.chat.id
        )

    rpc_client = RpcClient(asyncio.get_running_loop())

    # TODO: create task entry (in database)
    if getattr(update.message, 'voice', None):
        await rpc_client.call("handle_voice_request", update)

    elif getattr(update.message, 'video', None):
        await rpc_client.call("handle_video_request", update)

    elif getattr(update.message, 'video_note', None):
        await rpc_client.call("handle_video_note_request", update)
    # TODO: mark task complete


async def send_message_tg(message, chat_id):
    async with httpx.AsyncClient() as client:
        response = await client.post(
            f"https://api.telegram.org/bot{settings.TELEGRAM_BOT_TOKEN}/sendMessage",
            json={"chat_id": chat_id, "text": f"Ваше сообщение: {message}"},
        )
        print(response.status_code, response.text)
        response.raise_for_status()
