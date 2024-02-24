import logging
from bson import ObjectId
from fastapi import HTTPException
from models.token import token_type
from models.user import UserInDB
from utils.database_config import get_mongo_db


class AuthRepository:
    db = get_mongo_db()

    def create_user(self, user: UserInDB):
        try:
            user_dict = user.to_dict()
            user_dict["_id"] = ObjectId()
            return self.db.users.insert_one(user_dict)
        except Exception as e:
            logging.error(e)
            raise HTTPException(
                status_code=400, detail=f"User {user.username} already exists"
            )

    def get_user_from_db(self, username) -> UserInDB | None:
        mongo_response = self.db.users.find_one({"username": username})
        if mongo_response is None:
            return None
        return UserInDB(**mongo_response)

    def revoke_token(self, token: str, token_type: token_type):
        try:
            return self.db.revoked_tokens.insert_one(
                {"token": token, "token_type": token_type.value}
            )
        except Exception as e:
            logging.error(e)
            raise HTTPException(status_code=400, detail="Error revoking token")
