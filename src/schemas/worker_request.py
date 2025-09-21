from pydantic import BaseModel
from .telegram import TelegramUpdate

class WorkerRequest(BaseModel):
    function_name: str
    update: TelegramUpdate