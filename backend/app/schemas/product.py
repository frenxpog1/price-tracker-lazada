"""
Pydantic schemas for product search and tracking.
"""
from typing import List, Optional
from decimal import Decimal
from datetime import datetime
from pydantic import BaseModel, Field, HttpUrl


class ProductResult(BaseModel):
    """Schema for a single product search result."""
    platform: str = Field(..., description="E-commerce platform (lazada, shopee, tiktokshop)")
    product_url: str = Field(..., description="URL to the product page")
    product_name: str = Field(..., description="Product name/title")
    current_price: Decimal = Field(..., description="Current price")
    currency: str = Field(default="PHP", description="Currency code")
    image_url: Optional[str] = Field(None, description="Product image URL")
    availability: bool = Field(default=True, description="Whether product is in stock")
    scraped_at: datetime = Field(..., description="When the data was scraped")


class SearchResults(BaseModel):
    """Schema for product search results from all platforms."""
    query: str = Field(..., description="Search query used")
    results: List[ProductResult] = Field(default_factory=list, description="List of products found")
    total_results: int = Field(..., description="Total number of results")
    platforms_searched: List[str] = Field(..., description="Platforms that were searched")
    platforms_failed: List[str] = Field(default_factory=list, description="Platforms that failed")
    search_time_seconds: float = Field(..., description="Time taken to search")


class PriceHistoryEntry(BaseModel):
    """Schema for a single price history entry."""
    price: Decimal = Field(..., description="Price at this point in time")
    currency: str = Field(default="PHP", description="Currency code")
    checked_at: datetime = Field(..., description="When the price was checked")
    availability: bool = Field(default=True, description="Whether product was available")


class PriceHistoryResponse(BaseModel):
    """Schema for price history response."""
    product_id: str = Field(..., description="Tracked product ID")
    product_name: str = Field(..., description="Product name")
    product_url: str = Field(..., description="Product URL")
    platform: str = Field(..., description="E-commerce platform")
    current_price: Optional[Decimal] = Field(None, description="Current price")
    price_threshold: Decimal = Field(..., description="User's price threshold")
    history: List[PriceHistoryEntry] = Field(default_factory=list, description="Price history entries")
    total_entries: int = Field(..., description="Total number of history entries")
