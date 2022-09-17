from pydantic import BaseModel

from src.utils.response_generation.main import get_text


class WarehouseResponseDeleteSchema(BaseModel):
    message: str = get_text('delete').format('warehouse', 1)


class WarehouseResponsePatchSchema(BaseModel):
    message: str = get_text('patch').format('warehouse', 1)


class WarehouseResponsePostSchema(BaseModel):
    message: str = get_text('post').format('warehouse', 1)
