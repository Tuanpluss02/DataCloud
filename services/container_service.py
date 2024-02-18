from http.client import BAD_REQUEST
from fastapi import HTTPException
from models.database_type import Database, DatabaseType
import docker

client = docker.from_env()

class ContainerService:
    def create_container(username: str, database_type: str):
        database = get_database_type(database_type)
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
            raise HTTPException(status_code=BAD_REQUEST, detail=f"You already have a container for {database_type} database. Please delete it first.")
        return {"message": f"Container created for user: {username}", 
                "container_id": container.id,
                "host_port": host_port}
    
    def delete_container(username: str, database_type: str):
        database = get_database_type(database_type)
        try: 
            container_name = f"{username}_{database.image.split(':')[0].lower()}_container"
            container = client.containers.get(container_name)
            container.stop()
            container.remove()
        except docker.errors.NotFound:
            raise HTTPException(status_code=BAD_REQUEST, detail=f"Database {database_type} not found for user: {username}")
        return {"message": f"Container deleted for user: {username}"}
    
    def list_containers(username: str):
        containers = client.containers.list(all=True, filters={"name": f"{username}_"})
        return {"containers": [container.name for container in containers]}



def get_database_type(database_type: str)-> Database:
    database_type = database_type.upper()
    if database_type not in DatabaseType.__members__: 
        raise HTTPException(status_code=BAD_REQUEST, detail=f"Database type {database_type} not found, please choose from {list(DatabaseType.__members__.keys())}")
    return DatabaseType[database_type].value