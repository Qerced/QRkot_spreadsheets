import re
import string
from typing import Union

from fastapi import Depends
from fastapi_users import (
    BaseUserManager, FastAPIUsers, IntegerIDMixin, InvalidPasswordException
)
from fastapi_users.authentication import (
    AuthenticationBackend, BearerTransport, JWTStrategy
)
from fastapi_users_db_sqlalchemy import SQLAlchemyUserDatabase
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.config import settings
from app.core.db import get_async_session
from app.models import User
from app.schemas.user import UserCreate

TOKEN_URL = 'auth/jwt/login'
BACKEND_NAME = 'jwt'
REASON_PASSWORD = 'Password should be at least 3 characters'


async def get_user_db(session: AsyncSession = Depends(get_async_session)):
    yield SQLAlchemyUserDatabase(session, User)

bearer_transport = BearerTransport(tokenUrl=TOKEN_URL)


def get_jwt_strategy() -> JWTStrategy:
    return JWTStrategy(secret=settings.secret, lifetime_seconds=3600)


auth_backend = AuthenticationBackend(
    name=BACKEND_NAME,
    transport=bearer_transport,
    get_strategy=get_jwt_strategy
)


class UserManager(IntegerIDMixin, BaseUserManager[User, int]):
    async def validate_password(
            self, password: str, user: Union[UserCreate, User]
    ) -> None:
        if re.fullmatch(
            f'[{re.escape(string.ascii_letters + string.digits)}]{{3,20}}',
            password
        ) is None:
            raise InvalidPasswordException(
                reason=REASON_PASSWORD
            )


async def get_user_manager(user_crud=Depends(get_user_db)):
    yield UserManager(user_crud)

fastapi_users = FastAPIUsers[User, int](get_user_manager, [auth_backend])
current_user = fastapi_users.current_user(active=True)
current_superuser = fastapi_users.current_user(active=True, superuser=True)
