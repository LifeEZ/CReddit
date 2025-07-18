from typing import List, Optional, Any, Dict
from motor.motor_asyncio import AsyncIOMotorDatabase
from bson import ObjectId


class BaseRepository:
    """Base repository class providing common database operations."""
    
    def __init__(self, db: AsyncIOMotorDatabase, collection_name: str):
        self.db = db
        self.collection = db[collection_name]
    
    async def find_one(self, filter_dict: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """Find a single document by filter."""
        return await self.collection.find_one(filter_dict)
    
    async def find_one_by_id(self, id: str) -> Optional[Dict[str, Any]]:
        """Find a single document by ID."""
        try:
            return await self.collection.find_one({"_id": ObjectId(id)})
        except (ValueError, TypeError):
            return None
    
    async def find_many(self, filter_dict: Dict[str, Any] = None, skip: int = 0, limit: int = 10) -> List[Dict[str, Any]]:
        """Find multiple documents with optional filtering and pagination."""
        filter_dict = filter_dict or {}
        cursor = self.collection.find(filter_dict).skip(skip).limit(limit)
        documents = []
        async for doc in cursor:
            documents.append(doc)
        return documents
    
    async def create(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Create a new document."""
        result = await self.collection.insert_one(data)
        data["_id"] = result.inserted_id
        return data
    
    async def update(self, id: str, data: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """Update a document by ID."""
        try:
            result = await self.collection.update_one(
                {"_id": ObjectId(id)},
                {"$set": data}
            )
            if result.modified_count > 0:
                return await self.find_one_by_id(id)
            return None
        except (ValueError, TypeError):
            return None
    
    async def delete(self, id: str) -> bool:
        """Delete a document by ID."""
        try:
            result = await self.collection.delete_one({"_id": ObjectId(id)})
            return result.deleted_count > 0
        except (ValueError, TypeError):
            return False
    
    async def exists(self, filter_dict: Dict[str, Any]) -> bool:
        """Check if a document exists."""
        return await self.collection.count_documents(filter_dict) > 0 