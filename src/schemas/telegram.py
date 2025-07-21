from typing import *
from pydantic import BaseModel, ConfigDict

# {"update_id": 336069162, "message": {"message_id": 25,
#                                      "from": {"id": 325645648, "is_bot": false,
#                                               "first_name": "Ilya",
#                                               "last_name": "Spirin",
#                                               "username": "Spilva",
#                                               "language_code": "ru",
#                                               "is_premium": true},
#                                      "chat": {"id": 325645648,
#                                               "first_name": "Ilya",
#                                               "last_name": "Spirin",
#                                               "username": "Spilva",
#                                               "type": "private"},
#                                      "date": 1753022959,
#                                      "voice": {"duration": 1,
#                                                "mime_type": "audio/ogg",
#                                                "file_id": "AwACAgIAAxkBAAMZaH0B7-V-PDH1yOfWfSeFRopP0JMAArp7AALBAAHoSz7P4u-cU53vNgQ",
#                                                "file_unique_id": "AgADunsAAsEAAehL",
#                                                "file_size": 1504}}}
#


# {"update_id": 336069163, "message": {"message_id": 26,
#                                      "from": {"id": 325645648, "is_bot": false,
#                                               "first_name": "Ilya",
#                                               "last_name": "Spirin",
#                                               "username": "Spilva",
#                                               "language_code": "ru",
#                                               "is_premium": true},
#                                      "chat": {"id": 325645648,
#                                               "first_name": "Ilya",
#                                               "last_name": "Spirin",
#                                               "username": "Spilva",
#                                               "type": "private"},
#                                      "date": 1753024143,
#                                      "video_note": {"duration": 2,
#                                                     "length": 384,
#                                                     "thumbnail": {
#                                                         "file_id": "AAMCAgADGQEAAxpofQaPrgIatWXy7_m0tzMM41wpwwACQXEAAv3q6EtlAAFebwX5qHYBAAdtAAM2BA",
#                                                         "file_unique_id": "AQADQXEAAv3q6Ety",
#                                                         "file_size": 18619,
#                                                         "width": 320,
#                                                         "height": 320},
#                                                     "thumb": {
#                                                         "file_id": "AAMCAgADGQEAAxpofQaPrgIatWXy7_m0tzMM41wpwwACQXEAAv3q6EtlAAFebwX5qHYBAAdtAAM2BA",
#                                                         "file_unique_id": "AQADQXEAAv3q6Ety",
#                                                         "file_size": 18619,
#                                                         "width": 320,
#                                                         "height": 320},
#                                                     "file_id": "DQACAgIAAxkBAAMaaH0Gj64CGrVl8u_5tLczDONcKcMAAkFxAAL96uhLZQABXm8F-ah2NgQ",
#                                                     "file_unique_id": "AgADQXEAAv3q6Es",
#                                                     "file_size": 168812}}}

class BaseModelExtraAllow(BaseModel):
    model_config = ConfigDict(extra='ignore')

class Chat(BaseModelExtraAllow):
    id: int
    type: str
    title: Optional[str] = None
    username: Optional[str] = None
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    is_forum: Optional[bool] = None

class Voice(BaseModelExtraAllow):
    file_id: str
    file_unique_id: str
    duration: int
    mime_type: str
    file_size: int

class Audio(BaseModelExtraAllow):
    file_id: str
    file_unique_id: str
    duration: int
    performer: Optional[str] = None
    title: Optional[str] = None
    file_name: Optional[str] = None
    mime_type: Optional[str] = None
    file_size: Optional[int] = None

class Video(BaseModelExtraAllow):
    file_id: str
    file_unique_id: str
    width: int
    height: int
    duration: int
    file_name: Optional[str] = None
    mime_type: Optional[str] = None
    file_size: Optional[int] = None

class VideoNote(BaseModelExtraAllow):
    file_id: str
    file_unique_id: str
    length: int
    duration: int
    file_size: Optional[int] = None

class Message(BaseModelExtraAllow):
    message_id: int
    chat: Chat
    text: Optional[AnyStr] = None
    voice: Optional[Voice] = None
    audio: Optional[Audio] = None
    video: Optional[Video] = None
    video_note: Optional[VideoNote] = None


class TelegramUpdate(BaseModelExtraAllow):
    update_id: int
    message: Optional[Message] = None

