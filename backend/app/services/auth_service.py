"""
Authentication service for user registration and login.
"""
from sqlalchemy.orm import Session

from app.repositories.user_repository import UserRepository
from app.core.security import verify_password, get_password_hash, create_access_token
from app.core.exceptions import AuthenticationError, ValidationError
from app.schemas.auth import UserRegister, UserLogin, UserResponse
from app.core.logging import get_logger

logger = get_logger(__name__)


class AuthService:
    """Service for authentication operations."""
    
    def __init__(self, db: Session):
        self.db = db
        self.user_repo = UserRepository(db)
    
    def register_user(self, user_data: UserRegister) -> UserResponse:
        """
        Register a new user.
        
        Args:
            user_data: User registration data
        
        Returns:
            User response with token
        
        Raises:
            ValidationError: If email already exists or validation fails
        """
        logger.info(f"Registering new user: {user_data.email}")
        
        # Check if user already exists
        existing_user = self.user_repo.get_user_by_email(user_data.email)
        if existing_user:
            logger.warning(f"Registration failed: Email already exists - {user_data.email}")
            raise ValidationError("Email already registered", field="email")
        
        # Hash password
        password_hash = get_password_hash(user_data.password)
        
        # Create user
        user = self.user_repo.create_user(
            email=user_data.email,
            password_hash=password_hash
        )
        
        # Generate token
        token = create_access_token(data={"sub": str(user.id)})
        
        logger.info(f"User registered successfully: {user.email}")
        
        return UserResponse(
            user_id=str(user.id),
            email=user.email,
            token=token
        )
    
    def login_user(self, login_data: UserLogin) -> UserResponse:
        """
        Authenticate user and generate token.
        
        Args:
            login_data: User login credentials
        
        Returns:
            User response with token
        
        Raises:
            AuthenticationError: If credentials are invalid
        """
        logger.info(f"Login attempt for user: {login_data.email}")
        
        # Get user by email
        user = self.user_repo.get_user_by_email(login_data.email)
        if not user:
            logger.warning(f"Login failed: User not found - {login_data.email}")
            raise AuthenticationError("Invalid email or password")
        
        # Verify password
        if not user.password_hash:
            logger.warning(f"Login failed: Account uses OAuth - {login_data.email}")
            raise AuthenticationError("Please log in using Google for this account")
            
        if not verify_password(login_data.password, user.password_hash):
            logger.warning(f"Login failed: Invalid password - {login_data.email}")
            raise AuthenticationError("Invalid email or password")
        
        # Generate token
        token = create_access_token(data={"sub": str(user.id)})
        
        logger.info(f"User logged in successfully: {user.email}")
        
        return UserResponse(
            user_id=str(user.id),
            email=user.email,
            token=token
        )
    
    def get_current_user_id(self, user_id: str) -> str:
        """
        Verify user exists and return user ID.
        
        Args:
            user_id: User's unique identifier
        
        Returns:
            User ID if valid
        
        Raises:
            AuthenticationError: If user not found
        """
        user = self.user_repo.get_user_by_id(user_id)
        if not user:
            raise AuthenticationError("User not found")
        return str(user.id)
