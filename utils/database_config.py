import logging
from fastapi import HTTPException
from pymongo import MongoClient
import pymongo
from .config import get_settings

class MongoManager:
    client: MongoClient = None
    settings = get_settings()

    @classmethod
    def get_client(cls):
        if cls.client is None:
            cls.client = MongoClient(cls.settings.mongodb_uri)
        return cls.client

    @classmethod
    def get_database(cls):
        return cls.get_client()[cls.settings.mongodb_name]

    @classmethod
    def get_user_collection(cls):
        db = cls.get_database()
        return db.users

    @classmethod
    def get_token_collection(cls):
        db = cls.get_database()
        return db.revoked_tokens
    
    @classmethod
    def initialize_collections(cls):
        db = cls.get_database()
        logging.warn(db.list_collection_names())
        cls.initialize_collection(db, "users", "username")
        cls.initialize_collection(db, "revoked_tokens", "token")

    @classmethod
    def initialize_collection(cls, database, collection_name, index_field):
        collection_list = database.list_collection_names()
        if collection_name not in collection_list:
            try:
                database.create_collection(collection_name)
                collection = database[collection_name]
                collection.create_index([(index_field, 1)], unique=True)
            except pymongo.errors.PyMongoError as e:
                logging.error(f"Error initializing collection {collection_name}: {str(e)}")
                raise HTTPException(status_code=500, detail=str(e))
    
    @classmethod
    def close_mongo_connection(cls):
        if cls.client:
            cls.client.close()
            cls.client = None

