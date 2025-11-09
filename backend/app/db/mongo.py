import os
from functools import lru_cache

from motor.motor_asyncio import AsyncIOMotorClient
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    MONGO_URL: str
    MONGO_DB_NAME: str = "price_scraper"

    class Config:
        env_file = ".env"

@lru_cache
def get_settings() -> Settings:
    return Settings()

settings = get_settings()   

mongo_client = AsyncIOMotorClient(settings.MONGO_URL)
mongo_db = mongo_client[settings.MONGO_DB_NAME]

def get_mongo_db():
    return mongo_db