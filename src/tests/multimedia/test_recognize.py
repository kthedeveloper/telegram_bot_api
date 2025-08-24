import pytest
from service.recognize import recognize

# !/usr/bin/env python3

import wave
import sys
import traceback


# from websocket import create_connection
#
# ws = create_connection("ws://localhost:2700")
#
# wf = wave.open(sys.argv[1], "rb")
# ws.send('{ "config" : { "sample_rate" : %d } }' % (wf.getframerate()))
# buffer_size = int(wf.getframerate() * 0.2) # 0.2 seconds of audio
#
# try:
#
#     while True:
#         data = wf.readframes(buffer_size)
#
#         if len(data) == 0:
#             break
#
#         ws.send_binary(data)
#         print (ws.recv())
#     ws.send('{"eof" : 1}')
#     print (ws.recv())
#
# except Exception as err:
#     print(''.join(traceback.format_exception(type(err), err, err.__traceback__)))

@pytest.fixture(scope="module")
def file_wav():
    return "/home/spilva/audio_2025-08-07_19-44-16.wav"


@pytest.fixture(scope="module")
def kaldi_url():
    return "ws://127.0.0.1:2700"


@pytest.mark.asyncio
async def test_recognize(file_wav, kaldi_url):
    expected_result = "один два три четыре пять"
    assert await recognize(file_wav, kaldi_url) == expected_result