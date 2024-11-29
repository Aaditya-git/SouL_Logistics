from fastapi import APIRouter, HTTPException, status
from app.db.models.shipments import Shipment
from app.db.database import (
    insert_shipment,
    query_by_shipment_id,
    update_shipment,
    delete_shipment,
)
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

router = APIRouter()

@router.post('/shipments', status_code=status.HTTP_201_CREATED)
async def create_shipment(shipment: Shipment):
    try:
        shipment_data = shipment.dict()

        # Insert the shipment into the database
        result = await insert_shipment(shipment_data)

        # Check if the insertion was successful (using result.inserted_id)
        if not result.inserted_id:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Failed to create shipment."
            )

        return {"message": "Shipment created successfully", "shipment_id": str(result.inserted_id)}
    
    except Exception as e:
        logger.error(f"Error creating shipment: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An unexpected error occurred."
        )


@router.get('/shipments/{shipment_id}', status_code=status.HTTP_200_OK)
async def get_shipment(shipment_id: str):
    """
    Fetch details of a specific shipment.
    """
    try:
        shipment_data = await query_by_shipment_id(shipment_id)
        if not shipment_data:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Shipment not found."
            )
        return {
            "shipment_id": shipment_data["shipment_id"],
            "status": shipment_data["status"],
            "details": "Shipment details fetched successfully",
        }
    except ValueError as ve:
        logger.error(f"Invalid Shipment ID: {shipment_id} - {ve}")
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail="Invalid shipment ID."
        )
    except Exception as e:
        logger.error(f"Error fetching shipment {shipment_id}: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An unexpected error occurred."
        )

@router.put("/shipments/{shipment_id}", status_code=status.HTTP_200_OK)
async def update_shipment(shipment_id: str, shipment: Shipment):
    """
    Update an existing shipment.
    """
    try:
        shipment_data = shipment.dict()
        response = await update_shipment(shipment_id, shipment_data)
        if not response:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Shipment not found or update failed."
            )
        return {
            "message": "Shipment updated successfully",
            "shipment": shipment
        }
    except ValueError as ve:
        logger.error(f"Validation Error: {ve}")
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail=str(ve)
        )
    except Exception as e:
        logger.error(f"Error updating shipment {shipment_id}: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An unexpected error occurred."
        )

@router.delete("/shipments/{shipment_id}", status_code=status.HTTP_200_OK)
async def delete_shipment(shipment_id: str):
    """
    Delete a shipment by ID.
    """
    try:
        response = await delete_shipment(shipment_id)
        if not response:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Shipment not found or already deleted."
            )
        return {"message": "Shipment deleted successfully"}
    except ValueError as ve:
        logger.error(f"Invalid Shipment ID: {shipment_id} - {ve}")
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail="Invalid shipment ID."
        )
    except Exception as e:
        logger.error(f"Error deleting shipment {shipment_id}: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An unexpected error occurred."
        )
