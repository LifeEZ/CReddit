from motor.motor_asyncio import AsyncIOMotorClient, AsyncIOMotorDatabase
from ..config import settings

# Create client instance
client = AsyncIOMotorClient(settings.DATABASE_URL)
database = client[settings.DATABASE_NAME]


# Database dependency
async def get_db() -> AsyncIOMotorDatabase:
    return database
