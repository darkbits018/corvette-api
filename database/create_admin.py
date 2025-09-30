# sc-siem-corvette/database/create_admin.py
import sys
import os

# Add the project root to the Python path to allow for module imports
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from database.database import Base, engine, SessionLocal
from models.user import User
from models.role import Role
from schemas.default_roles import default_roles  # Import the list of default roles

def create_initial_data():
    """
    Initializes the database by creating tables and seeding it with default roles
    and an admin user. This script is non-destructive and safe to run multiple times.
    It will only add data that is missing.
    """
    db = SessionLocal()

    try:
        print("Creating tables if they don't exist...")
        # This command is non-destructive and will only create missing tables.
        Base.metadata.create_all(bind=engine)
        print("Tables checked/created.")

        # --- Seed Roles ---
        for role_schema in default_roles:
            db_role = db.query(Role).filter(Role.name == role_schema.name).first()
            if not db_role:
                print(f"Creating role: '{role_schema.name}'...")
                # Convert enum keys to string values for JSON serialization
                permissions_dict = {p.value: v for p, v in role_schema.permissions.items()}
                new_role = Role(
                    name=role_schema.name,
                    description=role_schema.description,
                    permissions=permissions_dict
                )
                db.add(new_role)
                print(f"Role '{role_schema.name}' created.")
            else:
                print(f"Role '{role_schema.name}' already exists. Skipping.")
        
        db.commit() # Commit roles before creating user

        # --- Seed Admin User ---
        admin_username = "admin"
        db_admin_user = db.query(User).filter(User.username == admin_username).first()
        if not db_admin_user:
            print(f"Creating admin user: '{admin_username}'...")
            # Fetch the admin role that should now exist
            admin_role_db = db.query(Role).filter(Role.name == "Admin").first()
            if not admin_role_db:
                # This should not happen if the roles loop ran correctly
                print("CRITICAL: Admin role not found after seeding. Cannot create admin user.")
                return

            admin_user = User(
                username=admin_username,
                email="admin@example.com",
                role_id=admin_role_db.id,
                is_active=True
            )
            admin_user.set_password("admin")  # Set default password
            db.add(admin_user)
            db.commit()
            print("Admin user created with username 'admin' and password 'admin'.")
        else:
            print(f"Admin user '{admin_username}' already exists. Skipping.")

    finally:
        db.close()

if __name__ == "__main__":
    print("Starting database seeding...")
    create_initial_data()
    print("Database seeding complete.")
