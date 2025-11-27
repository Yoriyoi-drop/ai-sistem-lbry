from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from ..database.connection import get_db
from ..schemas.user import User, UserCreate, UserUpdate
from ..services.user_service import UserService
from ..utils.dependencies import get_current_user, get_current_admin_user


router = APIRouter(prefix="/users", tags=["Users"])


@router.get("/", response_model=List[User])
def read_users(
    skip: int = 0,
    limit: int = 100,
    current_user = Depends(get_current_admin_user),  # Only admin can list all users
    db: Session = Depends(get_db)
):
    """
    Retrieve users with pagination (admin only)
    """
    user_service = UserService(db)
    users = user_service.get_users(skip=skip, limit=limit)
    return users


@router.get("/me", response_model=User)
def read_current_user(current_user = Depends(get_current_user)):
    """
    Get current user info
    """
    return current_user


@router.get("/{user_id}", response_model=User)
def read_user(
    user_id: int,
    current_user = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Get a specific user by ID
    """
    user_service = UserService(db)
    user = user_service.get_user_by_id(user_id)
    
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    
    # Check if user is requesting their own info or is admin
    if user_id != current_user.id and not current_user.is_admin:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to access this user"
        )
    
    return user


@router.put("/{user_id}", response_model=User)
def update_user(
    user_id: int,
    user_update: UserUpdate,
    current_user = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Update a specific user
    """
    user_service = UserService(db)
    user = user_service.get_user_by_id(user_id)
    
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    
    # Check if user is updating their own info or is admin
    if user_id != current_user.id and not current_user.is_admin:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to update this user"
        )
    
    # Prevent non-admins from changing roles
    if not current_user.is_admin and user_update.role is not None:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to change user role"
        )
    
    updated_user = user_service.update_user(user_id, user_update)
    if not updated_user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    
    return updated_user


@router.delete("/{user_id}")
def delete_user(
    user_id: int,
    current_user = Depends(get_current_admin_user),  # Only admin can delete users
    db: Session = Depends(get_db)
):
    """
    Delete a user (admin only)
    """
    user_service = UserService(db)
    success = user_service.delete_user(user_id)
    
    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    
    return {"message": "User deleted successfully"}