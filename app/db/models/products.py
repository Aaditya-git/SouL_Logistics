from pydantic import BaseModel
from typing import Optional

class Product(BaseModel):
    product_id: str  # Unique identifier for the product
    name: str  # Name of the product
    description: Optional[str] = None  # Description of the product
    price: float  # Price of the product
    category: Optional[str] = None  # Category of the product (e.g., "Electronics")
    available_stock: int  # Number of items available in inventory
