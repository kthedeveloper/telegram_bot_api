from sqlalchemy import Column, Integer, String, BigInteger
from db.models.base import Base


class Task(Base):
    __tablename__ = "task"

    id = Column(Integer, primary_key=True, autoincrement=True)
    chat_id = Column(BigInteger, nullable=False)
    file_id = Column(String, nullable=False)
    status = Column(String, default="created", nullable=False)
