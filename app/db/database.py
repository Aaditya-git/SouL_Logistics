import asyncio
from app.config import get_database
from dotenv import load_dotenv
import os
from bson import ObjectId
import time

load_dotenv()
db = get_database()

if db is not None:
    users_collection = db[os.getenv('USERS_COLLECTION')]
    products_collection = db[os.getenv('PRODUCTS_COLLECTION')]
    warehouses_collection = db[os.getenv('WAREHOUSES_COLLECTION')]
    inventory_collection = db[os.getenv('INVENTORY_COLLECTION')]
    orders_collection = db[os.getenv('ORDERS_COLLECTION')]
    shipments_collection = db[os.getenv('SHIPMENTS_COLLECTION')]
else:
    print("Database connection failed during initialization.")


# -------- USERS FUNCTIONS --------
async def insert_user(user_data):
    if db is None:
        raise ValueError('Database connection is not available.')
    result = await asyncio.to_thread(users_collection.insert_one, user_data)
    return str(result.inserted_id)


async def query_user(user_id):
    if db is None:
        raise ValueError("Database connection is not available.")
    try:
        object_id = ObjectId(user_id)
    except:
        raise ValueError("Invalid ObjectId format")
    
    result = await asyncio.to_thread(users_collection.find_one, {'_id': object_id})
    
    if result:
        result["_id"] = str(result["_id"])
        return result
    else:
        return None


async def query_user_by_email(email):
    if db is None:
        raise ValueError("Database connection is not available.")
    result = await asyncio.to_thread(users_collection.find_one, {'email': email})
    result["_id"] = str(result["_id"])
    return result["_id"], result["region"]


async def update_user(user_id, user_data):
    if db is None:
        raise ValueError('Database connection is not available.')
    result = await asyncio.to_thread(users_collection.update_one, {'user_id': user_id}, {'$set': user_data})
    return result


async def delete_user(user_id):
    if db is None:
        raise ValueError('Database connection is not available.')
    result = await asyncio.to_thread(users_collection.delete_one, {'user_id': user_id})
    return result


# -------- PRODUCTS FUNCTION --------
async def insert_product(product_data):
    if db is None:
        raise ValueError('Database connection is not available.')
    result = await asyncio.to_thread(products_collection.insert_one, product_data)
    return str(result.inserted_id)


async def query_product(product_id):
    if db is None:
        raise ValueError("Database connection is not available.")
    try:
        object_id = ObjectId(product_id)
    except:
        raise ValueError("Invalid ObjectId format")
    
    result = await asyncio.to_thread(products_collection.find_one, {'_id': object_id})
    
    if result:
        result["_id"] = str(result["_id"])
        return result
    else:
        return None


async def query_all_products():
    if db is None:
        raise ValueError('Database connection is not available.')
    
    products_list = products_collection.find({})
    products = []
    for product in products_list:
        product["_id"] = str(product["_id"])
        products.append(product)
    return products


async def update_product(product_id, product_data):
    if db is None:
        raise ValueError('Database connection is not available.')
    result = await asyncio.to_thread(products_collection.update_one, {'product_id': product_id}, {'$set': product_data})
    return result


async def delete_product(product_id):
    if db is None:
        raise ValueError('Database connection is not available.')
    result = await asyncio.to_thread(products_collection.delete_one, {'product_id': product_id})
    return result


# -------- WAREHOUSES FUNCTION --------
async def insert_warehouse(warehouse_data):
    if db is None:
        raise ValueError('Database connection is not available.')
    result = await asyncio.to_thread(warehouses_collection.insert_one, warehouse_data)
    return str(result.inserted_id)


async def query_warehouse(warehouse_id):
    if db is None:
        raise ValueError("Database connection is not available.")
    try:
        object_id = ObjectId(warehouse_id)
    except:
        raise ValueError("Invalid ObjectId format")
    
    result = await asyncio.to_thread(warehouses_collection.find_one, {'_id': object_id})
    
    if result:
        result["_id"] = str(result["_id"])
        return result
    else:
        return None


async def update_warehouse(warehouse_id, warehouse_data):
    if db is None:
        raise ValueError('Database connection is not available.')
    result = await asyncio.to_thread(warehouses_collection.update_one, {'warehouse_id': warehouse_id}, {'$set': warehouse_data})
    return result


async def delete_warehouse(warehouse_id):
    if db is None:
        raise ValueError('Database connection is not available.')
    result = await asyncio.to_thread(warehouses_collection.delete_one, {'warehouse_id': warehouse_id})
    return result

async def query_warehouse_by_region(region):
    if db is None:
        raise ValueError('Database connection is not available')
    result = await asyncio.to_thread(warehouses_collection.find, {'region': region})
    return result


# -------- INVENTORY FUNCTIONS --------
async def insert_inventory(inventory_data):
    if db is None:
        raise ValueError('Database connection is not available.')
    result = await asyncio.to_thread(inventory_collection.insert_one, inventory_data)
    return str(result.inserted_id)


async def query_inventory(item_id):
    if db is None:
        raise ValueError("Database connection is not available.")
    result = await asyncio.to_thread(inventory_collection.find_one, {'inventory_id': item_id})
    if result:
        result["_id"] = str(result["_id"])
    return result


async def update_inventory(item_id, inventory_data):
    if db is None:
        raise ValueError('Database connection is not available.')
    result = await asyncio.to_thread(inventory_collection.update_one, {'inventory_id': item_id}, {'$set': inventory_data})
    return result


async def delete_inventory(item_id):
    if db is None:
        raise ValueError('Database connection is not available.')
    result = await asyncio.to_thread(inventory_collection.delete_one, {'inventory_id': item_id})
    return result


async def query_inventory_by_warehouse_id(warehouse_id, product_id):
    if db is None:
        raise ValueError('Database connection is not available.')
    result = await asyncio.to_thread(inventory_collection.find, {'warehouse_id': warehouse_id, 'product_id': product_id})
    return result

# -------- ORDERS FUNCTIONS --------
async def insert_order(order_data):
    if db is None:
        raise ValueError('Database connection is not available.')
    result = await asyncio.to_thread(orders_collection.insert_one, order_data)
    return str(result.inserted_id)


async def query_order(order_id):
    if db is None:
        raise ValueError("Database connection is not available.")
    try:
        object_id = ObjectId(order_id)
    except:
        raise ValueError("Invalid ObjectId format")
    
    result = await asyncio.to_thread(orders_collection.find_one, {'_id': object_id})
    
    if result:
        result["_id"] = str(result["_id"])
        return result
    else:
        return None


async def query_all_orders(user_id):
    if db is None:
        raise ValueError('Database connection is not available.')
    orders_list = await asyncio.to_thread(orders_collection.find, {'user_id': user_id})
    orders = []
    for order in orders_list:
        order["_id"] = str(order["_id"])
        orders.append(order)
    return orders


async def update_order(order_id, order_data):
    if db is None:
        raise ValueError('Database connection is not available.')
    result = await asyncio.to_thread(orders_collection.update_one, {'order_id': order_id}, {'$set': order_data})
    return result


async def delete_order(order_id):
    if db is None:
        raise ValueError('Database connection is not available.')
    result = await asyncio.to_thread(orders_collection.delete_one, {'order_id': order_id})
    return result


# -------- SHIPMENT FUNCTIONS --------
async def insert_shipment(shipment_data):
    if db is None:
        raise ValueError('Database connection is not available.')
    result = await asyncio.to_thread(shipments_collection.insert_one, shipment_data)
    return str(result.inserted_id)


async def query_shipment(shipment_id):
    if db is None:
        raise ValueError("Database connection is not available.")
    result = await asyncio.to_thread(shipments_collection.find_one, {'shipment_id': shipment_id})
    if result:
        result["_id"] = str(result["_id"])
    return result


async def update_shipment(shipment_id, shipment_data):
    if db is None:
        raise ValueError('Database connection is not available.')
    result = await asyncio.to_thread(shipments_collection.update_one, {'shipment_id': shipment_id}, {'$set': shipment_data})
    return result


async def delete_shipment(shipment_id):
    if db is None:
        raise ValueError('Database connection is not available.')
    result = await asyncio.to_thread(shipments_collection.delete_one, {'shipment_id': shipment_id})
    return result


async def update_shipment_status(order_id: str, initial_status: str):
    print(f"Initial status: {initial_status}")
    if initial_status.upper() == "PROCESSING":
        object_id = ObjectId(order_id)
        print(f"Object ID: {object_id}")
        
        await asyncio.sleep(15)

        await asyncio.to_thread(
            orders_collection.update_one,
            {"_id": object_id},
            {"$set": {"status": "Shipped"}}
        )
        await asyncio.sleep(15)

        await asyncio.to_thread(
            orders_collection.update_one,
            {"_id": object_id},
            {"$set": {"status": "In Transit"}}
        )
        await asyncio.sleep(15)
        
        
        await asyncio.to_thread(
            orders_collection.update_one,
            {"_id": object_id},
            {"$set": {"status": "Delivered"}}
        )
    else:
        print(f"Order {order_id} status '{initial_status}' is not valid for processing.")