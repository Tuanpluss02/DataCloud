import re
from fastapi import HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from pydantic import BaseModel


def verify_auth_request(request: OAuth2PasswordRequestForm) -> BaseModel:
    username_pattern = r"^[a-zA-Z0-9]{4,20}$"
    if not re.match(username_pattern, request.username):
        raise HTTPException(
            status_code=400,
            detail="Username must be alphanumeric and between 4 and 20 characters",
        )
    if len(request.password) < 6:
        raise HTTPException(
            status_code=400, detail="Password must be at least 6 characters"
        )
