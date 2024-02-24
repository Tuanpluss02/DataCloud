from pydantic import BaseModel

from models.database_type import DatabaseType


class User(BaseModel):
    username: str
    disabled: bool | None = False
    database_used: list[DatabaseType] | None = None


class UserInDB(User):
    hashed_password: str

    def to_dict(self):
        return self.model_dump()
