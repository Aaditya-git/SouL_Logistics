from pydantic import BaseModel, Field, field_validator
from typing import Optional, List
from datetime import datetime
from enum import Enum

class ShipmentStatus(str, Enum):
    PLACED = "Placed"
    PROCESSING = "Processing"
    SHIPPED = "Shipped"
    IN_TRANSIT = "In Transit"
    OUT_FOR_DELIVERY = "Out for Delivery"
    DELIVERED = "Delivered"
    RETURNED = "Returned"
    CANCELLED = "Cancelled"

class ShippingMethod(str, Enum):
    STANDARD = "Standard"
    EXPRESS = "Express"
    OVERNIGHT = "Overnight"
    TWO_DAY = "Two Day"
    GROUND = "Ground"
    INTERNATIONAL = "International"

class Address(BaseModel):
    street: str = Field(..., 
        min_length=2, 
        max_length=200, 
        description="Street address"
    )
    city: str = Field(..., 
        min_length=2, 
        max_length=100, 
        description="City name"
    )
    state: str = Field(..., 
        min_length=2, 
        max_length=50, 
        description="State or province"
    )
    postal_code: str = Field(..., 
        pattern=r'^\d{5}(-\d{4})?$', 
        description="Postal code (US format)"
    )
    country: str = Field(..., 
        min_length=2, 
        max_length=100, 
        description="Country name"
    )

class ShipmentItem(BaseModel):
    product_id: str = Field(..., 
        description="Unique product identifier",
        pattern=r'^PROD\d{5}$'
    )
    quantity: int = Field(..., 
        gt=0, 
        description="Number of items in shipment"
    )
    price: float = Field(..., 
        gt=0, 
        description="Price per item"
    )

class ShipmentTracking(BaseModel):
    order_id: str = Field(..., 
        description="Associated order identifier", 
        pattern=r'^ORD\d{6}$',
        examples=["ORD123456"]
    )
    customer_id: Optional[str] = Field(
        None, 
        description="Customer unique identifier",
        pattern=r'^CUST\d{5}$'
    )
    items: List[ShipmentItem] = Field(..., 
        description="Items in the shipment"
    )
    shipping_address: Address = Field(..., 
        description="Destination shipping address"
    )
    billing_address: Optional[Address] = Field(
        None, 
        description="Billing address (if different from shipping)"
    )
    status: ShipmentStatus = Field(
        default=ShipmentStatus.PLACED, 
        description="Current status of the shipment"
    )
    shipping_method: ShippingMethod = Field(
        default=ShippingMethod.STANDARD, 
        description="Selected shipping method"
    )
    tracking_number: Optional[str] = Field(
        None, 
        description="Carrier tracking number",
        pattern=r'^[A-Z0-9]{10,20}$'
    )
    carrier: Optional[str] = Field(
        None, 
        description="Shipping carrier name"
    )
    shipping_cost: Optional[float] = Field(
        None, 
        gt=0, 
        description="Total shipping cost"
    )
    estimated_delivery_date: Optional[str] = Field(
        None, 
        description="Estimated delivery date"
    )
    actual_delivery_date: Optional[str] = Field(
        None, 
        description="Actual delivery date"
    )
    created_at: str = Field(
        default_factory=lambda: datetime.now().isoformat(), 
        description="Timestamp when shipment was created"
    )
    last_updated_at: Optional[str] = Field(
        default_factory=lambda: datetime.now().isoformat(), 
        description="Timestamp of last shipment status update"
    )
    notes: Optional[List[str]] = Field(
        None, 
        description="Additional notes about the shipment"
    )

    @field_validator('estimated_delivery_date', 'actual_delivery_date')
    @classmethod
    def validate_date_format(cls, v):
        if v is not None:
            try:
                datetime.fromisoformat(v)
            except ValueError:
                raise ValueError('Date must be in ISO format (YYYY-MM-DD or YYYY-MM-DDTHH:MM:SS)')
        return v

    @field_validator('shipping_cost')
    @classmethod
    def validate_shipping_cost(cls, v):
        if v is not None and v < 0:
            raise ValueError('Shipping cost must be non-negative')
        return v

    def update_status(self, new_status: ShipmentStatus):
        """
        Method to update shipment status and timestamp
        """
        self.status = new_status
        self.last_updated_at = datetime.now().isoformat()

    def add_tracking_info(self, tracking_number: str, carrier: str):
        """
        Method to add tracking information
        """
        self.tracking_number = tracking_number
        self.carrier = carrier
        self.last_updated_at = datetime.now().isoformat()