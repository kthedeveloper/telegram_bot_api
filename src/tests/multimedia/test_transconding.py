import os
from service.worker import transcode_audio


def test_transconding():
    file_ogg = "/home/spilva/audio_2025-08-07_19-44-16.ogg"
    file_wav = "/home/spilva/audio_2025-08-07_19-44-16.wav"

    transcode_audio(file_ogg, file_wav)

    file_info = os.stat(file_wav)

    assert file_info.st_size > 0
