from fastapi import APIRouter 
from controllers.auth_controller import router as auth_router
from controllers.container_controller import router as container_router 
from controllers.dgapi_controller import router as pulumi_router


router = APIRouter()
router.include_router(auth_router,prefix="/auth", tags=["Authentication"])
router.include_router(container_router, prefix="/container", tags=["Docker Container Management"])
router.include_router(pulumi_router, prefix="/pulumi", tags=["Pulumi DigitalOcean Management"])