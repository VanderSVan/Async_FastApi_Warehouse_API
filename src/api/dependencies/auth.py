from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import Depends, status
from fastapi.security import OAuth2PasswordBearer

from src.config import get_settings
from src.api.dependencies.db import get_db
from src.api.models.user import UserModel
from src.api.schemas.jwt.base_shemas import TokenSchema
from src.api.crud_operations.user_auth import UserAuthOperation
from src.utils.exceptions.base import JSONException
from src.utils.exceptions.user import UserException
from src.utils.response_generation.main import get_text
from src.utils.auth.jwt import JWT

setting = get_settings()
api_url = setting.API_URL

oauth2_scheme = OAuth2PasswordBearer(tokenUrl=f"{api_url}/users/auth/token")


async def get_current_user(token: str = Depends(oauth2_scheme),
                           db: AsyncSession = Depends(get_db)
                           ) -> UserModel:
    """Gets the current user data from the JWT"""
    payload: dict = JWT.extract_payload_from_token(token)
    username: str = payload.get("sub")

    if username is None:
        raise JSONException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            message="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"}
        )
    token_data = TokenSchema(username=username)

    return await UserAuthOperation(db).find_by_param_or_404('username', token_data.username)


async def get_current_confirmed_user(current_user: UserModel = Depends(get_current_user)
                                     ) -> UserModel:
    """
    Gets the current user data from the JWT and checks the user's status.
    If status is 'unconfirmed' raises Unauthorized exception.
    """
    match current_user.status:
        case 'unconfirmed':
            raise JSONException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                message=get_text('email_not_confirmed')
            )
        case _:
            return current_user


async def get_current_admin(current_user: UserModel = Depends(get_current_user)
                            ) -> UserModel:
    """
    Gets the current user data from the JWT and checks the user's role.
    If role is 'client' raises Forbidden exception.
    """
    match current_user.role:
        case 'admin':
            return current_user
        case _:
            UserException.raise_forbidden_request()
