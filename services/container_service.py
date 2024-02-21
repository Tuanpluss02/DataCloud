from http.client import BAD_REQUEST
import logging
import socket
from fastapi import HTTPException
from models.database_type import Database, DatabaseType
import docker

from utils.config import get_settings
from utils.get_ip import get_ip_address
from utils.gen_pass import generate_password

client = docker.from_env()
settings = get_settings()

class ContainerService:
    def create_container(username: str, database: Database):
        database_type = database.image.split(':')[0].lower()            
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
            ports=database.ports
            )
            container.reload()
            host_port = container.attrs["NetworkSettings"]["Ports"][list(database.ports.keys())[0]][0]["HostPort"]
        except Exception as e:
            logging.error(e)
            raise HTTPException(status_code=BAD_REQUEST, detail=f"You already have a container for {database_type} database. Please delete it first.")
        return {
            "message": f"Container created for user: {username}", 
                "database_type": database_type,
                "host_ip": get_ip_address(),
                "host_port": host_port,
                "environment": database.environment,
            }
    
    def delete_container(username: str, database: Database):
        database_type = database.image.split(':')[0].lower()
        try: 
            container_name = f"{username}_{database.image.split(':')[0].lower()}_container"
            container = client.containers.get(container_name)
            container.stop()
            container.remove()
        except docker.errors.NotFound:
            raise HTTPException(status_code=BAD_REQUEST, detail=f"Database {database_type} not found for user: {username}")
        return {"message": f"Database {database_type} deleted for user: {username}"}
    
    def list_containers(username: str):
        containers = client.containers.list(all=True, filters={"name": f"{username}_"})
        return {"containers": [container.name for container in containers]}



