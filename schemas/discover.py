# sc-siem-corvette/schemas/discover.py
from pydantic import BaseModel, Field
from typing import Optional, List, Dict, Any

# --- Supporting Models for the Request ---

class TimeRange(BaseModel):
    from_: str = Field(..., alias='from', description="Start of the time range. Format: YYYY-MM-DDTHH:MM:SS.sssZ")
    to: str = Field(..., description="End of the time range. Format: YYYY-MM-DDTHH:MM:SS.sssZ")

class DynamicFilter(BaseModel):
    field: str
    value: Any
    type: str = Field("term", description="Filter type (e.g., 'term', 'match', 'range')")
    operator: Optional[str] = Field(None, description="For range filters (e.g., 'gte', 'lte')")

class SortOption(BaseModel):
    field: str
    order: str = Field("desc", description="Sort order: 'asc' or 'desc'")

# --- Main Request and Response Schemas ---

class DiscoverRequest(BaseModel):
    index_pattern: str
    client_id: Optional[str] = None
    size: int = 100
    from_: int = Field(0, alias='from')
    time_range: Optional[TimeRange] = None
    query: Dict[str, Any] = Field(default_factory=lambda: {"match_all": {}})
    filters: Optional[List[DynamicFilter]] = None
    sort: Optional[List[SortOption]] = None
    aggregations: Optional[Dict[str, Any]] = Field(None, alias="aggs")
    highlight: Optional[Dict[str, Any]] = None
    fields: Optional[List[str]] = Field(None, description="List of fields to return from _source")

class Hit(BaseModel):
    """Represents a single search hit, with field names safe for Pydantic."""
    index: str  # Renamed from _index
    source: Dict[str, Any]  # Renamed from _source
    highlight: Optional[Dict[str, List[str]]] = None

class DiscoverResponse(BaseModel):
    hits: List[Hit]
    total: int
    aggregations: Optional[Dict[str, Any]] = {}
