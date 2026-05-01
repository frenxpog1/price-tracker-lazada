"""
TrackedProduct model for products being monitored by users.
"""
from sqlalchemy import Column, String, Numeric, DateTime, ForeignKey, Text, Index
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from datetime import datetime
import uuid

from app.core.database import Base


class TrackedProduct(Base):
    """
    TrackedProduct model representing products users are monitoring.
    
    Attributes:
        id: Unique product tracking identifier (UUID)
        user_id: Foreign key to user who is tracking this product
        platform: E-commerce platform (lazada, shopee, tiktok)
        product_name: Name of the product
        product_url: URL to the product page
        current_price: Current price of the product
        price_threshold: Target price for notifications
        currency: Currency code (default: USD)
        image_url: URL to product image
        created_at: Timestamp when tracking started
        last_checked: Timestamp of last price check
        user: Relationship to user
        price_history: Relationship to price history entries
        notifications: Relationship to notifications
    """
    __tablename__ = "tracked_products"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    platform = Column(String(50), nullable=False)
    product_name = Column(String(500), nullable=False)
    product_url = Column(Text, nullable=False)
    current_price = Column(Numeric(10, 2), nullable=False)
    price_threshold = Column(Numeric(10, 2), nullable=False)
    currency = Column(String(10), default="USD", nullable=False)
    image_url = Column(Text)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    last_checked = Column(DateTime)
    
    # Relationships
    user = relationship("User", back_populates="tracked_products")
    price_history = relationship(
        "PriceHistory", 
        back_populates="tracked_product", 
        cascade="all, delete-orphan",
        order_by="PriceHistory.checked_at.desc()"
    )
    notifications = relationship(
        "Notification", 
        back_populates="tracked_product", 
        cascade="all, delete-orphan"
    )
    
    # Indexes for performance
    __table_args__ = (
        Index('idx_tracked_products_user_id', 'user_id'),
        Index('idx_tracked_products_last_checked', 'last_checked'),
    )
    
    def __repr__(self) -> str:
        return f"<TrackedProduct(id={self.id}, product_name={self.product_name[:30]}, platform={self.platform})>"
