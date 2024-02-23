from typing import Annotated
from fastapi import APIRouter, Depends
from fastapi.responses import JSONResponse
from middlewares.vaidate_user import get_current_user
from models.database_type import Database
from models.user import UserInDB
from services.droplet_service import DropletService


router = APIRouter()

@router.post("")
def create_droplet(
    user : Annotated[UserInDB, Depends(get_current_user)],
    database_type:str
    ):
    response =  DropletService.create_droplet(user.username, database_type)
    return JSONResponse(
        status_code=201,
        content=response
    )