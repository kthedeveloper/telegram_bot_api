import abc


class BaseRecognizer(abc.ABC):

    @abc.abstractmethod
    async def recognize(self) -> str:
        raise NotImplementedError()
