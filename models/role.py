# sc-siem-corvette/models/role.py
from sqlalchemy import Column, Integer, String, Text, JSON
from sqlalchemy.orm import relationship
from database.database import Base


class Role(Base):
    """
    Represents a user role within the SIEM application.
    Roles define a set of permissions for users.
    This model is used for Role-Based Access Control (RBAC).
    Permissions are stored flexibly, e.g., as a JSON object.
    """
    __tablename__ = "roles"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True, nullable=False)
    description = Column(Text, nullable=True)
    permissions = Column(JSON, nullable=False, default=dict)

    # Relationship back to users who have this role
    users = relationship("User", back_populates="role", lazy="selectin")

    def __repr__(self):
        return f"<Role(id={self.id}, name='{self.name}')>"

# Consider moving helper methods to services or utils
