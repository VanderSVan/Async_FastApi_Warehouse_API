from sqlalchemy import select, update, insert, and_, desc

from src.api.schemas.price.base_schemas import (PricePatchSchema,
                                                PricePostSchema)
from src.api.crud_operations.base_crud_operations import ModelOperation
from src.api.models.price import PriceModel
from src.api.crud_operations.utils.base_crud_utils import QueryExecutor


from src.api.crud_operations.utils.price import check_input_price_data


class PriceOperation(ModelOperation):
    def __init__(self, db):
        self.model = PriceModel
        self.model_name = 'price'
        self.db = db

    async def find_all_by_params(self, **kwargs) -> list[PriceModel] | list[None]:
        """
        Searches all prices by parameters
        :param kwargs: price parameters
        :return: Found list of `PriceModel` or list of None.
        """
        price = kwargs.get('price')
        datetime = kwargs.get('datetime')
        product_id = kwargs.get('product_id')
        warehouse_group_id = kwargs.get('warehouse_group_id')
        offset = kwargs.get('offset')
        limit = kwargs.get('limit')
        query = (
            select(self.model)
            .where(
                and_(
                    (PriceModel.price <= price
                     if price is not None else True),
                    (PriceModel.datetime <= datetime
                     if datetime is not None else True),
                    (PriceModel.product_id == product_id
                     if product_id is not None else True),
                    (PriceModel.warehouse_group_id == warehouse_group_id
                     if warehouse_group_id is not None else True)
                )
            )
            .order_by(desc(self.model.datetime))
            .offset(offset)
            .limit(limit)
        )
        return await QueryExecutor.get_multiple_result(query, self.db)

    @check_input_price_data
    async def patch_obj(self, new_data: PricePatchSchema, id_: int) -> bool:
        """
        Updates price values into db with new data;
        :param id_: price id;
        :param new_data: new data to update.
        :return: True or raise exception if price is not found.
        """
        await self.find_by_id_or_404(id_)
        query = (update(self.model)
                 .where(self.model.id == id_)
                 .values(**new_data.dict(exclude_unset=True))
                 )
        return await QueryExecutor.patch_obj(query, self.db, self.model_name)

    @check_input_price_data
    async def add_obj(self, new_data: PricePostSchema) -> bool:
        """
        Adds new price into db;
        :param new_data: price data.
        :return: True or raise exception if price cannot be added.
        """
        max_obj_id: int = await self.get_max_id()
        new_obj_data: dict = dict(id=max_obj_id + 1, **new_data.dict())

        query = insert(self.model).values(new_obj_data)
        return await QueryExecutor.add_obj(query, self.db, self.model_name)