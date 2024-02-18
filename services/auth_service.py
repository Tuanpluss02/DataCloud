import crypt
from datetime import datetime, timedelta, timezone
from typing import Annotated

from fastapi import Depends, FastAPI, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jose import JWTError, jwt
from passlib.context import CryptContext
from pydantic import BaseModel
from models.user import UserInDB
from repositories.auth_repository import AuthRepository

from utils.config import get_settings
from utils.password_ecrypt import get_password_hash, verify_password



auth_repo = AuthRepository()

class AuthServices:    
    def authenticate_user(username: str, password: str):
        user = auth_repo.get_user_from_db(username=username)
        if not verify_password(password, user.hashed_password):
            raise HTTPException(status_code=401, detail="Incorrect username or password")
        return user
    
    def register_user(username: str, password: str):
        is_existing_user = auth_repo.get_user_from_db(username)
        if is_existing_user:
            raise HTTPException(status_code=400, detail=f"User {username} already exists")
        hashed_password = get_password_hash(password)
        user = {}
        user["username"] = username
        user["hashed_password"] = hashed_password
        user["database_used"] = []
        dbuser = UserInDB(**user)
        auth_repo.create_user(dbuser)
        return dbuser
        
        
        
        
    
    

