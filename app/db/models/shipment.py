from pydantic import BaseModel
from typing import Optional

class Shipment(BaseModel):
    shipment_id: str  # Unique identifier for the shipment
    order_id: str  # ID of the associated order
    warehouse_id: str  # Warehouse from which the shipment is dispatched
    status: Optional[str] = "In Transit"  # Shipment status (e.g., "In Transit", "Delivered")
    estimated_delivery: Optional[str] = None  # Estimated delivery date
    tracking_info: Optional[str] = None  # Tracking details for the shipment
