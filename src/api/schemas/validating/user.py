from dataclasses import dataclass
from typing import NoReturn

from fastapi import status

from src.utils.exceptions.base import JSONException


@dataclass
class UserPasswordValidator:
    """Checks user password"""
    password_data: dict

    def validate_data(self) -> dict:
        """Main validator."""
        self._validate_password()
        return self.password_data

    def _validate_password(self) -> NoReturn:
        """Checks passwords for equality."""

        password: str = self.password_data.get('password')
        password_confirm: str = self.password_data.get('password_confirm')

        if password != password_confirm:
            raise JSONException(
                status_code=status.HTTP_400_BAD_REQUEST,
                message="Data of fields password and password_confirm must be equal"
            )
