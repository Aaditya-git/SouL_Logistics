from fastapi import FastAPI
from app.routes import inventory, orders, products, shipments, users

app = FastAPI(title="Logistics and Supply Chain API")

# Include all routers
app.include_router(inventory.router, prefix="/inventory", tags=["Inventory"])
app.include_router(orders.router, prefix="/orders", tags=["Orders"])
app.include_router(products.router, prefix="/products", tags=["Products"])
app.include_router(shipments.router, prefix="/shipments", tags=["Shipments"])
app.include_router(users.router, prefix="/users", tags=["Users"])

@app.get("/")
def root():
    return {"message": "Logistics API is up and running!"}
