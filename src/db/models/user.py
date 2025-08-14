from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from db.models.base import Base


class User(Base):
    id = Column(Integer, primary_key=True, autoincrement=True)
    username = Column(String, unique=True, nullable=False)
    chat_id = Column(Integer, nullable=False)
