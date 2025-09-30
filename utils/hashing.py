# sc-siem-corvette/utils/hashing.py
from passlib.context import CryptContext
import hashlib

# Use passlib for secure password hashing. Bcrypt is a good choice.
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def _prepare_password(password: str) -> str:
    """Prepare password for bcrypt by handling the 72-byte limitation."""
    # If password is longer than 72 bytes, hash it first to ensure consistent length
    if len(password.encode('utf-8')) > 72:
        return hashlib.sha256(password.encode('utf-8')).hexdigest()
    return password


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verifies a plain password against its hash."""
    prepared_password = _prepare_password(plain_password)
    return pwd_context.verify(prepared_password, hashed_password)


def get_password_hash(password: str) -> str:
    """Generates a hash for a given password."""
    prepared_password = _prepare_password(password)
    return pwd_context.hash(prepared_password)
