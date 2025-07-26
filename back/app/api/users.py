from fastapi import APIRouter, HTTPException, Depends
from ..core.security import get_password_hash
from ..core.database import get_db
from ..models.schemas import UserCreate, UserResponse
from ..repository.user_repository import UserRepository
from typing import List

router = APIRouter(prefix="/users", tags=["users"])


@router.post("/", response_model=UserResponse)
async def create_user(
    user: UserCreate,
    db=Depends(get_db)
):
    user_repo = UserRepository(db)
    
    if await user_repo.username_or_email_exists(user.username, user.email):
        raise HTTPException(
            status_code=400,
            detail="Username or email already exists"
        )

    hashed_password = get_password_hash(user.password)
    user_data = await user_repo.create_user(
        user.username, 
        user.email, 
        hashed_password
    )
    
    return UserResponse(**user_data)


@router.get("/", response_model=List[UserResponse])
async def list_users(
    skip: int = 0,
    limit: int = 10,
    db=Depends(get_db)
):
    user_repo = UserRepository(db)
    users = await user_repo.get_users_paginated(skip=skip, limit=limit)
    return [UserResponse(**user) for user in users]


@router.get("/{username}", response_model=UserResponse)
async def get_user_by_username(
    username: str,
    db=Depends(get_db)
):
    user_repo = UserRepository(db)
    user = await user_repo.find_by_username(username)
    
    if not user:
        raise HTTPException(
            status_code=404,
            detail="User not found"
        )
    return UserResponse(**user)
