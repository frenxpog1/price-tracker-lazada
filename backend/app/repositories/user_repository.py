"""
User repository for database operations.
"""
from typing import Optional
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError

from app.models.user import User
from app.core.exceptions import DatabaseError, ValidationError


class UserRepository:
    """Repository for user database operations."""
    
    def __init__(self, db: Session):
        self.db = db
    
    def create_user(self, email: str, password_hash: str) -> User:
        """
        Create a new user.
        
        Args:
            email: User's email address
            password_hash: Hashed password
        
        Returns:
            Created user object
        
        Raises:
            ValidationError: If email already exists
            DatabaseError: If database operation fails
        """
        try:
            user = User(email=email, password_hash=password_hash)
            self.db.add(user)
            self.db.commit()
            self.db.refresh(user)
            return user
        except IntegrityError:
            self.db.rollback()
            raise ValidationError("Email already registered", field="email")
        except Exception as e:
            self.db.rollback()
            raise DatabaseError(f"Failed to create user: {str(e)}")
    
    def get_user_by_email(self, email: str) -> Optional[User]:
        """
        Get user by email address.
        
        Args:
            email: User's email address
        
        Returns:
            User object if found, None otherwise
        """
        return self.db.query(User).filter(User.email == email).first()
    
    def get_user_by_id(self, user_id: str) -> Optional[User]:
        """
        Get user by ID.
        
        Args:
            user_id: User's unique identifier
        
        Returns:
            User object if found, None otherwise
        """
        return self.db.query(User).filter(User.id == user_id).first()
    
    def update_user_email(self, user_id: str, new_email: str) -> Optional[User]:
        """
        Update user's email address.
        
        Args:
            user_id: User's unique identifier
            new_email: New email address
        
        Returns:
            Updated user object if found, None otherwise
        
        Raises:
            ValidationError: If new email already exists
            DatabaseError: If database operation fails
        """
        try:
            user = self.get_user_by_id(user_id)
            if not user:
                return None
            
            user.email = new_email
            self.db.commit()
            self.db.refresh(user)
            return user
        except IntegrityError:
            self.db.rollback()
            raise ValidationError("Email already in use", field="email")
        except Exception as e:
            self.db.rollback()
            raise DatabaseError(f"Failed to update email: {str(e)}")
