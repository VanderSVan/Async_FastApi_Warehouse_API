from dataclasses import dataclass
from typing import Optional, Type, Any

from fastapi import Depends, Path, Body, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from src.api.schemas.user.base_schemas import (UserGetSchema,
                                               UserPostSchema,
                                               UserResetPasswordSchema)
from src.api.schemas.user.response_schemas import (UserResponseConfirmEmailSchema,
                                                   UserResponseResetPasswordSchema,
                                                   UserResponseConfirmResetPasswordSchema)
from src.api.models.user import UserModel
from src.api.dependencies.db import get_db
from src.api.dependencies.auth import get_current_confirmed_user
from src.api.schemas.jwt.response_schemas import TokenResponseSchema


@dataclass
class UserAuthSwaggerGetUser:
    current_confirmed_user: UserModel = Depends(get_current_confirmed_user)
    db: Session = Depends(get_db)


@dataclass
class UserAuthSwaggerCreateToken:
    form_data: OAuth2PasswordRequestForm = Depends()
    db: Session = Depends(get_db)


@dataclass
class UserAuthSwaggerRegisterUser:
    data: UserPostSchema = Body(
        ...,
        example={
            'username': 'some_user',
            'email': 'some_user@example.com',
            'phone': '123456789123456',
            'role': 'user',
            'password': 'really_strong_password'
        }
    )
    db: Session = Depends(get_db)


@dataclass
class UserAuthSwaggerConfirmEmail:
    sign: str = Path(..., description='It is encoded user data, such as a username')
    db: Session = Depends(get_db)


@dataclass
class UserAuthSwaggerResetPassword:
    current_confirmed_user: UserModel = Depends(get_current_confirmed_user)
    db: Session = Depends(get_db)


@dataclass
class UserAuthSwaggerConfirmResetPassword:
    sign: str = Path(..., description='It is encoded user data, such as a username')
    new_password_data: UserResetPasswordSchema = Body(
        ...,
        example={
            'password': 'really_strong_password',
            'password_confirm': 'really_strong_password'
        }
    )
    db: Session = Depends(get_db)


@dataclass
class UserAuthOutputGetCurrentUser:
    summary: Optional[str] = 'Get current user info'
    description: Optional[str] = (
        "**Returns** current user info. <br />"
        "Available to all **confirmed users.**"
    )
    response_model: Optional[Type[Any]] = UserGetSchema
    status_code: Optional[int] = status.HTTP_200_OK
    response_description: str = 'Current user'


@dataclass
class UserAuthOutputConfirmEmail:
    summary: Optional[str] = 'Confirm email address'
    description: Optional[str] = (
        "**Confirms** user's email. <br />"
        "**Accessible to all.** <br />"
        "**sign**: it is encoded user data, such as a username."
    )
    response_model: Optional[Type[Any]] = UserResponseConfirmEmailSchema
    status_code: Optional[int] = status.HTTP_200_OK


@dataclass
class UserAuthOutputResetPassword:
    summary: Optional[str] = "Reset user's password"
    description: Optional[str] = (
        "**Resets** user's password. <br />"
        "Available to all **confirmed users.**"
    )
    response_model: Optional[Type[Any]] = UserResponseResetPasswordSchema
    status_code: Optional[int] = status.HTTP_200_OK


@dataclass
class UserAuthOutputGetToken:
    summary: Optional[str] = 'Get user token via login'
    description: Optional[str] = (
        "**Gets** user token by entering your username and password. <br />"
        "**Accessible to all.**"
    )
    response_model: Optional[Type[Any]] = TokenResponseSchema
    status_code: Optional[int] = status.HTTP_200_OK


@dataclass
class UserAuthOutputRegister:
    summary: Optional[str] = 'Register a new user'
    description: Optional[str] = (
        "**Gets** new user data and saves it into db. <br />"
        "**Accessible to all.**"
    )
    response_model: Optional[Type[Any]] = UserGetSchema
    status_code: Optional[int] = status.HTTP_200_OK


@dataclass
class UserAuthOutputConfirmNewPassword:
    summary: Optional[str] = "Confirm new user's password"
    description: Optional[str] = (
        "**Gets** the user's new password and saves it in the database. <br />"
        "**Accessible to all.** <br />"
        "**sign**: it is encoded user data, such as a username."
    )
    response_model: Optional[Type[Any]] = UserResponseConfirmResetPasswordSchema
    status_code: Optional[int] = status.HTTP_200_OK

