from datetime import datetime as dt

from pydantic import BaseModel, Field


class ProductCountBaseSchema(BaseModel):
    count: int = Field(..., example=500)
    datetime: dt = Field(..., example=dt.utcnow().strftime('%Y-%m-%dT%H:%M:%S'))
    product_id: int = Field(..., ge=1)
    warehouse_group_id: int = Field(..., ge=1)


class ProductCountGetSchema(ProductCountBaseSchema):
    id: int

    class Config:
        orm_mode = True


class ProductCountDeleteSchema(ProductCountBaseSchema):
    pass


class ProductCountPatchSchema(ProductCountBaseSchema):
    count: int | None = Field(None, example=2500)
    datetime: dt | None = Field(None, example=dt.utcnow().strftime('%Y-%m-%dT%H:%M:%S'))
    product_id: int | None = Field(None, ge=1)
    warehouse_group_id: int | None = Field(None, ge=1)


class ProductCountPostSchema(ProductCountBaseSchema):
    pass
