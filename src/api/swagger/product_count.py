from dataclasses import dataclass
from datetime import datetime as dt
from typing import Optional, Type, Any

from fastapi import Query, Path, Body, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession

from src.api.schemas.product_count.base_schemas import (ProductCountGetSchema,
                                                        ProductCountPatchSchema,
                                                        ProductCountPostSchema)
from src.api.schemas.product_count.response_schemas import (ProductCountResponsePatchSchema,
                                                            ProductCountResponseDeleteSchema,
                                                            ProductCountResponsePostSchema)
from src.api.models.user import UserModel
from src.api.dependencies.db import get_db
from src.api.dependencies.auth import get_current_admin


@dataclass
class ProductCountInterfaceGetAll:
    count: int = Query(default=None, description="Product count")
    from_dt: dt = Query(default=None, description='Datetime from. (format: 2022-11-11T11:11:11)')
    to_dt: dt = Query(default=None, description='To datetime. (format: 2022-11-12T11:11:11)')
    product_id: int = Query(default=None, description="Product id")
    warehouse_id: int = Query(default=None, description="Warehouse group id")
    offset: int = Query(default=None, description='How far to offset')
    limit: int = Query(default=None, description='How much to limit')
    admin: UserModel = Depends(get_current_admin)
    db: AsyncSession = Depends(get_db)


@dataclass
class ProductCountInterfaceGet:
    product_count_id: int = Path(..., ge=1)
    admin: UserModel = Depends(get_current_admin)
    db: AsyncSession = Depends(get_db)


@dataclass
class ProductCountInterfaceDelete:
    product_count_id: int = Path(..., ge=1)
    admin: UserModel = Depends(get_current_admin)
    db: AsyncSession = Depends(get_db)


@dataclass
class ProductCountInterfacePatch:
    product_count_id: int = Path(..., ge=1)
    data: ProductCountPatchSchema = Body(..., example={
        'count': 1000,
        'datetime': "2022-11-11T11:11:11",
        'product_id': 1,
        'warehouse_id': 2,
    }
                                         )
    admin: UserModel = Depends(get_current_admin)
    db: AsyncSession = Depends(get_db)


@dataclass
class ProductCountInterfacePost:
    data: ProductCountPostSchema = Body(..., example={
        'count': 20000,
        'datetime': "2022-11-11T11:11:11",
        'product_id': 1,
        'warehouse_id': 1,
    }
                                        )
    admin: UserModel = Depends(get_current_admin)
    db: AsyncSession = Depends(get_db)


@dataclass
class ProductCountOutputGetAll:
    summary: Optional[str] = 'Get all product counts by parameters'
    description: Optional[str] = (
        "**Returns** all product counts from db by **parameters**.<br />"
        "Only available to **admins.**"
    )
    response_model: Optional[Type[Any]] = list[ProductCountGetSchema] | None
    status_code: Optional[int] = status.HTTP_200_OK
    response_description: str = 'List of product counts'


@dataclass
class ProductCountOutputGet:
    summary: Optional[str] = 'Get product count by product count id'
    description: Optional[str] = (
        "**Returns** product count from db by **product count id**.<br />"
        "Only available to **admins.**"
    )
    response_model: Optional[Type[Any]] = ProductCountGetSchema | None
    status_code: Optional[int] = status.HTTP_200_OK
    response_description: str = 'Product count data'


@dataclass
class ProductCountOutputDelete:
    summary: Optional[str] = 'Delete product count by product count id'
    description: Optional[str] = (
        "**Deletes** product count from db by **product count id**. <br />"
        "Only available to **admins.**"
    )
    response_model: Optional[Type[Any]] = ProductCountResponseDeleteSchema
    status_code: Optional[int] = status.HTTP_200_OK


@dataclass
class ProductCountOutputPatch:
    summary: Optional[str] = 'Patch product count by product count id'
    description: Optional[str] = (
        "**Updates** product count from db by **product count id**. <br />"
        "Only available to **admins.**"
    )
    response_model: Optional[Type[Any]] = ProductCountResponsePatchSchema
    status_code: Optional[int] = status.HTTP_200_OK


@dataclass
class ProductCountOutputPost:
    summary: Optional[str] = 'Add new product count'
    description: Optional[str] = (
        "**Adds** new product count into db. <br />"
        "Only available to **admins.**"
    )
    response_model: Optional[Type[Any]] = ProductCountResponsePostSchema
    status_code: Optional[int] = status.HTTP_201_CREATED
