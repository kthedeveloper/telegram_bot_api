from db.repo.user_repo import UserRepository


async def handle_start(username: str, chat_id: int):
    await UserRepository.create_user(username, chat_id)

