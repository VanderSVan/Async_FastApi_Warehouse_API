from typing import NoReturn

from sqlalchemy.ext.asyncio import AsyncSession

from src.api.crud_operations.product import ProductOperation


async def check_product_existence(product_id: int,
                                  async_session: AsyncSession
                                  ) -> NoReturn:
    product_crud = ProductOperation(async_session)
    await product_crud.find_by_id_or_404(product_id)
