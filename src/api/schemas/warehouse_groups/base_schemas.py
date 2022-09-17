from pydantic import BaseModel, Field, constr


class WarehouseGroupBaseSchema(BaseModel):
    name: str = Field(..., example='ozon')


class WarehouseGroupGetSchema(WarehouseGroupBaseSchema):
    id: int

    class Config:
        orm_mode = True


class WarehouseGroupDeleteSchema(WarehouseGroupBaseSchema):
    pass


class WarehouseGroupPatchSchema(WarehouseGroupBaseSchema):
    name: constr(to_lower=True) | None = Field(None, example='wildberries')


class WarehouseGroupPostSchema(WarehouseGroupBaseSchema):
    name: constr(to_lower=True) = Field(..., example='yandex-market')
