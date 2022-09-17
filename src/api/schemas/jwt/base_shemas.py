from pydantic import BaseModel as BaseScheme


class TokenSchema(BaseScheme):
    username: str | None = None
