import json
import asyncio
import aiormq

from service.voice import handle_voice
from service.video import handle_video
from service.video_note import handle_video_note
from service.asr.recognizer_factory import create_recognizer
from schemas.worker_request import WorkerRequest
from schemas.telegram import TelegramUpdate
from service.worker import send_message_tg



async def handle_wav(wav_path, chat_id):
    recognizer = create_recognizer("vosk", wav_path, "ws://127.0.0.1:2700")
    recognized = await recognizer.recognize()

    await send_message_tg(recognized, chat_id)


async def handle_voice_request(update: TelegramUpdate):
    wav_path = handle_voice(update)
    await handle_wav(wav_path, update.message.chat.id)

async def handle_video_request(update: TelegramUpdate):
    wav_path = handle_video(update)
    await handle_wav(wav_path, update.message.chat.id)

async def handle_video_note_request(update: TelegramUpdate):
    wav_path = handle_video_note(update)
    await handle_wav(wav_path, update.message.chat.id)



callback_map = {
    "handle_voice_request": handle_voice_request,
    "handle_video_request": handle_video_request,
    "handle_video_note_request": handle_video_note_request,
}


async def on_message(message:aiormq.abc.DeliveredMessage):
    # expect body to be WorkerRequest
    body = str(message.body.decode())

    request = WorkerRequest(**json.load(body))  # noqa

    func = callback_map.get(request.function_name)
    if func is None:
        raise ValueError("unexpected function name requested")

    response = str(await func(request.update)).encode()

    await message.channel.basic_publish(
        response, routing_key=message.header.properties.reply_to,
        properties=aiormq.spec.Basic.Properties(
            correlation_id=message.header.properties.correlation_id
        ),
    )

    await message.channel.basic_ack(message.delivery.delivery_tag)


async def main():
    # Perform connection
    # TODO: create config option
    connection = await aiormq.connect("amqp://guest:guest@localhost/")

    # Creating a channel
    channel = await connection.channel()

    # Declaring queue
    # TODO: create config option
    declare_ok = await channel.queue_declare('rpc_queue')

    # Start listening the queue with name 'hello'
    await channel.basic_consume(declare_ok.queue, on_message)

if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.create_task(main())

    loop.run_forever()