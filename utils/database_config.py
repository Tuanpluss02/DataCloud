from pymongo import MongoClient
from utils.config import get_settings

settings = get_settings()


def get_mongo_db():
    db = MongoClient(settings.mongodb_url)
    return db[settings.mongodb_name]


def get_mongo_user_collection():
    db = get_mongo_db()
    return db.users


def get_mongo_token_collection():
    db = get_mongo_db()
    return db.revoked_tokens
