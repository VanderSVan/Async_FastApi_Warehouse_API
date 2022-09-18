from dataclasses import asdict

from fastapi import APIRouter, Depends, status
from fastapi.responses import ORJSONResponse

from src.api.models.product_count import ProductCountModel
from src.api.swagger.product_count import (
    ProductCountInterfaceGetAll,
    ProductCountInterfaceGet,
    ProductCountInterfaceDelete,
    ProductCountInterfacePatch,
    ProductCountInterfacePost,

    ProductCountOutputGetAll,
    ProductCountOutputGet,
    ProductCountOutputDelete,
    ProductCountOutputPatch,
    ProductCountOutputPost
)
from src.api.crud_operations.product_count import ProductCountOperation
from src.utils.response_generation.main import get_text

router = APIRouter(
    prefix="/product_counts",
    tags=["product counts"],
)


@router.get("/", **asdict(ProductCountOutputGetAll()))
async def get_all_product_counts(product_count: ProductCountInterfaceGetAll = Depends()
                                 ) -> list[ProductCountModel] | list[None]:
    """
    Returns all product counts from db by parameters.
    Only available to admins.
    """
    crud = ProductCountOperation(product_count.db)
    return await crud.find_all_by_params(product_count=product_count.count,
                                         from_dt=product_count.from_dt,
                                         to_dt=product_count.to_dt,
                                         product_id=product_count.product_id,
                                         warehouse_group_id=product_count.warehouse_group_id,
                                         offset=product_count.offset,
                                         limit=product_count.limit)


@router.get("/{product_count_id}", **asdict(ProductCountOutputGet()))
async def get_product_count(product_count: ProductCountInterfaceGet = Depends()
                            ) -> ProductCountModel | None:
    """
    Returns one product count from db by product count id.
    Only available to admins.
    """
    crud = ProductCountOperation(product_count.db)
    return await crud.find_by_id(product_count.product_count_id)


@router.delete("/{product_count_id}", **asdict(ProductCountOutputDelete()))
async def delete_product_count(product_count: ProductCountInterfaceDelete = Depends()) -> ORJSONResponse:
    """
    Deletes product count from db by product count id.
    Only available to admins.
    """
    crud = ProductCountOperation(product_count.db)
    await crud.delete_obj(product_count.product_count_id)

    return ORJSONResponse(
        status_code=status.HTTP_200_OK,
        content={
            "message": get_text('delete').format(crud.model_name, product_count.product_count_id)
        }
    )


@router.patch("/{product_count_id}", **asdict(ProductCountOutputPatch()))
async def patch_product_count(product_count: ProductCountInterfacePatch = Depends()
                              ) -> ORJSONResponse:
    """
    Updates product count data.
    Only available to admins.
    """
    crud = ProductCountOperation(product_count.db)
    await crud.patch_obj(product_count.data, product_count.product_count_id)

    return ORJSONResponse(
        status_code=status.HTTP_200_OK,
        content={
            "message": get_text('patch').format(crud.model_name, product_count.product_count_id)
        }
    )


@router.post("/create", **asdict(ProductCountOutputPost()))
async def add_product_count(product_count: ProductCountInterfacePost = Depends()) -> ORJSONResponse:
    """
    Adds new product count into db.
    Only available to admins.
    """
    crud = ProductCountOperation(product_count.db)
    await crud.add_obj(product_count.data)

    return ORJSONResponse(
        status_code=status.HTTP_201_CREATED,
        content={
            "message": get_text('post').format(crud.model_name)
        }
    )
