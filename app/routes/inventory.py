# from fastapi import APIRouter, HTTPException
# from app.db.models.inventory import Inventory

# router = APIRouter()

# # Create a new inventory item
# @router.post("/inventory")
# async def create_inventory_item(item: Inventory):
#     try:
#         # Logic to save the item to the database
#         return {"message": "Inventory item created successfully", "item": item}
#     except Exception as e:
#         raise HTTPException(status_code=400, detail=str(e))

# # Get an inventory item by ID
# @router.get("/inventory/{item_id}")
# async def get_inventory_item(item_id: str):
#     try:
#         # Logic to fetch item from the database
#         return {"item_id": item_id, "details": "Item details fetched"}
#     except Exception as e:
#         raise HTTPException(status_code=404, detail=str(e))

# # Update an inventory item
# @router.put("/inventory/{item_id}")
# async def update_inventory_item(item_id: str, item: Inventory):
#     try:
#         # Logic to update item in the database
#         return {"message": "Inventory item updated successfully", "item": item}
#     except Exception as e:
#         raise HTTPException(status_code=400, detail=str(e))

# # Delete an inventory item
# @router.delete("/inventory/{item_id}")
# async def delete_inventory_item(item_id: str):
#     try:
#         # Logic to delete the item from the database
#         return {"message": "Inventory item deleted successfully"}
#     except Exception as e:
#         raise HTTPException(status_code=400, detail=str(e))


from fastapi import APIRouter, HTTPException, status
from app.db.models.inventory import Inventory
from app.db.database import (
    insert_inventory,
    query_by_inventory_id,
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
        item_data = item.dict()
        response = await insert_inventory(item_data)
        if not response:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Failed to create inventory item."
            )
        return {"message": "Inventory item created successfully", "item": item}
    except Exception as e:
        logger.error(f"Error creating inventory item: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An unexpected error occurred."
        )

@router.get('/inventory/{item_id}', status_code=status.HTTP_200_OK)
async def get_inventory(item_id: str):
    try:
        item_data = await query_by_inventory_id(item_id)
        if not item_data:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Inventory item not found."
            )
        return item_data
    except Exception as e:
        logger.error(f"Error fetching inventory item {item_id}: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An unexpected error occurred."
        )

@router.put('/inventory/{item_id}', status_code=status.HTTP_200_OK)
async def update_inventory(item_id: str, item: Inventory):
    try:
        item_data = item.dict()
        response = await update_inventory(item_id, item_data)
        if not response:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Inventory item not found or update failed."
            )
        return {"message": "Inventory item updated successfully", "item": item}
    except Exception as e:
        logger.error(f"Error updating inventory item {item_id}: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An unexpected error occurred."
        )

@router.delete('/inventory/{item_id}', status_code=status.HTTP_200_OK)
async def delete_inventory(item_id: str):
    try:
        response = await delete_inventory(item_id)
        if not response:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Inventory item not found or already deleted."
            )
        return {"message": "Inventory item deleted successfully"}
    except Exception as e:
        logger.error(f"Error deleting inventory item {item_id}: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An unexpected error occurred."
        )
