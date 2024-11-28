from fastapi import FastAPI
from app.routes import inventory, orders, products, shipments, users
import uvicorn

# Initialize FastAPI app
app = FastAPI()

# Include the routes for each entity
app.include_router(inventory.router, prefix="/api", tags=["Inventory"])
app.include_router(orders.router, prefix="/api", tags=["Orders"])
app.include_router(products.router, prefix="/api", tags=["Products"])
app.include_router(shipments.router, prefix="/api", tags=["Shipments"])
app.include_router(users.router, prefix="/api", tags=["Users"])

# Root endpoint
@app.get("/")
async def root():
    return {"message": "Welcome to the Logistics and Supply Chain Management API"}

# If the script is run directly, start the FastAPI app with Uvicorn
if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
