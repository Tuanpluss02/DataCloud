from typing import Annotated
from fastapi import APIRouter, Depends
from fastapi.responses import JSONResponse
from middlewares.vaidate_user import get_current_user
from models.user import UserInDB
from services.droplet_service import DropletService


router = APIRouter()


@router.post("")
def create_droplet(
    user: Annotated[UserInDB, Depends(get_current_user)], database_type: str
):
    response = DropletService.create_droplet(user, database_type)
    return JSONResponse(status_code=201, content=response)


@router.get("/{droplet_id}")
def get_droplet(user: Annotated[UserInDB, Depends(get_current_user)], droplet_id: str):
    response = DropletService.get_droplet(user, droplet_id)
    return JSONResponse(status_code=200, content=response)


@router.delete("/{droplet_id}")
def delete_droplet(
    user: Annotated[UserInDB, Depends(get_current_user)], droplet_id: str
):
    response = DropletService.delete_droplet(user, droplet_id)
    return JSONResponse(status_code=200, content=response)
