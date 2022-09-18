from datetime import datetime as dt

from pydantic import BaseModel, Field, condecimal


class PriceBaseSchema(BaseModel):
    price: condecimal(decimal_places=2) = Field(..., example=5000.00)
    datetime: dt = Field(..., example=dt.utcnow().strftime('%Y-%m-%dT%H:%M:%S'))
    product_id: int = Field(..., ge=1)
    warehouse_id: int = Field(..., ge=1)


class PriceGetSchema(PriceBaseSchema):
    id: int
    price: float = Field(..., example=5000.00)

    class Config:
        orm_mode = True


class PriceDeleteSchema(PriceBaseSchema):
    pass


class PricePatchSchema(PriceBaseSchema):
    price: condecimal(decimal_places=2) | None = Field(None, example=2500.50)
    datetime: dt | None = Field(None, example=dt.utcnow().strftime('%Y-%m-%dT%H:%M:%S'))
    product_id: int | None = Field(None, ge=1)
    warehouse_id: int | None = Field(None, ge=1)


class PricePostSchema(PriceBaseSchema):
    pass
