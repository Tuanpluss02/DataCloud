import time
from fastapi import HTTPException
import requests
from utils.config import get_settings
from utils.gen_pass import generate_password

from utils.get_droplet_config import generate_droplet_response, get_payload_request

settings = get_settings()
headers = {"Authorization": f"Bearer {settings.digitalocean_key}"}
DIGITALOCEAN_API_URL = "https://api.digitalocean.com/v2/droplets"

class DropletService:
    def create_droplet(username: str, database_type: str):
        if database_type is None:
            raise HTTPException(status_code=400, detail="Database type is required")
        database_type = database_type.lower()
        if database_type not in ["mysql", "postgres", "mongo", "redis", "kafka"]:
            raise HTTPException(status_code=400, detail=f"Database type {database_type} not found, please choose from MYSQL, POSTGRES, MONGO, REDIS, KAFKA")
        try:
            default_password = generate_password()
            payload = get_payload_request(username=username,database_type=database_type, default_password= default_password)
            
            response = requests.post(
                DIGITALOCEAN_API_URL,
                headers=headers,
                json=payload
            )
            if response.status_code == 202:
                response_parsed = response.json()
                droplet_id = response_parsed['droplet']['id']
                droplet_ip = DropletService.get_droplet_public_ip(droplet_id)
                return generate_droplet_response(username, database_type, default_password,ip_address=droplet_ip, droplet_id=droplet_id)
            else:
                return {"status": "error", "detail": response.json()}
        except Exception as e:
            raise HTTPException(status_code=400, detail=str(e))
    
    def get_droplet_public_ip(droplet_id: str):
        try:
            retry_count = 0
            droplet_ready = False
            ipv4_info = None
            while not droplet_ready and retry_count < 5:
                droplet_response = requests.get(
                    f"{DIGITALOCEAN_API_URL}/{droplet_id}",
                    headers=headers,
                )
                if droplet_response.status_code == 200:
                    droplet_data = droplet_response.json()
                    if droplet_data['droplet']['status'] == 'active':
                        droplet_ready = True
                        networks = droplet_data['droplet']['networks']['v4']
                        ipv4_info = next((item for item in networks if item["type"] == "public"), None)
                        if ipv4_info:
                            ip_address = ipv4_info['ip_address']
                            return ip_address
                elif droplet_response.status_code == 404:
                    raise HTTPException(status_code=400, detail="An error occured while trying to get droplet.")
                retry_count += 1
                time.sleep(30)
            if not ipv4_info:
                raise HTTPException(status_code=400, detail="An error occured while trying to get droplet.")
        except Exception as e:
            raise HTTPException(status_code=400, detail=str(e))
        

       


    