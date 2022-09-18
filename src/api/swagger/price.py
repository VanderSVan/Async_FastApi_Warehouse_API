from dataclasses import dataclass
from datetime import datetime as dt
from typing import Optional, Type, Any

from fastapi import Query, Path, Body, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession

from src.api.schemas.price.base_schemas import (PriceGetSchema,
                                                PricePatchSchema,
                                                PricePostSchema)
from src.api.schemas.price.response_schemas import (PriceResponsePatchSchema,
                                                    PriceResponseDeleteSchema,
                                                    PriceResponsePostSchema)
from src.api.models.user import UserModel
from src.api.dependencies.db import get_db
from src.api.dependencies.auth import (get_current_admin,
                                       get_current_confirmed_user)


@dataclass
class PriceInterfaceGetAll:
    price: float = Query(default=None, description="Product price")
    from_dt: dt = Query(default=None, description='Datetime from. (format: 2022-11-11T11:11:11)')
    to_dt: dt = Query(default=None, description='To datetime. (format: 2022-11-12T11:11:11)')
    product_id: int = Query(default=None, description="Product id")
    warehouse_id: int = Query(default=None, description="Warehouse id")
    offset: int = Query(default=None, description='How far to offset')
    limit: int = Query(default=None, description='How much to limit')
    current_confirmed_user: UserModel = Depends(get_current_confirmed_user)
    db: AsyncSession = Depends(get_db)


@dataclass
class PriceInterfaceGet:
    price_id: int = Path(..., ge=1)
    current_confirmed_user: UserModel = Depends(get_current_confirmed_user)
    db: AsyncSession = Depends(get_db)


@dataclass
class PriceInterfaceDelete:
    price_id: int = Path(..., ge=1)
    admin: UserModel = Depends(get_current_admin)
    db: AsyncSession = Depends(get_db)


@dataclass
class PriceInterfacePatch:
    price_id: int = Path(..., ge=1)
    data: PricePatchSchema = Body(..., example={
        'price': 555.55,
        'datetime': "2022-11-11T11:11:11",
        'product_id': 1,
        'warehouse_id': 2,
    }
                                  )
    admin: UserModel = Depends(get_current_admin)
    db: AsyncSession = Depends(get_db)


@dataclass
class PriceInterfacePost:
    data: PricePostSchema = Body(..., example={
        'price': 11111.11,
        'datetime': "2022-11-11T11:11:11",
        'product_id': 1,
        'warehouse_id': 1,
    }
                                  )
    admin: UserModel = Depends(get_current_admin)
    db: AsyncSession = Depends(get_db)


@dataclass
class PriceOutputGetAll:
    summary: Optional[str] = 'Get all price by parameters'
    description: Optional[str] = (
        "**Returns** all prices from db by **parameters**.<br />"
        "Available to all **registered users.**"
    )
    response_model: Optional[Type[Any]] = list[PriceGetSchema] | None
    status_code: Optional[int] = status.HTTP_200_OK
    response_description: str = 'List of price'


@dataclass
class PriceOutputGet:
    summary: Optional[str] = 'Get price by price id'
    description: Optional[str] = (
        "**Returns** price from db by **price id**.<br />"
        "Available to all **registered users.**"
    )
    response_model: Optional[Type[Any]] = PriceGetSchema | None
    status_code: Optional[int] = status.HTTP_200_OK
    response_description: str = 'Price data'


@dataclass
class PriceOutputDelete:
    summary: Optional[str] = 'Delete price by price id'
    description: Optional[str] = (
        "**Deletes** price from db by **price id**. <br />"
        "Only available to **admins.**"
    )
    response_model: Optional[Type[Any]] = PriceResponseDeleteSchema
    status_code: Optional[int] = status.HTTP_200_OK


@dataclass
class PriceOutputPatch:
    summary: Optional[str] = 'Patch price by price id'
    description: Optional[str] = (
        "**Updates** price from db by **price id**. <br />"
        "Only available to **admins.**"
    )
    response_model: Optional[Type[Any]] = PriceResponsePatchSchema
    status_code: Optional[int] = status.HTTP_200_OK


@dataclass
class PriceOutputPost:
    summary: Optional[str] = 'Add new price'
    description: Optional[str] = (
        "**Adds** new price into db. <br />"
        "Only available to **admins.**"
    )
    response_model: Optional[Type[Any]] = PriceResponsePostSchema
    status_code: Optional[int] = status.HTTP_201_CREATED
