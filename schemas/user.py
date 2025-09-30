# sc-siem-corvette/schemas/user.py
from pydantic import BaseModel, EmailStr, Field
from typing import Optional

# --- Schemas for other modules ---
from .role import RoleResponse


# --- Schemas for Request Data (Input Validation) ---

class UserCreate(BaseModel):
    """
    Schema for creating a new user.
    """
    username: str
    email: EmailStr
    password: str
    role: str  # Role is assigned by name
    client_id: Optional[str] = Field(None, description="Assign a client_id for multi-tenant access control.")


class UserUpdate(BaseModel):
    """
    Schema for updating an existing user.
    """
    username: Optional[str] = None
    email: Optional[EmailStr] = None
    is_active: Optional[bool] = None
    role_id: Optional[int] = None
    client_id: Optional[str] = None


# --- Schemas for Response Data (Output Serialization) ---

class UserBase(BaseModel):
    """
    Base schema containing common user fields for responses.
    """
    id: int
    username: str
    email: EmailStr
    is_active: bool
    role_id: int
    client_id: Optional[str] = None

    class Config:
        from_attributes = True


class UserResponse(UserBase):
    """
    Schema for returning user data in responses, including role details.
    """
    role: RoleResponse

    class Config:
        from_attributes = True
