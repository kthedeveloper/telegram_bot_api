import asyncio
import json
import wave
import websockets


async def recognize(path, url):
    recognition_result = 'not recognized'
    loop = asyncio.get_running_loop()

    def send_stream(ws: websockets.ClientConnection):
        with wave.open(path, "rb") as wf:
            config = '{"config": {"sample_rate": %d}}' % wf.getframerate()
            asyncio.run_coroutine_threadsafe(ws.send(config), loop).result()

            buffer_size = int(wf.getframerate() * 0.2)

            while True:
                data = wf.readframes(buffer_size)

                if len(data) == 0:
                    break

                asyncio.run_coroutine_threadsafe(ws.send(data), loop).result()

            asyncio.run_coroutine_threadsafe(ws.send('{"eof" : 1}'),
                                             loop).result()

    async def read_stream(ws: websockets.ClientConnection):
        async for message in ws:
            try:
                m = json.loads(message)
            except json.decoder.JSONDecodeError:
                continue

            # partial = m.get('partial')
            final = m.get('text')

            # if partial:
            #     print(partial)

            if final:
                nonlocal recognition_result
                recognition_result = final

    async with websockets.connect(
            url) as ws:  # type: websockets.ClientConnection

        send = loop.run_in_executor(None, send_stream, ws)
        await asyncio.gather(asyncio.wrap_future(send), read_stream(ws))

    return recognition_result
