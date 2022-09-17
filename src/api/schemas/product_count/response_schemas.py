from pydantic import BaseModel

from src.utils.response_generation.main import get_text


class ProductCountResponseDeleteSchema(BaseModel):
    message: str = get_text('delete').format('product_count object', 1)


class ProductCountResponsePatchSchema(BaseModel):
    message: str = get_text('patch').format('product_count object', 1)


class ProductCountResponsePostSchema(BaseModel):
    message: str = get_text('post').format('product_count object', 1)
