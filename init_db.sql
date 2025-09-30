-- Seed data for the roles table
-- This script ensures that the default roles are present in the database.

-- The permissions JSON object grants or denies access to specific features.
-- A value of 'true' means the permission is granted.

-- 1. Administrator Role: Has all permissions enabled.
INSERT INTO roles (name, description, permissions)
VALUES (
    'admin',
    'Administrator with full system access',
    '{
        "can_manage_users": true,
        "can_manage_roles": true,
        "can_manage_indices": true,
        "can_manage_ips": true,
        "can_view_all_logs": true,
        "can_view_logs": true,
        "can_setup_alerts": true,
        "can_view_alerts": true,
        "can_view_dashboard": true,
        "can_view_analytics": true,
        "can_generate_reports": true
    }'
) ON CONFLICT (name) DO NOTHING;

-- 2. Standard User Role: Has basic viewing permissions.
INSERT INTO roles (name, description, permissions)
VALUES (
    'user',
    'Standard user with basic data viewing permissions',
    '{
        "can_manage_users": false,
        "can_manage_roles": false,
        "can_manage_indices": false,
        "can_manage_ips": false,
        "can_view_all_logs": false,
        "can_view_logs": true,
        "can_setup_alerts": false,
        "can_view_alerts": true,
        "can_view_dashboard": true,
        "can_view_analytics": false,
        "can_generate_reports": false
    }'
) ON CONFLICT (name) DO NOTHING;
