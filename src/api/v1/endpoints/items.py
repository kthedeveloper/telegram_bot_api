from fastapi import APIRouter, HTTPException

from schemas.item import ItemsList, Item

router = APIRouter()

items = [
    {"id": 1, "name": "Item 1"},
    {"id": 2, "name": "Item 2"},
    {"id": 3, "name": "Item 3"},
    {"id": 4, "name": "Item 4"},
]


@router.get("/", response_model=ItemsList)
async def read_all_items():
    return {"data": items, "total": len(items)}

@router.get("/{item_id}", response_model=Item)
async def read_item(item_id: int):
    for item in items:
        if item["id"] == item_id:
            return item
    raise HTTPException(status_code=404, detail="Item not found")

@router.delete("/{item_id}")
def delete_item(item_id: int):
    global items
    items = [i for i in items if i["id"] != item_id]
    return {"message": f"Item {item_id} deleted"}

@router.put("/create", response_model=Item)
def create_item(item: Item):

    items.append({"id": item.id, "name": item.name})

    return item