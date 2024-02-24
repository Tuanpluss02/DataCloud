
from bson import ObjectId
from fastapi import HTTPException
import pymongo
from models.user import UserInDB
from utils.database_config import MongoManager


class UserRepository:
    db_user = MongoManager.get_user_collection()
    
    def create_user(self, user: UserInDB):
        try:
            user_dict = user.to_dict()
            user_dict["_id"] = ObjectId()
            return self.db_user.insert_one(user_dict)
        except pymongo.errors.DuplicateKeyError as e:
            raise HTTPException(
                status_code=400, detail=f"User {user.username} already exists"
            )
        except Exception as e:
            raise HTTPException(status_code=500, detail="Error creating user")
    
    def add_new_container_to_user(self, user: UserInDB, container_id: str):
        try:
            user.containers.append(container_id)
            self.db_user.update_one({"username": user.username}, {"$set": user.to_dict()})
        except Exception as e:
            raise HTTPException(status_code=400, detail="Error adding container to user")
    
    def add_new_droplet_to_user(self, user: UserInDB, droplet_id: str):
        try:
            user.droplets.append(droplet_id)
            self.db_user.update_one({"username": user.username}, {"$set": user.to_dict()})
        except Exception as e:
            raise HTTPException(status_code=400, detail="Error adding droplet to user")
        
    def get_user_by_username(self, username: str) -> UserInDB | None:
        try:
            user = self.db_user.find_one({"username": username})
            return UserInDB(**user) if user else None
        except Exception as e:
            raise HTTPException(status_code=400, detail="Error getting user from database")