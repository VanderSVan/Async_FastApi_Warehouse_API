from dataclasses import asdict

from fastapi import APIRouter, Depends, status
from fastapi.responses import JSONResponse

from src.api.models.product import ProductModel
from src.api.swagger.product import (
    ProductSwaggerGetAll,
    ProductSwaggerGet,
    ProductSwaggerDelete,
    ProductSwaggerPatch,
    ProductSwaggerPost,

    ProductOutputGetAll,
    ProductOutputGet,
    ProductOutputDelete,
    ProductOutputPatch,
    ProductOutputPost
)
from src.api.crud_operations.product import ProductOperation
from src.utils.response_generation.main import get_text


router = APIRouter(
    prefix="/products",
    tags=["products"],
)


@router.get("/", **asdict(ProductOutputGetAll()))
async def get_all_products(product: ProductSwaggerGetAll = Depends()) -> list[ProductModel] | list[None]:
    """
    Returns all products from db by parameters.
    Only available to admins.
    """
    crud = ProductOperation(product.db)

    if product.name:
        product: ProductModel = await crud.find_by_param_or_404('name', product.name.lower())
        return [product]

    return await crud.find_all()


@router.get("/{product_id}", **asdict(ProductOutputGet()))
async def get_product(product: ProductSwaggerGet = Depends()) -> ProductModel | None:
    """
    Returns one product from db by product id.
    Only available to admins.
    """
    crud = ProductOperation(product.db)
    return await crud.find_by_id(product.product_id)


@router.delete("/{product_id}", **asdict(ProductOutputDelete()))
async def delete_product(product: ProductSwaggerDelete = Depends()) -> JSONResponse:
    """
    Deletes product from db by product id.
    Only available to admins.
    """
    crud = ProductOperation(product.db)
    await crud.delete_obj(product.product_id)

    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content={
            "message": get_text('delete').format(crud.model_name, product.product_id)
        }
    )


@router.patch("/{product_id}", **asdict(ProductOutputPatch()))
async def patch_product(product: ProductSwaggerPatch = Depends()) -> JSONResponse:
    """
    Updates product data.
    Only available to admins.
    """
    crud = ProductOperation(product.db)
    await crud.patch_obj(product.product_id, product.data)

    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content={
            "message": get_text('patch').format(crud.model_name, product.product_id)
        }
    )


@router.post("/create", **asdict(ProductOutputPost()))
async def add_product(product: ProductSwaggerPost = Depends()) -> JSONResponse:
    """
    Adds new product into db.
    Only available to admins.
    """
    crud = ProductOperation(product.db)
    await crud.add_obj(product.data)

    return JSONResponse(
        status_code=status.HTTP_201_CREATED,
        content={
            "message": get_text('post').format(crud.model_name)
        }
    )
