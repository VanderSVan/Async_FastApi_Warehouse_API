from typing import NoReturn
from fastapi import status

from src.api.models.user import UserModel
from src.utils.exceptions.base import JSONException
from src.utils.response_generation.main import get_text


class UserException:
    @staticmethod
    def raise_not_authenticate() -> NoReturn:
        raise JSONException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            message=get_text('authenticate_failed'),
            headers={"WWW-Authenticate": "Bearer"}
        )

    @staticmethod
    def raise_forbidden_request() -> NoReturn:
        raise JSONException(
            status_code=status.HTTP_403_FORBIDDEN,
            message=get_text('forbidden_request')
        )

    @staticmethod
    def raise_email_already_confirmed(user: UserModel) -> NoReturn:
        raise JSONException(
            status_code=status.HTTP_400_BAD_REQUEST,
            message=get_text('email_already_confirmed').format(user.username)
        )

    @staticmethod
    def raise_passwords_not_equal() -> NoReturn:
        raise JSONException(
            status_code=status.HTTP_400_BAD_REQUEST,
            message=get_text('passwords_not_equal')
        )
