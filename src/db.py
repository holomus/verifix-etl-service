from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
import os

# Create an engine connected to your database
async_engine = create_async_engine(os.environ['DATABASE_URL'])

# Create a configured "Session" class
Session = async_sessionmaker(bind=async_engine)