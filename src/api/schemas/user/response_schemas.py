from pydantic import BaseModel

from src.utils.response_generation.main import get_text


class UserResponsePatchSchema(BaseModel):
    message: str = get_text('patch').format('user', 1)


class UserResponseDeleteSchema(BaseModel):
    message: str = get_text('delete').format('user', 1)


class UserResponsePostSchema(BaseModel):
    message: str = get_text('post').format('user', 1)


class UserResponseConfirmEmailSchema(BaseModel):
    message: str = get_text('email_confirmed')


class UserResponseResetPasswordSchema(BaseModel):
    message: str = get_text('reset_password')


class UserResponseConfirmResetPasswordSchema(BaseModel):
    message: str = get_text('changed_password')

