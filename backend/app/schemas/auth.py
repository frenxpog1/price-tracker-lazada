"""
Pydantic schemas for authentication requests and responses.
"""
from typing import Optional
from datetime import datetime
from pydantic import BaseModel, EmailStr, Field


class UserRegister(BaseModel):
    """Schema for user registration request."""
    email: EmailStr = Field(..., description="User's email address")
    password: str = Field(..., min_length=8, description="Password (minimum 8 characters)")


class UserLogin(BaseModel):
    """Schema for user login request."""
    email: EmailStr = Field(..., description="User's email address")
    password: str = Field(..., description="User's password")


class UserResponse(BaseModel):
    """Schema for user response (after registration or login)."""
    user_id: str = Field(..., description="Unique user identifier")
    email: str = Field(..., description="User's email address")
    token: str = Field(..., description="JWT access token")


class TokenData(BaseModel):
    """Schema for decoded token data."""
    user_id: Optional[str] = None
