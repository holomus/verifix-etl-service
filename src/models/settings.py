from sqlalchemy import Column, BigInteger, String, UniqueConstraint, ForeignKeyConstraint
from sqlalchemy.orm import relationship
from .base import Base

# Model for the verifix.smartup_pipe_settings table
class SmartupPipes(Base):
  __tablename__ = 'smartup_pipes'

  id = Column(BigInteger, primary_key=True, nullable=True, autoincrement=True)
  company_code = Column(String(100), nullable=False)
  host = Column(String(500), nullable=False)
  client_id = Column(String(500), nullable=False)
  client_secret = Column(String(500), nullable=False)

  cursors = relationship('SmartupCursors', back_populates='pipe', cascade="all, delete-orphan")

  __table_args__ = (
    UniqueConstraint('company_code', 'host', name='smartup_pipes_u1'),
  )

class SmartupCursors(Base):
  __tablename__ = 'smartup_cursors'

  pipe_id = Column(BigInteger, primary_key=True, nullable=True)
  extraction_key = Column(String(100), primary_key=True, nullable=True)
  last_cursor = Column(BigInteger, nullable=True)

  pipe = relationship('SmartupPipes', back_populates='cursors')
  __table_args__ = (
    ForeignKeyConstraint(['pipe_id'], ['smartup_pipes.id'], ondelete='CASCADE'),
  )
  