# W:/pyProjects/sc-siem-corvette/routes/users.py
print("=== Loading users routes ===")
from fastapi import APIRouter, Depends, status, HTTPException
from sqlalchemy.orm import Session
from typing import List

# Database and security imports
from database.database import get_db
from utils.hashing import get_password_hash
from utils.security import require_permission
from utils.permissions import Permissions

# Schema imports
from schemas.user import UserCreate, UserResponse

# Model imports
from models.user import User
from models.role import Role

router = APIRouter()


@router.post("/", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
async def create_user(user: UserCreate, db: Session = Depends(get_db),
                      _=Depends(require_permission(Permissions.CAN_MANAGE_USERS))):
    """
    Creates a new user in the database. Requires 'can_manage_users' permission.
    """
    existing_user = db.query(User).filter((User.username == user.username) | (User.email == user.email)).first()
    if existing_user:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Username or email already registered")

    role_db = db.query(Role).filter(Role.name == user.role).first()
    if not role_db:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Role '{user.role}' not found")

    hashed_password = get_password_hash(user.password)
    new_user = User(
        username=user.username,
        email=user.email,
        hashed_password=hashed_password,
        role_id=role_db.id,
        client_id=user.client_id  # Save the client_id
    )

    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return new_user


@router.get("/", response_model=List[UserResponse])
async def get_users(db: Session = Depends(get_db), _=Depends(require_permission(Permissions.CAN_MANAGE_USERS))):
    """
    Retrieves a list of all users. Requires 'can_manage_users' permission.
    """
    users = db.query(User).all()
    return users


print("=== Users routes loaded successfully ===")
