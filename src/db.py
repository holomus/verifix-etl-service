from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
import config

# Create an engine connected to your database
async_engine = create_async_engine(f'postgresql+asyncpg://{config.DATABASE_USERNAME}:{config.DATABASE_PASSWORD}@{config.DATABASE_URL}:{config.DATABASE_PORT}/{config.DATABASE_NAME}')

# Create a configured "Session" class
Session = async_sessionmaker(bind=async_engine)