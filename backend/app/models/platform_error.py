"""
PlatformError model for logging scraping errors and platform issues.
"""
from sqlalchemy import Column, String, Text, DateTime, Index
from sqlalchemy.dialects.postgresql import UUID
from datetime import datetime
import uuid

from app.core.database import Base


class PlatformError(Base):
    """
    PlatformError model representing errors encountered when scraping platforms.
    
    Attributes:
        id: Unique error identifier (UUID)
        platform: Platform name (lazada, shopee, tiktok)
        error_type: Type of error (connection, timeout, parsing, etc.)
        error_message: Detailed error message
        occurred_at: Timestamp when error occurred
    """
    __tablename__ = "platform_errors"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    platform = Column(String(50), nullable=False)
    error_type = Column(String(100), nullable=False)
    error_message = Column(Text)
    occurred_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    
    # Indexes for performance
    __table_args__ = (
        Index('idx_platform_errors_occurred_at', 'occurred_at'),
        Index('idx_platform_errors_platform', 'platform'),
    )
    
    def __repr__(self) -> str:
        return f"<PlatformError(id={self.id}, platform={self.platform}, error_type={self.error_type})>"
