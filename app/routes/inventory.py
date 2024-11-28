from fastapi import APIRouter, HTTPException
from app.db.database import inventory_collection
from app.db.models.inventory import Inventory

router = APIRouter()

@router.get("/")
def get_all_inventory():
    return list(inventory_collection.find({}, {"_id": 0}))

@router.post("/")
def add_inventory(item: Inventory):
    inventory_collection.insert_one(item.dict())
    return {"message": "Inventory item added successfully!"}

@router.get("/{product_id}")
def get_inventory_by_product(product_id: str):
    result = inventory_collection.find_one({"product_id": product_id}, {"_id": 0})
    if not result:
        raise HTTPException(status_code=404, detail="Product not found in inventory")
    return result
