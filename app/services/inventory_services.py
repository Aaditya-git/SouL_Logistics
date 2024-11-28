from app.db.database import inventory_collection

def find_nearest_warehouse(region: str, product_id: str):
    return inventory_collection.find_one({"region": region, "product_id": product_id})
