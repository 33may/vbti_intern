import pytest
from unittest.mock import patch, AsyncMock
from app.services.userService import fetch_users, fetch_user, create_user, delete_user, login_user, get_user_by_email
from app.schemas.userSchema import UserAdd, UserLogin, UserGet
from app.utils.exceptions.NotFound import NotFound
from app.utils.exceptions.alreadyExistEx import AlreadyExistEx
from app.utils.exceptions.WrongCredentials import WrongCredentials


@pytest.mark.asyncio
async def test_fetch_users():
    with patch('app.db.repos.userRepo.UserRepo.db_get_users', new_callable=AsyncMock) as mock_db_get_users:
        mock_db_get_users.return_value = [UserGet(id=1, email="test@example.com")]

        result = await fetch_users()

        assert len(result) == 1
        assert result[0].email == "test@example.com"


@pytest.mark.asyncio
async def test_fetch_user_success():
    with patch('app.db.repos.userRepo.UserRepo.db_get_user_by_id', new_callable=AsyncMock) as mock_db_get_user_by_id:
        mock_db_get_user_by_id.return_value = UserGet(id=1, email="test@example.com")

        result = await fetch_user(1)

        assert result.email == "test@example.com"


@pytest.mark.asyncio
async def test_fetch_user_not_found():
    with patch('app.db.repos.userRepo.UserRepo.db_get_user_by_id', new_callable=AsyncMock) as mock_db_get_user_by_id:
        mock_db_get_user_by_id.return_value = None

        with pytest.raises(NotFound):
            await fetch_user(1)


@pytest.mark.asyncio
async def test_create_user_already_exists():
    with patch('app.db.repos.userRepo.UserRepo.db_get_user_by_email',
               new_callable=AsyncMock) as mock_db_get_user_by_email:
        mock_db_get_user_by_email.return_value = UserGet(id=1, email="test@example.com")

        with pytest.raises(AlreadyExistEx):
            await create_user(UserAdd(email="test@example.com", password="password123"))


@pytest.mark.asyncio
async def test_create_user_success():
    with patch('app.db.repos.userRepo.UserRepo.db_get_user_by_email',
               new_callable=AsyncMock) as mock_db_get_user_by_email:
        mock_db_get_user_by_email.return_value = None

        with patch('app.db.repos.userRepo.UserRepo.db_add_user', new_callable=AsyncMock) as mock_db_add_user:
            mock_db_add_user.return_value = UserGet(id=1, email="newuser@example.com")

            with patch('app.services.userService.createToken', return_value="token123"):
                token = await create_user(UserAdd(email="newuser@example.com", password="password123"))

                assert token == "token123"


@pytest.mark.asyncio
async def test_delete_user_success():
    with patch('app.db.repos.userRepo.UserRepo.db_get_user_by_id', new_callable=AsyncMock) as mock_db_get_user_by_id:
        mock_db_get_user_by_id.return_value = UserGet(id=1, email="test@example.com")

        with patch('app.db.repos.userRepo.UserRepo.db_delete_user', new_callable=AsyncMock) as mock_db_delete_user:
            await delete_user(1)
            mock_db_delete_user.assert_called_once()


@pytest.mark.asyncio
async def test_delete_user_not_found():
    with patch('app.db.repos.userRepo.UserRepo.db_get_user_by_id', new_callable=AsyncMock) as mock_db_get_user_by_id:
        mock_db_get_user_by_id.return_value = None

        with pytest.raises(NotFound):
            await delete_user(1)


@pytest.mark.asyncio
async def test_login_user_success():
    with patch('app.db.repos.userRepo.UserRepo.db_verify_user', new_callable=AsyncMock) as mock_db_verify_user:
        mock_db_verify_user.return_value = UserGet(id=1, email="test@example.com")

        with patch('app.services.userService.createToken', return_value="token123"):
            token = await login_user(UserLogin(email="test@example.com", password="password"))

            assert token == "token123"


@pytest.mark.asyncio
async def test_login_user_wrong_credentials():
    with patch('app.db.repos.userRepo.UserRepo.db_verify_user', new_callable=AsyncMock) as mock_db_verify_user:
        mock_db_verify_user.return_value = None

        with pytest.raises(WrongCredentials):
            await login_user(UserLogin(email="test@example.com", password="wrongpassword"))
