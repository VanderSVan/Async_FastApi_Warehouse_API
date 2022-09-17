from pydantic import BaseModel, Field, constr


class WarehouseBaseSchema(BaseModel):
    name: str = Field(..., example='number-1')
    warehouse_group_id: int = Field(..., ge=1)


class WarehouseGetSchema(WarehouseBaseSchema):
    id: int

    class Config:
        orm_mode = True


class WarehouseDeleteSchema(WarehouseBaseSchema):
    pass


class WarehousePatchSchema(WarehouseBaseSchema):
    name: constr(to_lower=True) | None = Field(None, example='number-2')
    warehouse_group_id: int | None = Field(None, ge=1)


class WarehousePostSchema(WarehouseBaseSchema):
    name: constr(to_lower=True) = Field(..., example='number-3')
    warehouse_group_id: int = Field(..., ge=1)
