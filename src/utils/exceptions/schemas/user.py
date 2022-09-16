from typing import NoReturn
from fastapi import status

from src.utils.exceptions.base import JSONException
from src.utils.response_generation.main import get_text


class SchemaUserException:
    @staticmethod
    def raise_passwords_not_equal() -> NoReturn:
        raise JSONException(
            status_code=status.HTTP_400_BAD_REQUEST,
            message=get_text('passwords_not_equal')
        )
