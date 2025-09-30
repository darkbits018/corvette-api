# sc-siem-corvette/services/role_service.py (or utils/role_utils.py)
from models.role import Role
from typing import Dict, Any


def has_permission(role: Role, permission_name: str) -> bool:
    """
    Checks if a role object has a specific permission.
    Assumes permissions are stored in a dictionary-like structure (e.g., JSON).
    """
    # Ensure permissions is a dict (handles potential JSON string or None)
    perms = role.permissions if isinstance(role.permissions, dict) else {}
    return perms.get(permission_name, False)


def set_permission(role: Role, permission_name: str, value: bool):
    """
    Sets the value of a specific permission for a role object.
    """
    if not isinstance(role.permissions, dict):
        role.permissions = {}
    role.permissions[permission_name] = value


def get_permissions(role: Role) -> Dict[str, Any]:
    """
    Returns the dictionary of permissions for a role object.
    """
    return role.permissions if isinstance(role.permissions, dict) else {}

# You could also add functions here to create default roles if needed
# def create_default_roles(db_session): ...
