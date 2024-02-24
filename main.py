import logging
from fastapi import FastAPI
from controllers import router as api_router
import uvicorn

from utils.database_config import MongoManager


def startup_event():
    MongoManager.initialize_collections()

def shutdown_event():
    MongoManager.close_mongo_connection()

app = FastAPI(on_startup=[startup_event], on_shutdown=[shutdown_event])
app.include_router(api_router)

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=80)
