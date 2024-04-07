from typing import Annotated
from fastapi import APIRouter, Body, Depends, Request
from fastapi.responses import JSONResponse
from controllers.verify_request.create_db_request import get_database_instance
from middlewares.vaidate_user import get_current_user
from models.database_type import Database, DatabaseType
from models.user import UserInDB
from services.container_service import ContainerService
from utils.custom_response import IResponse

router = APIRouter()


@router.post("")
def create_container(
    request: Request,
    database_type: str, user: Annotated[UserInDB, Depends(get_current_user)]
):
    database: Database = get_database_instance(
        database_type=database_type, database_list=DatabaseType
    )
    response = ContainerService.create_container(user, database)
    return IResponse.init(
        path=request.url.path,
        status_code=200,
        message="Container created successfully",
        data=response,
    )


@router.delete("/{container_id}")
def delete_container(  request: Request,
    container_id: str, user: Annotated[UserInDB, Depends(get_current_user)]
):
    response = ContainerService.delete_container(user, container_id)
    return IResponse.init(
        path=request.url.path,
        status_code=200,
        message="Container deleted successfully",
        data=response,
    )


@router.get("/{container_id}")
def get_container(  request: Request,
    container_id: str, user: Annotated[UserInDB, Depends(get_current_user)]
):
    response = ContainerService.get_container(user, container_id)
    return IResponse.init(
        path=request.url.path,
        status_code=200,
        message="Container fetched successfully",
        data=response,
    )


@router.get("")
def list_containers(  request: Request,user: Annotated[UserInDB, Depends(get_current_user)]):
    response = ContainerService.list_containers(user)
    return IResponse.init(
        path=request.url.path,
        status_code=200,
        message="Containers fetched successfully",
        data=response,
    )
