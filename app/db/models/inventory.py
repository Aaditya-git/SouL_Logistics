from pydantic import BaseModel, Field, field_validator
from typing import Optional

class Inventory(BaseModel):
    inventory_id: str = Field(..., description="Unique identifier for the inventory record")
    warehouse_id: str = Field(..., description="ID of the warehouse storing the inventory")
    product_id: str = Field(..., description="ID of the product in inventory")
    quantity: int = Field(..., ge=0, description="Current quantity of the product in inventory")
    minimum_stock_level: Optional[int] = Field(None, ge=0, description="Minimum stock level before reordering")
    maximum_stock_level: Optional[int] = Field(None, ge=0, description="Maximum recommended stock level")
    last_restocked_at: Optional[str] = Field(None, description="Timestamp of last restock")
    status: str = Field(default="In Stock", description="Current inventory status")
    
    @field_validator('status')
    @classmethod
    def validate_status(cls, v):
        valid_statuses = [
            "In Stock", 
            "Low Stock", 
            "Out of Stock", 
            "Backordered"
        ]
        if v not in valid_statuses:
            raise ValueError(f'Invalid status. Must be one of: {", ".join(valid_statuses)}')
        return v
