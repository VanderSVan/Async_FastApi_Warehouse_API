from pydantic import BaseModel as BaseScheme


class TokenResponseSchema(BaseScheme):
    access_token: str
    token_type: str
