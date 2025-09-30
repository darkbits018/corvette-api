# sc-siem-corvette/utils/security.py
from jose import JWTError, jwt
from datetime import datetime, timedelta
from typing import Optional
import os
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from pydantic import BaseModel
from sqlalchemy.orm import Session

# --- Project-specific Imports ---
from utils.permissions import Permissions
from models.user import User
from database.database import get_db

# --- JWT Handling ---
SECRET_KEY = os.getenv("SECRET_KEY", "your_default_secret_key_change_this")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", 30))
REFRESH_TOKEN_EXPIRE_MINUTES = int(os.getenv("REFRESH_TOKEN_EXPIRE_MINUTES", 60 * 24 * 7)) # 7 days


def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire, "token_type": "access"})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


def create_refresh_token(data: dict, expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=REFRESH_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire, "token_type": "refresh"})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


# --- Authentication & Permission Dependencies ---
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/v1/auth/login")

class TokenData(BaseModel):
    username: Optional[str] = None
    client_id: Optional[str] = None


def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        token_type = payload.get("token_type")
        username: str = payload.get("sub")
        client_id: Optional[str] = payload.get("client_id")

        if username is None or token_type not in ["access", "refresh"]:
            raise credentials_exception
        
        token_data = TokenData(username=username, client_id=client_id)
    except JWTError:
        raise credentials_exception

    user = db.query(User).filter(User.username == token_data.username).first()
    if user is None:
        raise credentials_exception
    
    # Attach the token type to the user object for endpoint-specific validation
    user.token_type = token_type
    return user


def require_permission(required_permission: Permissions):
    def permission_checker(current_user: User = Depends(get_current_user)):
        if not hasattr(current_user, 'role') or not current_user.role:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="User has no assigned role.")

        role_permissions = current_user.role.permissions or {}
        if not role_permissions.get(required_permission.value, False):
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=f"Not enough permissions. Requires: {required_permission.value}")

    return permission_checker
