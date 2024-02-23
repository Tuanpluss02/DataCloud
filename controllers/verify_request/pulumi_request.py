
from http.client import BAD_REQUEST
from fastapi import HTTPException

from models.dgapi_cluster import DigitalOceanCluster , DigitalOceanClusterType


def get_dgocean_cluster(database_type: str)-> DigitalOceanCluster :
    if database_type is None:
        raise HTTPException(status_code=BAD_REQUEST, detail="Database type is required")
    database_type = database_type.upper()
    if database_type not in DigitalOceanClusterType.__members__: 
        raise HTTPException(status_code=BAD_REQUEST, detail=f"Database type {database_type} not found, please choose from {list(DigitalOceanClusterType.__members__.keys())}")
    return DigitalOceanClusterType[database_type].value