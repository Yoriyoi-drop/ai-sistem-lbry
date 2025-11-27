"""
User service for Infinite AI Security Platform
"""
from typing import Optional, List
from sqlalchemy.orm import Session
from ..database.models import User as UserModel
from ..schemas.user import UserCreate, UserUpdate
from ..utils.security import get_password_hash


class UserService:
    def __init__(self, db: Session):
        self.db = db

    def get_user_by_id(self, user_id: int) -> Optional[UserModel]:
        """Get a user by ID"""
        return self.db.query(UserModel).filter(UserModel.id == user_id).first()

    def get_user_by_email(self, email: str) -> Optional[UserModel]:
        """Get a user by email"""
        return self.db.query(UserModel).filter(UserModel.email == email).first()

    def get_user_by_username(self, username: str) -> Optional[UserModel]:
        """Get a user by username"""
        return self.db.query(UserModel).filter(UserModel.username == username).first()

    def get_users(self, skip: int = 0, limit: int = 100) -> List[UserModel]:
        """Get a list of users with pagination"""
        return self.db.query(UserModel).offset(skip).limit(limit).all()

    def create_user(self, user_create: UserCreate) -> UserModel:
        """Create a new user"""
        hashed_password = get_password_hash(user_create.password)
        db_user = UserModel(
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
        return db_user

    def update_user(self, user_id: int, user_update: UserUpdate) -> Optional[UserModel]:
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
        return db_user

    def delete_user(self, user_id: int) -> bool:
        """Delete a user"""
        db_user = self.get_user_by_id(user_id)
        if not db_user:
            return False

        self.db.delete(db_user)
        self.db.commit()
        return True