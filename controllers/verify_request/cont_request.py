from http.client import BAD_REQUEST

from fastapi import HTTPException
from models.database_type import Database, DatabaseType


def get_database_type(database_type: str) -> Database:
    if database_type is None:
        raise HTTPException(status_code=BAD_REQUEST, detail="Database type is required")
    database_type = database_type.upper()
    if database_type not in DatabaseType.__members__: 
        raise HTTPException(status_code=BAD_REQUEST, detail=f"Database type {database_type} not found, please choose from {list(DatabaseType.__members__.keys())}")
    return DatabaseType[database_type].value