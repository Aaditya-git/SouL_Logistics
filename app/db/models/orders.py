from pydantic import BaseModel
from typing import Optional

class Order(BaseModel):
    order_id: str  # Unique identifier for the order
    user_id: str  # ID of the user placing the order
    product_id: str  # ID of the product being ordered
    quantity: int  # Number of items ordered
    status: Optional[str] = "Pending"  # Status of the order (e.g., "Pending", "Shipped", "Delivered")
    shipping_address: Optional[str] = None  # Address where the order will be shipped
    created_at: Optional[str] = None  # Timestamp when the order was created
