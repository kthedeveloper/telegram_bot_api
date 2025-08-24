import os
import asyncio
import httpx
from concurrent.futures import ThreadPoolExecutor, ProcessPoolExecutor
from core.config import settings
from schemas.telegram import TelegramUpdate
from .transcode import transcode_audio
from .utils import write_file

SAVE_DIR = "/opt/voice_messages"
os.makedirs(SAVE_DIR, exist_ok=True)

executor = ThreadPoolExecutor()
executor_process = ProcessPoolExecutor()


async def handle_voice(telegram_update: TelegramUpdate):
    chat_id = telegram_update.message.chat.id
    voice = telegram_update.message.voice

    async with httpx.AsyncClient() as client:
        file_info_resp = await client.get(
            f"https://api.telegram.org/bot{settings.TELEGRAM_BOT_TOKEN}/getFile",
            params={"file_id": voice.file_id}
        )
        file_info_resp.raise_for_status()
        file_path = file_info_resp.json()["result"]["file_path"]

        voice_response = await client.get(
            f"https://api.telegram.org/file/bot{settings.TELEGRAM_BOT_TOKEN}/{file_path}"
        )
        voice_response.raise_for_status()

        file_name = f"{chat_id}_{telegram_update.message.message_id}"
        file_save_path = os.path.join(SAVE_DIR, file_name + ".ogg")
        file_save_path_wav = file_save_path + ".wav"

        await asyncio.get_running_loop().run_in_executor(
            executor, write_file, file_save_path, voice_response.content)

        await asyncio.get_running_loop().run_in_executor(
            executor_process, transcode_audio, file_save_path, file_save_path_wav
        )

        return file_save_path_wav