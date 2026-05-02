"""
Authentication API endpoints.
"""
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from pydantic import BaseModel
from google.oauth2 import id_token
from google.auth.transport import requests as google_requests

from app.core.database import get_db
from app.dependencies import get_current_user_id
from app.services.auth_service import AuthService
from app.schemas.auth import UserRegister, UserLogin, UserResponse
from app.core.exceptions import AuthenticationError, ValidationError
from app.core.logging import get_logger

logger = get_logger(__name__)

router = APIRouter()


class GoogleAuthRequest(BaseModel):
    """Google OAuth token request"""
    token: str


@router.post("/register", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
async def register(
    user_data: UserRegister,
    db: Session = Depends(get_db)
):
    """
    Register a new user.
    
    - **email**: Valid email address
    - **password**: Minimum 8 characters
    
    Returns user information and JWT token.
    """
    try:
        auth_service = AuthService(db)
        return auth_service.register_user(user_data)
    except ValidationError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail={"message": e.message, "field": e.field}
        )


@router.post("/login", response_model=UserResponse)
async def login(
    login_data: UserLogin,
    db: Session = Depends(get_db)
):
    """
    Login with email and password.
    
    - **email**: User's email address
    - **password**: User's password
    
    Returns user information and JWT token.
    """
    try:
        auth_service = AuthService(db)
        return auth_service.login_user(login_data)
    except AuthenticationError as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=e.message
        )


@router.get("/me", response_model=UserResponse)
async def get_current_user(
    user_id: str = Depends(get_current_user_id),
    db: Session = Depends(get_db)
):
    """
    Get current user information.
    Requires authentication token.
    
    Returns user information based on JWT token.
    """
    from app.repositories.user_repository import UserRepository
    
    user_repo = UserRepository(db)
    user = user_repo.get_user_by_id(user_id)
    
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    
    return UserResponse(
        user_id=str(user.id),
        email=user.email,
        token=""  # No new token needed for /me endpoint
    )


@router.post("/google", response_model=UserResponse)
async def google_auth(
    auth_request: GoogleAuthRequest,
    db: Session = Depends(get_db)
):
    """
    Authenticate with Google OAuth.
    
    - **token**: Google ID token from frontend
    
    Returns user information and JWT token.
    """
    error_details = []
    
    try:
        from app.config import settings
        
        # Check if Client ID is configured
        if not settings.GOOGLE_CLIENT_ID:
            error_details.append("GOOGLE_CLIENT_ID not configured")
            raise ValueError("GOOGLE_CLIENT_ID not set")
        
        error_details.append(f"Client ID configured: {settings.GOOGLE_CLIENT_ID[:20]}...")
        
        # Verify the Google token with our Client ID
        try:
            idinfo = id_token.verify_oauth2_token(
                auth_request.token,
                google_requests.Request(),
                settings.GOOGLE_CLIENT_ID
            )
            error_details.append("Token verified successfully")
        except Exception as verify_error:
            error_details.append(f"Token verification failed: {type(verify_error).__name__}: {str(verify_error)}")
            raise
        
        # Get user email from Google token
        email = idinfo.get('email')
        if not email:
            error_details.append("No email in token")
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail={"error": "Email not found in Google token", "debug": error_details}
            )
        
        error_details.append(f"Email extracted: {email}")
        
        # Check if user exists, if not create one
        from app.repositories.user_repository import UserRepository
        from app.models.user import User
        from app.core.security import create_access_token
        import uuid
        
        user_repo = UserRepository(db)
        user = user_repo.get_user_by_email(email)
        
        if not user:
            error_details.append("Creating new user")
            # Create new user with Google email
            user = User(
                id=uuid.uuid4(),
                email=email,
                password_hash=""  # No password for Google OAuth users
            )
            db.add(user)
            db.commit()
            db.refresh(user)
            error_details.append("User created successfully")
        else:
            error_details.append("Existing user found")
        
        # Generate JWT token
        token = create_access_token({"sub": str(user.id)})
        error_details.append("JWT token generated")
        
        return UserResponse(
            user_id=str(user.id),
            email=user.email,
            token=token
        )
        
    except HTTPException:
        raise
    except Exception as e:
        error_msg = f"{type(e).__name__}: {str(e)}"
        error_details.append(f"Final error: {error_msg}")
        logger.error(f"Google auth error: {error_msg}", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail={"error": error_msg, "debug": error_details}
        )
