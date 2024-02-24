from http.client import BAD_REQUEST
import logging
from fastapi import HTTPException
from models.database_type import Database
import docker

from utils.config import get_settings
from utils.get_ip import get_ip_address
from utils.gen_pass import generate_password

client = docker.from_env()
settings = get_settings()


class ContainerService:
    def create_container(username: str, database: Database):
        database_type = database.image.split(":")[0].lower()
        container_name = f"{username}_{database_type}_container"
        if database_type == "ubuntu/kafka":
            container_name = f"{username}_kafka_container"
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
        return {
            "message": f"Container created for user: {username}",
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

    def get_container(username: str, container_id: str):
        try:
            container = client.containers.get(container_id)
            container.reload()
        except docker.errors.NotFound:
            raise HTTPException(
                status_code=BAD_REQUEST,
                detail=f"Container {container_id} not found for user: {username}",
            )
        except Exception as e:
            logging.error(e)
            raise HTTPException(
                status_code=BAD_REQUEST,
                detail=f"An error occured while trying to get container {container_id} for user: {username}",
            )
        return {
            "user": username,
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

    def delete_container(username: str, container_id: str):
        try:
            container = client.containers.get(container_id)
            container.stop()
            container.remove()
        except docker.errors.NotFound:
            raise HTTPException(
                status_code=BAD_REQUEST,
                detail=f"Container {container_id} not found for user: {username}",
            )
        return {"message": f"Container {container_id} deleted for user: {username}"}

    def list_containers(username: str):
        containers = client.containers.list(all=True, filters={"name": f"{username}_"})
        return {
            "user": username,
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

    def list_running_containers(username: str):
        containers = client.containers.list(filters={"name": f"{username}_"})
        return {
            "user": username,
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
