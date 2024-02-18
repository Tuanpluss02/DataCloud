import logging
from typing import Annotated
from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordRequestForm
from middlewares.vaidate_user import get_current_user
from models.user import UserInDB

from services.auth_service import AuthServices
from utils.token import create_access_token, create_refresh_token

router = APIRouter()

@router.post("/login")
def user_login(form_data: Annotated[OAuth2PasswordRequestForm, Depends()]):
    user = AuthServices.authenticate_user(form_data.username, form_data.password)
    access_token = create_access_token(data={"sub": user.username})
    refresh_token = create_refresh_token(data={"sub": user.username})
    return {"access_token": access_token, "refresh_token": refresh_token, "token_type": "bearer"}
    
    
@router.post("/register")
def user_register(form_data: Annotated[OAuth2PasswordRequestForm, Depends()]):
    user = AuthServices.register_user(form_data.username, form_data.password)
    access_token = create_access_token(data={"sub": user.username})
    refresh_token = create_refresh_token(data={"sub": user.username})
    return {"access_token": access_token, "refresh_token": refresh_token, "token_type": "bearer"} 
    
@router.post("/logout")
def user_logout(user : Annotated[UserInDB, Depends(get_current_user)]):
    AuthServices.logout_user(user)
    return {"message": "User Logged out successfully"}

@router.get("/refresh")
def refresh_token(user : Annotated[UserInDB, Depends(get_current_user)]):
    access_token = create_access_token(data={"sub": user.username})
    return {"access_token": access_token, "token_type": "bearer"}