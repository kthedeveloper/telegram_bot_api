from fastapi import APIRouter

router = APIRouter()

@router.get("/")
async def read_all_items():

    return [
        {"id": 1, "name": "Product 1"},
        {"id": 2, "name": "Product 2"},
        {"id": 3, "name": "Product 3"},
        {"id": 4, "name": "Product 4"},
    ]