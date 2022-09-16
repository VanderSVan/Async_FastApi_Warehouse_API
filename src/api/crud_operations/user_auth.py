from typing import NoReturn

from src.api.models.user import UserModel
from src.api.crud_operations.user import UserOperation
from src.api.schemas.user.base_schemas import (UserPatchSchema,
                                               UserPostSchema,
                                               UserUpdatePasswordSchema)
from src.utils.exceptions.user import UserException
from src.utils.auth.password_cryptograph import PasswordCryptographer
from src.utils.celery.celery_tasks import send_email


class UserAuthOperation(UserOperation):
    async def authenticate_user(self, username: str, password: str) -> UserModel:
        user = await self.find_by_param_or_404('username', username)

        if not PasswordCryptographer.verify(password, user.hashed_password):
            UserException.raise_not_authenticate()

        return user

    @staticmethod
    def send_user_registration_email(user: UserPostSchema) -> NoReturn:
        """
        Composes email with action link and start sending letter to email using `celery`.
        """
        send_email.delay(
            username=user.username,
            email=user.email,
            action='confirm_email'
        )

    async def confirm_user_email(self, username: str) -> bool:
        user_obj: UserModel = await self.find_by_param_or_404('username', username)
        self._check_user_status(user_obj)
        return await self.patch_obj(user_obj.id, UserPatchSchema(status='confirmed'))

    @staticmethod
    def send_password_reset_email(user) -> NoReturn:
        """
        Compose email with action link and start sending letter to email using `celery`.
        """
        send_email.delay(
            username=user.username,
            email=user.email,
            action='reset_password'
        )

    async def confirm_reset_password(self, username: str, new_password: str) -> bool:
        user_obj: UserModel = await self.find_by_param_or_404('username', username)
        hashed_password: str = PasswordCryptographer.bcrypt(new_password)
        return await self.patch_obj(
            user_obj.id,
            UserUpdatePasswordSchema(hashed_password=hashed_password)
        )

    @staticmethod
    def _check_user_status(user: UserModel) -> NoReturn:
        if user.status == 'confirmed':
            UserException.raise_email_already_confirmed(user)
