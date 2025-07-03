from typing import List

from pydantic import BaseModel


class Item(BaseModel):
    id: int
    name: str

class ItemsList(BaseModel):
    data: List[Item]
    total: int
