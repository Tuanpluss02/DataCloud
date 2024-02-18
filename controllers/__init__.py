from fastapi import APIRouter 
from controllers.auth_controller import router as auth_router
from controllers.container_controller import router as container_router 


router = APIRouter()
router.include_router(auth_router,prefix="/auth", tags=["Authentication"])
router.include_router(container_router, prefix="/container", tags=["Container Management"])