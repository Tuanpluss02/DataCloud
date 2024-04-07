from re import I
from typing import Annotated
from fastapi import APIRouter, Depends, Request
from fastapi.responses import JSONResponse
from controllers.verify_request.new_droplet_request import validate_new_droplet_request
from middlewares.vaidate_user import get_current_user
from models.user import UserInDB
from services.droplet_service import DropletService
from utils.custom_response import IResponse


router = APIRouter()


@router.post("")
def create_droplet(
      request: Request,
    user: Annotated[UserInDB, Depends(get_current_user)], database_type: str
):
    database_type = validate_new_droplet_request(database_type)
    response = DropletService.create_droplet(user, database_type)
    return IResponse.init(
        path=request.url.path,
        status_code=200,
        message="Droplet created successfully",
        data=response,
    )

@router.get("")
def get_all_droplets(  request: Request,user: Annotated[UserInDB, Depends(get_current_user)]):
    response = DropletService.get_all_droplets(user)
    return IResponse.init(
        path=request.url.path,
        status_code=200,
        message="Droplets fetched successfully",
        data=response,
    )

@router.get("/{droplet_id}")
def get_droplet(  request: Request,user: Annotated[UserInDB, Depends(get_current_user)], droplet_id: str):
    response = DropletService.get_droplet(user, droplet_id)
    return IResponse.init(
        path=request.url.path,
        status_code=200,
        message="Droplet fetched successfully",
        data=response,
    )


@router.delete("/{droplet_id}")
def delete_droplet(  request: Request,
    user: Annotated[UserInDB, Depends(get_current_user)], droplet_id: str
):
    response = DropletService.delete_droplet(user, droplet_id)
    return IResponse.init(
        path=request.url.path,
        status_code=200,
        message="Droplet deleted successfully",
        data=response,
    )
