from sqlalchemy import Column, BigInteger, String, Numeric, Index, ForeignKeyConstraint
from sqlalchemy.orm import relationship
from .base import Base

# Model for the smartup_products table
class SmartupProducts(Base):
  __tablename__ = 'smartup_products'
  
  pipe_id = Column(BigInteger, primary_key=True, nullable=False)
  product_id = Column(BigInteger, primary_key=True, nullable=False)
  code = Column(String(500))
  name = Column(String(500), nullable=False)
  weight_netto = Column(Numeric(10, 4))
  weight_brutto = Column(Numeric(10, 4))
  litr = Column(Numeric(10, 4))


# Model for the smartup_product_types table
class SmartupProductTypes(Base):
  __tablename__ = 'smartup_product_types'
  
  pipe_id = Column(BigInteger, primary_key=True, nullable=False)
  product_group_id = Column(BigInteger, primary_key=True, nullable=False)
  product_id = Column(BigInteger, primary_key=True, nullable=False)
  product_type_id = Column(BigInteger, nullable=False)
  
  __table_args__ = (
    Index('smartup_product_types_i1', 'pipe_id', 'product_type_id', 'product_group_id'),
    Index('smartup_product_types_i2', 'pipe_id', 'product_type_id'),
    Index('smartup_product_types_i3', 'pipe_id', 'product_group_id'),
    ForeignKeyConstraint(['pipe_id', 'product_id'], ['smartup_products.pipe_id', 'smartup_products.product_id'], ondelete='CASCADE')
  )
