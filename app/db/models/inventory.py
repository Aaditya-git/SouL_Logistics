from pydantic import BaseModel, Field
from typing import Optional

class Inventory(BaseModel):
    product_id: str
    warehouse_id: str
    quantity: int
    region: str
    warehouse_location: Optional[str] = Field(None, description="Latitude,Longitude format")
