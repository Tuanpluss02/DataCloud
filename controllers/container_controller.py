from fastapi import APIRouter
import docker

from models.database_type import DatabaseType

router = APIRouter()
client = docker.from_env()

@router.post("/create/{username}")
def create_container(username: str, database_type: str):
    database_type = database_type.upper()
    if database_type not in DatabaseType.__members__: 
        return {"message": f"Database type {database_type} not found"}
    database = DatabaseType[database_type].value
    container_name = f"{username}_{database.image.split(':')[0].lower()}_container"
    try:
        container = client.containers.run(
        image=database.image,
        detach=True,
        environment=database.environment,
        name=container_name,
        ports=database.ports
        )
        container.reload()
        host_port = container.attrs["NetworkSettings"]["Ports"][list(database.ports.keys())[0]][0]["HostPort"]
    except  docker.errors.APIError:
        return {"message": f"You already have a container for {database_type} database. Please delete it first."}
    return {"message": f"Container created for user: {username}", "container_id": container.id, "host_port": host_port}


@router.delete("/delete/{username}")
def delete_container(username: str, database_type: str):
    database_type = database_type.upper()
    if database_type not in DatabaseType.__members__: 
        return {"message": f"Database type {database_type} not found"}
    database = DatabaseType[database_type].value
    try: 
        container_name = f"{username}_{database.image.split(':')[0].lower()}_container"
        container = client.containers.get(container_name)
        container.stop()
        container.remove()
        return {"message": f"Container deleted for user: {username}"}
    except docker.errors.NotFound:
        return {"message": f"Container not found for user: {username}"}

@router.get("/list/{username}")
def list_containers(username: str):
    containers = client.containers.list(all=True, filters={"name": f"{username}_"})
    return {"containers": [container.name for container in containers]}