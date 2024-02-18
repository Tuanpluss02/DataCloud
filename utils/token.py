
from datetime import datetime, timedelta, timezone
from utils.config import get_settings
from jose import JWTError, jwt


settings = get_settings()

def create_access_token(data: dict):
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + timedelta(minutes=settings.access_token_expire_minutes)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, settings.access_token_secret_key, algorithm=settings.algorithm)
    return encoded_jwt


def create_refresh_token(data: dict):
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + timedelta(minutes=settings.refresh_token_expire_minutes)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, settings.refresh_token_secret_key, algorithm=settings.algorithm)
    return encoded_jwt

def decode_access_token(token: str):
    try:
        payload = jwt.decode(token, settings.access_token_secret_key, algorithms=[settings.algorithm])
        return payload
    except JWTError:
        return None
    
def decode_refresh_token(token: str):
    try:
        payload = jwt.decode(token, settings.refresh_token_secret_key, algorithms=[settings.algorithm])
        return payload
    except JWTError:
        return None
    