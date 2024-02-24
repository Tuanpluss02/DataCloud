from http.client import BAD_REQUEST
import logging
from fastapi import HTTPException
from models.database_type import Database
import docker
from models.user import UserInDB

from utils.config import get_settings
from utils.get_ip import get_ip_address
from utils.gen_pass import generate_password

client = docker.from_env()
settings = get_settings()


class ContainerService:
    def create_container(user: UserInDB, database: Database):
        database_type = database.image.split(":")[0].lower()
        container_name = f"{user.username}_{database_type}_container"
        if database_type == "ubuntu/kafka":
            container_name = f"{user.username}_kafka_container"
        database.change_password(generate_password())
        try:
            container = client.containers.run(
                image=database.image,
                detach=True,
                environment=database.environment,
                name=container_name,
                ports=database.ports,
            )
            container.reload()
            host_port = container.attrs["NetworkSettings"]["Ports"][
                list(database.ports.keys())[0]
            ][0]["HostPort"]
        except Exception as e:
            logging.error(e)
            raise HTTPException(
                status_code=BAD_REQUEST,
                detail=f"You already have a container for {database_type} database. Please delete it first.",
            )
        user.containers.append(container.short_id)
        user.save()
        return {
            "message": f"Container created for user: {user.username}",
            "container": {
                "id": container.short_id,
                "name": container.name,
                "image": container.image.tags[0],
                "status": container.status,
                "host": get_ip_address(),
                "port": host_port,
                "enviroment": database.environment,
            },
        }

    def get_container(user: UserInDB, container_id: str):
        if container_id not in user.containers:
            raise HTTPException(
                status_code=BAD_REQUEST,
                detail=f"Container {container_id} not found for user: {user.username}",
            )
        try:
            container = client.containers.get(container_id)
            container.reload()
        except docker.errors.NotFound:
            raise HTTPException(
                status_code=BAD_REQUEST,
                detail=f"Container {container_id} not found for user: {user.username}",
            )
        except Exception as e:
            logging.error(e)
            raise HTTPException(
                status_code=BAD_REQUEST,
                detail=f"An error occured while trying to get container {container_id} for user: {user.username}",
            )
        return {
            "user": user.username,
            "container": {
                "id": container.short_id,
                "name": container.name,
                "image": container.image.tags[0],
                "status": container.status,
                "host": get_ip_address(),
                "port": (
                    container.attrs["NetworkSettings"]["Ports"][
                        list(container.ports.keys())[0]
                    ][0]["HostPort"]
                    if container.status == "running"
                    else None
                ),
                "enviroment": container.attrs["Config"]["Env"],
            },
        }

    def delete_container(user: UserInDB, container_id: str):
        if container_id not in user.containers:
            raise HTTPException(
                status_code=BAD_REQUEST,
                detail=f"Container {container_id} not found for user: {user.username}",
            )
        try:
            container = client.containers.get(container_id)
            container.stop()
            container.remove()
            user.containers.remove(container_id)
            user.save()
        except docker.errors.NotFound:
            raise HTTPException(
                status_code=BAD_REQUEST,
                detail=f"Container {container_id} not found for user: {user.username}",
            )
        return {"message": f"Container {container_id} deleted for user: {user.username}"}

    def list_containers(user: UserInDB):
        containers = client.containers.list(all=True, filters={"name": f"{user.username}_"})
        return {
            "user": user.username,
            "contaniner_count": len(containers),
            "containers": [
                {
                    "id": container.short_id,
                    "name": container.name,
                    "image": container.image.tags[0],
                    "status": container.status,
                }
                for container in containers
            ],
        }


