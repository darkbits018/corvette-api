# sc-siem-corvette/routes/templates.py
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from database.database import get_db
from services import opensearch_service
from utils.security import get_current_user
from models.user import User
from utils.permissions import Permissions

router = APIRouter()

@router.post("/templates/{name}", status_code=status.HTTP_201_CREATED)
async def create_template(
    name: str,
    template: dict,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Creates or updates an index template."""
    user_permissions = current_user.role.permissions or {}
    if not user_permissions.get(Permissions.CAN_MANAGE_INDICES.value, False):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not enough permissions. Requires can_manage_indices."
        )
    try:
        response = await opensearch_service.create_index_template(name, template)
        return response
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"An unexpected error occurred: {e}"
        )

@router.get("/templates/{name}")
async def get_template(
    name: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Gets an index template."""
    user_permissions = current_user.role.permissions or {}
    if not user_permissions.get(Permissions.CAN_MANAGE_INDICES.value, False):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not enough permissions. Requires can_manage_indices."
        )
    try:
        response = await opensearch_service.get_index_template(name)
        return response
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"An unexpected error occurred: {e}"
        )

@router.delete("/templates/{name}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_template(
    name: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Deletes an index template."""
    user_permissions = current_user.role.permissions or {}
    if not user_permissions.get(Permissions.CAN_MANAGE_INDICES.value, False):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not enough permissions. Requires can_manage_indices."
        )
    try:
        await opensearch_service.delete_index_template(name)
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"An unexpected error occurred: {e}"
        )

@router.head("/templates/{name}", status_code=status.HTTP_200_OK)
async def template_exists(
    name: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Checks if an index template exists."""
    user_permissions = current_user.role.permissions or {}
    if not user_permissions.get(Permissions.CAN_MANAGE_INDICES.value, False):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not enough permissions. Requires can_manage_indices."
        )
    try:
        if not await opensearch_service.index_template_exists(name):
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"An unexpected error occurred: {e}"
        )
