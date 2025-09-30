from pydantic import BaseModel, Field
from typing import Dict, Any, Optional

class IndexSchema(BaseModel):
    index_name: str = Field(..., description="Name of the OpenSearch index.")
    template_name: Optional[str] = Field(None, description="Optional name of the index template to use.")
    settings: Optional[Dict[str, Any]] = Field(None, description="Optional index settings.")
    mappings: Optional[Dict[str, Any]] = Field(None, description="Optional index mappings.")
