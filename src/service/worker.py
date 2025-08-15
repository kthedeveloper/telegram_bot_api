from schemas.telegram import TelegramUpdate
from .voice import handle_voice
from .video import handle_video
from .video_note import handle_video_note
from service.user_service import handle_start


async def process_request(update: TelegramUpdate):
    if update.message and update.message.text == "/start":
        return await handle_start(
            update.message.chat.username, update.message.chat.id
        )

    if getattr(update.message, 'voice', None):
        await handle_voice(update)
    elif getattr(update.message, 'video', None):
        await handle_video(update)
    elif getattr(update.message, 'video_note', None):
        await handle_video_note(update)