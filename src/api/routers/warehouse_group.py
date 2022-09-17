from dataclasses import asdict

from fastapi import APIRouter, Depends, status
from fastapi.responses import JSONResponse

from src.api.models.warehouse_group import WarehouseGroupModel
from src.api.swagger.warehouse_group import (
    WarehouseGroupSwaggerGetAll,
    WarehouseGroupSwaggerGet,
    WarehouseGroupSwaggerDelete,
    WarehouseGroupSwaggerPatch,
    WarehouseGroupSwaggerPost,

    WarehouseGroupOutputGetAll,
    WarehouseGroupOutputGet,
    WarehouseGroupOutputDelete,
    WarehouseGroupOutputPatch,
    WarehouseGroupOutputPost
)
from src.api.crud_operations.warehouse_group import WarehouseGroupOperation
from src.utils.response_generation.main import get_text


router = APIRouter(
    prefix="/warehouse_groups",
    tags=["warehouse groups"],
)


@router.get("/", **asdict(WarehouseGroupOutputGetAll()))
async def get_all_warehouse_groups(warehouse_group: WarehouseGroupSwaggerGetAll = Depends()) -> list[WarehouseGroupModel] | list[None]:
    """
    Returns all warehouse groups from db by parameters.
    Only available to admins.
    """
    crud = WarehouseGroupOperation(warehouse_group.db)

    if warehouse_group.name:
        warehouse_group: WarehouseGroupModel = await crud.find_by_param_or_404('name', warehouse_group.name.lower())
        return [warehouse_group]

    return await crud.find_all()


@router.get("/{warehouse_group_id}", **asdict(WarehouseGroupOutputGet()))
async def get_warehouse_group(warehouse_group: WarehouseGroupSwaggerGet = Depends()) -> WarehouseGroupModel | None:
    """
    Returns one warehouse group from db by warehouse group id.
    Only available to admins.
    """
    crud = WarehouseGroupOperation(warehouse_group.db)
    return await crud.find_by_id(warehouse_group.warehouse_group_id)


@router.delete("/{warehouse_group_id}", **asdict(WarehouseGroupOutputDelete()))
async def delete_warehouse_group(warehouse_group: WarehouseGroupSwaggerDelete = Depends()) -> JSONResponse:
    """
    Deletes warehouse group from db by warehouse group id.
    Only available to admins.
    """
    crud = WarehouseGroupOperation(warehouse_group.db)
    await crud.delete_obj(warehouse_group.warehouse_group_id)

    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content={
            "message": get_text('delete').format(crud.model_name, warehouse_group.warehouse_group_id)
        }
    )


@router.patch("/{warehouse_group_id}", **asdict(WarehouseGroupOutputPatch()))
async def patch_warehouse_group(warehouse_group: WarehouseGroupSwaggerPatch = Depends()) -> JSONResponse:
    """
    Updates warehouse group data.
    Only available to admins.
    """
    crud = WarehouseGroupOperation(warehouse_group.db)
    await crud.patch_obj(warehouse_group.warehouse_group_id, warehouse_group.data)

    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content={
            "message": get_text('patch').format(crud.model_name, warehouse_group.warehouse_group_id)
        }
    )


@router.post("/create", **asdict(WarehouseGroupOutputPost()))
async def add_warehouse_group(warehouse_group: WarehouseGroupSwaggerPost = Depends()) -> JSONResponse:
    """
    Adds new warehouse group into db.
    Only available to admins.
    """
    crud = WarehouseGroupOperation(warehouse_group.db)
    await crud.add_obj(warehouse_group.data)

    return JSONResponse(
        status_code=status.HTTP_201_CREATED,
        content={
            "message": get_text('post').format(crud.model_name)
        }
    )
