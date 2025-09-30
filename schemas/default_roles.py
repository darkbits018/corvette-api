# sc-siem-corvette/schemas/default_roles.py
from schemas.role import RoleCreate
from utils.permissions import Permissions

# Define default roles to be used for seeding the database or for reference.

# Admin Role: Full access, including the ability to create custom roles.
admin_role = RoleCreate(
    name="Admin",
    description="Full access to manage users, indices, IPs, alerts; view all logs/analytics.",
    permissions={
        Permissions.CAN_MANAGE_USERS: True,
        Permissions.CAN_MANAGE_ROLES: True,
        Permissions.CAN_MANAGE_INDICES: True,
        Permissions.CAN_MANAGE_IPS: True,
        Permissions.CAN_SETUP_ALERTS: True,
        Permissions.CAN_VIEW_ALL_LOGS: True,
        Permissions.CAN_VIEW_ANALYTICS: True,
        Permissions.CAN_VIEW_ALERTS: True,
        Permissions.CAN_GENERATE_REPORTS: True,
    }
)

# User Role: Standard user with multi-tenant access
user_role = RoleCreate(
    name="User",
    description="Monitor logs, analytics, alerts for assigned client_id (multi-tenant).",
    permissions={
        Permissions.CAN_VIEW_LOGS: True,
        Permissions.CAN_VIEW_ANALYTICS: True,
        Permissions.CAN_VIEW_ALERTS: True,
    }
)

# A list containing all default roles, which can be iterated over.
# Admins can create additional custom roles with flexible permissions using the API.
default_roles = [admin_role, user_role]
