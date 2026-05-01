"""
PriceHistory model for tracking price changes over time.
"""
from sqlalchemy import Column, Numeric, DateTime, ForeignKey, Index
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from datetime import datetime
import uuid

from app.core.database import Base


class PriceHistory(Base):
    """
    PriceHistory model representing historical price data for tracked products.
    
    Attributes:
        id: Unique price history entry identifier (UUID)
        tracked_product_id: Foreign key to tracked product
        price: Price at the time of check
        checked_at: Timestamp when price was checked
        tracked_product: Relationship to tracked product
    """
    __tablename__ = "price_history"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    tracked_product_id = Column(
        UUID(as_uuid=True), 
        ForeignKey("tracked_products.id", ondelete="CASCADE"), 
        nullable=False
    )
    price = Column(Numeric(10, 2), nullable=False)
    checked_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    
    # Relationships
    tracked_product = relationship("TrackedProduct", back_populates="price_history")
    
    # Indexes for performance
    __table_args__ = (
        Index('idx_price_history_product_id', 'tracked_product_id'),
        Index('idx_price_history_checked_at', 'checked_at'),
    )
    
    def __repr__(self) -> str:
        return f"<PriceHistory(id={self.id}, price={self.price}, checked_at={self.checked_at})>"
