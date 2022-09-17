from pydantic import BaseModel

from src.utils.response_generation.main import get_text


class PriceResponseDeleteSchema(BaseModel):
    message: str = get_text('delete').format('price', 1)


class PriceResponsePatchSchema(BaseModel):
    message: str = get_text('patch').format('price', 1)


class PriceResponsePostSchema(BaseModel):
    message: str = get_text('post').format('price', 1)
