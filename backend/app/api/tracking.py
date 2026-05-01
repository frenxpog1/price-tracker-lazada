"""
API endpoints for product tracking.
"""
from typing import List
from uuid import UUID
from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from app.dependencies import get_db, get_current_user_id
from app.services.tracking_service import TrackingService
from app.schemas.tracking import (
    TrackedProductCreate,
    TrackedProductResponse,
    ThresholdUpdate
)
from app.core.logging import get_logger

logger = get_logger(__name__)

router = APIRouter()


@router.post(
    "/products",
    response_model=TrackedProductResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Track a new product",
    description="Start tracking a product for price changes"
)
async def create_tracked_product(
    product_data: TrackedProductCreate,
    user_id: UUID = Depends(get_current_user_id),
    db: Session = Depends(get_db)
) -> TrackedProductResponse:
    """
    Create a new tracked product for the authenticated user.
    
    Args:
        product_data: Product tracking data
        user_id: Authenticated user ID (from JWT token)
        db: Database session
        
    Returns:
        Created tracked product data
    """
    tracking_service = TrackingService(db)
    
    logger.info(
        f"User {user_id} creating tracked product: {product_data.product_name}",
        extra={"user_id": str(user_id), "platform": product_data.platform}
    )
    
    return tracking_service.create_tracked_product(user_id, product_data)


@router.get(
    "/products",
    response_model=List[TrackedProductResponse],
    summary="Get tracked products",
    description="Get all products tracked by the authenticated user"
)
async def get_tracked_products(
    user_id: UUID = Depends(get_current_user_id),
    db: Session = Depends(get_db)
) -> List[TrackedProductResponse]:
    """
    Get all tracked products for the authenticated user.
    
    Args:
        user_id: Authenticated user ID (from JWT token)
        db: Database session
        
    Returns:
        List of tracked products
    """
    tracking_service = TrackingService(db)
    
    logger.info(
        f"User {user_id} retrieving tracked products",
        extra={"user_id": str(user_id)}
    )
    
    return tracking_service.get_user_tracked_products(user_id)


@router.get(
    "/products/{product_id}",
    response_model=TrackedProductResponse,
    summary="Get tracked product",
    description="Get a specific tracked product by ID"
)
async def get_tracked_product(
    product_id: UUID,
    user_id: UUID = Depends(get_current_user_id),
    db: Session = Depends(get_db)
) -> TrackedProductResponse:
    """
    Get a specific tracked product for the authenticated user.
    
    Args:
        product_id: ID of the tracked product
        user_id: Authenticated user ID (from JWT token)
        db: Database session
        
    Returns:
        Tracked product data
    """
    tracking_service = TrackingService(db)
    
    logger.info(
        f"User {user_id} retrieving tracked product {product_id}",
        extra={"user_id": str(user_id), "product_id": str(product_id)}
    )
    
    return tracking_service.get_tracked_product(product_id, user_id)


@router.patch(
    "/products/{product_id}/threshold",
    response_model=TrackedProductResponse,
    summary="Update price threshold",
    description="Update the price threshold for a tracked product"
)
async def update_threshold(
    product_id: UUID,
    threshold_data: ThresholdUpdate,
    user_id: UUID = Depends(get_current_user_id),
    db: Session = Depends(get_db)
) -> TrackedProductResponse:
    """
    Update the price threshold for a tracked product.
    
    Args:
        product_id: ID of the tracked product
        threshold_data: New threshold data
        user_id: Authenticated user ID (from JWT token)
        db: Database session
        
    Returns:
        Updated tracked product data
    """
    tracking_service = TrackingService(db)
    
    logger.info(
        f"User {user_id} updating threshold for product {product_id}",
        extra={
            "user_id": str(user_id),
            "product_id": str(product_id),
            "new_threshold": float(threshold_data.price_threshold)
        }
    )
    
    return tracking_service.update_threshold(product_id, user_id, threshold_data)


@router.delete(
    "/products/{product_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Delete tracked product",
    description="Stop tracking a product"
)
async def delete_tracked_product(
    product_id: UUID,
    user_id: UUID = Depends(get_current_user_id),
    db: Session = Depends(get_db)
) -> None:
    """
    Delete a tracked product.
    
    Args:
        product_id: ID of the tracked product
        user_id: Authenticated user ID (from JWT token)
        db: Database session
    """
    tracking_service = TrackingService(db)
    
    logger.info(
        f"User {user_id} deleting tracked product {product_id}",
        extra={"user_id": str(user_id), "product_id": str(product_id)}
    )
    
    tracking_service.delete_tracked_product(product_id, user_id)
