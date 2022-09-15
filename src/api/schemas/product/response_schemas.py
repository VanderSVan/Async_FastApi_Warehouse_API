from pydantic import BaseModel

from src.utils.response_generation.main import get_text


class ProductResponseDeleteSchema(BaseModel):
    message: str = get_text('delete').format('product', 1)


class ProductResponsePatchSchema(BaseModel):
    message: str = get_text('patch').format('product', 1)


class ProductResponsePostSchema(BaseModel):
    message: str = get_text('post').format('product', 1)
