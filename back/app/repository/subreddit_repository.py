from typing import List
from datetime import datetime, UTC
from .base import BaseRepository
from motor.motor_asyncio import AsyncIOMotorDatabase


class SubredditRepository(BaseRepository):
    """Repository for subreddit-related database operations."""
    
    def __init__(self, db: AsyncIOMotorDatabase):
        super().__init__(db, "subreddits")
    
    async def find_by_name(self, name: str) -> dict:
        """Find subreddit by name."""
        return await self.find_one({"name": name})
    
    async def name_exists(self, name: str) -> bool:
        """Check if subreddit name already exists."""
        return await self.exists({"name": name})
    
    async def create_subreddit(
        self,
        name: str,
        description: str,
        rules: List[str],
        created_by: str
    ) -> dict:
        """Create a new subreddit."""
        subreddit_data = {
            "name": name,
            "description": description,
            "rules": rules,
            "created_by": created_by,
            "moderators": [created_by],
            "members": 1,
            "created_at": datetime.now(UTC)
        }
        return await self.create(subreddit_data)
    
    async def get_subreddits_paginated(
        self, 
        skip: int = 0, 
        limit: int = 10
    ) -> List[dict]:
        """Get subreddits with pagination."""
        return await self.find_many(skip=skip, limit=limit)
    
    async def increment_members(self, subreddit_id: str, increment: int = 1) -> bool:
        """Increment subreddit member count."""
        try:
            result = await self.collection.update_one(
                {"_id": subreddit_id},
                {"$inc": {"members": increment}}
            )
            return result.modified_count > 0
        except (ValueError, TypeError):
            return False 