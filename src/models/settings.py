from sqlalchemy import Column, Integer, String

from .base import Base

# class PipeSettings(Base):
#   __tablename__ = 'pipe_settings'

#   id = Column(Integer, primary_key=True, autoincrement=True)

class SmartupPipeSettings(Base):
  __tablename__ = 'smartup_pipe_settings'

  id = Column(Integer, primary_key=True, autoincrement=True)
  company_code=Column(String, unique=True, nullable=False)
  host=Column(String, nullable=False)
  client_id=Column(String, nullable=False)
  client_secret=Column(String, nullable=False)
