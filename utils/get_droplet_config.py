
import time
from fastapi import HTTPException
from utils.gen_pass import generate_password


def get_user_data(username: str, database_type: str, default_password: str):
    user_data_map = {
        "mysql": f"""
        - export DEBIAN_FRONTEND=noninteractive
        - echo "mysql-server mysql-server/root_password password {default_password}" | debconf-set-selections
        - echo "mysql-server mysql-server/root_password_again password {default_password}" | debconf-set-selections
        - apt-get update
        - apt-get install -y mysql-server
        - systemctl start mysql
        - systemctl enable mysql
        - mysql -uroot -p{default_password} -e "CREATE USER '{username}'@'%' IDENTIFIED BY 'actual_password';"
        - mysql -uroot -p{default_password} -e "GRANT ALL PRIVILEGES ON *.* TO '{username}'@'%' WITH GRANT OPTION;"
        - mysql -uroot -p{default_password} -e "FLUSH PRIVILEGES;"
        """,
        "postgres": f"""
        - apt-get update
        - apt-get install -y postgresql postgresql-contrib
        - systemctl start postgresql
        - systemctl enable postgresql
        - sudo -u postgres psql -c "CREATE USER {username} WITH PASSWORD '{default_password}';"
        - sudo -u postgres psql -c "ALTER USER {username} CREATEDB;"
        """,
        "mongo": f"""
        - apt-get update
        - apt-get install -y mongodb
        - systemctl start mongodb
        - systemctl enable mongodb
        - mongo --eval 'db.createUser({{user:"{username}",pwd:"{default_password}",roles:[{{role:"readWrite",db:"{username}_mongo"}}]}});'
        """,
        "redis": f"""
        - apt-get update
        - apt-get install -y redis-server
        - systemctl start redis-server
        - systemctl enable redis-server
        """,
        "kafka": """
        - echo "deb [arch=amd64] http://repo.confluent.io/deb/5.5 stable main" | tee /etc/apt/sources.list.d/confluent.list
        - wget -qO - http://packages.confluent.io/deb/5.5/archive.key | apt-key add -
        - apt-get update && apt-get install -y confluent-community-2.12
        """
    }
    return user_data_map.get(database_type)

def get_payload_request(username :str, database_type:str, default_password:str):
    user_data =  get_user_data(username=username, database_type=database_type, default_password=default_password)
    return {
        "name": f"{username}-{database_type}-droplet",
        "region": "sgp1",
        "size": "s-1vcpu-1gb",
        "image": "ubuntu-20-04-x64",
        "backups": False,
        "ipv6": True,
        "user_data": f"""#cloud-config
runcmd:
{user_data}
""",
        "private_networking": None,
        "volumes": None,
        "tags": ["web"]
    }

def generate_droplet_response(username: str, database_type: str, default_password: str, ip_address: str, droplet_id: str):
    database_port_map = {
        "mysql": 3306,
        "postgres": 5432,
        "mongo": 27017,
        "redis": 6379,
        "kafka": 9092
    }
    return {
        "status": "success",
        "detail": {
            "droplet_id": droplet_id,
            "username": username,
            "default_password": default_password if database_type in ["mysql", "postgres", "mongo"] else None,
            "database_type": database_type,
            "ip_address": ip_address,
            "port": database_port_map.get(database_type)
        }
    }