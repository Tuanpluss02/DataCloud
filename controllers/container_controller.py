from fastapi import APIRouter


from models.database_type import DatabaseType
from services.container_service import ContainerService

router = APIRouter()


@router.post("/create/{username}")
def create_container(username: str, database_type: str):
    return ContainerService.create_container(username, database_type)

@router.delete("/delete/{username}")
def delete_container(username: str, database_type: str):
    return ContainerService.delete_container(username, database_type)

@router.get("/list/{username}")
def list_containers(username: str):
    return ContainerService.list_containers(username)