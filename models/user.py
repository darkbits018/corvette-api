# sc-siem-corvette/models/user.py
from sqlalchemy import Column, Integer, String, Boolean, ForeignKey
from sqlalchemy.orm import relationship
from database.database import Base
from utils.hashing import get_password_hash, verify_password


class User(Base):
    """
    Represents a user in the SIEM application.
    This model stores user credentials and links to their role.
    """
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True, nullable=False)
    email = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    is_active = Column(Boolean, default=True)

    # Foreign key to Role
    role_id = Column(Integer, ForeignKey('roles.id'), nullable=False)
    
    # Add client_id for multi-tenancy. Can be nullable for system-wide users like admins.
    client_id = Column(String, nullable=True, index=True)

    # Relationships
    role = relationship("Role", back_populates="users")

    def set_password(self, password: str):
        self.hashed_password = get_password_hash(password)

    def check_password(self, password: str) -> bool:
        return verify_password(password, self.hashed_password)

    def __repr__(self):
        return f"<User(id={self.id}, username='{self.username}', client_id='{self.client_id}')>"
