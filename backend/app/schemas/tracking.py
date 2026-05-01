"""
Pydantic schemas for product tracking.
"""
from typing import Optional
from decimal import Decimal
from datetime import datetime
from pydantic import BaseModel, Field, HttpUrl, field_validator


class TrackedProductCreate(BaseModel):
    """Schema for creating a tracked product."""
    platform: str = Field(..., description="E-commerce platform (lazada, shopee, tiktokshop)")
    product_url: str = Field(..., description="URL to the product page")
    product_name: str = Field(..., description="Product name/title")
    current_price: Decimal = Field(..., gt=0, description="Current price (must be positive)")
    price_threshold: Decimal = Field(..., gt=0, description="Price threshold for notifications (must be positive)")
    currency: str = Field(default="PHP", description="Currency code")
    image_url: Optional[str] = Field(None, description="Product image URL")
    
    @field_validator('price_threshold')
    @classmethod
    def validate_positive_price(cls, v: Decimal) -> Decimal:
        """Ensure price threshold is positive."""
        if v <= 0:
            raise ValueError('Price threshold must be greater than 0')
        return v


class TrackedProductResponse(BaseModel):
    """Schema for tracked product response."""
    id: str = Field(..., description="Tracked product ID")
    user_id: str = Field(..., description="User ID who is tracking this product")
    platform: str = Field(..., description="E-commerce platform")
    product_url: str = Field(..., description="Product URL")
    product_name: str = Field(..., description="Product name")
    current_price: Optional[Decimal] = Field(None, description="Current price")
    price_threshold: Decimal = Field(..., description="Price threshold for notifications")
    currency: str = Field(default="PHP", description="Currency code")
    image_url: Optional[str] = Field(None, description="Product image URL")
    last_checked: Optional[datetime] = Field(None, description="Last time price was checked")
    created_at: datetime = Field(..., description="When tracking started")
    
    class Config:
        from_attributes = True


class ThresholdUpdate(BaseModel):
    """Schema for updating price threshold."""
    price_threshold: Decimal = Field(..., gt=0, description="New price threshold (must be positive)")
    
    @field_validator('price_threshold')
    @classmethod
    def validate_positive_threshold(cls, v: Decimal) -> Decimal:
        """Ensure threshold is positive."""
        if v <= 0:
            raise ValueError('Price threshold must be greater than 0')
        return v
