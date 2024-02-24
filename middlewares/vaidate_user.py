from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer
from jose import JWTError
from models.user import UserInDB

from repositories.auth_repository import AuthRepository
from utils.token import decode_access_token

reusable_oauth2 = HTTPBearer(scheme_name="Authorization")
auth_repo = AuthRepository()


def get_current_user(
    http_authorization_credentials=Depends(reusable_oauth2),
) -> UserInDB:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = decode_access_token(http_authorization_credentials.credentials)
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
    except Exception:
        raise credentials_exception
    user: UserInDB = auth_repo.get_user_from_db(username=username)
    if user is None:
        raise credentials_exception
    return user


def get_token(http_authorization_credentials=Depends(reusable_oauth2)) -> str:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = decode_access_token(http_authorization_credentials.credentials)
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception
    user: UserInDB = auth_repo.get_user_from_db(username=username)
    if user is None:
        raise credentials_exception
    return http_authorization_credentials.credentials
