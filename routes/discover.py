# sc-siem-corvette/routes/discover.py
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

# Project imports
from database.database import get_db
from schemas.discover import DiscoverRequest, DiscoverResponse
from services import opensearch_service
from utils.security import get_current_user
from models.user import User
from utils.permissions import Permissions

router = APIRouter()


@router.post("/", response_model=DiscoverResponse)
async def discover_logs(
    request: DiscoverRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Fetches raw logs from OpenSearch based on the provided index pattern and filters.
    Permissions are enforced based on the user's role and client_id.
    """
    # 1. Permission and Client ID validation
    user_permissions = current_user.role.permissions or {}
    is_admin = user_permissions.get(Permissions.CAN_MANAGE_INDICES.value, False)

    if not is_admin:
        # Non-admins must have CAN_VIEW_LOGS
        if not user_permissions.get(Permissions.CAN_VIEW_LOGS.value, False):
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Not enough permissions. Requires can_view_logs."
            )
        
        # Non-admins are restricted by client_id
        if not current_user.client_id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="User is not associated with a client_id."
            )
        
        if not request.client_id:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="client_id is required for this user."
            )

        if request.client_id != current_user.client_id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="User is not permitted to view logs for the requested client_id."
            )
    
    # 2. Fetch logs from OpenSearch
    # The opensearch_service will handle the actual query and error handling
    try:
        response = await opensearch_service.fetch_logs(request)
        return response
    except HTTPException as e:
        # Re-raise HTTP exceptions from the service layer
        raise e
    except Exception as e:
        # Catch any other unexpected errors
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"An unexpected error occurred: {e}"
        )
