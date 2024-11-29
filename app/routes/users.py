from fastapi import APIRouter, HTTPException, status
from app.db.models.users import User
from app.db.database import (
    insert_user,
    query_by_user_id,
    update_user,
    delete_user_from_db,
)
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

router = APIRouter()

@router.post('/users', status_code=status.HTTP_201_CREATED)
async def create_user(user: User):
    try:
        user_data = user.dict()
        response = await insert_user(user_data)
        if not response:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Failed to create user."
            )
        return {"message": "User created successfully", "user": user}
    except Exception as e:
        logger.error(f"Error creating user: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An unexpected error occurred."
        )

@router.get('/users/{user_id}', status_code=status.HTTP_200_OK)
async def get_user(user_id: str):
    try:
        user_data = await query_by_user_id(user_id)
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
async def update_user(user_id: str, user: User):
    try:
        user_data = user.dict()
        response = await update_user(user_id, user_data)
        if not response:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not found or update failed."
            )
        return {"message": "User updated successfully", "user": user}
    except Exception as e:
        logger.error(f"Error updating user {user_id}: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An unexpected error occurred."
        )

@router.delete('/users/{user_id}', status_code=status.HTTP_200_OK)
async def delete_user(user_id: str):
    try:
        response = await delete_user_from_db(user_id)
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
