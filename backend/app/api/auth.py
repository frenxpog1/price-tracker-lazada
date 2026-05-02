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
    try:
        from app.config import settings
        
        logger.info(f"Google OAuth attempt - Client ID configured: {bool(settings.GOOGLE_CLIENT_ID)}")
        
        # Verify the Google token with our Client ID
        try:
            idinfo = id_token.verify_oauth2_token(
                auth_request.token,
                google_requests.Request(),
                settings.GOOGLE_CLIENT_ID
            )
            logger.info("Google token verified successfully")
        except Exception as verify_error:
            logger.error(f"Token verification failed: {type(verify_error).__name__}: {str(verify_error)}")
            raise
        
        # Get user email from Google token
        email = idinfo.get('email')
        if not email:
            logger.error("No email in Google token")
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Email not found in Google token"
            )
        
        logger.info(f"Google OAuth for email: {email}")
        
        # Check if user exists, if not create one
        from app.repositories.user_repository import UserRepository
        from app.models.user import User
        from app.core.security import create_access_token
        import uuid
        
        user_repo = UserRepository(db)
        user = user_repo.get_user_by_email(email)
        
        if not user:
            logger.info(f"Creating new user for: {email}")
            # Create new user with Google email
            user = User(
                id=uuid.uuid4(),
                email=email,
                password_hash=""  # No password for Google OAuth users
            )
            db.add(user)
            db.commit()
            db.refresh(user)
            logger.info(f"Created new user via Google OAuth: {email}")
        else:
            logger.info(f"Existing user found: {email}")
        
        # Generate JWT token
        token = create_access_token({"sub": str(user.id)})
        
        logger.info(f"Google OAuth successful for: {email}")
        
        return UserResponse(
            user_id=str(user.id),
            email=user.email,
            token=token
        )
        
    except ValueError as e:
        # Invalid token
        logger.error(f"Invalid Google token - ValueError: {str(e)}", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=f"Invalid Google token: {str(e)}"
        )
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Google auth error - {type(e).__name__}: {str(e)}", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Authentication failed: {type(e).__name__}: {str(e)}"
        )
