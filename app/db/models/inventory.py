from pydantic import BaseModel
from typing import Optional

class Inventory(BaseModel):
    item_id: str  # Unique identifier for the item
    warehouse_id: str  # Warehouse where the item is stored
    quantity: int  # Number of items available
    restock_threshold: Optional[int] = 10  # Minimum stock level before restocking
    status: Optional[str] = "Available"  # Status of the item (e.g., "Available", "Out of Stock")
