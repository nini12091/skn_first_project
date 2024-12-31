from fastapi import APIRouter
from pydantic import BaseModel

router = APIRouter()

class Item(BaseModel):
    name: str
    description: str | None = None
    price: float
    tax: float | None = None

@router.get("/")
def read_root():
    return {"message": "Welcome to FastAPI with Routers!"}

@router.get("/items/{item_id}")
def read_item(item_id: int, q: str | None = None):
    return {"item_id": item_id, "q": q}

@router.post("/items/")
def create_item(item: Item):
    return {
        "name": item.name,
        "description": item.description,
        "price": item.price,
        "tax": item.tax,
        "message": "Item successfully created!"
    }