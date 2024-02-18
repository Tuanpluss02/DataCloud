from fastapi import APIRouter
from services.container_service import ContainerService

router = APIRouter()
container_service = ContainerService()

@router.post("/create/{username}")
def create_container(username: str, database_type: str):
    return container_service.create_container(username, database_type)

@router.delete("/delete/{username}")
def delete_container(username: str, database_type: str):
    return container_service.delete_container(username, database_type)

@router.get("/list/{username}")
def list_containers(username: str):
    return container_service.list_containers(username)