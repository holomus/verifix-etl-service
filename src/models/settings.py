from sqlalchemy import Column, BigInteger, String, DateTime, ARRAY

from .base import Base

# Model for the verifix.smartup_pipe_settings table
class SmartupPipeSettings(Base):
    __tablename__ = 'smartup_pipe_settings'

    id = Column(BigInteger, primary_key=True, autoincrement=True)
    company_code = Column(String(100), nullable=False)
    filial_codes = Column(ARRAY(String(500)), nullable=False)
    host = Column(String(500), nullable=False)
    client_id = Column(String(500), nullable=False)
    client_secret = Column(String(500), nullable=False)
    last_execution_time = Column(DateTime)