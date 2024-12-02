from pydantic import BaseModel, Field, field_validator
from typing import Optional, List, Dict
from datetime import datetime

PRODUCT_CATEGORIES = [
    "iPhone", "iPad", "Mac", "Apple Watch", "AirPods",
    "Apple TV", "HomePod", "Accessories",
    "Services", "Refurbished", "Vintage and Obsolete"
]

class Product(BaseModel):
    name: str = Field(..., 
        min_length=2, 
        max_length=100, 
        description="Name of the product"
    )
    description: Optional[str] = Field(
        None, 
        max_length=500, 
        description="Detailed description of the product"
    )
    price: float = Field(..., 
        gt=0, 
        description="Price of the product (must be positive)"
    )
    category: str = Field(..., 
        description="Category of the product"
    )
    available_stock: int = Field(..., 
        ge=0, 
        description="Number of items available in inventory"
    )

    sku: Optional[str] = Field(
        None, 
        description="Stock Keeping Unit - unique identifier for inventory tracking"
    )
    manufacturer: Optional[str] = Field(
        None, 
        description="Manufacturer or brand of the product"
    )
    weight: Optional[float] = Field(
        None, 
        gt=0, 
        description="Weight of the product in kilograms"
    )
    dimensions: Optional[Dict[str, float]] = Field(
        None, 
        description="Product dimensions (length, width, height in cm)"
    )
    tags: Optional[List[str]] = Field(
        None, 
        description="Additional tags for product categorization"
    )
    is_active: bool = Field(
        default=True, 
        description="Whether the product is currently available for sale"
    )
    created_at: str = Field(
        default_factory=lambda: datetime.now().isoformat(), 
        description="Timestamp when the product was added"
    )
    last_updated_at: Optional[str] = Field(
        default_factory=lambda: datetime.now().isoformat(),
        description="Timestamp of the last product information update"
    )

    @field_validator('category')
    @classmethod
    def validate_category(cls, v):
        if v not in PRODUCT_CATEGORIES:
            raise ValueError(f'Invalid category. Must be one of: {", ".join(PRODUCT_CATEGORIES)}')
        return v

    @field_validator('dimensions')
    @classmethod
    def validate_dimensions(cls, v):
        if v is not None:
            required_keys = ['length', 'width', 'height']
            if not all(key in v for key in required_keys):
                raise ValueError('Dimensions must include length, width, and height')
            if any(val <= 0 for val in v.values()):
                raise ValueError('Dimension values must be positive')
        return v
