from pydantic import BaseModel, Field, constr


class ProductBaseSchema(BaseModel):
    name: str = Field(..., example='pants')


class ProductGetSchema(ProductBaseSchema):
    id: int

    class Config:
        orm_mode = True


class ProductDeleteSchema(ProductBaseSchema):
    pass


class ProductPatchSchema(ProductBaseSchema):
    name: constr(to_lower=True) | None = Field(None, example='T-shirt')


class ProductPostSchema(ProductBaseSchema):
    name: constr(to_lower=True) = Field(..., example='jacket')
