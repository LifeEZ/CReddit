from fastapi import APIRouter, HTTPException, Depends
from ..core.security import get_password_hash
from ..core.database import get_db
from ..models.schemas import UserCreate, UserResponse
from datetime import datetime, UTC
from typing import List

router = APIRouter(prefix="/users", tags=["users"])


@router.post("/", response_model=UserResponse)
async def create_user(
    user: UserCreate,
    db=Depends(get_db)
):
    if await db.users.find_one({
        "$or": [
            {"username": user.username},
            {"email": user.email}
        ]
    }):
        raise HTTPException(
            status_code=400,
            detail="Username or email already exists"
        )

    hashed_password = get_password_hash(user.password)

    user_data = {
        "username": user.username,
        "email": user.email,
        "password": hashed_password,
        "karma": 0,
        "created_at": datetime.now(UTC)
    }

    result = await db.users.insert_one(user_data)
    user_data["_id"] = result.inserted_id
    return UserResponse(**user_data)


@router.get("/", response_model=List[UserResponse])
async def list_users(
    skip: int = 0,
    limit: int = 10,
    db=Depends(get_db)
):
    cursor = db.users.find().skip(skip).limit(limit)
    users = []
    async for user in cursor:
        users.append(UserResponse(**user))
    return users


@router.get("/{username}", response_model=UserResponse)
async def get_user_by_username(
    username: str,
    db=Depends(get_db)
):
    user = await db.users.find_one({"username": username})
    if not user:
        raise HTTPException(
            status_code=404,
            detail="User not found"
        )
    return UserResponse(**user)
