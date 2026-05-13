"""
Dependency injection utilities for FastAPI.
Provides common dependencies used across API endpoints.
"""
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.orm import Session
from typing import Optional

from app.core.database import get_db
from app.core.exceptions import AuthenticationError, AuthorizationError


# HTTP Bearer token security scheme
security = HTTPBearer(auto_error=False)


async def get_current_user_id(
    credentials: HTTPAuthorizationCredentials = Depends(security),
    db: Session = Depends(get_db)
) -> str:
    """
    Extract and validate user ID from JWT token.
    
    Args:
        credentials: HTTP Bearer token from Authorization header
        db: Database session
    
    Returns:
        User ID extracted from valid token
    
    Raises:
        HTTPException: If token is invalid or expired
    """
    from app.core.security import decode_access_token
    from app.services.auth_service import AuthService
    
    if not credentials:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Not authenticated"
        )
    
    # Decode token
    user_id = decode_access_token(credentials.credentials)
    if not user_id:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired token"
        )
    
    # Verify user exists
    auth_service = AuthService(db)
    try:
        return auth_service.get_current_user_id(user_id)
    except AuthenticationError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User not found"
        )


async def get_optional_current_user_id(
    credentials: Optional[HTTPAuthorizationCredentials] = Depends(security),
    db: Session = Depends(get_db)
) -> Optional[str]:
    """
    Extract user ID from JWT token if present, otherwise return None.
    Useful for endpoints that work with or without authentication.
    
    Args:
        credentials: Optional HTTP Bearer token
    
    Returns:
        User ID if token is valid, None otherwise
    """
    if credentials is None:
        return None
    
    try:
        return await get_current_user_id(credentials, db)
    except HTTPException:
        return None
