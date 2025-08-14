from schemas.telegram import TelegramUpdate
from .voice import handle_voice
from .video import handle_video
from .video_note import handle_video_note

async def process_request(update: TelegramUpdate):
    if getattr(update.message, 'voice', None):
        await handle_voice(update)
    elif getattr(update.message, 'video', None):
        await handle_video(update)
    elif getattr(update.message, 'video_note', None):
        await handle_video_note(update)