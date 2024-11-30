from fastapi import FastAPI, HTTPException, status
from app.db.models.orders import Order
from app.routes import users, products, warehouse, inventory, orders, shipments
from app.db.database import (
    insert_order,
    query_warehouse_by_region,
    query_inventory_by_warehouse_id,
    update_inventory
)

import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI()

app.include_router(users.router, prefix="/api", tags=["Users"])
app.include_router(products.router, prefix="/api", tags=["Products"])
app.include_router(warehouse.router, prefix="/api", tags=["Warehouse"])
app.include_router(inventory.router, prefix="/api", tags=["Inventory"])
app.include_router(orders.router, prefix="/api", tags=["Orders"])
app.include_router(shipments.router, prefix="/api", tags=["Shipments"])

@app.get("/")
async def root():
    return {"message": "Welcome to the Logistics and Supply Chain Management API"}

@app.post('/order', status_code=status.HTTP_201_CREATED)
async def palce_order(order: Order):
    try:
        state_region_mappings = {
            'AL': 'us-east-1', 'AK': 'us-east-2', 'AZ': 'us-west-1', 'AR': 'us-west-2', 'CA': 'us-central',
            'CO': 'us-east-1', 'CT': 'us-east-2', 'DE': 'us-west-1', 'FL': 'us-west-2', 'GA': 'us-central',
            'HI': 'us-east-1', 'ID': 'us-east-2', 'IL': 'us-west-1', 'IN': 'us-west-2', 'IA': 'us-central',
            'KS': 'us-east-1', 'KY': 'us-east-2', 'LA': 'us-west-1', 'ME': 'us-west-2', 'MD': 'us-central',
            'MA': 'us-east-1', 'MI': 'us-east-2', 'MN': 'us-west-1', 'MS': 'us-west-2', 'MO': 'us-central',
            'MT': 'us-east-1', 'NE': 'us-east-2', 'NV': 'us-west-1', 'NH': 'us-west-2', 'NJ': 'us-central',
            'NM': 'us-east-1', 'NY': 'us-east-2', 'NC': 'us-west-1', 'ND': 'us-west-2', 'OH': 'us-central',
            'OK': 'us-east-1', 'OR': 'us-east-2', 'PA': 'us-west-1', 'RI': 'us-west-2', 'SC': 'us-central',
            'SD': 'us-east-1', 'TN': 'us-east-2', 'TX': 'us-west-1', 'UT': 'us-west-2', 'VT': 'us-central',
            'VA': 'us-east-1', 'WA': 'us-east-2', 'WV': 'us-west-1', 'WI': 'us-west-2', 'WY': 'us-central'
        }
        order_data = order.model_dump()
        order_data["status"] = "Pending"
        order_data["region"] = state_region_mappings.get(order_data["state"], 'Unknown Region')
        warehouses = await query_warehouse_by_region(order_data["region"])
        for warehouse in warehouses:
            inventory = await query_inventory_by_warehouse_id(warehouse["warehouse_id"], order_data["product_id"])
            for inv in inventory:
                if inv["quantity"] - order_data["quantity"] > inv["minimum_stock_level"]:
                    res = await update_inventory(inv["inventory_id"], {"quantity": inv["quantity"] - order_data["quantity"]})
                    if res:
                        order_data["status"] = "Processing"
                        response = await insert_order(order_data)
                        if not response:
                            raise HTTPException(
                                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                                detail="Failed to create order."
                            )
                        return {"message": "Order created successfully", "order": response}
        if order["status"] == "Pending":
            return {"message": "Order cannot be fulfilled", "order": order_data}
    except Exception as e:
        logger.error(f"Error creating order: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An unexpected error occurred."
        )