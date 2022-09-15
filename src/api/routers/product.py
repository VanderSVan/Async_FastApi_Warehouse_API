from dataclasses import asdict

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from src.api.models.product import ProductModel
from src.api.dependencies.db import get_db
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


router = APIRouter(
    prefix="/products",
    tags=["products"],
)


@router.get("/", **asdict(ProductOutputGetAll()))
async def get_all_products(product: ProductSwaggerGetAll = Depends(),
                           db: Session = Depends(get_db)
                           ):
    crud = ProductOperation(db)

    if product.name:
        product: ProductModel = await crud.find_by_param_or_404('name', product.name.lower())
        return [product]

    return await crud.find_all()


@router.get("/{product_id}", **asdict(ProductOutputGet()))
async def get_product(product: ProductSwaggerGet = Depends(),
                      db: Session = Depends(get_db)
                      ):
    crud = ProductOperation(db)
    return await crud.find_by_id_or_404(product.product_id)


@router.delete("/{product_id}", **asdict(ProductOutputDelete()))
async def delete_product(product: ProductSwaggerDelete = Depends(),
                         db: Session = Depends(get_db)
                         ):
    crud = ProductOperation(db)
    return await crud.delete_obj(product.product_id)


@router.patch("/{product_id}", **asdict(ProductOutputPatch()))
async def patch_product(product: ProductSwaggerPatch = Depends(),
                        db: Session = Depends(get_db)
                        ):
    crud = ProductOperation(db)
    return await crud.patch_obj(product.product_id, product.data)


@router.post("/create/", **asdict(ProductOutputPost()))
async def add_product(product: ProductSwaggerPost = Depends(),
                      db: Session = Depends(get_db)
                      ):
    crud = ProductOperation(db)
    return await crud.add_obj(product.data)
