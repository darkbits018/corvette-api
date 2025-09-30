# W:/pyProjects/sc-siem-corvette/utils/permissions.py
from enum import Enum


class Permissions(str, Enum):
    """
    Enumeration of all available permissions in the system.
    Using an Enum provides a single source of truth and prevents typos.
    """
    # User & Role Management
    CAN_MANAGE_USERS = "can_manage_users"
    CAN_MANAGE_ROLES = "can_manage_roles"

    # Data & Log Management
    CAN_MANAGE_INDICES = "can_manage_indices"
    CAN_MANAGE_IPS = "can_manage_ips"
    CAN_VIEW_ALL_LOGS = "can_view_all_logs"
    CAN_VIEW_LOGS = "can_view_logs" # For regular users, potentially restricted

    # Alerting
    CAN_SETUP_ALERTS = "can_setup_alerts"
    CAN_VIEW_ALERTS = "can_view_alerts"

    # Analytics & Reporting
    CAN_VIEW_DASHBOARD = "can_view_dashboard"
    CAN_VIEW_ANALYTICS = "can_view_analytics"
    CAN_GENERATE_REPORTS = "can_generate_reports"
