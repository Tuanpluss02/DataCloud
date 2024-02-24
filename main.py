import logging
from fastapi import FastAPI
from controllers import router as api_router
import uvicorn


from utils.database_config import get_mongo_db


def startup_event():
    db = get_mongo_db()
    if "users" not in db.list_collection_names():
        try:
            db.create_collection("users")
            users = db.users
            users.create_index("username", username="username", unique=True)
        except Exception as e:
            logging.error(e)
            raise Exception("Error creating collection")
    if "revoked_tokens" not in db.list_collection_names():
        try:
            db.create_collection("revoked_tokens")
            tokens = db.revoked_tokens
            tokens.create_index("token", name="token", unique=True)
        except Exception as e:
            logging.error(e)
            raise Exception("Error creating collection")


app = FastAPI(on_startup=[startup_event])
app.include_router(api_router)

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=80)
