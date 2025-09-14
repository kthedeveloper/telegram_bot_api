from service.asr.base_recognizer import BaseRecognizer


class WhisperRecognizer(BaseRecognizer):
    def __init__(self, url, path) -> None:
        self.url = url
        self.path = path

    async def recognize(self):
        raise NotImplementedError()