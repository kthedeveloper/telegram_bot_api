import av
import asyncio
import os
import httpx
from core.config import settings
from schemas.telegram import *
from concurrent.futures import ThreadPoolExecutor, ProcessPoolExecutor

SAVE_DIR = "/opt/voice_messages"
os.makedirs(SAVE_DIR, exist_ok=True)

executor = ThreadPoolExecutor()
executor_process = ProcessPoolExecutor()


async def process_request(telegram_update: TelegramUpdate):
    message = telegram_update.message.text
    chat_id = telegram_update.message.chat.id
    voice = telegram_update.message.voice

    async with httpx.AsyncClient() as client:
        if chat_id and message:
            response = await client.post(
                f"https://api.telegram.org/bot{settings.TELEGRAM_BOT_TOKEN}/sendMessage",
                json={"chat_id": chat_id, "text": f"Ваше сообщение: {message}"},
            )
            print(response.status_code, response.text)
            response.raise_for_status()

        elif chat_id and voice:
            file_id = voice.file_id

            file_info_resp = await client.get(
                f"https://api.telegram.org/bot{settings.TELEGRAM_BOT_TOKEN}/getFile",
                params={"file_id": file_id}
            )
            file_info_resp.raise_for_status()
            file_path = file_info_resp.json()["result"]["file_path"]

            file_url = f"https://api.telegram.org/file/bot{settings.TELEGRAM_BOT_TOKEN}/{file_path}"
            voice_response = await client.get(file_url)
            voice_response.raise_for_status()

            file_name = f"{chat_id}_{telegram_update.message.message_id}"
            file_save_path = os.path.join(SAVE_DIR, file_name + ".ogg")
            file_save_path_wav = file_save_path + ".wav"

            def write_file():
                with open(file_save_path, "wb") as f:
                    f.write(voice_response.content)

            await asyncio.get_running_loop().run_in_executor(executor,
                                                             write_file)

            await client.post(
                f"https://api.telegram.org/bot{settings.TELEGRAM_BOT_TOKEN}/sendMessage",
                json={"chat_id": chat_id,
                      "text": "Сообщение принято в обработку"}
            )

            await asyncio.get_running_loop().run_in_executor(
                executor_process,
                transcode_audio, file_save_path, file_save_path_wav
            )


def transcode_audio(input_file_path: str, output_file_path: str):
    with av.open(input_file_path) as file_in:
        in_stream = file_in.streams.audio[0]
        with av.open(output_file_path, 'w', format='wav') as file_out:
            out_stream = file_out.add_stream(
                'pcm_s16le',  # Signed PCM 16bit
                rate=16000,
                layout='mono'
            )
            for frame in file_in.decode(in_stream):
                for packet in out_stream.encode(frame):
                    file_out.mux(packet)

            for packet in out_stream.encode():
                file_out.mux(packet)
