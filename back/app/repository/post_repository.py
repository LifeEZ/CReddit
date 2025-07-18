from typing import Optional, List
from datetime import datetime, UTC
from bson import ObjectId
from .base import BaseRepository
from motor.motor_asyncio import AsyncIOMotorDatabase


class PostRepository(BaseRepository):
    """Repository for post-related database operations."""
    
    def __init__(self, db: AsyncIOMotorDatabase):
        super().__init__(db, "posts")
    
    async def create_post(
        self, 
        title: str, 
        content: str, 
        author_id: str, 
        subreddit_id: str
    ) -> dict:
        """Create a new post."""
        post_data = {
            "title": title,
            "content": content,
            "author_id": author_id,
            "subreddit_id": subreddit_id,
            "votes": 0,
            "comments": 0,
            "created_at": datetime.now(UTC)
        }
        return await self.create(post_data)
    
    async def get_posts_paginated(self, skip: int = 0, limit: int = 10) -> List[dict]:
        """Get posts with pagination."""
        return await self.find_many(skip=skip, limit=limit)
    
    async def get_posts_by_subreddit(
        self, 
        subreddit_id: str, 
        skip: int = 0, 
        limit: int = 10
    ) -> List[dict]:
        """Get posts by subreddit with pagination."""
        return await self.find_many(
            {"subreddit_id": subreddit_id}, 
            skip=skip, 
            limit=limit
        )
    
    async def get_posts_by_author(
        self, 
        author_id: str, 
        skip: int = 0, 
        limit: int = 10
    ) -> List[dict]:
        """Get posts by author with pagination."""
        return await self.find_many(
            {"author_id": author_id}, 
            skip=skip, 
            limit=limit
        )
    
    async def increment_votes(self, post_id: str, increment: int = 1) -> bool:
        """Increment post votes."""
        try:
            result = await self.collection.update_one(
                {"_id": ObjectId(post_id)},
                {"$inc": {"votes": increment}}
            )
            return result.modified_count > 0
        except (ValueError, TypeError):
            return False
    
    async def increment_comments(self, post_id: str, increment: int = 1) -> bool:
        """Increment post comment count."""
        try:
            result = await self.collection.update_one(
                {"_id": ObjectId(post_id)},
                {"$inc": {"comments": increment}}
            )
            return result.modified_count > 0
        except (ValueError, TypeError):
            return False 