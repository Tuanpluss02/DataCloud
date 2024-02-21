from enum import Enum

class DigitalOceanCluster :
    engine : str
    node_count : int | None = 1
    region: str | None = "sgp1"
    size: str | None = "db-s-1vcpu-1gb",
    version: str
    def __init__(self, engine: str, version: str, node_count: int | None = 1, region: str | None = "sgp1", size: str | None = "db-s-1vcpu-1gb"):
        self.engine = engine
        self.node_count = node_count
        self.region = region
        self.size = size
        self.version = version

class DigitalOceanClusterType(Enum):
    POSTGRES = DigitalOceanCluster (
    engine="pg",
    node_count=1,
    region="sgp1",
    size="db-s-1vcpu-1gb",
    version="15")
    
    MYSQL = DigitalOceanCluster (
    engine="mysql",
    node_count=1,
    region="sgp1",
    size="db-s-1vcpu-1gb",
    version="8")

    REDIS = DigitalOceanCluster (
    engine="redis",
    node_count=1,
    region="sgp1",
    size="db-s-1vcpu-1gb",
    version="7")

    KAFKA =  DigitalOceanCluster (
    engine="kafka",
    node_count=3,
    region="sgp1",
    size="db-s-1vcpu-1gb",
    version="3.5")


    MONGO = DigitalOceanCluster (
    engine="mongodb",
    node_count=1,
    region="nyc3",
    size="db-s-1vcpu-1gb",
    version="4")
