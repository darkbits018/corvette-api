# sc-siem-corvette/schemas/role.py
from pydantic import BaseModel, Field
from typing import Optional, Dict
from utils.permissions import Permissions


# --- Schemas for Request Data (Input Validation) ---

class RoleCreate(BaseModel):
    """
    Schema for creating a new role.
    Used for request validation when an admin defines a new role.
    Permissions are provided as a dictionary.
    """
    name: str = Field(..., min_length=1, description="Unique name for the role")
    description: Optional[str] = Field(None, description="Description of the role's purpose")
    # Permissions are provided as a dictionary/object
    # Example: {"can_view_logs": true, "can_manage_users": false}
    permissions: Dict[Permissions, bool] = Field(
        default_factory=dict,
        description="Dictionary of permission names and their boolean values. Only defined permissions are allowed."
    )


class RoleUpdate(BaseModel):
    """
    Schema for updating an existing role.
    Used for request validation when an admin modifies a role.
    Fields are optional as not all might be updated at once.
    Name is typically not updated to maintain references.
    """
    # name: Optional[str] = Field(None, min_length=1) # Usually not changed
    description: Optional[str] = Field(None, description="Updated description of the role")
    # Permissions can be updated. Sending an empty dict or omitting it
    # means no change to existing permissions.
    permissions: Optional[Dict[Permissions, bool]] = Field(
        None,
        description="Dictionary of permission names and their new boolean values. Omit or send {} for no change. Only defined permissions are allowed."
    )


# --- Schemas for Response Data (Output Serialization) ---

class RoleBase(BaseModel):
    """
    Base schema containing common role fields for responses.
    """
    id: int
    name: str
    description: Optional[str] = None

    class Config:
        from_attributes = True  # For SQLAlchemy model serialization


class RoleResponse(RoleBase):
    """
    Schema for returning role data in responses.
    Includes the full set of permissions associated with the role.
    """
    # Return permissions as a dictionary
    permissions: Dict[Permissions, bool] = Field(
        default_factory=dict,
        description="Dictionary of permission names and their boolean values for this role."
    )

    class Config:
        from_attributes = True

# Optional: Schema for role details in user responses (avoids circular refs if needed)
# This might be defined in schemas/user.py or here if needed elsewhere
# class RoleInUserResponse(BaseModel):
#     id: int
#     name: str
#     description: Optional[str] = None
#     # Potentially include a subset of permissions if needed in user context?
#     # permissions_summary: List[str] = [] # e.g., list of permission names they have
#     class Config:
#         from_attributes = True
