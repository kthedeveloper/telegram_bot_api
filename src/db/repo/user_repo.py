from sqlalchemy import select
from db.session import async_session, AsyncSession
from db.models.user import User


class UserRepository:

    @staticmethod
    async def create_user(username: str, chat_id: int):
        async with async_session() as session:  # type: AsyncSession
            statement = select(User).filter(User.chat_id == chat_id)  # noqa
            result = await session.execute(statement)

            user_exists = result.one_or_none() is not None

        if not user_exists:
            async with async_session() as session:  # type: AsyncSession
                user = User(username=username, chat_id=chat_id)
                session.add(user)
                await session.commit()
