from fastapi import APIRouter, HTTPException
from app.db.models.products import Product

router = APIRouter()

# Add a new product
@router.post("/products")
async def add_product(product: Product):
    try:
        # Logic to save the product to the database
        return {"message": "Product added successfully", "product": product}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

# Get product by ID
@router.get("/products/{product_id}")
async def get_product(product_id: str):
    try:
        # Logic to fetch product from the database
        return {"product_id": product_id, "details": "Product details fetched"}
    except Exception as e:
        raise HTTPException(status_code=404, detail=str(e))

# Update product details
@router.put("/products/{product_id}")
async def update_product(product_id: str, product: Product):
    try:
        # Logic to update product in the database
        return {"message": "Product updated successfully", "product": product}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

# Delete a product
@router.delete("/products/{product_id}")
async def delete_product(product_id: str):
    try:
        # Logic to delete the product from the database
        return {"message": "Product deleted successfully"}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
