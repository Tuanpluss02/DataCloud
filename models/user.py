from pydantic import BaseModel



class User(BaseModel):
    username: str
    disabled: bool | None = False
    containers: list[str] | None = []
    droplets: list[str] | None = []


class UserInDB(User):
    hashed_password: str

    def to_dict(self):
        return self.model_dump()
