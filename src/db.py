from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import config

# Create an engine connected to your database
engine = create_engine(f'postgresql://{config.DATABASE_USERNAME}:{config.DATABASE_PASSWORD}@{config.DATABASE_URL}:{config.DATABASE_PORT}/{config.DATABASE_NAME}')

# Create a configured "Session" class
Session = sessionmaker(bind=engine)
