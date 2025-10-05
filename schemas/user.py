from pydantic import BaseModel, Field, EmailStr
from datetime import datetime
from typing import Optional

class UserBase(BaseModel):
    email: EmailStr = Field(..., description="Email address")
    full_name: Optional[str] = Field(None, max_length=100, description="Full name")

class UserCreate(UserBase):
    password: str = Field(..., min_length=6, max_length=72, description="Password (max 72 characters)")

class UserUpdate(BaseModel):
    email: Optional[EmailStr] = None
    full_name: Optional[str] = Field(None, max_length=100)
    is_active: Optional[bool] = None

class UserResponse(UserBase):
    id: int
    is_active: bool
    is_superuser: bool
    provider: str
    avatar_url: Optional[str] = None
    created_at: datetime
    updated_at: Optional[datetime] = None
    
    class Config:
        from_attributes = True

class UserInDB(UserResponse):
    hashed_password: str

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    email: Optional[str] = None

class UserLogin(BaseModel):
    email: EmailStr = Field(..., description="Email address")
    password: str = Field(..., max_length=72, description="Password (max 72 characters)")

class GoogleUserInfo(BaseModel):
    id: str
    email: str
    name: str
    picture: Optional[str] = None
    verified_email: bool = True

class GoogleAuthResponse(BaseModel):
    access_token: str
    token_type: str
    user: UserResponse
