from typing import Iterable, Optional
from sqlalchemy import select, update
from db.session import async_session
from db.models.task import Task

class TaskRepository:
    @staticmethod
    async def create_task(chat_id: int, file_id: str, status: str = "queued") -> Task:
        async with async_session() as session:
            task = Task(chat_id=chat_id, file_id=file_id, status=status)
            session.add(task)
            await session.commit()
            await session.refresh(task)
            return task

    @staticmethod
    async def set_status(task_id: int, status: str) -> None:
        async with async_session() as session:
            await session.execute(
                update(Task).where(Task.id == task_id).values(status=status)
            )
            await session.commit()

    @staticmethod
    async def list_unfinished(statuses: Iterable[str] = ("queued", "processing")) -> list[Task]:
        async with async_session() as session:
            res = await session.execute(
                select(Task).where(Task.status.in_(statuses))
            )
            return list(res.scalars().all())

    @staticmethod
    async def get(task_id: int) -> Optional[Task]:
        async with async_session() as session:
            res = await session.execute(select(Task).where(Task.id == task_id))
            return res.scalar_one_or_none()
