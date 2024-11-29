from fastapi import APIRouter, HTTPException, status
from app.db.models.orders import Order
from app.db.database import (
    insert_order,
    query_by_order_id,
    update_order,
    delete_order,
)
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

router = APIRouter()

@router.post('/orders', status_code=status.HTTP_201_CREATED)
async def create_order(order: Order):
    try:
        order_data = order.dict()
        response = await insert_order(order_data)
        if not response:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Failed to create order."
            )
        return {"message": "Order created successfully", "order": order}
    except Exception as e:
        logger.error(f"Error creating order: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An unexpected error occurred."
        )

@router.get('/orders/{order_id}', status_code=status.HTTP_200_OK)
async def get_order(order_id: str):
    try:
        order_data = await query_by_order_id(order_id)
        if not order_data:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Order not found."
            )
        return order_data
    except Exception as e:
        logger.error(f"Error fetching order {order_id}: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An unexpected error occurred."
        )

@router.put('/orders/{order_id}', status_code=status.HTTP_200_OK)
async def update_order(order_id: str, order: Order):
    try:
        order_data = order.dict()
        response = await update_order(order_id, order_data)
        if not response:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Order not found or update failed."
            )
        return {"message": "Order updated successfully", "order": order}
    except Exception as e:
        logger.error(f"Error updating order {order_id}: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An unexpected error occurred."
        )

@router.delete('/orders/{order_id}', status_code=status.HTTP_200_OK)
async def delete_order(order_id: str):
    try:
        response = await delete_order(order_id)
        if not response:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Order not found or already deleted."
            )
        return {"message": "Order deleted successfully"}
    except Exception as e:
        logger.error(f"Error deleting order {order_id}: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An unexpected error occurred."
        )
