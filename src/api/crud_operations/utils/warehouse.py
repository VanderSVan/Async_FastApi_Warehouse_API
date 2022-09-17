from src.api.schemas.warehouse.base_schemas import (WarehousePatchSchema,
                                                    WarehousePostSchema)
from src.api.crud_operations.utils.warehouse_group import check_warehouse_group_existence


def check_input_warehouse_data(func):
    async def wrapper(
            self,
            new_data: WarehousePatchSchema | WarehousePostSchema,
            *args,
            **kwargs
    ):
        """
        Checks input data for patch and post `warehouse` object.
        """
        if hasattr(new_data, 'warehouse_group_id'):
            await check_warehouse_group_existence(
                new_data.warehouse_group_id,
                self.db
            )

        return await func(self, new_data, *args, **kwargs)

    return wrapper
