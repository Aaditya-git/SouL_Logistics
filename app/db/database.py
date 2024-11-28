from app.config import get_database
from dotenv import load_dotenv
import os

load_dotenv()
db = get_database()

if db is not None:
    inventory_collection = db[os.getenv('INVENTORY_COLLECTION')]
    orders_collection = db[os.getenv('ORDERS_COLLECTION')]
    products_collection = db[os.getenv('PRODUCTS_COLLECTION')]
    shipments_collection = db[os.getenv('SHIPMENTS_COLLECTION')]
    users_collection = db[os.getenv('USERS_COLLECTION')]
else:
    print("Database connection failed during initialization.")

def insert_shipment(shipment_data):
    if db is None:
        raise ValueError('Database connection is not available.')
    return shipments_collection.insert_one(shipment_data)

def update_shipment(shipment_id, shipment_data):
    if db is None:
        raise ValueError('Database connection is not available.')
    return shipments_collection.update_one({'shipment_id': shipment_id}, {'$set': shipment_data})

def delete_shipment(shipment_id):
    if db is None:
        raise ValueError('Database connection is not available.')
    return shipments_collection.delete_one(shipment_id)

def query_by_shipment_id(shipment_id):
    if db is None:
        raise ValueError("Database connection is not available.")
    return shipments_collection.find_one({'shipment_id': shipment_id})