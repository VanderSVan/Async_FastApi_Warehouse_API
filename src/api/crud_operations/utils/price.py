from src.api.schemas.price.base_schemas import (PricePatchSchema,
                                                PricePostSchema)
from src.api.crud_operations.utils.warehouse_group import check_warehouse_group_existence
from src.api.crud_operations.utils.product import check_product_existence


def check_input_price_data(func):
    async def wrapper(
            self,
            new_data: PricePatchSchema | PricePostSchema,
            *args,
            **kwargs
    ):
        """
        Checks input data for patch and post `price` object.
        """
        clean_data: dict = new_data.dict(exclude_unset=True)
        if clean_data.get('product_id'):
            await check_product_existence(
                new_data.warehouse_group_id,
                self.db
            )
        if clean_data.get('warehouse_group_id'):
            await check_warehouse_group_existence(
                new_data.warehouse_group_id,
                self.db
            )
        if clean_data.get('datetime'):
            await self.raise_err_if_exists('datetime', new_data.datetime)

        return await func(self, new_data, *args, **kwargs)

    return wrapper

