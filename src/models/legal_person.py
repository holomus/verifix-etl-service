from sqlalchemy import Column, BigInteger, String, Index, ForeignKeyConstraint
from sqlalchemy.orm import relationship
from .base import Base

# Model for the smartup_legal_persons table
class SmartupLegalPersons(Base):
  __tablename__ = 'smartup_legal_persons'
  
  pipe_id = Column(BigInteger, primary_key=True, nullable=False)
  person_id = Column(BigInteger, primary_key=True, nullable=False)
  name = Column(String(500), nullable=False)
  short_name = Column(String(500), nullable=False)
  code = Column(String(100))
  region_code = Column(String(500))

  __table_args__ = (
    Index('smartup_legal_persons_i1', 'pipe_id', 'region_code'),
  )

# Model for the smartup_legal_person_types table
class SmartupLegalPersonTypes(Base):
  __tablename__ = 'smartup_legal_person_types'
  
  pipe_id = Column(BigInteger, primary_key=True, nullable=False)
  person_group_code = Column(String(500), primary_key=True, nullable=False)
  person_id = Column(BigInteger, primary_key=True, nullable=False)
  person_type_code = Column(String(500), nullable=False)
  
  __table_args__ = (
    Index('smartup_legal_person_types_i1', 'pipe_id', 'person_type_code', 'person_group_code'),
    Index('smartup_legal_person_types_i2', 'pipe_id', 'person_type_code'),
    Index('smartup_legal_person_types_i3', 'pipe_id', 'person_group_code'),
    ForeignKeyConstraint(['pipe_id', 'person_id'], ['smartup_legal_persons.pipe_id', 'smartup_legal_persons.person_id'], ondelete='CASCADE')
  )

