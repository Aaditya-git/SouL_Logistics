import asyncio
from pymongo.results import InsertOneResult
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

# def insert_shipment(shipment_data):
#     if db is None:
#         raise ValueError('Database connection is not available.')
#     return shipments_collection.insert_one(shipment_data)
# async def insert_shipment(shipment_data):
#     if db is None:
#         raise ValueError('Database connection is not available.')

#     # Run the synchronous database operation in a background thread
#     result = await asyncio.to_thread(shipments_collection.insert_one, shipment_data)

#     # Return the InsertOneResult object, not directly an awaitable
#     return result


# def update_shipment(shipment_id, shipment_data):
#     if db is None:
#         raise ValueError('Database connection is not available.')
#     return shipments_collection.update_one({'shipment_id': shipment_id}, {'$set': shipment_data})

# def delete_shipment(shipment_id):
#     if db is None:
#         raise ValueError('Database connection is not available.')
#     return shipments_collection.delete_one(shipment_id)

# def query_by_shipment_id(shipment_id):
#     if db is None:
#         raise ValueError("Database connection is not available.")
#     return shipments_collection.find_one({'shipment_id': shipment_id})
async def insert_shipment(shipment_data):
    if db is None:
        raise ValueError('Database connection is not available.')
    # Run the synchronous database operation in a background thread
    result = await asyncio.to_thread(shipments_collection.insert_one, shipment_data)
    return result

async def update_shipment(shipment_id, shipment_data):
    if db is None:
        raise ValueError('Database connection is not available.')
    # Run the synchronous update operation in a background thread
    result = await asyncio.to_thread(shipments_collection.update_one, {'shipment_id': shipment_id}, {'$set': shipment_data})
    return result

async def delete_shipment(shipment_id):
    if db is None:
        raise ValueError('Database connection is not available.')
    # Run the synchronous delete operation in a background thread
    result = await asyncio.to_thread(shipments_collection.delete_one, {'shipment_id': shipment_id})
    return result

async def query_by_shipment_id(shipment_id):
    if db is None:
        raise ValueError("Database connection is not available.")
    # Run the synchronous find operation in a background thread
    result = await asyncio.to_thread(shipments_collection.find_one, {'shipment_id': shipment_id})
    return result



# ------------INVENTORY FUNCTIONS------------
# def insert_inventory(inventory_data):
#     if db is None:
#         raise ValueError('Database connection is not available.')
#     return inventory_collection.insert_one(inventory_data)

# def update_inventory(item_id, inventory_data):
#     if db is None:
#         raise ValueError('Database connection is not available.')
#     return inventory_collection.update_one({'item_id': item_id}, {'$set': inventory_data})

# def delete_inventory(item_id):
#     if db is None:
#         raise ValueError('Database connection is not available.')
#     return inventory_collection.delete_one({'item_id': item_id})

# def query_by_inventory_id(item_id):
#     if db is None:
#         raise ValueError("Database connection is not available.")
#     return inventory_collection.find_one({'item_id': item_id})

async def insert_inventory(inventory_data):
    if db is None:
        raise ValueError('Database connection is not available.')
    result = await asyncio.to_thread(inventory_collection.insert_one, inventory_data)
    return result

async def update_inventory(item_id, inventory_data):
    if db is None:
        raise ValueError('Database connection is not available.')
    result = await asyncio.to_thread(inventory_collection.update_one, {'item_id': item_id}, {'$set': inventory_data})
    return result

async def delete_inventory(item_id):
    if db is None:
        raise ValueError('Database connection is not available.')
    result = await asyncio.to_thread(inventory_collection.delete_one, {'item_id': item_id})
    return result

async def query_by_inventory_id(item_id):
    if db is None:
        raise ValueError("Database connection is not available.")
    result = await asyncio.to_thread(inventory_collection.find_one, {'item_id': item_id})
    return result


# -------- USERS FUNCTIONS --------
# def insert_user(user_data):
#     if db is None:
#         raise ValueError('Database connection is not available.')
#     return users_collection.insert_one(user_data)

# def update_user(user_id, user_data):
#     if db is None:
#         raise ValueError('Database connection is not available.')
#     return users_collection.update_one({'user_id': user_id}, {'$set': user_data})

# def delete_user(user_id):
#     if db is None:
#         raise ValueError('Database connection is not available.')
#     return users_collection.delete_one({'user_id': user_id})

# def query_by_user_id(user_id):
#     if db is None:
#         raise ValueError("Database connection is not available.")
#     return users_collection.find_one({'user_id': user_id})

async def insert_user(user_data):
    if db is None:
        raise ValueError('Database connection is not available.')
    result = await asyncio.to_thread(users_collection.insert_one, user_data)
    return result

async def update_user(user_id, user_data):
    if db is None:
        raise ValueError('Database connection is not available.')
    result = await asyncio.to_thread(users_collection.update_one, {'user_id': user_id}, {'$set': user_data})
    return result

async def delete_user_from_db(user_id):
    if db is None:
        raise ValueError('Database connection is not available.')
    result = await asyncio.to_thread(users_collection.delete_one, {'user_id': user_id})
    return result

async def query_by_user_id(user_id):
    if db is None:
        raise ValueError("Database connection is not available.")
    result = await asyncio.to_thread(users_collection.find_one, {'user_id': user_id})
    return result


# -------- Products Functions --------
# def insert_product(product_data):
#     if db is None:
#         raise ValueError('Database connection is not available.')
#     return products_collection.insert_one(product_data)

# def update_product(product_id, product_data):
#     if db is None:
#         raise ValueError('Database connection is not available.')
#     return products_collection.update_one({'product_id': product_id}, {'$set': product_data})

# def delete_product(product_id):
#     if db is None:
#         raise ValueError('Database connection is not available.')
#     return products_collection.delete_one({'product_id': product_id})

# def query_by_product_id(product_id):
#     if db is None:
#         raise ValueError("Database connection is not available.")
#     return products_collection.find_one({'product_id': product_id})


async def insert_product(product_data):
    if db is None:
        raise ValueError('Database connection is not available.')
    result = await asyncio.to_thread(products_collection.insert_one, product_data)
    return result

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

async def query_by_product_id(product_id):
    if db is None:
        raise ValueError("Database connection is not available.")
    result = await asyncio.to_thread(products_collection.find_one, {'product_id': product_id})
    return result

# -------- Orders Functions --------
# def insert_order(order_data):
#     if db is None:
#         raise ValueError('Database connection is not available.')
#     return orders_collection.insert_one(order_data)

# def update_order(order_id, order_data):
#     if db is None:
#         raise ValueError('Database connection is not available.')
#     return orders_collection.update_one({'order_id': order_id}, {'$set': order_data})

# def delete_order(order_id):
#     if db is None:
#         raise ValueError('Database connection is not available.')
#     return orders_collection.delete_one({'order_id': order_id})

# def query_by_order_id(order_id):
#     if db is None:
#         raise ValueError("Database connection is not available.")
#     return orders_collection.find_one({'order_id': order_id})


async def insert_order(order_data):
    if db is None:
        raise ValueError('Database connection is not available.')
    result = await asyncio.to_thread(orders_collection.insert_one, order_data)
    return result

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

async def query_by_order_id(order_id):
    if db is None:
        raise ValueError("Database connection is not available.")
    result = await asyncio.to_thread(orders_collection.find_one, {'order_id': order_id})
    return result
