from service.asr.base_recognizer import BaseRecognizer
from service.asr.vosk import VoskRecognizer
from service.asr.whisper import WhisperRecognizer


def create_recognizer(engine, url, path) -> BaseRecognizer:
    if engine == 'vosk':
        return VoskRecognizer(url, path)
    if engine == 'whisper':
        return WhisperRecognizer(url, path)
    raise ValueError(f'Unknown recognizer engine {engine}')
