from typing import NoReturn

from sqlalchemy.ext.asyncio import AsyncSession

from src.api.crud_operations.warehouse_group import WarehouseGroupOperation


async def check_warehouse_group_existence(warehouse_group_id: int,
                                          async_session: AsyncSession
                                          ) -> NoReturn:
    warehouse_group_crud = WarehouseGroupOperation(async_session)
    await warehouse_group_crud.find_by_id_or_404(warehouse_group_id)
