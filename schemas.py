"""Pydantic schemas for request/response validation and type safety."""
from pydantic import BaseModel, EmailStr, Field
from typing import Optional, List
from datetime import datetime
from app.models.user import UserRole

# ============== TOKEN SCHEMAS ==============

class TokenData(BaseModel):
    """Schema for JWT token payload."""
    username: Optional[str] = None

# ============== USER SCHEMAS ==============

class UserBase(BaseModel):
    """Base user schema with common fields."""
    username: str = Field(..., min_length=3, max_length=50)
    email: EmailStr
    full_name: Optional[str] = Field(None, max_length=100)

class UserCreate(UserBase):
    """Schema for user registration with password."""
    password: str = Field(..., min_length=8, max_length=100)

class UserUpdate(BaseModel):
    """Schema for user profile updates."""
    email: Optional[EmailStr] = None
    full_name: Optional[str] = Field(None, max_length=100)
    password: Optional[str] = Field(None, min_length=8, max_length=100)

class UserResponse(UserBase):
    """Schema for user response data."""
    id: int
    role: UserRole
    is_active: bool
    created_at: datetime

    class Config:
        from_attributes = True

# ============== POST SCHEMAS ==============

class PostBase(BaseModel):
    """Base post schema."""
    title: str = Field(..., min_length=1, max_length=200)
    content: Optional[str] = None

class PostCreate(PostBase):
    """Schema for creating a post."""
    pass

class PostUpdate(BaseModel):
    """Schema for updating a post."""
    title: Optional[str] = Field(None, min_length=1, max_length=200)
    content: Optional[str] = None

class PostResponse(PostBase):
    """Schema for post response data."""
    id: int
    created_at: datetime
    owner_id: int

    class Config:
        from_attributes = True

# ============== COMMENT SCHEMAS ==============

class CommentBase(BaseModel):
    """Base comment schema."""
    content: str = Field(..., min_length=1)

class CommentCreate(CommentBase):
    """Schema for creating a comment."""
    post_id: int

class CommentUpdate(BaseModel):
    """Schema for updating a comment."""
    content: Optional[str] = None

class CommentResponse(CommentBase):
    """Schema for comment response data."""
    id: int
    created_at: datetime
    post_id: int
    owner_id: int

    class Config:
        from_attributes = True

# ============== LIKE SCHEMAS ==============

class LikeCreate(BaseModel):
    """Schema for creating a like."""
    post_id: int

class LikeResponse(BaseModel):
    """Schema for like response data."""
    id: int
    post_id: int
    user_id: int

    class Config:
        from_attributes = True