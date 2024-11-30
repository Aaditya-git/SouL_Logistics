from pydantic import BaseModel, Field, field_validator
from typing import Optional
from datetime import datetime
import re

class Order(BaseModel):
    order_id: str = Field(..., description="Unique identifier for the order")
    user_id: str = Field(..., description="ID of the user placing the order")
    product_id: str = Field(..., description="ID of the product being ordered")
    quantity: int = Field(..., gt=0, description="Number of items ordered")
    status: str = Field(default="Pending", description="Status of the order")
    address: str = Field(None, max_length=200, description="Shipping address line 1")
    city: str = Field(None, max_length=100, description="Shipping city")
    state: str = Field(None, max_length=50, description="Shipping state")
    zip_code: str = Field(None, description="Shipping postal/ZIP code")
    region: Optional[str] = Field(None, description="Geographic region for the order")
    created_at: Optional[str] = Field(default_factory=lambda: datetime.now().isoformat(), description="Timestamp when the order was created")

    @field_validator('status')
    @classmethod
    def validate_status(cls, v):
        valid_statuses = [
            "Pending", 
            "Processing", 
            "Shipped", 
            "Delivered", 
            "Cancelled", 
            "Returned"
        ]
        if v not in valid_statuses:
            raise ValueError(f'Invalid order status. Must be one of: {", ".join(valid_statuses)}')
        return v

    @field_validator('state')
    @classmethod
    def validate_state(cls, v):
        if v is None:
            return v
        valid_states = [
            'AL', 'AK', 'AZ', 'AR', 'CA', 'CO', 'CT', 'DE', 'FL', 'GA', 
            'HI', 'ID', 'IL', 'IN', 'IA', 'KS', 'KY', 'LA', 'ME', 'MD', 
            'MA', 'MI', 'MN', 'MS', 'MO', 'MT', 'NE', 'NV', 'NH', 'NJ', 
            'NM', 'NY', 'NC', 'ND', 'OH', 'OK', 'OR', 'PA', 'RI', 'SC', 
            'SD', 'TN', 'TX', 'UT', 'VT', 'VA', 'WA', 'WV', 'WI', 'WY'
        ]
        if v.upper() not in valid_states:
            raise ValueError('Invalid US state abbreviation')
        return v.upper()

    @field_validator('zip_code')
    @classmethod
    def validate_zip_code(cls, v):
        if v is None:
            return v
        zip_regex = re.compile(r'^\d{5}(-\d{4})?$')
        if not zip_regex.match(v):
            raise ValueError('Invalid ZIP code. Use format: 12345 or 12345-6789')
        return v
    
    @field_validator('region')
    @classmethod
    def validate_region(cls, v):
        VALID_REGIONS = [
            "us-east-1", "us-east-2", "us-west-1", "us-west-2", "us-central"
        ]
        
        if v.lower() not in [region.lower() for region in VALID_REGIONS]:
            raise ValueError(f'Invalid region. Must be one of: {", ".join(VALID_REGIONS)}')
        return v.lower()

    model_config = {
        "extra": "ignore",
        "populate_by_name": True
    }