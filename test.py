from fastapi import FastAPI, HTTPException, status
from pydantic import BaseModel


class Item(BaseModel):
    id: int
    name: str

inventory = {}

app = FastAPI()


@app.get("/item/{item_id}")
def get_item(*, item_id: int, name: str):
    for item_id in inventory:
        if inventory[item_id].name == name:

                return inventory[item_id]        
        
    raise HTTPException(status_code=404, detail="item not found")

@app.post("/create-item/{item_id}")
def create_item(item: Item, item_id: int):
    if item_id in inventory:
        return {"error": "item already exists"}
    
    inventory[item_id] = item
    return inventory[item_id]
