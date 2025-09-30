# sc-siem-corvette/auth/auth.py
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from sqlalchemy.orm import Session
from typing import Optional
import os
from utils.security import SECRET_KEY, ALGORITHM  # Import from security utils
from database.database import get_db  # Assuming you have a function to get DB session
from models.user import User  # Import the User model
from schemas.user import UserResponse  # Import the User response schema for type hinting

# Define the OAuth2 scheme. The 'tokenUrl' points to your login endpoint.
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/token")  # Adjust path if needed


# Re-import SECRET_KEY and ALGORITHM here or pass them if needed
# SECRET_KEY and ALGORITHM are imported from utils.security

async def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)) -> User:
    """
    FastAPI dependency to get the current authenticated user from the JWT token.
    Verifies the token, extracts the user ID, fetches the user from the database,
    and returns the User model instance.
    """
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        # Decode the JWT token
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id: int = payload.get("sub")  # Standard claim for subject (user ID)
        if user_id is None:
            raise credentials_exception
        # Optional: Add role or other claims check here if needed immediately
        # role: str = payload.get("role")
        # if role not in ["admin", "user"]: # Example check
        #     raise credentials_exception

    except JWTError:
        raise credentials_exception

    # Fetch user from database using the ID from the token
    user = db.query(User).filter(User.id == user_id).first()
    if user is None:
        raise credentials_exception
    return user  # Returns the SQLAlchemy User model instance


# Optional: Dependency to get current active user
async def get_current_active_user(current_user: User = Depends(get_current_user)) -> User:
    """Dependency to ensure the user is active."""
    if not current_user.is_active:
        raise HTTPException(status_code=400, detail="Inactive user")
    return current_user

# Optional: Dependency to check specific role (can be used in route definitions)
# def require_role(required_role_name: str):
#     async def role_checker(current_user: User = Depends(get_current_active_user)):
#         if current_user.role.name != required_role_name:
#             raise HTTPException(status_code=403, detail=f"Access denied. Required role: {required_role_name}")
#         return current_user
#     return role_checker

# Example usage in a route:
# @router.get("/admin-data")
# async def read_admin_data(current_user: User = Depends(require_role("Admin"))):
#     return {"message": "This is admin data", "user": current_user.username}
