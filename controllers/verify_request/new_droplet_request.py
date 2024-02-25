
from fastapi import HTTPException


def validate_new_droplet_request(database_type: str):
        if database_type is None:
            raise HTTPException(status_code=400, detail="Database type is required")
        database_type = database_type.lower()
        if database_type not in ["mysql", "postgres", "mongo", "redis"]:
            raise HTTPException(
                status_code=400,
                detail=f"Database type {database_type} not found, please choose from MYSQL, POSTGRES, MONGO, REDIS",
            )
        return database_type