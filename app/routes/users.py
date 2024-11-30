from fastapi import APIRouter, HTTPException, status
from app.db.models.users import User
from app.db.database import (
    insert_user,
    query_user,
    update_user,
    delete_user,
)
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

router = APIRouter()

@router.post('/users', status_code=status.HTTP_201_CREATED)
async def create_user(user: User):
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
        user_data = user.model_dump()
        if user_data["state"]:
            user_data["region"] = state_region_mappings.get(user_data["state"], 'Unknown Region')
        response = await insert_user(user_data)
        if not response:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Failed to create user."
            )
        user_data["_id"] = response
        return {"message": "User created successfully", "user": user_data}
    except Exception as e:
        logger.error(f"Error creating user: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An unexpected error occurred."
        )

@router.get('/users/{user_id}', status_code=status.HTTP_200_OK)
async def get_user(user_id: str):
    try:
        user_data = await query_user(user_id)
        if not user_data:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not found."
            )
        return user_data
    except Exception as e:
        logger.error(f"Error fetching user {user_id}: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An unexpected error occurred."
        )

@router.put('/users/{user_id}', status_code=status.HTTP_200_OK)
async def edit_user(user_id: str, user: User):
    try:
        user_data = user.model_dump()
        response = await update_user(user_id, user_data)
        if not response:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not found or update failed."
            )
        return {"message": "User updated successfully", "user": user_data}
    except Exception as e:
        logger.error(f"Error updating user {user_id}: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An unexpected error occurred."
        )

@router.delete('/users/{user_id}', status_code=status.HTTP_200_OK)
async def remove_user(user_id: str):
    try:
        response = await delete_user(user_id)
        if not response:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not found or already deleted."
            )
        return {"message": "User deleted successfully"}
    except Exception as e:
        logger.error(f"Error deleting user {user_id}: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An unexpected error occurred."
        )
