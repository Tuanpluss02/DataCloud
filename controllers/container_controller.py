from typing import Annotated
from fastapi import APIRouter, Depends
from middlewares.vaidate_user import get_current_user
from models.user import UserInDB
from services.container_service import ContainerService

router = APIRouter()
container_service = ContainerService()

@router.post("")
def create_container(database_type: str, user : Annotated[UserInDB, Depends(get_current_user)]):
    return container_service.create_container(user.username, database_type)

@router.delete("")
def delete_container(database_type: str,user : Annotated[UserInDB, Depends(get_current_user)]):
    return container_service.delete_container(user.username, database_type)

@router.get("")
def list_containers(user : Annotated[UserInDB, Depends(get_current_user)]):
    return container_service.list_containers(user.username)