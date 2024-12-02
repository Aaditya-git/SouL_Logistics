from pydantic import BaseModel, EmailStr, Field, field_validator
from typing import Optional
import re

class User(BaseModel):
    name: str = Field(..., min_length=2, max_length=100, description="Full name of the user")
    email: EmailStr = Field(..., description="Email address of the user")
    password: str = Field(..., min_length=2, max_length=20, description="Password of the user")
    phone: str = Field(..., description="Phone number")
    address: str = Field(None, max_length=200, description="Address line 1")
    city: str = Field(None, max_length=100, description="City")
    state: str = Field(None, max_length=50, description="State")
    zip_code: str = Field(None, description="Postal/ZIP code")
    region: Optional[str] = Field(None, description="Geographic region for the user")

    @field_validator('phone')
    def validate_phone_number(cls, v):
        if v is None:
            return v
        phone_regex = re.compile(r'^(\+1\s?)?(\(\d{3}\)|\d{3})[\s.-]?\d{3}[\s.-]?\d{4}$')
        if not phone_regex.match(v):
            raise ValueError('Invalid phone number format. Use formats like: +1 (123) 456-7890 or 123-456-7890')
        return v

    @field_validator('state')
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

    class Config:
        extra = 'ignore'
        populate_by_name = True