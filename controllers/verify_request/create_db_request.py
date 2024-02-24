from enum import Enum
from http.client import BAD_REQUEST
from fastapi import HTTPException


def get_database_instance(database_type: str, database_list: Enum):
    if database_type is None:
        raise HTTPException(status_code=BAD_REQUEST, detail="Database type is required")
    database_type = database_type.upper()
    if database_type not in database_list.__members__:
        raise HTTPException(
            status_code=BAD_REQUEST,
            detail=f"Database type {database_type} not found, please choose from {list(database_list.__members__.keys())}",
        )
    return database_list[database_type].value
