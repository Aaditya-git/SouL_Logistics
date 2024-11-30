from fastapi import APIRouter, HTTPException, status
from app.db.models.warehouse import Warehouse
from app.db.database import (
    insert_warehouse,
    query_warehouse,
    update_warehouse,
    delete_warehouse,
)
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

router = APIRouter()

@router.post('/warehouse', status_code=status.HTTP_201_CREATED)
async def create_warehouse(warehouse: Warehouse):
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
        warehouse_data = warehouse.model_dump()
        if warehouse_data["state"]:
            warehouse_data["region"] = state_region_mappings.get(warehouse_data["state"], 'Unknown Region')
        response = await insert_warehouse(warehouse_data)
        if not response:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Failed to create warehouse."
            )
        warehouse_data["_id"] = response
        return {"message": "Warehouse created successfully", "warehouse": warehouse_data}
    except Exception as e:
        logger.error(f"Error creating warehouse: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An unexpected error occurred."
        )

@router.get('/warehouse/{warehouse_id}', status_code=status.HTTP_200_OK)
async def get_warehouse(warehouse_id: str):
    try:
        warehouse_data = await query_warehouse(warehouse_id)
        if not warehouse_data:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Warehouse not found."
            )
        return warehouse_data
    except Exception as e:
        logger.error(f"Error fetching warehouse {warehouse_id}: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An unexpected error occurred."
        )

@router.put('/warehouse/{warehouse_id}', status_code=status.HTTP_200_OK)
async def edit_warehouse(warehouse_id: str, warehouse: Warehouse):
    try:
        warehouse_data = warehouse.model_dump()
        response = await update_warehouse(warehouse_id, warehouse_data)
        if not response:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Warehouse not found or update failed."
            )
        return {"message": "Warehouse updated successfully", "warehouse": warehouse_data}
    except Exception as e:
        logger.error(f"Error updating warehouse {warehouse_id}: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An unexpected error occurred."
        )

@router.delete('/warehouse/{warehouse_id}', status_code=status.HTTP_200_OK)
async def remove_warehouse(warehouse_id: str):
    try:
        response = await delete_warehouse(warehouse_id)
        if not response:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Warehouse not found or already deleted."
            )
        return {"message": "Warehouse deleted successfully"}
    except Exception as e:
        logger.error(f"Error deleting warehouse {warehouse_id}: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An unexpected error occurred."
        )
