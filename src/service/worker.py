from db.repo.task_repo import TaskRepository
from schemas.telegram import TelegramUpdate
from .voice import handle_voice
from .video import handle_video
from .video_note import handle_video_note
from service.user_service import handle_start


async def process_request(update: TelegramUpdate):
    msg = update.message

    if msg.text == "/start":
        return await handle_start(msg.chat.username, msg.chat.id)

    chat_id = msg.chat.id

    if msg.voice:
        task = await TaskRepository.create_task(chat_id=chat_id, file_id=msg.voice.file_id, status="queued")
        await handle_voice(update)
    elif msg.video:
        task = await TaskRepository.create_task(chat_id=chat_id, file_id=msg.video.file_id, status="queued")
        await handle_video(update)
    elif msg.video_note:
        task = await TaskRepository.create_task(chat_id=chat_id, file_id=msg.video_note.file_id, status="queued")
        await handle_video_note(update)
    else:
        return {"ok": False, "reason": "unsupported"}

    await TaskRepository.set_status(task.id, "done")
    return {"ok": True, "task_id": task.id}