from app.config import get_database

db = get_database()

# Collections
inventory_collection = db["inventory"]
orders_collection = db["orders"]
products_collection = db["products"]
shipments_collection = db["shipments"]
users_collection = db["users"]
