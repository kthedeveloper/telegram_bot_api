import pytest
import pytest_mock

from unittest.mock import AsyncMock, MagicMock, patch

from db.repo.user_repo import UserRepository
from service.user_service import handle_start


@pytest.mark.asyncio
async def test_user_service():
    with patch('db.repo.user_repo.UserRepository.create_user') as mock:
        await handle_start("user", 1234)
        mock.assert_awaited_once()
        assert mock.await_args.args == ("user", 1234)


@pytest.mark.asyncio
async def test_user_service_():
    UserRepository.create_user = AsyncMock()
    await handle_start("user", 1234)
    UserRepository.create_user.assert_awaited_once()
    assert UserRepository.create_user.await_args.args == ("user", 1234)