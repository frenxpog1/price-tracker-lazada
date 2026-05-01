"""
Notification model for tracking email notifications sent to users.
"""
from sqlalchemy import Column, String, Numeric, DateTime, ForeignKey, Index
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from datetime import datetime
import uuid

from app.core.database import Base


class Notification(Base):
    """
    Notification model representing email notifications sent to users.
    
    Attributes:
        id: Unique notification identifier (UUID)
        user_id: Foreign key to user who received notification
        tracked_product_id: Foreign key to product that triggered notification
        old_price: Previous price before drop
        new_price: New price that triggered notification
        sent_at: Timestamp when notification was sent
        delivery_status: Status of email delivery (sent, failed, bounced)
        user: Relationship to user
        tracked_product: Relationship to tracked product
    """
    __tablename__ = "notifications"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    tracked_product_id = Column(
        UUID(as_uuid=True), 
        ForeignKey("tracked_products.id", ondelete="CASCADE"), 
        nullable=False
    )
    old_price = Column(Numeric(10, 2), nullable=False)
    new_price = Column(Numeric(10, 2), nullable=False)
    sent_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    delivery_status = Column(String(50), default="sent", nullable=False)
    
    # Relationships
    user = relationship("User", back_populates="notifications")
    tracked_product = relationship("TrackedProduct", back_populates="notifications")
    
    # Indexes for performance
    __table_args__ = (
        Index('idx_notifications_user_id', 'user_id'),
        Index('idx_notifications_sent_at', 'sent_at'),
    )
    
    def __repr__(self) -> str:
        return f"<Notification(id={self.id}, old_price={self.old_price}, new_price={self.new_price}, status={self.delivery_status})>"
