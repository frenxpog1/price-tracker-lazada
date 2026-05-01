"""
Service for product tracking business logic.
"""
from typing import List, Optional
from uuid import UUID
from decimal import Decimal
from sqlalchemy.orm import Session

from app.repositories.product_repository import ProductRepository
from app.repositories.history_repository import HistoryRepository
from app.models.tracked_product import TrackedProduct
from app.schemas.tracking import TrackedProductCreate, TrackedProductResponse, ThresholdUpdate
from app.core.exceptions import NotFoundError, ValidationError
from app.core.logging import get_logger

logger = get_logger(__name__)


class TrackingService:
    """Service for managing product tracking operations."""
    
    def __init__(self, db: Session):
        """
        Initialize service with database session.
        
        Args:
            db: SQLAlchemy database session
        """
        self.db = db
        self.product_repo = ProductRepository(db)
        self.history_repo = HistoryRepository(db)
    
    def create_tracked_product(
        self,
        user_id: UUID,
        product_data: TrackedProductCreate
    ) -> TrackedProductResponse:
        """
        Create a new tracked product for a user.
        
        Args:
            user_id: ID of the user tracking the product
            product_data: Product tracking data
            
        Returns:
            TrackedProductResponse with created product data
            
        Raises:
            ValidationError: If product data is invalid
        """
        try:
            # Create tracked product
            tracked_product = self.product_repo.create_tracked_product(
                user_id=user_id,
                platform=product_data.platform,
                product_name=product_data.product_name,
                product_url=product_data.product_url,
                current_price=float(product_data.current_price),
                price_threshold=float(product_data.price_threshold),
                currency=product_data.currency,
                image_url=product_data.image_url
            )
            
            # Create initial price history entry
            self.history_repo.create_price_history_entry(
                tracked_product_id=tracked_product.id,
                price=float(product_data.current_price)
            )
            
            logger.info(
                f"User {user_id} started tracking product: {tracked_product.product_name}",
                extra={
                    "user_id": str(user_id),
                    "product_id": str(tracked_product.id),
                    "platform": product_data.platform
                }
            )
            
            return self._to_response(tracked_product)
            
        except Exception as e:
            logger.error(
                f"Failed to create tracked product for user {user_id}: {str(e)}",
                extra={"user_id": str(user_id), "error": str(e)}
            )
            self.db.rollback()
            raise ValidationError(f"Failed to create tracked product: {str(e)}")
    
    def get_user_tracked_products(
        self,
        user_id: UUID
    ) -> List[TrackedProductResponse]:
        """
        Get all tracked products for a user.
        
        Args:
            user_id: ID of the user
            
        Returns:
            List of TrackedProductResponse instances
        """
        tracked_products = self.product_repo.get_user_tracked_products(user_id)
        
        logger.info(
            f"Retrieved {len(tracked_products)} tracked products for user {user_id}",
            extra={"user_id": str(user_id), "count": len(tracked_products)}
        )
        
        return [self._to_response(product) for product in tracked_products]
    
    def get_tracked_product(
        self,
        product_id: UUID,
        user_id: UUID
    ) -> TrackedProductResponse:
        """
        Get a specific tracked product for a user.
        
        Args:
            product_id: ID of the tracked product
            user_id: ID of the user (for authorization)
            
        Returns:
            TrackedProductResponse
            
        Raises:
            NotFoundError: If product not found or unauthorized
        """
        tracked_product = self.product_repo.get_tracked_product_by_id(
            product_id=product_id,
            user_id=user_id
        )
        
        if not tracked_product:
            raise NotFoundError(f"Tracked product {product_id} not found")
        
        return self._to_response(tracked_product)
    
    def update_threshold(
        self,
        product_id: UUID,
        user_id: UUID,
        threshold_data: ThresholdUpdate
    ) -> TrackedProductResponse:
        """
        Update the price threshold for a tracked product.
        Checks if current price is below new threshold and triggers notification if needed.
        
        Args:
            product_id: ID of the tracked product
            user_id: ID of the user (for authorization)
            threshold_data: New threshold data
            
        Returns:
            Updated TrackedProductResponse
            
        Raises:
            NotFoundError: If product not found or unauthorized
        """
        tracked_product = self.product_repo.update_price_threshold(
            product_id=product_id,
            user_id=user_id,
            new_threshold=float(threshold_data.price_threshold)
        )
        
        if not tracked_product:
            raise NotFoundError(f"Tracked product {product_id} not found")
        
        # Check if current price is below new threshold
        # If so, a notification should be triggered (handled by notification service)
        if tracked_product.current_price and tracked_product.current_price <= tracked_product.price_threshold:
            logger.info(
                f"Price threshold updated and current price is below threshold for product {product_id}",
                extra={
                    "product_id": str(product_id),
                    "current_price": float(tracked_product.current_price),
                    "new_threshold": float(tracked_product.price_threshold)
                }
            )
            # Note: Actual notification sending will be handled by NotificationService
            # when it's implemented in Task 11
        
        logger.info(
            f"Updated threshold for product {product_id} to {threshold_data.price_threshold}",
            extra={
                "product_id": str(product_id),
                "user_id": str(user_id),
                "new_threshold": float(threshold_data.price_threshold)
            }
        )
        
        return self._to_response(tracked_product)
    
    def delete_tracked_product(
        self,
        product_id: UUID,
        user_id: UUID
    ) -> bool:
        """
        Delete a tracked product.
        
        Args:
            product_id: ID of the tracked product
            user_id: ID of the user (for authorization)
            
        Returns:
            True if deleted successfully
            
        Raises:
            NotFoundError: If product not found or unauthorized
        """
        success = self.product_repo.delete_tracked_product(
            product_id=product_id,
            user_id=user_id
        )
        
        if not success:
            raise NotFoundError(f"Tracked product {product_id} not found")
        
        logger.info(
            f"Deleted tracked product {product_id} for user {user_id}",
            extra={"product_id": str(product_id), "user_id": str(user_id)}
        )
        
        return True
    
    def _to_response(self, tracked_product: TrackedProduct) -> TrackedProductResponse:
        """
        Convert TrackedProduct model to response schema.
        
        Args:
            tracked_product: TrackedProduct model instance
            
        Returns:
            TrackedProductResponse
        """
        return TrackedProductResponse(
            id=str(tracked_product.id),
            user_id=str(tracked_product.user_id),
            platform=tracked_product.platform,
            product_url=tracked_product.product_url,
            product_name=tracked_product.product_name,
            current_price=tracked_product.current_price,
            price_threshold=tracked_product.price_threshold,
            currency=tracked_product.currency,
            image_url=tracked_product.image_url,
            last_checked=tracked_product.last_checked,
            created_at=tracked_product.created_at
        )
