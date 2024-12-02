from fastapi import APIRouter, HTTPException, status
from app.db.models.orders import Order
from app.db.database import (
    insert_order,
    query_order,
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
        if order_data["state"]:
            order_data["region"] = state_region_mappings.get(order_data["state"], 'Unknown Region')
        response = await insert_order(order_data)
        if not response:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Failed to create order."
            )
        return {"message": f"Order created successfully with id {response}"}
    except Exception as e:
        logger.error(f"Error creating order: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An unexpected error occurred."
        )

@router.get('/orders/{order_id}', status_code=status.HTTP_200_OK)
async def get_order(order_id: str):
    try:
        order_data = await query_order(order_id)
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
async def edit_order(order_id: str, order: Order):
    try:
        order_data = order.model_dump()
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
async def remove_order(order_id: str):
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
