import asyncio
import json
import wave
import websockets
from service.asr.base_recognizer import BaseRecognizer


class VoskRecognizer(BaseRecognizer):

    def __init__(self, url, path) -> None:
        super().__init__()
        self.url = url
        self.path = path

    async def recognize(self):
        recognition_result = 'not recognized'
        loop = asyncio.get_running_loop()

        def send_stream(ws: websockets.ClientConnection):
            with wave.open(self.path, "rb") as wf:
                config = '{"config": {"sample_rate": %d}}' % wf.getframerate()
                asyncio.run_coroutine_threadsafe(ws.send(config),
                                                 loop).result()

                buffer_size = int(wf.getframerate() * 0.2)

                while True:
                    data = wf.readframes(buffer_size)

                    if len(data) == 0:
                        break

                    asyncio.run_coroutine_threadsafe(ws.send(data),
                                                     loop).result()

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
                self.url) as ws:  # type: websockets.ClientConnection

            send = loop.run_in_executor(None, send_stream, ws)
            await asyncio.gather(asyncio.wrap_future(send), read_stream(ws))

        return recognition_result
