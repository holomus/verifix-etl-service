"""A collection of ORM sqlalchemy models"""

from sqlalchemy import Column, Integer, String, Float, ForeignKey, Date, Boolean
from sqlalchemy.orm import relationship

from .base import Base

class Order(Base):
    __tablename__ = 'orders'
    
    company_code = Column(String, primary_key=True)
    deal_id = Column(Integer, primary_key=True)
    filial_code = Column(String)
    external_id = Column(String)
    subfilial_code = Column(String)
    deal_time = Column(Date)
    delivery_number = Column(String)
    delivery_date = Column(Date)
    booked_date = Column(Date)
    total_amount = Column(Float)
    room_id = Column(Integer)
    room_code = Column(String)
    room_name = Column(String)
    robot_code = Column(String)
    lap_code = Column(String)
    sales_manager_id = Column(Integer)
    sales_manager_code = Column(String)
    sales_manager_name = Column(String)
    expeditor_id = Column(Integer)
    expeditor_code = Column(String)
    expeditor_name = Column(String)
    person_id = Column(Integer)
    person_code = Column(String)
    person_name = Column(String)
    person_local_code = Column(String)
    person_latitude = Column(Float)
    person_longitude = Column(Float)
    person_tin = Column(String)
    currency_code = Column(String)
    owner_person_code = Column(String)
    manager_code = Column(String)
    van_code = Column(String)
    contract_code = Column(String)
    contract_number = Column(String)
    invoice_number = Column(String)
    payment_type_code = Column(String)
    visit_payment_type_code = Column(String)
    note = Column(String)
    deal_note = Column(String)
    status = Column(String)
    with_marking = Column(Boolean)
    self_shipment = Column(Boolean)
    total_weight_netto = Column(Float)
    total_weight_brutto = Column(Float)
    total_litre = Column(Float)

    # Relationships
    order_products = relationship("OrderProduct", back_populates="order")

class OrderProduct(Base):
    __tablename__ = 'order_products'

    company_code = Column(String, primary_key=True)
    deal_id = Column(Integer, primary_key=True)
    product_unit_id = Column(Integer, primary_key=True)
    external_id = Column(String)
    product_code = Column(String)
    product_local_code = Column(String)
    product_name = Column(String)
    serial_number = Column(String)
    expiry_date = Column(Date)
    order_quant = Column(Float)
    sold_quant = Column(Float)
    return_quant = Column(Float)
    inventory_kind = Column(String)
    on_balance = Column(Boolean)
    card_code = Column(String)
    warehouse_code = Column(String)
    product_price = Column(Float)
    margin_amount = Column(Float)
    margin_value = Column(Float)
    margin_kind = Column(String)
    vat_amount = Column(Float)
    vat_percent = Column(Float)
    sold_amount = Column(Float)
    price_type_code = Column(String)

from sqlalchemy import (
    create_engine, Column, String, BigInteger, DateTime, Date, Numeric, Boolean, ForeignKey
)
from sqlalchemy.orm import declarative_base, relationship

Base = declarative_base()

# Model for the verifix.smartup_pipe_settings table
class SmartupPipeSettings(Base):
    __tablename__ = 'smartup_pipe_settings'
    __table_args__ = {'schema': 'verifix'}

    id = Column(BigInteger, primary_key=True, autoincrement=True)
    company_code = Column(String(100), nullable=False)
    host = Column(String(500), nullable=False)
    client_id = Column(String(500), nullable=False)
    client_secret = Column(String(500), nullable=False)

# Model for the verifix.smartup_orders table
class SmartupOrders(Base):
    __tablename__ = 'smartup_orders'
    __table_args__ = {'schema': 'verifix'}

    company_code = Column(String(100), primary_key=True, nullable=False)
    deal_id = Column(BigInteger, primary_key=True, nullable=False)
    filial_code = Column(String(500))
    external_id = Column(String(500))
    subfilial_code = Column(String(500))
    deal_time = Column(DateTime)
    delivery_number = Column(String(500))
    delivery_date = Column(Date)
    booked_date = Column(Date)
    total_amount = Column(Numeric(20, 6))
    room_id = Column(BigInteger)
    room_code = Column(String(500))
    room_name = Column(String(500))
    robot_code = Column(String(500))
    lap_code = Column(String(500))
    sales_manager_id = Column(BigInteger)
    sales_manager_code = Column(String(500))
    sales_manager_name = Column(String(1000))
    expeditor_id = Column(BigInteger)
    expeditor_code = Column(String(500))
    expeditor_name = Column(String(1000))
    person_id = Column(BigInteger)
    person_code = Column(String(500))
    person_name = Column(String(1000))
    person_local_code = Column(String(500))
    person_latitude = Column(Numeric(20, 15))
    person_longitude = Column(Numeric(20, 15))
    person_tin = Column(String(500))
    currency_code = Column(String(500))
    owner_person_code = Column(String(500))
    manager_code = Column(String(500))
    van_code = Column(String(500))
    contract_code = Column(String(500))
    contract_number = Column(String(500))
    invoice_number = Column(String(500))
    payment_type_code = Column(String(500))
    visit_payment_type_code = Column(String(500))
    note = Column(String(1000))
    deal_note = Column(String(1000))
    status = Column(String(10))
    with_marking = Column(Boolean)
    self_shipment = Column(Boolean)
    total_weight_netto = Column(Numeric(20, 6))
    total_weight_brutto = Column(Numeric(20, 6))
    total_litre = Column(Numeric(20, 6))

    # Relationship to order products
    products = relationship('SmartupOrderProducts', back_populates='order', cascade="all, delete")

# Model for the verifix.smartup_order_products table
class SmartupOrderProducts(Base):
    __tablename__ = 'smartup_order_products'
    __table_args__ = {'schema': 'verifix'}

    company_code = Column(String(100), primary_key=True, nullable=False)
    deal_id = Column(BigInteger, primary_key=True, nullable=False)
    product_unit_id = Column(BigInteger, primary_key=True, nullable=False)
    external_id = Column(String(500))
    product_code = Column(String(500))
    product_local_code = Column(String(500))
    product_name = Column(String(500))
    serial_number = Column(String(500))
    expiry_date = Column(Date)
    order_quant = Column(Numeric(20, 6))
    sold_quant = Column(Numeric(20, 6))
    return_quant = Column(Numeric(20, 6))
    inventory_kind = Column(Numeric(20, 6))
    on_balance = Column(Boolean)
    card_code = Column(String(500))
    warehouse_code = Column(String(500))
    product_price = Column(Numeric(20, 6))
    margin_amount = Column(Numeric(20, 6))
    margin_value = Column(Numeric(20, 6))
    margin_kind = Column(String(500))
    vat_amount = Column(Numeric(20, 6))
    vat_percent = Column(Numeric(20, 6))
    sold_amount = Column(Numeric(20, 6))
    price_type_code = Column(String(500))

    # Foreign Key to SmartupOrders
    order = relationship('SmartupOrders', back_populates='products')
    __table_args__ = (
        ForeignKey('verifix.smartup_orders.company_code', 'verifix.smartup_orders.deal_id', ondelete='CASCADE'),
    )

# Setup the engine and Base metadata
engine = create_engine('postgresql://user:password@localhost/dbname')
Base.metadata.create_all(engine)
