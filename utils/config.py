from functools import lru_cache
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    access_token_secret_key: str
    refresh_token_secret_key: str
    algorithm: str
    access_token_expire_minutes: int
    refresh_token_expire_minutes: int
    mongodb_uri: str
    mongodb_name: str
    fernet_key: str
    digitalocean_key: str
    digitalocean_ssh_key: str
    model_config = SettingsConfigDict(env_file=".env")


@lru_cache
def get_settings():
    return Settings()
