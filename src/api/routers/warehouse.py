from dataclasses import asdict

from fastapi import APIRouter, Depends, status
from fastapi.responses import ORJSONResponse

from src.api.models.warehouse import WarehouseModel
from src.api.swagger.warehouse import (
    WarehouseInterfaceGetAll,
    WarehouseInterfaceGet,
    WarehouseInterfaceDelete,
    WarehouseInterfacePatch,
    WarehouseInterfacePost,

    WarehouseOutputGetAll,
    WarehouseOutputGet,
    WarehouseOutputDelete,
    WarehouseOutputPatch,
    WarehouseOutputPost
)
from src.api.crud_operations.warehouse import WarehouseOperation
from src.utils.response_generation.main import get_text


router = APIRouter(
    prefix="/warehouses",
    tags=["warehouses"],
)


@router.get("/", **asdict(WarehouseOutputGetAll()))
async def get_all_warehouses(warehouse: WarehouseInterfaceGetAll = Depends()
                             ) -> list[WarehouseModel] | list[None]:
    """
    Returns all warehouses from db by parameters.
    Available to all registered users.
    """
    crud = WarehouseOperation(warehouse.db)
    return await crud.find_all_by_params(name=warehouse.name,
                                         warehouse_group_id=warehouse.warehouse_group_id,
                                         offset=warehouse.offset,
                                         limit=warehouse.limit)


@router.get("/{warehouse_id}", **asdict(WarehouseOutputGet()))
async def get_warehouse(warehouse: WarehouseInterfaceGet = Depends()
                        ) -> WarehouseModel | None:
    """
    Returns one warehouse from db by warehouse id.
    Available to all registered users.
    """
    crud = WarehouseOperation(warehouse.db)
    return await crud.find_by_id(warehouse.warehouse_id)


@router.delete("/{warehouse_id}", **asdict(WarehouseOutputDelete()))
async def delete_warehouse(warehouse: WarehouseInterfaceDelete = Depends()) -> ORJSONResponse:
    """
    Deletes warehouse from db by warehouse id.
    Only available to admins.
    """
    crud = WarehouseOperation(warehouse.db)
    await crud.delete_obj(warehouse.warehouse_id)

    return ORJSONResponse(
        status_code=status.HTTP_200_OK,
        content={
            "message": get_text('delete').format(crud.model_name, warehouse.warehouse_id)
        }
    )


@router.patch("/{warehouse_id}", **asdict(WarehouseOutputPatch()))
async def patch_warehouse(warehouse: WarehouseInterfacePatch = Depends()
                          ) -> ORJSONResponse:
    """
    Updates warehouse data.
    Only available to admins.
    """
    crud = WarehouseOperation(warehouse.db)
    await crud.patch_obj(warehouse.data, warehouse.warehouse_id)

    return ORJSONResponse(
        status_code=status.HTTP_200_OK,
        content={
            "message": get_text('patch').format(crud.model_name, warehouse.warehouse_id)
        }
    )


@router.post("/create", **asdict(WarehouseOutputPost()))
async def add_warehouse(warehouse: WarehouseInterfacePost = Depends()) -> ORJSONResponse:
    """
    Adds new warehouse into db.
    Only available to admins.
    """
    crud = WarehouseOperation(warehouse.db)
    await crud.add_obj(warehouse.data)

    return ORJSONResponse(
        status_code=status.HTTP_201_CREATED,
        content={
            "message": get_text('post').format(crud.model_name)
        }
    )
