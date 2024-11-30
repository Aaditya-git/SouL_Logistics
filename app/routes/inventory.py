from fastapi import APIRouter, HTTPException, status
from app.db.models.inventory import Inventory
from app.db.database import (
    insert_inventory,
    query_inventory,
    update_inventory,
    delete_inventory,
)
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

router = APIRouter()

@router.post('/inventory', status_code=status.HTTP_201_CREATED)
async def create_inventory(item: Inventory):
    try:
        item_data = item.model_dump()
        response = await insert_inventory(item_data)
        if not response:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Failed to create inventory item."
            )
        return {"message": "Inventory created successfully", "item": item}
    except Exception as e:
        logger.error(f"Error creating inventory item: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An unexpected error occurred."
        )

@router.get('/inventory/{item_id}', status_code=status.HTTP_200_OK)
async def get_inventory(item_id: str):
    try:
        item_data = await query_inventory(item_id)
        if not item_data:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Inventory not found."
            )
        return item_data
    except Exception as e:
        logger.error(f"Error fetching inventory {item_id}: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An unexpected error occurred."
        )

@router.put('/inventory/{item_id}', status_code=status.HTTP_200_OK)
async def edit_inventory(item_id: str, item: Inventory):
    try:
        item_data = item.model_dump()
        response = await update_inventory(item_id, item_data)
        if not response:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Inventory not found or update failed."
            )
        return {"message": "Inventory updated successfully", "item": item}
    except Exception as e:
        logger.error(f"Error updating inventory {item_id}: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An unexpected error occurred."
        )

@router.delete('/inventory/{item_id}', status_code=status.HTTP_200_OK)
async def remove_inventory(item_id: str):
    try:
        response = await delete_inventory(item_id)
        if not response:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Inventory not found or already deleted."
            )
        return {"message": "Inventory deleted successfully"}
    except Exception as e:
        logger.error(f"Error deleting inventory {item_id}: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An unexpected error occurred."
        )
