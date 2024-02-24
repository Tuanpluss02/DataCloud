
import json
import time
from fastapi import HTTPException
from utils.config import Settings
from utils.gen_pass import generate_password

settings = Settings()

def get_payload_request(username :str, database_type:str):
    db_engine_map = {
        'mysql': 'mysql',
        'postgres': 'pg',
        'mongo': 'mongodb',
        'redis': 'redis',
    }
    db_version_map = {
        "mysql": "8",
        "postgres": "16",
        "mongo": "6",
        "redis": "7",
    }
    return {
    "name": f"{username}-{database_type}-database",
    "engine": db_engine_map.get(database_type),
    "version": db_version_map.get(database_type),
    "region": "sgp1",
    "size": "db-s-1vcpu-1gb",
    "num_nodes": 1,
    "tags": [
        "production"
    ]
}

def extract_database_info(response_json):
    important_details = {
        "database": {
            "id": response_json["database"]["id"],
            "name": response_json["database"]["name"],
            "engine": response_json["database"]["engine"],
            "version": response_json["database"]["version"],
            "status": response_json["database"]["status"],
            "connection": {
                "protocol": response_json["database"]["connection"]["protocol"],
                "uri": response_json["database"]["connection"]["uri"],
                "host": response_json["database"]["connection"]["host"],
                "port": response_json["database"]["connection"]["port"],
                "user": response_json["database"]["connection"]["user"],
                "password": response_json["database"]["connection"]["password"],
                "ssl": response_json["database"]["connection"]["ssl"]
            }
        }
    }
    return important_details