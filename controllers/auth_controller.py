import logging
from typing import Annotated
from fastapi import APIRouter, Depends
from fastapi.responses import JSONResponse
from fastapi.security import OAuth2PasswordRequestForm
from controllers.verify_request.auth_request import verify_auth_request
from middlewares.vaidate_user import get_current_user, get_token
from models.user import UserInDB

from services.auth_service import AuthServices
from utils.token import create_access_token, create_refresh_token

router = APIRouter()

@router.post("/login")
def user_login(form_data: Annotated[OAuth2PasswordRequestForm, Depends()]):
    verify_auth_request(form_data)
    user = AuthServices.authenticate_user(form_data.username, form_data.password)
    access_token = create_access_token(data={"sub": user.username})
    refresh_token = create_refresh_token(data={"sub": user.username})
    
    response_data = {
        "access_token": access_token,
        "refresh_token": refresh_token,
        "token_type": "bearer"
    }
    
    return JSONResponse(status_code=200, content=response_data)
    
@router.post("/register")
def user_register(form_data: Annotated[OAuth2PasswordRequestForm, Depends()]):
    verify_auth_request(form_data)
    user = AuthServices.register_user(form_data.username, form_data.password)
    access_token = create_access_token(data={"sub": user.username})
    refresh_token = create_refresh_token(data={"sub": user.username})
    return JSONResponse(
        status_code=200,
        content={"access_token": access_token, "refresh_token": refresh_token, "token_type": "bearer"}
        )
    
@router.post("/logout")
def user_logout(token : Annotated[str, Depends(get_token)]):
    AuthServices.logout_user(token)
    return JSONResponse(
        status_code=200,
        content={"message": "User logged out successfully"}
        )

@router.get("/refresh")
def refresh_token(user : Annotated[UserInDB, Depends(get_current_user)]):
    access_token = create_access_token(data={"sub": user.username})
    return JSONResponse(
        status_code=200,
        content={"access_token": access_token, "token_type": "bearer"}
        )