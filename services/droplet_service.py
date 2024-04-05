from fastapi import HTTPException
import requests
from models.user import UserInDB
from repositories.user_repository import UserRepository
from utils.config import get_settings

from utils.get_droplet_config import extract_database_info, get_payload_request

settings = get_settings()
headers = {"Authorization": f"Bearer {settings.digitalocean_key}"}
DIGITALOCEAN_API_URL = "https://api.digitalocean.com/v2/databases"
user_repo = UserRepository()

class DropletService:
    def create_droplet(user: UserInDB, database_type: str):
        if len(user.droplets) >= 2:
            raise HTTPException(
                status_code=400,
                detail="You have reached the maximum number of databases"
            )
        try:
            payload = get_payload_request(
                username=user.username, database_type=database_type
            )
            response = requests.post(
                DIGITALOCEAN_API_URL, headers=headers, json=payload
            )
            if response.status_code == 201:
                db_info =  extract_database_info(response.json())
                user.droplets.append(db_info["database"]["id"])
                user_repo.update_user(user)
                return db_info
            else:
                raise HTTPException(
                    status_code=response.status_code, detail=response.json()
                )
        except Exception as e:
            raise HTTPException(status_code=response.status_code, detail=e.__dict__)

    def get_all_droplets(user: UserInDB):
        if len(user.droplets) == 0:
            return {"message": "No databases found"}
        try:
            response = []
            for droplet_id in user.droplets:
                response.append(
                    extract_database_info(
                        requests.get(f"{DIGITALOCEAN_API_URL}/{droplet_id}", headers=headers).json()
                    )
                )
        except Exception as e:
            raise HTTPException(status_code=response.status_code, detail=e.__dict__)

    def get_droplet( user: UserInDB,droplet_id: str):
        if droplet_id not in user.droplets:
            raise HTTPException(
                status_code=404, detail=f"Droplet with id {droplet_id} not found"
            )
        try:
            response = requests.get(
                f"{DIGITALOCEAN_API_URL}/{droplet_id}", headers=headers
            )
            if response.status_code == 200:
                return extract_database_info(response.json())
            else:
                raise HTTPException(
                    status_code=response.status_code, detail=response.json()
                )
        except Exception as e:
            raise HTTPException(status_code=response.status_code, detail=e.__dict__)

    def delete_droplet(user: UserInDB, droplet_id: str):
        if droplet_id not in user.droplets:
            raise HTTPException(
                status_code=404, detail=f"Droplet with id {droplet_id} not found"
            )
        try:
            response = requests.delete(
                f"{DIGITALOCEAN_API_URL}/{droplet_id}", headers=headers
            )
            if response.status_code == 204:
                user.droplets.remove(droplet_id)
                user_repo.update_user(user)
                return {"message": "Database deleted successfully"}
            else:
                raise HTTPException(
                    status_code=response.status_code, detail=response.json()
                )
        except Exception as e:
            raise HTTPException(status_code=response.status_code, detail=e.__dict__)
    
