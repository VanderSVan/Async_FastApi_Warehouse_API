from dataclasses import dataclass
from typing import Optional, Type, Any

from fastapi import Query, Path, Body, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession

from src.api.schemas.product.base_schemas import (ProductGetSchema,
                                                  ProductPatchSchema,
                                                  ProductPostSchema)
from src.api.schemas.product.response_schemas import (ProductResponseDeleteSchema,
                                                      ProductResponsePatchSchema,
                                                      ProductResponsePostSchema)
from src.api.models.user import UserModel
from src.api.dependencies.db import get_db
from src.api.dependencies.auth import (get_current_admin,
                                       get_current_confirmed_user)


@dataclass
class ProductSwaggerGetAll:
    name: str = Query(default=None, description='Product name')
    offset: int = Query(default=None, description='How far to offset')
    limit: int = Query(default=None, description='How many limit')
    current_confirmed_user: UserModel = Depends(get_current_confirmed_user)
    db: AsyncSession = Depends(get_db)


@dataclass
class ProductSwaggerGet:
    product_id: int = Path(..., ge=1)
    current_confirmed_user: UserModel = Depends(get_current_confirmed_user)
    db: AsyncSession = Depends(get_db)


@dataclass
class ProductSwaggerDelete:
    product_id: int = Path(..., ge=1)
    admin: UserModel = Depends(get_current_admin)
    db: AsyncSession = Depends(get_db)


@dataclass
class ProductSwaggerPatch:
    product_id: int = Path(..., ge=1)
    data: ProductPatchSchema = Body(..., example={'name': 'T-shirt'})
    admin: UserModel = Depends(get_current_admin)
    db: AsyncSession = Depends(get_db)


@dataclass
class ProductSwaggerPost:
    data: ProductPostSchema = Body(..., example={'name': 'jacket'})
    admin: UserModel = Depends(get_current_admin)
    db: AsyncSession = Depends(get_db)
    

@dataclass
class ProductOutputGetAll:
    summary: Optional[str] = 'Get all products by parameters'
    description: Optional[str] = (
        "**Returns** all products from db by **parameters**.<br />"
        "Available to all **registered users.**"
    )
    response_model: Optional[Type[Any]] = list[ProductGetSchema]
    status_code: Optional[int] = status.HTTP_200_OK
    response_description: str = 'List of products'
    
    
@dataclass
class ProductOutputGet:
    summary: Optional[str] = 'Get product by product id'
    description: Optional[str] = (
        "**Returns** product from db by **product id**.<br />"
        "Available to all **registered users.**"
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
