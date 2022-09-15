from dataclasses import dataclass
from typing import Any, NoReturn

from pydantic import BaseModel as BaseSchema
from sqlalchemy import select, delete, update, insert, func, asc
from sqlalchemy.orm import Session

from src.db.db_sqlalchemy import BaseModel
from src.api.crud_operations.utils.base_crud_utils import QueryExecutor
from src.utils.exceptions.crud.base import CRUDException


@dataclass
class ModelOperation:
    model: BaseModel
    model_name: str
    patch_schema: type(BaseSchema)
    db: Session

    async def get_max_id(self) -> int:
        """
        Gets the max object id for this model in the db.
        :return: max id as int.
        """
        query = select(func.max(self.model.id))
        max_id: int | None = await QueryExecutor.get_single_result(query, self.db)

        if not max_id:
            max_id = 0

        return max_id

    async def find_all(self) -> list[BaseModel]:
        """
        Finds all objects in the db.
        :return: objects list or an empty list if no objects were found.
        """
        query = select(self.model).order_by(asc(self.model.id))
        return await QueryExecutor.get_multiple_result(query, self.db)

    async def find_by_id(self, id_: int) -> BaseModel | None:
        """
        Finds the object by the given id;
        :param id_: object id.
        :return: object or None if object not found.
        """
        query = select(self.model).where(self.model.id == id_)
        return await QueryExecutor.get_single_result(query, self.db)

    async def find_by_id_or_404(self, id_: int) -> BaseModel:
        """
        Finds the object by the given id,
        but if there is no such object, it raises an error;
        :param id_: object id.
        :return: object or raises an error if object is not found.
        """
        found_obj: BaseModel = await self.find_by_id(id_)

        if not found_obj:
            CRUDException.raise_obj_not_found(self.model_name, id_)

        return found_obj

    async def find_by_param(self, param_name: str, param_value: Any) -> BaseModel | None:
        """
        Finds the object by the given parameter.
        :return: object or None if object not found.
        """
        self._check_param_name_in_model(param_name)
        query = select(self.model).where(getattr(self.model, param_name) == param_value)
        return await QueryExecutor.get_single_result(query, self.db)

    async def find_by_param_or_404(self, param_name: str, param_value: Any) -> BaseModel | None:
        """
        Finds the object by the given parameter,
        but if there is no such object, it raises an error.
        :return: object or raise exception if object not found.
        """
        found_obj: BaseModel | None = await self.find_by_param(param_name, param_value)

        if not found_obj:
            CRUDException.raise_param_not_found(self.model_name, param_name, param_value)

        return found_obj

    async def patch_obj(self, id_: int, new_data: BaseSchema) -> bool:
        """
        Updates object values into db with new data;
        :param id_: object id;
        :param new_data: new data to update.
        :return: True or raise exception if object is not found.
        """
        await self.find_by_id_or_404(id_)
        query = update(self.model).where(self.model.id == id_).values(**new_data.dict())
        return await QueryExecutor.patch_obj(query, self.db, self.model_name)

    async def delete_obj(self, id_: int) -> bool:
        """
        Deletes object from db by the given id object;
        :param id_: True or raise exception if object is not found.
        """
        await self.find_by_id_or_404(id_)
        query = delete(self.model).where(self.model.id == id_)
        return await QueryExecutor.delete_obj(query, self.db)

    async def add_obj(self, new_data: BaseSchema) -> bool:
        """
        Adds new object into db;
        :param new_data: object data.
        :return: True or raise exception if object cannot be added.
        """
        max_obj_id: int = await self.get_max_id()
        new_obj_data: dict = dict(id=max_obj_id + 1, **new_data.dict())

        query = insert(self.model).values(new_obj_data)
        return await QueryExecutor.add_obj(query, self.db, self.model_name)

    def _check_param_name_in_model(self, param_name) -> NoReturn:
        """
        If the model does not have a given parameter name, then raises the error.
        """
        if not hasattr(self.model, param_name):
            CRUDException.raise_error_500(f"{self.model_name} has no {param_name} attribute")
