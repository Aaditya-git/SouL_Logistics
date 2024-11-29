from fastapi import APIRouter, HTTPException, status
from app.db.models.products import Product
from app.db.database import (
    insert_product,
    query_by_product_id,
    update_product,
    delete_product,
)
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

router = APIRouter()

@router.post('/products', status_code=status.HTTP_201_CREATED)
async def create_product(product: Product):
    try:
        product_data = product.dict()
        response = await insert_product(product_data)
        if not response:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Failed to create product."
            )
        return {"message": "Product created successfully", "product": product}
    except Exception as e:
        logger.error(f"Error creating product: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An unexpected error occurred."
        )

@router.get('/products/{product_id}', status_code=status.HTTP_200_OK)
async def get_product(product_id: str):
    try:
        product_data = await query_by_product_id(product_id)
        if not product_data:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Product not found."
            )
        return product_data
    except Exception as e:
        logger.error(f"Error fetching product {product_id}: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An unexpected error occurred."
        )

@router.put('/products/{product_id}', status_code=status.HTTP_200_OK)
async def update_product(product_id: str, product: Product):
    try:
        product_data = product.dict()
        response = await update_product(product_id, product_data)
        if not response:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Product not found or update failed."
            )
        return {"message": "Product updated successfully", "product": product}
    except Exception as e:
        logger.error(f"Error updating product {product_id}: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An unexpected error occurred."
        )

@router.delete('/products/{product_id}', status_code=status.HTTP_200_OK)
async def delete_product(product_id: str):
    try:
        response = await delete_product(product_id)
        if not response:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Product not found or already deleted."
            )
        return {"message": "Product deleted successfully"}
    except Exception as e:
        logger.error(f"Error deleting product {product_id}: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An unexpected error occurred."
        )
