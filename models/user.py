from typing import Optional
from pydantic import BaseModel


class User(BaseModel):
    username: str
    hashed_password: str
    salt: str
    disabled: bool = False
    
    def __getitem__(self, key):
        return self.__dict__[key]

