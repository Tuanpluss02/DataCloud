import logging
from fastapi import FastAPI
import pymongo
from controllers.auth_controller import router as auth_router
from controllers.container_controller import router as cont_router
import uvicorn

from utils.database_config import get_mongo_db

def startup_event():
    db = get_mongo_db(); 
    if "users" not in db.list_collection_names():
        try:
            db.create_collection("users")
            users = db.users
            users.create_index(
                "username", username="username", unique=True)            
        except Exception as e:
            logging.error(e)


app = FastAPI(on_startup=[startup_event])
app.include_router(auth_router)
app.include_router(cont_router)


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)