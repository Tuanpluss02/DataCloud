from typing import Annotated
from fastapi import APIRouter, Depends
from fastapi.responses import JSONResponse
from controllers.verify_request.cont_request import get_database_type
from middlewares.vaidate_user import get_current_user
from models.database_type import Database
from models.user import UserInDB
from services.container_service import ContainerService

router = APIRouter()

@router.post("")
def create_container(database_type: str, user : Annotated[UserInDB, Depends(get_current_user)]):
    database: Database = get_database_type(database_type)
    response =  ContainerService.create_container(user.username, database)
    return JSONResponse(
        status_code=200,
        content=response
        )

@router.delete("")
def delete_container(database_type: str,user : Annotated[UserInDB, Depends(get_current_user)]):
    database: Database = get_database_type(database_type)
    response =  ContainerService.delete_container(user.username, database)
    return JSONResponse(
        status_code=200,
        content=response
        )

@router.get("")
def list_containers(user : Annotated[UserInDB, Depends(get_current_user)]):
    response =  ContainerService.list_containers(user.username)
    return JSONResponse(
        status_code=200,
        content=response
        )
