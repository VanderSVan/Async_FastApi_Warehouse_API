from src.api.schemas.warehouse.base_schemas import (WarehousePatchSchema,
                                                    WarehousePostSchema)
from src.api.crud_operations.warehouse_group import WarehouseGroupOperation


def check_input_warehouse_data(func):
    async def wrapper(
            self,
            new_data: WarehousePatchSchema | WarehousePostSchema,
            *args,
            **kwargs
    ):
        """Searches `warehouse_group_id` raises 404 if it doesn't exist."""
        if hasattr(new_data, 'warehouse_group_id'):
            warehouse_group_crud = WarehouseGroupOperation(self.db)
            await warehouse_group_crud.find_by_id_or_404(new_data.warehouse_group_id)

        return await func(self, new_data, *args, **kwargs)

    return wrapper
