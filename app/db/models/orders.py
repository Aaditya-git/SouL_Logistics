from pydantic import BaseModel

class Order(BaseModel):
    order_id: str
    user_id: str
    product_id: str
    quantity: int
    status: str  # e.g., "Pending", "Shipped", "Delivered"
