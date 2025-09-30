# sc-siem-corvette/schemas/auth.py
from pydantic import BaseModel


class LoginRequest(BaseModel):
    """
    Schema for validating user login credentials from a request body.
    FastAPI will use this to ensure the username and password fields are present.
    """
    username: str
    password: str


class Token(BaseModel):
    """
    Schema for the response when a user successfully logs in.
    It provides the JWT access token and the token type (bearer).
    """
    access_token: str
    token_type: str


class TokenData(BaseModel):
    """
    Schema for the data encoded within the JWT.
    This is used internally to safely extract the user identifier ('sub') from the token.
    """
    username: str | None = None
