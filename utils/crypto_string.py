from cryptography.fernet import Fernet

from utils.config import get_settings

settings = get_settings()
fernet = Fernet(settings.fernet_key)


def encrypt_string(plain_string: str) -> str:
    return fernet.encrypt(plain_string.encode())


def decrypt_string(encrypt_string: str, key: str) -> str:
    return fernet.decrypt(encrypt_string).decode()
