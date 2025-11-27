from sqlalchemy.orm import Session
from typing import List, Optional
from ..models.user import User
from ..schemas.user import UserCreate, UserUpdate
from ..utils.security import get_password_hash
import logging

logger = logging.getLogger(__name__)

class UserRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_user_by_id(self, user_id: int) -> Optional[User]:
        """Get a user by ID"""
        return self.db.query(User).filter(User.id == user_id).first()

    def get_user_by_email(self, email: str) -> Optional[User]:
        """Get a user by email"""
        return self.db.query(User).filter(User.email == email).first()

    def get_user_by_username(self, username: str) -> Optional[User]:
        """Get a user by username"""
        return self.db.query(User).filter(User.username == username).first()

    def get_users(self, skip: int = 0, limit: int = 100) -> List[User]:
        """Get a list of users with pagination"""
        return self.db.query(User).offset(skip).limit(limit).all()

    def create_user(self, user_create: UserCreate) -> User:
        """Create a new user"""
        hashed_password = get_password_hash(user_create.password)
        db_user = User(
            email=user_create.email,
            username=user_create.username,
            full_name=user_create.full_name,
            hashed_password=hashed_password,
            is_active=user_create.is_active,
            is_superuser=user_create.is_superuser
        )
        self.db.add(db_user)
        self.db.commit()
        self.db.refresh(db_user)
        logger.info(f"User created with ID: {db_user.id}")
        return db_user

    def update_user(self, user_id: int, user_update: UserUpdate) -> Optional[User]:
        """Update a user"""
        db_user = self.get_user_by_id(user_id)
        if not db_user:
            return None

        update_data = user_update.dict(exclude_unset=True)
        if "password" in update_data:
            update_data["hashed_password"] = get_password_hash(update_data["password"])
            del update_data["password"]

        for field, value in update_data.items():
            setattr(db_user, field, value)

        self.db.commit()
        self.db.refresh(db_user)
        logger.info(f"User updated with ID: {db_user.id}")
        return db_user

    def delete_user(self, user_id: int) -> bool:
        """Delete a user"""
        db_user = self.get_user_by_id(user_id)
        if not db_user:
            return False

        self.db.delete(db_user)
        self.db.commit()
        logger.info(f"User deleted with ID: {user_id}")
        return True

    def authenticate_user(self, username: str, password: str) -> Optional[User]:
        """Authenticate a user by username and password"""
        user = self.get_user_by_username(username)
        if not user or not user.hashed_password:
            return None
            
        # We need to import verify_password here to avoid circular imports
        from ..utils.security import verify_password
        if not verify_password(password, user.hashed_password):
            return None

        return user