from fastapi import FastAPI
from controllers.auth_controller import router as auth_router
from controllers.db_controller import router as db_router

app = FastAPI()

app.include_router(auth_router)
app.include_router(db_router)

if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)