from dataclasses import dataclass
from datetime import datetime as dt
from typing import Optional, Type, Any

from fastapi import Query, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession

from src.api.schemas.current_stocks.base_schemas import CurrentStocksGetSchema

from src.api.models.user import UserModel
from src.api.dependencies.db import get_db
from src.api.dependencies.auth import get_current_admin


@dataclass
class CurrentStocksInterfaceGetAll:
    warehouse_id: int = Query(..., description="Warehouse id")
    datetime: dt = Query(default=None, description='Datetime (format: 2022-11-11T11:11:11)')
    admin: UserModel = Depends(get_current_admin)
    db: AsyncSession = Depends(get_db)


@dataclass
class CurrentStocksOutputGetAll:
    summary: Optional[str] = 'Get all current_stocks by parameters'
    description: Optional[str] = (
        "**Returns** all current_stocks from db by **parameters**.<br />"
        "Only available to **admins.**"
    )
    response_model: Optional[Type[Any]] = list[CurrentStocksGetSchema]
    status_code: Optional[int] = status.HTTP_200_OK
    response_description: str = 'List of current stocks'
