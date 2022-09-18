from datetime import datetime as dt

from pydantic import BaseModel, Field


class CurrentStocksBaseSchema(BaseModel):
    product_id: int = Field(..., ge=1)
    product_name: str = Field(..., example='pants')
    warehouse_id: int = Field(..., ge=1)
    price: float = Field(..., example=5000.00)
    dt_price: dt = Field(..., example=dt.utcnow().strftime('%Y-%m-%dT%H:%M:%S'))
    count: int | None = Field(None, example=2500)
    dt_count: dt = Field(..., example=dt.utcnow().strftime('%Y-%m-%dT%H:%M:%S'))


class CurrentStocksGetSchema(CurrentStocksBaseSchema):

    class Config:
        orm_mode = True
