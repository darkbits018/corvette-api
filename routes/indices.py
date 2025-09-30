from fastapi import APIRouter, HTTPException, status, Depends
from typing import List, Dict, Any

from services.opensearch_service import client
from schemas.index import IndexSchema
from utils.security import require_permission
from utils.permissions import Permissions

router = APIRouter()

@router.post("/", status_code=status.HTTP_201_CREATED)
async def create_index(index: IndexSchema, _=Depends(require_permission(Permissions.CAN_MANAGE_INDICES))):
    """
    Creates a new OpenSearch index.
    If a template_name is provided, the index will be created without any specific settings or mappings,
    and OpenSearch will apply a matching template.
    """
    if not client:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="OpenSearch service is not available"
        )
    try:
        body = {}
        if not index.template_name:
            body = {
                "settings": index.settings,
                "mappings": index.mappings
            }
        client.indices.create(index=index.index_name, body=body)
        return {"message": f"Index '{index.index_name}' created successfully."}
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"An error occurred while creating the index: {e}"
        )

@router.get("/", response_model=Dict[str, Any])
async def get_all_indices(_=Depends(require_permission(Permissions.CAN_MANAGE_INDICES))):
    """
    Retrieves all indices from OpenSearch.
    """
    if not client:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="OpenSearch service is not available"
        )
    try:
        indices = client.indices.get(index="*")
        return indices
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"An error occurred while retrieving indices: {e}"
        )

@router.get("/{index_name}", response_model=Dict[str, Any])
async def get_index(index_name: str, _=Depends(require_permission(Permissions.CAN_MANAGE_INDICES))):
    """
    Retrieves a specific OpenSearch index.
    """
    if not client:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="OpenSearch service is not available"
        )
    try:
        index = client.indices.get(index=index_name)
        return index
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"An error occurred while retrieving the index: {e}"
        )

@router.delete("/{index_name}")
async def delete_index(index_name: str, _=Depends(require_permission(Permissions.CAN_MANAGE_INDICES))):
    """
    Deletes a specific OpenSearch index.
    """
    if not client:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="OpenSearch service is not available"
        )
    try:
        client.indices.delete(index=index_name)
        return {"message": f"Index '{index_name}' deleted successfully."}
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"An error occurred while deleting the index: {e}"
        )
