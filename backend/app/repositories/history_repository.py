"""
Repository for price history database operations.
"""
from typing import List, Optional
from uuid import UUID
from datetime import datetime
from sqlalchemy.orm import Session
from sqlalchemy import select

from app.models.price_history import PriceHistory
from app.core.logging import get_logger

logger = get_logger(__name__)


class HistoryRepository:
    """Repository for managing price history in the database."""
    
    def __init__(self, db: Session):
        """
        Initialize repository with database session.
        
        Args:
            db: SQLAlchemy database session
        """
        self.db = db
    
    def create_price_history_entry(
        self,
        tracked_product_id: UUID,
        price: float,
        checked_at: datetime = None
    ) -> PriceHistory:
        """
        Create a new price history entry.
        
        Args:
            tracked_product_id: ID of the tracked product
            price: Price at the time of check
            checked_at: Optional timestamp (defaults to current time)
            
        Returns:
            Created PriceHistory instance
        """
        price_entry = PriceHistory(
            tracked_product_id=tracked_product_id,
            price=price,
            checked_at=checked_at or datetime.utcnow()
        )
        
        self.db.add(price_entry)
        self.db.commit()
        self.db.refresh(price_entry)
        
        logger.info(
            f"Created price history entry for product {tracked_product_id}: {price}",
            extra={
                "product_id": str(tracked_product_id),
                "price": price,
                "checked_at": price_entry.checked_at.isoformat()
            }
        )
        
        return price_entry
    
    def get_price_history(
        self,
        tracked_product_id: UUID,
        limit: int = None
    ) -> List[PriceHistory]:
        """
        Get price history for a tracked product.
        
        Args:
            tracked_product_id: ID of the tracked product
            limit: Optional limit on number of entries to return
            
        Returns:
            List of PriceHistory instances ordered by checked_at descending
        """
        query = select(PriceHistory).where(
            PriceHistory.tracked_product_id == tracked_product_id
        ).order_by(PriceHistory.checked_at.desc())
        
        if limit:
            query = query.limit(limit)
        
        result = self.db.execute(query)
        return list(result.scalars().all())
    
    def get_latest_price_entry(
        self,
        tracked_product_id: UUID
    ) -> Optional[PriceHistory]:
        """
        Get the most recent price history entry for a tracked product.
        
        Args:
            tracked_product_id: ID of the tracked product
            
        Returns:
            Most recent PriceHistory instance or None if no history exists
        """
        query = select(PriceHistory).where(
            PriceHistory.tracked_product_id == tracked_product_id
        ).order_by(PriceHistory.checked_at.desc()).limit(1)
        
        result = self.db.execute(query)
        return result.scalar_one_or_none()
    
    def delete_price_history(
        self,
        tracked_product_id: UUID
    ) -> int:
        """
        Delete all price history entries for a tracked product.
        This is typically called when a tracked product is deleted (cascade).
        
        Args:
            tracked_product_id: ID of the tracked product
            
        Returns:
            Number of entries deleted
        """
        query = select(PriceHistory).where(
            PriceHistory.tracked_product_id == tracked_product_id
        )
        
        result = self.db.execute(query)
        entries = result.scalars().all()
        count = len(entries)
        
        for entry in entries:
            self.db.delete(entry)
        
        self.db.commit()
        
        logger.info(
            f"Deleted {count} price history entries for product {tracked_product_id}",
            extra={"product_id": str(tracked_product_id), "count": count}
        )
        
        return count
