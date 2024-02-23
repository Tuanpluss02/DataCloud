from typing import Annotated
from fastapi import APIRouter, Depends
from controllers.verify_request.pulumi_request import get_dgocean_cluster
from middlewares.vaidate_user import get_current_user
from models.database_type import Database
from models.dgapi_cluster import DigitalOceanCluster 
from models.user import UserInDB



router = APIRouter()

# @router.post("")
# def create_container(database_type: str, user : Annotated[UserInDB, Depends(get_current_user)]):
#     database: DigitalOceanCluster  = get_dgocean_cluster(database_type)
#     return PulumiService.create_cluster(user.username, database)