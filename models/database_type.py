from enum import Enum


class Database:
    image: str
    environment: dict
    ports: dict

    def __init__(self, image: str, environment: dict, ports: dict):
        self.image = image
        self.environment = environment
        self.ports = ports

    def __getitem__(self, key):
        return self.__dict__[key]

    def __setitem__(self, key, value):
        self.__dict__[key] = value

    def change_password(self, new_password):
        for key in self.environment.keys():
            if "PASSWORD" in key.upper():
                self.environment[key] = new_password
                break


class DatabaseType(Enum):
    MYSQL = Database(
        image="mysql:latest",
        environment={
            "MYSQL_ROOT_PASSWORD": "root",
        },
        ports={"3306/tcp": None},
    )
    POSTGRES = Database(
        image="postgres:latest",
        environment={
            "POSTGRES_PASSWORD": "root",
        },
        ports={"5432/tcp": None},
    )
    MONGODB = Database(
        image="mongo:latest",
        environment={
            "MONGO_INITDB_ROOT_USERNAME": "root",
            "MONGO_INITDB_ROOT_PASSWORD": "root",
        },
        ports={"27017/tcp": None},
    )
    REDIS = Database(image="redis:latest", environment={}, ports={"6379/tcp": None})
    KAFKA = Database(
        image="ubuntu/kafka:latest", environment={}, ports={"9092/tcp": None}
    )

    def __getitem__(self, key):
        return self.__dict__[key]
