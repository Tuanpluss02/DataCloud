from enum import Enum
from pydantic import BaseModel


class token_type(Enum):
    ACCESS_TOKEN = "access_token"
    REFRESH_TOKEN = "refresh_token"


class token(BaseModel):
    token: str
    token_type: token_type

    def to_dict(self):
        return self.model_dump()
