from dataclasses import dataclass
from typing import NoReturn

from src.utils.exceptions.schemas.user import SchemaUserException


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
            SchemaUserException.raise_passwords_not_equal()
