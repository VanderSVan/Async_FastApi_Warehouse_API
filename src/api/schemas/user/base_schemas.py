from typing import Literal

from pydantic import (BaseModel as BaseSchema,
                      EmailStr,
                      Field,
                      root_validator)

from src.api.schemas.validating.user import UserPasswordValidator


class UserBaseSchema(BaseSchema):
    username: str = Field(..., min_length=5, max_length=100)
    email: EmailStr
    phone: str = Field(..., min_length=9, max_length=15, regex=r'^([\d]+)$')
    role: Literal['admin'] | Literal['user'] | Literal['noname']


class UserPatchSchema(UserBaseSchema):
    username: str | None = Field(None, min_length=5, max_length=100)
    email: EmailStr | None = Field(None)
    phone: str | None = Field(None, min_length=9, max_length=15, regex=r'^([\d]+)$')
    role: Literal['admin'] | Literal['user'] | Literal['noname'] | None = Field(None)
    status: Literal['confirmed'] | Literal['unconfirmed'] | None = Field(None)


class UserDeleteSchema(UserBaseSchema):
    pass


class UserPostSchema(UserBaseSchema):
    password: str = Field(..., min_length=8, max_length=30)


class UserGetSchema(UserBaseSchema):
    id: int
    status: Literal['confirmed'] | Literal['unconfirmed']

    class Config:
        orm_mode = True


class UserResetPasswordSchema(BaseSchema):
    password: str = Field(
        ...,
        title='Password',
        min_length=8,
        max_length=30,
    )
    password_confirm: str = Field(
        ...,
        title='Repeat your password',
        min_length=8,
        max_length=30,
    )

    @root_validator()
    def user_password_validate(cls, values):
        validator = UserPasswordValidator(values)
        return validator.validate_data()


class UserUpdatePasswordSchema(UserPatchSchema):
    hashed_password: str = Field(
        ...,
        title='Hashed password',
        min_length=8,
        max_length=100,
    )
