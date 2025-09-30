# W:/pyProjects/sc-siem-corvette/routes/roles.py
from fastapi import APIRouter, Depends, status, HTTPException
from sqlalchemy.orm import Session
from typing import List

from database.database import get_db
from utils.security import require_permission
from utils.permissions import Permissions
from models.role import Role
from schemas.role import RoleCreate, RoleResponse

router = APIRouter()


@router.get("/permissions", response_model=List[str])
async def get_all_permissions():
    """
    Returns a list of all available permission strings in the system.
    Useful for frontends that need to display permission options.
    """
    return [p.value for p in Permissions]


@router.post("/", response_model=RoleResponse, status_code=status.HTTP_201_CREATED)
async def create_role(
    role: RoleCreate, 
    db: Session = Depends(get_db),
    _=Depends(require_permission(Permissions.CAN_MANAGE_ROLES))
):
    """
    Creates a new role. Requires 'can_manage_roles' permission.
    """
    existing_role = db.query(Role).filter(Role.name == role.name).first()
    if existing_role:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT, 
            detail=f"Role '{role.name}' already exists"
        )

    permissions_data = {p.value: v for p, v in role.permissions.items()}

    new_role = Role(
        name=role.name,
        description=role.description,
        permissions=permissions_data
    )

    db.add(new_role)
    db.commit()
    db.refresh(new_role)

    return new_role


@router.get("/", response_model=List[RoleResponse])
async def get_roles(db: Session = Depends(get_db)):
    """
    Retrieves a list of all roles from the database.
    """
    roles = db.query(Role).all()
    return roles
