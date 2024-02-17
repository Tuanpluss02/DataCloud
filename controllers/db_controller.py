from fastapi import APIRouter

router = APIRouter()


@router.get("/doc")
def doc():
    return {"message": "Documentation endpoint"}