from dataclasses import dataclass
from typing import Literal, Optional, Type, Any

from fastapi import Query, Path, Body, Depends, status
from sqlalchemy.orm import Session

from src.api.schemas.user.base_schemas import (UserGetSchema,
                                               UserPatchSchema,
                                               UserPostSchema)
from src.api.schemas.user.response_schemas import (UserResponsePatchSchema,
                                                   UserResponseDeleteSchema,
                                                   UserResponsePostSchema)
from src.api.models.user import UserModel
from src.api.dependencies.db import get_db
from src.api.dependencies.auth import get_current_admin


@dataclass
class UserSwaggerGetAll:
    phone: str = Query(default=None, description="Phone number")
    status: Literal['confirmed'] | Literal['unconfirmed'] = Query(
        default=None, description="'confirmed' or 'unconfirmed'"
    )
    admin: UserModel = Depends(get_current_admin)
    db: Session = Depends(get_db)


@dataclass
class UserSwaggerGet:
    user_id: int = Path(..., ge=1)
    admin: UserModel = Depends(get_current_admin)
    db: Session = Depends(get_db)


@dataclass
class UserSwaggerDelete:
    user_id: int = Path(..., ge=1)
    admin: UserModel = Depends(get_current_admin)
    db: Session = Depends(get_db)
    
    
@dataclass
class UserSwaggerPatch:
    user_id: int = Path(..., ge=1)
    data: UserPatchSchema = Body(..., example={
        "username": "some_username",
        "email": "user@example.com",
        "phone": "123456789",
        "role": "client",
        "status": "unconfirmed"
    })
    admin: UserModel = Depends(get_current_admin)
    db: Session = Depends(get_db)


@dataclass
class UserSwaggerPost:
    data: UserPostSchema = Body(..., example={
        "username": "some_username",
        "email": "user@example.com",
        "phone": "123456789",
        "role": "client",
        "password": "some_strong_password"
    })
    admin: UserModel = Depends(get_current_admin)
    db: Session = Depends(get_db)


@dataclass
class UserOutputGetAll:
    summary: Optional[str] = 'Get all users by parameters'
    description: Optional[str] = (
        "**Returns** all users from db by **parameters**. <br />"
        "Only available to **admins.**"
    )
    response_model: Optional[Type[Any]] = list[UserGetSchema] | None
    status_code: Optional[int] = status.HTTP_200_OK
    response_description: str = 'List of users'
    

@dataclass
class UserOutputGet:
    summary: Optional[str] = 'Get user by user id'
    description: Optional[str] = (
        "**Returns** user from db by **user id**. <br />"
        "Only available to **admins.**"
    )
    response_model: Optional[Type[Any]] = UserGetSchema | None
    status_code: Optional[int] = status.HTTP_200_OK
    response_description: str = 'User data'
    

@dataclass
class UserOutputDelete:
    summary: Optional[str] = 'Delete user by user id'
    description: Optional[str] = (
        "**Deletes** user from db by **user id**. <br />"
        "Only available to **admins.**"
    )
    response_model: Optional[Type[Any]] = UserResponseDeleteSchema
    status_code: Optional[int] = status.HTTP_200_OK
    

@dataclass
class UserOutputPatch:
    summary: Optional[str] = 'Patch user by user id'
    description: Optional[str] = (
        "**Updates** user from db by **user id**. <br />"
        "Only available to **admins.**"
    )
    response_model: Optional[Type[Any]] = UserResponsePatchSchema
    status_code: Optional[int] = status.HTTP_200_OK


@dataclass
class UserOutputPost:
    summary: Optional[str] = 'Add new user'
    description: Optional[str] = (
        "**Adds** new user into db. <br />"
        "Only available to **admins.**"
    )
    response_model: Optional[Type[Any]] = UserResponsePostSchema
    status_code: Optional[int] = status.HTTP_201_CREATED

