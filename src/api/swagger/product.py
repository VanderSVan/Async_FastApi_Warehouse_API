from dataclasses import dataclass
from typing import Optional, Type, Any

from fastapi import Query, Path, Body, status

from src.api.schemas.product.base_schemas import (ProductGetSchema,
                                                  ProductPatchSchema,
                                                  ProductPostSchema)
from src.api.schemas.product.response_schemas import (ProductResponseDeleteSchema,
                                                      ProductResponsePatchSchema,
                                                      ProductResponsePostSchema)


@dataclass
class ProductSwaggerGetAll:
    name: str = Query(default=None, description='Product name')


@dataclass
class ProductSwaggerGet:
    product_id: int = Path(..., ge=1)


@dataclass
class ProductSwaggerDelete:
    product_id: int = Path(..., ge=1)


@dataclass
class ProductSwaggerPatch:
    product_id: int = Path(..., ge=1)
    data: ProductPatchSchema = Body(..., example={'name': 'T-shirt'})


@dataclass
class ProductSwaggerPost:
    data: ProductPostSchema = Body(..., example={'name': 'jacket'})
    

@dataclass
class ProductOutputGetAll:
    summary: Optional[str] = 'Get all products by parameters'
    description: Optional[str] = (
        "**Returns** all products from db by **parameters**.<br />"
        "Available to all **registered users**"
    )
    response_model: Optional[Type[Any]] = list[ProductGetSchema]
    status_code: Optional[int] = status.HTTP_200_OK
    response_description: str = 'List of products'
    
    
@dataclass
class ProductOutputGet:
    summary: Optional[str] = 'Get product by product id'
    description: Optional[str] = (
        "**Returns** product from db by **product id**.<br />"
        "Available to all **registered users**"
    )
    response_model: Optional[Type[Any]] = ProductGetSchema
    status_code: Optional[int] = status.HTTP_200_OK
    response_description: str = 'Product data'


@dataclass
class ProductOutputDelete:
    summary: Optional[str] = 'Delete product by product id'
    description: Optional[str] = (
        "**Deletes** product from db by **product id**. <br />"
        "Only available to **admins.**"
    )
    response_model: Optional[Type[Any]] = ProductResponseDeleteSchema
    status_code: Optional[int] = status.HTTP_200_OK
    
    
@dataclass
class ProductOutputPatch:
    summary: Optional[str] = 'Patch product by product id'
    description: Optional[str] = (
        "**Updates** product from db by **product id**. <br />"
        "Only available to **admins.**"
    )
    response_model: Optional[Type[Any]] = ProductResponsePatchSchema
    status_code: Optional[int] = status.HTTP_200_OK
    

@dataclass
class ProductOutputPost:
    summary: Optional[str] = 'Add new product'
    description: Optional[str] = (
        "**Adds** new product into db. <br />"
        "Only available to **admins.**"
    )
    response_model: Optional[Type[Any]] = ProductResponsePostSchema
    status_code: Optional[int] = status.HTTP_201_CREATED
