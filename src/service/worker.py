import httpx

from core.config import settings
from schemas.telegram import TelegramUpdate
from .voice import handle_voice
from .video import handle_video
from .video_note import handle_video_note
from service.user_service import handle_start
from service.recognize import recognize


async def process_request(update: TelegramUpdate):
    if update.message and update.message.text == "/start":
        return await handle_start(
            update.message.chat.username, update.message.chat.id
        )

    # TODO: create task entry (in database)
    if getattr(update.message, 'voice', None):
        wav_path = await handle_voice(update)
        # TODO: put kaldi url to the config
        recognized = await recognize(wav_path, "ws://127.0.0.1:2700")
        await send_message_tg(recognized, update.message.chat.id)

    elif getattr(update.message, 'video', None):
        await handle_video(update)
    elif getattr(update.message, 'video_note', None):
        await handle_video_note(update)
    # TODO: mark task complete


async def send_message_tg(message, chat_id):
    async with httpx.AsyncClient() as client:
        response = await client.post(
            f"https://api.telegram.org/bot{settings.TELEGRAM_BOT_TOKEN}/sendMessage",
            json={"chat_id": chat_id, "text": f"Ваше сообщение: {message}"},
        )
        print(response.status_code, response.text)
        response.raise_for_status()
