from pydantic import BaseModel, Field, field_validator
from typing import Optional
from datetime import datetime

VALID_REGIONS = [
    "us-east-1", "us-east-2", "us-west-1", "us-west-2", "us-central"
]

VALID_STATES = [
    'AL', 'AK', 'AZ', 'AR', 'CA', 'CO', 'CT', 'DE', 'FL', 'GA', 
    'HI', 'ID', 'IL', 'IN', 'IA', 'KS', 'KY', 'LA', 'ME', 'MD', 
    'MA', 'MI', 'MN', 'MS', 'MO', 'MT', 'NE', 'NV', 'NH', 'NJ', 
    'NM', 'NY', 'NC', 'ND', 'OH', 'OK', 'OR', 'PA', 'RI', 'SC', 
    'SD', 'TN', 'TX', 'UT', 'VT', 'VA', 'WA', 'WV', 'WI', 'WY'
]

class Warehouse(BaseModel):
    name: str = Field(..., min_length=2, max_length=100, description="Name of the warehouse")
    region: Optional[str] = Field(None, description="Geographic region of the warehouse")
    state: str = Field(..., description="State where the warehouse is located")
    address: str = Field(..., max_length=200, description="Warehouse address line 1")
    city: str = Field(..., max_length=100, description="City where the warehouse is located")
    zip_code: str = Field(..., description="Postal/ZIP code of the warehouse")
    contact_email: Optional[str] = Field(None, description="Contact email for the warehouse")
    contact_phone: Optional[str] = Field(None, description="Contact phone number")
    capacity: Optional[int] = Field(None, gt=0, description="Total storage capacity of the warehouse")
    is_active: bool = Field(default=True, description="Whether the warehouse is currently operational")
    created_at: str = Field(default_factory=lambda: datetime.now().isoformat(), description="Timestamp when the warehouse was added")

    @field_validator('region')
    @classmethod
    def validate_region(cls, v):
        if v.lower() not in [region.lower() for region in VALID_REGIONS]:
            raise ValueError(f'Invalid region. Must be one of: {", ".join(VALID_REGIONS)}')
        return v.lower()

    @field_validator('state')
    @classmethod
    def validate_state(cls, v):
        if v.upper() not in VALID_STATES:
            raise ValueError(f'Invalid state. Must be a valid US state abbreviation.')
        return v.upper()

    @field_validator('zip_code')
    @classmethod
    def validate_zip_code(cls, v):
        import re
        zip_regex = re.compile(r'^\d{5}(-\d{4})?$')
        if not zip_regex.match(v):
            raise ValueError('Invalid ZIP code. Use format: 12345 or 12345-6789')
        return v