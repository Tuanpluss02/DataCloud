from typing import Annotated
from fastapi import APIRouter, Body, Depends
from fastapi.responses import JSONResponse
from controllers.verify_request.create_db_request import get_database_instance
from middlewares.vaidate_user import get_current_user
from models.database_type import Database, DatabaseType
from models.user import UserInDB
from services.container_service import ContainerService

router = APIRouter()


@router.post("")
def create_container(
    database_type: str, user: Annotated[UserInDB, Depends(get_current_user)]
):
    database: Database = get_database_instance(
        database_type=database_type, database_list=DatabaseType
    )
    response = ContainerService.create_container(user, database)
    return JSONResponse(status_code=201, content=response)


@router.delete("{container_id}")
def delete_container(
    container_id: str, user: Annotated[UserInDB, Depends(get_current_user)]
):
    response = ContainerService.delete_container(user, container_id)
    return JSONResponse(status_code=200, content=response)


@router.get("{container_id}")
def get_container(
    container_id: str, user: Annotated[UserInDB, Depends(get_current_user)]
):
    response = ContainerService.get_container(user, container_id)
    return JSONResponse(status_code=200, content=response)


@router.get("")
def list_containers(user: Annotated[UserInDB, Depends(get_current_user)]):
    response = ContainerService.list_containers(user)
    return JSONResponse(status_code=200, content=response)
