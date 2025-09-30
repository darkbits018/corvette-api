# sc-siem-corvette/schemas/token.py
from pydantic import BaseModel
from typing import Optional


class Token(BaseModel):
    """
    Schema for the JWT access and refresh token response.
    """
    access_token: str
    refresh_token: str
    token_type: str


class TokenData(BaseModel):
    """
    Schema for data stored inside the JWT token.
    This represents the payload after decoding.
    """
    username: Optional[str] = None
