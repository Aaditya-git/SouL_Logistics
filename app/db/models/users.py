from pydantic import BaseModel, EmailStr
from typing import Optional

class User(BaseModel):
    user_id: str  # Unique identifier for the user
    name: str  # Full name of the user
    email: EmailStr  # Email address of the user
    address: Optional[str] = None  # Address of the user
    phone: Optional[str] = None  # Phone number of the user
    role: Optional[str] = "Customer"  # Role of the user (e.g., "Customer", "Admin")
