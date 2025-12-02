"""
Security utilities for Infinite AI Security Platform
"""
from passlib.context import CryptContext


# Password hashing context
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """
    Verify a plain password against a hashed password
    """
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password: str) -> str:
    """
    Generate a hash for a plain password
    """
    return pwd_context.hash(password)


# For backward compatibility
def hash_password(password: str) -> str:
    """
    Generate a hash for a plain password (alias for get_password_hash)
    """
    return get_password_hash(password)