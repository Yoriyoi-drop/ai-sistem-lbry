import hashlib
import secrets
from typing import Optional


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verify a plain password against a hashed password"""
    # Split stored hash and salt
    if "$" in hashed_password:
        stored_hash, salt = hashed_password.split("$")
        expected_hash = hashlib.sha256((plain_password + salt).encode()).hexdigest()
        return expected_hash == stored_hash
    return False


def get_password_hash(password: str) -> str:
    """Generate a hash for a plain password"""
    # Truncate password to 72 characters if needed to avoid bcrypt issues
    if len(password) > 72:
        password = password[:72]
    # Generate a random salt
    salt = secrets.token_hex(16)
    # Hash the password with salt
    pwd_hash = hashlib.sha256((password + salt).encode()).hexdigest()
    # Combine hash and salt
    return f"{pwd_hash}${salt}"