from motor.motor_asyncio import AsyncIOMotorClient, AsyncIOMotorDatabase
from typing import AsyncGenerator
from loguru import logger

from app.config import settings


class DatabaseManager:
    """Database connection manager."""
    
    def __init__(self):
        self.client: AsyncIOMotorClient = None
        self.database: AsyncIOMotorDatabase = None
    
    async def connect_to_database(self):
        """Connect to MongoDB database."""
        try:
            self.client = AsyncIOMotorClient(settings.mongodb_uri)
            self.database = self.client[settings.mongodb_database]
            logger.info("Connected to MongoDB successfully")
        except Exception as e:
            logger.error(f"Failed to connect to MongoDB: {e}")
            raise
    
    async def close_database_connection(self):
        """Close MongoDB database connection."""
        if self.client:
            self.client.close()
            logger.info("Closed MongoDB connection")
    
    def get_database(self) -> AsyncIOMotorDatabase:
        """Get database instance."""
        if not self.database:
            raise RuntimeError("Database not connected")
        return self.database


# Global database manager instance
db_manager = DatabaseManager()


async def get_database() -> AsyncGenerator[AsyncIOMotorDatabase, None]:
    """Get database dependency for FastAPI."""
    yield db_manager.get_database()


async def init_database():
    """Initialize database connection."""
    await db_manager.connect_to_database()


async def close_database():
    """Close database connection."""
    await db_manager.close_database_connection()