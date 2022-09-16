from pydantic import BaseModel

from src.utils.response_generation.main import get_text


class WarehouseGroupResponseDeleteSchema(BaseModel):
    message: str = get_text('delete').format('warehouse group', 1)


class WarehouseGroupResponsePatchSchema(BaseModel):
    message: str = get_text('patch').format('warehouse group', 1)


class WarehouseGroupResponsePostSchema(BaseModel):
    message: str = get_text('post').format('warehouse group', 1)
