from sqlalchemy import (
    Column, String, BigInteger, DateTime, Date, Numeric, Boolean, ForeignKeyConstraint
)
from sqlalchemy.orm import relationship
from .base import Base

# Model for the verifix.smartup_orders table
class SmartupOrders(Base):
  __tablename__ = 'smartup_orders'

  pipe_id = Column(BigInteger, primary_key=True, nullable=False)
  deal_id = Column(BigInteger, primary_key=True, nullable=False)
  filial_id = Column(BigInteger, nullable=False)                      
  deal_time = Column(DateTime, nullable=False)
  delivery_date = Column(Date, nullable=False)
  booked_date = Column(Date, nullable=False)
  room_id = Column(BigInteger, nullable=False)                        
  room_name = Column(String(1000), nullable=False)
  robot_id = Column(BigInteger, nullable=False)
  robot_name = Column(String(1000), nullable=False)
  sales_manager_id = Column(BigInteger, nullable=False)
  sales_manager_name = Column(String(1000), nullable=False)
  expeditor_id = Column(BigInteger)
  expeditor_name = Column(String(1000))
  person_id = Column(BigInteger, nullable=False)
  person_name = Column(String(1000), nullable=False)
  currency_id = Column(BigInteger, nullable=False)
  currency_code = Column(String(100), nullable=False)
  currency_name = Column(String(100), nullable=False)
  owner_person_id = Column(BigInteger)
  owner_person_name = Column(String(1000))
  manager_id = Column(BigInteger)
  manager_name = Column(String(1000))
  status = Column(String(100), nullable=False)
  
  # Relationship to order products
  products = relationship('SmartupOrderProducts', back_populates='order', cascade="all, delete")

# Model for the verifix.smartup_order_products table
class SmartupOrderProducts(Base):
  __tablename__ = 'smartup_order_products'

  pipe_id = Column(BigInteger, primary_key=True, nullable=False)
  product_unit_id = Column(BigInteger, primary_key=True, nullable=False)
  deal_id = Column(BigInteger, nullable=False)
  product_id = Column(BigInteger, nullable=False)
  product_name = Column(String(500), nullable=False)
  serial_number = Column(String(500))
  order_quant = Column(Numeric(20, 6), nullable=False)
  sold_quant = Column(Numeric(20, 6), nullable=False)
  return_quant = Column(Numeric(20, 6), nullable=False)
  inventory_kind = Column(String(10))
  on_balance = Column(Boolean)
  warehouse_id = Column(BigInteger)
  warehouse_name = Column(String(500))
  product_price = Column(Numeric(20, 6), nullable=False)
  margin_amount = Column(Numeric(20, 6), nullable=False)
  margin_amount_base = Column(Numeric(20, 6), nullable=False)
  margin_value = Column(Numeric(20, 6), nullable=False)
  margin_kind = Column(String(500), nullable=False)
  vat_amount = Column(Numeric(20, 6), nullable=False)
  vat_percent = Column(Numeric(20, 6), nullable=False)
  sold_amount = Column(Numeric(20, 6), nullable=False)
  sold_amount_base = Column(Numeric(20, 6), nullable=False)
  price_type_id = Column(BigInteger, nullable=False)
  price_type_name = Column(String(500), nullable=False)

  # Foreign Key to SmartupOrders
  order = relationship('SmartupOrders', back_populates='products')
  __table_args__ = (
      ForeignKeyConstraint(['pipe_id', 'deal_id'], ['smartup_orders.pipe_id', 'smartup_orders.deal_id'], ondelete='CASCADE'),
  )

class SmartupOrderProductAggregates(Base):
  __tablename__ = 'smartup_order_product_aggregates'
  
  pipe_id = Column(BigInteger, primary_key=True, nullable=False)
  sales_manager_id = Column(BigInteger, primary_key=True, nullable=False)
  filial_id = Column(BigInteger, primary_key=True, nullable=False)
  room_id = Column(BigInteger, primary_key=True, nullable=False)
  person_id = Column(BigInteger, primary_key=True, nullable=False)
  product_id = Column(BigInteger, primary_key=True, nullable=False)
  delivery_date = Column(Date, primary_key=True, nullable=False)
  deal_count = Column(Numeric(20, 6), nullable=False)
  sold_amount = Column(Numeric(20, 6),nullable=False)
  sold_quantity = Column(Numeric(20, 6), nullable=False)
  sold_weight = Column(Numeric(20, 6), nullable=False)