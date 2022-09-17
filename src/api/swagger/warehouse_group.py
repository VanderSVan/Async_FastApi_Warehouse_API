from dataclasses import dataclass
from typing import Optional, Type, Any

from fastapi import Query, Path, Body, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession

from src.api.schemas.warehouse_groups.base_schemas import (WarehouseGroupGetSchema,
                                                           WarehouseGroupPatchSchema,
                                                           WarehouseGroupPostSchema)
from src.api.schemas.warehouse_groups.response_schemas import (WarehouseGroupResponseDeleteSchema,
                                                               WarehouseGroupResponsePatchSchema,
                                                               WarehouseGroupResponsePostSchema)
from src.api.models.user import UserModel
from src.api.dependencies.db import get_db
from src.api.dependencies.auth import (get_current_admin,
                                       get_current_confirmed_user)


@dataclass
class WarehouseGroupSwaggerGetAll:
    name: str = Query(default=None, description='Warehouse group name')
    offset: int = Query(default=None, description='How far to offset')
    limit: int = Query(default=None, description='How many limit')
    current_confirmed_user: UserModel = Depends(get_current_confirmed_user)
    db: AsyncSession = Depends(get_db)


@dataclass
class WarehouseGroupSwaggerGet:
    warehouse_group_id: int = Path(..., ge=1)
    current_confirmed_user: UserModel = Depends(get_current_confirmed_user)
    db: AsyncSession = Depends(get_db)


@dataclass
class WarehouseGroupSwaggerDelete:
    warehouse_group_id: int = Path(..., ge=1)
    admin: UserModel = Depends(get_current_admin)
    db: AsyncSession = Depends(get_db)


@dataclass
class WarehouseGroupSwaggerPatch:
    warehouse_group_id: int = Path(..., ge=1)
    data: WarehouseGroupPatchSchema = Body(..., example={'name': 'wildberries'})
    admin: UserModel = Depends(get_current_admin)
    db: AsyncSession = Depends(get_db)


@dataclass
class WarehouseGroupSwaggerPost:
    data: WarehouseGroupPostSchema = Body(..., example={'name': 'yandex-market'})
    admin: UserModel = Depends(get_current_admin)
    db: AsyncSession = Depends(get_db)


@dataclass
class WarehouseGroupOutputGetAll:
    summary: Optional[str] = 'Get all warehouse groups by parameters'
    description: Optional[str] = (
        "**Returns** all warehouse groups from db by **parameters**.<br />"
        "Available to all **registered users.**"
    )
    response_model: Optional[Type[Any]] = list[WarehouseGroupGetSchema] | None
    status_code: Optional[int] = status.HTTP_200_OK
    response_description: str = 'List of warehouse groups'


@dataclass
class WarehouseGroupOutputGet:
    summary: Optional[str] = 'Get warehouse group by warehouse group id'
    description: Optional[str] = (
        "**Returns** warehouse group from db by **warehouse group id**.<br />"
        "Available to all **registered users.**"
    )
    response_model: Optional[Type[Any]] = WarehouseGroupGetSchema | None
    status_code: Optional[int] = status.HTTP_200_OK
    response_description: str = 'WarehouseGroup data'


@dataclass
class WarehouseGroupOutputDelete:
    summary: Optional[str] = 'Delete warehouse group by warehouse group id'
    description: Optional[str] = (
        "**Deletes** warehouse group from db by **warehouse group id**. <br />"
        "Only available to **admins.**"
    )
    response_model: Optional[Type[Any]] = WarehouseGroupResponseDeleteSchema
    status_code: Optional[int] = status.HTTP_200_OK


@dataclass
class WarehouseGroupOutputPatch:
    summary: Optional[str] = 'Patch warehouse group by warehouse group id'
    description: Optional[str] = (
        "**Updates** warehouse group from db by **warehouse group id**. <br />"
        "Only available to **admins.**"
    )
    response_model: Optional[Type[Any]] = WarehouseGroupResponsePatchSchema
    status_code: Optional[int] = status.HTTP_200_OK


@dataclass
class WarehouseGroupOutputPost:
    summary: Optional[str] = 'Add new warehouse group'
    description: Optional[str] = (
        "**Adds** new warehouse group into db. <br />"
        "Only available to **admins.**"
    )
    response_model: Optional[Type[Any]] = WarehouseGroupResponsePostSchema
    status_code: Optional[int] = status.HTTP_201_CREATED
