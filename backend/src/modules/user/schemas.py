from pydantic import BaseModel, EmailStr, Field
from typing import Optional
from datetime import datetime

class UserRegisterRequest(BaseModel):
    username: str = Field(..., min_length=3, max_length=256)
    email: EmailStr
    password: str = Field(..., min_length=8)
    first_name: str = Field(..., min_length=1, max_length=128)
    last_name: Optional[str] = None

class UserLoginRequest(BaseModel):
    username: str
    password: str

class UserResponse(BaseModel):
    id: int
    username: str
    email: str
    first_name: str
    last_name: Optional[str]
    active_or_archive: bool
    email_confirmed: bool
    primary_role_id: Optional[int]
    primary_role_name: Optional[str] = None
    created_at: datetime

    class Config:
        from_attributes = True

class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
    user: UserResponse

class RoleResponse(BaseModel):
    id: int
    name: str
    description: Optional[str]
    is_active: bool
    display_sequence: Optional[int]

    class Config:
        from_attributes = True

class UserRoleAssignRequest(BaseModel):
    user_id: int
    role_id: int
    expiry_date: Optional[datetime] = None
