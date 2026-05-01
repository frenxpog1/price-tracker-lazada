"""
Repository for tracked product database operations.
"""
from typing import List, Optional
from uuid import UUID
from sqlalchemy.orm import Session
from sqlalchemy import select

from app.models.tracked_product import TrackedProduct
from app.core.logging import get_logger

logger = get_logger(__name__)


class ProductRepository:
    """Repository for managing tracked products in the database."""
    
    def __init__(self, db: Session):
        """
        Initialize repository with database session.
        
        Args:
            db: SQLAlchemy database session
        """
        self.db = db
    
    def create_tracked_product(
        self,
        user_id: UUID,
        platform: str,
        product_name: str,
        product_url: str,
        current_price: float,
        price_threshold: float,
        currency: str = "PHP",
        image_url: Optional[str] = None
    ) -> TrackedProduct:
        """
        Create a new tracked product.
        
        Args:
            user_id: ID of the user tracking the product
            platform: E-commerce platform (lazada, shopee, tiktokshop)
            product_name: Name of the product
            product_url: URL to the product page
            current_price: Current price of the product
            price_threshold: Target price for notifications
            currency: Currency code (default: PHP)
            image_url: Optional URL to product image
            
        Returns:
            Created TrackedProduct instance
        """
        tracked_product = TrackedProduct(
            user_id=user_id,
            platform=platform,
            product_name=product_name,
            product_url=product_url,
            current_price=current_price,
            price_threshold=price_threshold,
            currency=currency,
            image_url=image_url
        )
        
        self.db.add(tracked_product)
        self.db.commit()
        self.db.refresh(tracked_product)
        
        logger.info(
            f"Created tracked product: {tracked_product.id} for user {user_id}",
            extra={"product_id": str(tracked_product.id), "user_id": str(user_id)}
        )
        
        return tracked_product
    
    def get_tracked_product_by_id(
        self,
        product_id: UUID,
        user_id: Optional[UUID] = None
    ) -> Optional[TrackedProduct]:
        """
        Get a tracked product by ID, optionally scoped to a user.
        
        Args:
            product_id: ID of the tracked product
            user_id: Optional user ID to scope the query
            
        Returns:
            TrackedProduct instance or None if not found
        """
        query = select(TrackedProduct).where(TrackedProduct.id == product_id)
        
        if user_id:
            query = query.where(TrackedProduct.user_id == user_id)
        
        result = self.db.execute(query)
        return result.scalar_one_or_none()
    
    def get_user_tracked_products(self, user_id: UUID) -> List[TrackedProduct]:
        """
        Get all tracked products for a specific user.
        
        Args:
            user_id: ID of the user
            
        Returns:
            List of TrackedProduct instances
        """
        query = select(TrackedProduct).where(
            TrackedProduct.user_id == user_id
        ).order_by(TrackedProduct.created_at.desc())
        
        result = self.db.execute(query)
        return list(result.scalars().all())
    
    def get_all_tracked_products(self) -> List[TrackedProduct]:
        """
        Get all tracked products across all users.
        Used by background tasks for price monitoring.
        
        Returns:
            List of all TrackedProduct instances
        """
        query = select(TrackedProduct).order_by(TrackedProduct.last_checked.asc())
        result = self.db.execute(query)
        return list(result.scalars().all())
    
    def update_tracked_product_price(
        self,
        product_id: UUID,
        new_price: float
    ) -> Optional[TrackedProduct]:
        """
        Update the current price of a tracked product.
        
        Args:
            product_id: ID of the tracked product
            new_price: New current price
            
        Returns:
            Updated TrackedProduct instance or None if not found
        """
        tracked_product = self.get_tracked_product_by_id(product_id)
        
        if not tracked_product:
            logger.warning(f"Tracked product not found: {product_id}")
            return None
        
        tracked_product.current_price = new_price
        self.db.commit()
        self.db.refresh(tracked_product)
        
        logger.info(
            f"Updated price for product {product_id}: {new_price}",
            extra={"product_id": str(product_id), "new_price": new_price}
        )
        
        return tracked_product
    
    def update_price_threshold(
        self,
        product_id: UUID,
        user_id: UUID,
        new_threshold: float
    ) -> Optional[TrackedProduct]:
        """
        Update the price threshold for a tracked product.
        User-scoped to ensure users can only update their own products.
        
        Args:
            product_id: ID of the tracked product
            user_id: ID of the user (for authorization)
            new_threshold: New price threshold
            
        Returns:
            Updated TrackedProduct instance or None if not found
        """
        tracked_product = self.get_tracked_product_by_id(product_id, user_id)
        
        if not tracked_product:
            logger.warning(
                f"Tracked product not found or unauthorized: {product_id}",
                extra={"product_id": str(product_id), "user_id": str(user_id)}
            )
            return None
        
        old_threshold = tracked_product.price_threshold
        tracked_product.price_threshold = new_threshold
        self.db.commit()
        self.db.refresh(tracked_product)
        
        logger.info(
            f"Updated threshold for product {product_id}: {old_threshold} -> {new_threshold}",
            extra={
                "product_id": str(product_id),
                "old_threshold": float(old_threshold),
                "new_threshold": new_threshold
            }
        )
        
        return tracked_product
    
    def delete_tracked_product(
        self,
        product_id: UUID,
        user_id: UUID
    ) -> bool:
        """
        Delete a tracked product.
        User-scoped to ensure users can only delete their own products.
        
        Args:
            product_id: ID of the tracked product
            user_id: ID of the user (for authorization)
            
        Returns:
            True if deleted, False if not found or unauthorized
        """
        tracked_product = self.get_tracked_product_by_id(product_id, user_id)
        
        if not tracked_product:
            logger.warning(
                f"Tracked product not found or unauthorized for deletion: {product_id}",
                extra={"product_id": str(product_id), "user_id": str(user_id)}
            )
            return False
        
        self.db.delete(tracked_product)
        self.db.commit()
        
        logger.info(
            f"Deleted tracked product: {product_id}",
            extra={"product_id": str(product_id), "user_id": str(user_id)}
        )
        
        return True
