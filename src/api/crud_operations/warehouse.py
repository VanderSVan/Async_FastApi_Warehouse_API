from sqlalchemy import select, update, insert, and_, asc

from src.api.schemas.warehouse.base_schemas import (WarehousePatchSchema,
                                                    WarehousePostSchema)
from src.api.crud_operations.base_crud_operations import ModelOperation
from src.api.models.warehouse import WarehouseModel
from src.api.crud_operations.utils.base_crud_utils import QueryExecutor
from src.api.crud_operations.utils.warehouse import check_input_warehouse_data


class WarehouseOperation(ModelOperation):
    def __init__(self, db):
        self.model = WarehouseModel
        self.model_name = 'warehouse'
        self.db = db

    async def find_all_by_params(self, **kwargs) -> list[WarehouseModel] | list[None]:
        """
        Searches all warehouses by parameters
        :param kwargs: warehouse parameters
        :return: Found list of `WarehouseModel` or list of None.
        """
        name = kwargs.get('name')
        warehouse_group_id = kwargs.get('warehouse_group_id')
        offset = kwargs.get('offset')
        limit = kwargs.get('limit')
        query = (
            select(self.model)
            .where(
                and_(
                    (WarehouseModel.name == name
                     if name is not None else True),
                    (WarehouseModel.warehouse_group_id == warehouse_group_id
                     if warehouse_group_id is not None else True)
                )
            )
            .order_by(asc(self.model.id))
            .offset(offset)
            .limit(limit)
        )
        return await QueryExecutor.get_multiple_result(query, self.db)

    @check_input_warehouse_data
    async def patch_obj(self, new_data: WarehousePatchSchema, id_: int) -> bool:
        """
        Updates warehouse values into db with new data;
        :param id_: warehouse id;
        :param new_data: new data to update.
        :return: True or raise exception if warehouse is not found.
        """
        await self.find_by_id_or_404(id_)
        query = (update(self.model)
                 .where(self.model.id == id_)
                 .values(**new_data.dict(exclude_unset=True))
                 )
        return await QueryExecutor.patch_obj(query, self.db, self.model_name)

    @check_input_warehouse_data
    async def add_obj(self, new_data: WarehousePostSchema) -> bool:
        """
        Adds new warehouse into db;
        :param new_data: warehouse data.
        :return: True or raise exception if warehouse cannot be added.
        """
        max_obj_id: int = await self.get_max_id()
        new_obj_data: dict = dict(id=max_obj_id + 1, **new_data.dict())

        query = insert(self.model).values(new_obj_data)
        return await QueryExecutor.add_obj(query, self.db, self.model_name)
