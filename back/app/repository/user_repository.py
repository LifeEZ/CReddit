from typing import Optional, List
from datetime import datetime, UTC
from .base import BaseRepository
from motor.motor_asyncio import AsyncIOMotorDatabase


class UserRepository(BaseRepository):
    """Repository for user-related database operations."""
    
    def __init__(self, db: AsyncIOMotorDatabase):
        super().__init__(db, "users")
    
    async def find_by_username(self, username: str) -> Optional[dict]:
        """Find user by username."""
        return await self.find_one({"username": username})
    
    async def find_by_email(self, email: str) -> Optional[dict]:
        """Find user by email."""
        return await self.find_one({"email": email})
    
    async def username_or_email_exists(self, username: str, email: str) -> bool:
        """Check if username or email already exists."""
        return await self.exists({
            "$or": [
                {"username": username},
                {"email": email}
            ]
        })
    
    async def create_user(self, username: str, email: str, hashed_password: str) -> dict:
        """Create a new user."""
        user_data = {
            "username": username,
            "email": email,
            "password": hashed_password,
            "karma": 0,
            "created_at": datetime.now(UTC)
        }
        return await self.create(user_data)
    
    async def get_users_paginated(self, skip: int = 0, limit: int = 10) -> List[dict]:
        """Get users with pagination."""
        return await self.find_many(skip=skip, limit=limit) 