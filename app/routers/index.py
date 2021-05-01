from fastapi import APIRouter

router = APIRouter()


@router.get("/")
async def index():
    return {"EZInventory api version": "0.0"}
