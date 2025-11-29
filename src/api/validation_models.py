"""
Validation models for organization and user management
Based on B2B SaaS transformation strategy
"""
from pydantic import BaseModel, EmailStr, field_validator
from typing import Optional
from src.database.models import RoleEnum, SubscriptionTier


class OrganizationCreateRequest(BaseModel):
    name: str
    owner_email: EmailStr
    owner_password: str
    billing_email: Optional[EmailStr] = None
    tier: Optional[SubscriptionTier] = SubscriptionTier.STARTER
    
    @field_validator('name')
    @classmethod
    def validate_name(cls, v):
        if not v or len(v.strip()) < 3:
            raise ValueError('Organization name must be at least 3 characters')
        return v.strip()


class OrganizationUpdateRequest(BaseModel):
    name: Optional[str] = None
    billing_email: Optional[EmailStr] = None
    tier: Optional[SubscriptionTier] = None
    
    @field_validator('name')
    @classmethod
    def validate_name(cls, v):
        if v is not None and (not v or len(v.strip()) < 3):
            raise ValueError('Organization name must be at least 3 characters')
        return v.strip() if v else v


class UserCreateRequest(BaseModel):
    email: EmailStr
    password: str
    username: Optional[str] = None
    role: Optional[RoleEnum] = RoleEnum.MEMBER
    
    @field_validator('password')
    @classmethod
    def validate_password(cls, v):
        if len(v) < 8:
            raise ValueError('Password must be at least 8 characters')
        return v


class UserUpdateRequest(BaseModel):
    role: Optional[RoleEnum] = None
    is_active: Optional[bool] = None
    username: Optional[str] = None