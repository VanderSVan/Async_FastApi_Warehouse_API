from dataclasses import dataclass
from typing import Optional, Type, Any

from fastapi import Query, Path, Body, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession

from src.api.schemas.warehouse.base_schemas import (WarehouseGetSchema,
                                                    WarehousePatchSchema,
                                                    WarehousePostSchema)
from src.api.schemas.warehouse.response_schemas import (WarehouseResponsePatchSchema,
                                                        WarehouseResponseDeleteSchema,
                                                        WarehouseResponsePostSchema)
from src.api.models.user import UserModel
from src.api.dependencies.db import get_db
from src.api.dependencies.auth import (get_current_admin,
                                       get_current_confirmed_user)


@dataclass
class WarehouseInterfaceGetAll:
    name: str = Query(default=None, description="Warehouse name")
    warehouse_group_id: int = Query(default=None, description="Warehouse group id")
    offset: int = Query(default=None, description='How far to offset')
    limit: int = Query(default=None, description='How many limit')
    current_confirmed_user: UserModel = Depends(get_current_confirmed_user)
    db: AsyncSession = Depends(get_db)


@dataclass
class WarehouseInterfaceGet:
    warehouse_id: int = Path(..., ge=1)
    current_confirmed_user: UserModel = Depends(get_current_confirmed_user)
    db: AsyncSession = Depends(get_db)


@dataclass
class WarehouseInterfaceDelete:
    warehouse_id: int = Path(..., ge=1)
    admin: UserModel = Depends(get_current_admin)
    db: AsyncSession = Depends(get_db)


@dataclass
class WarehouseInterfacePatch:
    warehouse_id: int = Path(..., ge=1)
    data: WarehousePatchSchema = Body(..., example={'name': 'number-1',
                                                    'warehouse_group_id': 1}
                                      )
    admin: UserModel = Depends(get_current_admin)
    db: AsyncSession = Depends(get_db)


@dataclass
class WarehouseInterfacePost:
    data: WarehousePostSchema = Body(..., example={'name': 'number-2',
                                                   'warehouse_group_id': 2}
                                     )
    admin: UserModel = Depends(get_current_admin)
    db: AsyncSession = Depends(get_db)


@dataclass
class WarehouseOutputGetAll:
    summary: Optional[str] = 'Get all warehouse by parameters'
    description: Optional[str] = (
        "**Returns** all warehouse from db by **parameters**.<br />"
        "Available to all **registered users.**"
    )
    response_model: Optional[Type[Any]] = list[WarehouseGetSchema] | None
    status_code: Optional[int] = status.HTTP_200_OK
    response_description: str = 'List of warehouse'


@dataclass
class WarehouseOutputGet:
    summary: Optional[str] = 'Get warehouse by warehouse id'
    description: Optional[str] = (
        "**Returns** warehouse from db by **warehouse id**.<br />"
        "Available to all **registered users.**"
    )
    response_model: Optional[Type[Any]] = WarehouseGetSchema | None
    status_code: Optional[int] = status.HTTP_200_OK
    response_description: str = 'Warehouse data'


@dataclass
class WarehouseOutputDelete:
    summary: Optional[str] = 'Delete warehouse by warehouse id'
    description: Optional[str] = (
        "**Deletes** warehouse from db by **warehouse id**. <br />"
        "Only available to **admins.**"
    )
    response_model: Optional[Type[Any]] = WarehouseResponseDeleteSchema
    status_code: Optional[int] = status.HTTP_200_OK


@dataclass
class WarehouseOutputPatch:
    summary: Optional[str] = 'Patch warehouse by warehouse id'
    description: Optional[str] = (
        "**Updates** warehouse from db by **warehouse id**. <br />"
        "Only available to **admins.**"
    )
    response_model: Optional[Type[Any]] = WarehouseResponsePatchSchema
    status_code: Optional[int] = status.HTTP_200_OK


@dataclass
class WarehouseOutputPost:
    summary: Optional[str] = 'Add new warehouse'
    description: Optional[str] = (
        "**Adds** new warehouse into db. <br />"
        "Only available to **admins.**"
    )
    response_model: Optional[Type[Any]] = WarehouseResponsePostSchema
    status_code: Optional[int] = status.HTTP_201_CREATED

