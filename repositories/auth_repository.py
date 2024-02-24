import logging
from bson import ObjectId
from fastapi import HTTPException
from models.token import token_type
from models.user import UserInDB
from utils.database_config import MongoManager



class AuthRepository:
    db_token = MongoManager.get_token_collection()

    def revoke_token(self, token: str, token_type: token_type):
        try:
            return self.db_token.insert_one(
                {"token": token, "token_type": token_type.value}
            )
        except Exception as e:
            logging.error(e)
            raise HTTPException(status_code=400, detail="Error revoking token")
    
    def is_token_revoked(self, token: str) -> bool:
        mongo_response = self.db_token.find_one({"token": token})
        return mongo_response is not None
