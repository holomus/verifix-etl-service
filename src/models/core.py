"""A collection of ORM sqlalchemy models"""

from sqlalchemy import Column, Integer, String, Float, ForeignKey, Date, Boolean
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class Order(Base):
    __tablename__ = 'orders'
    
    filial_code = Column(String)
    external_id = Column(String)
    deal_id = Column(Integer, primary_key=True)
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
    order_gifts = relationship("OrderGift", back_populates="order")
    order_actions = relationship("OrderAction", back_populates="order")
    order_consignments = relationship("OrderConsignment", back_populates="order")

class OrderProduct(Base):
    __tablename__ = 'order_products'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    order_id = Column(Integer, ForeignKey('orders.id'))
    external_id = Column(String)
    product_unit_id = Column(Integer)
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

    # Relationship
    details = relationship("Detail", back_populates="order_product")
    order = relationship("Order", back_populates="order_products")

class Detail(Base):
    __tablename__ = 'details'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    order_product_id = Column(Integer, ForeignKey('order_products.id'))
    expiry_date = Column(Date)
    card_code = Column(String)
    batch_number = Column(String)
    sold_quant = Column(Float)

    # Relationship
    order_product = relationship("OrderProduct", back_populates="details")

class OrderGift(Base):
    __tablename__ = 'order_gifts'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    order_id = Column(Integer, ForeignKey('orders.id'))
    external_id = Column(String)
    product_unit_id = Column(Integer)
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

    order = relationship("Order", back_populates="order_gifts")

class OrderAction(Base):
    __tablename__ = 'order_actions'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    order_id = Column(Integer, ForeignKey('orders.id'))
    external_id = Column(String)
    product_unit_id = Column(Integer)
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
    bonus_id = Column(String)
    action_name = Column(String)

    order = relationship("Order", back_populates="order_actions")

class OrderConsignment(Base):
    __tablename__ = 'order_consignments'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    order_id = Column(Integer, ForeignKey('orders.id'))
    external_id = Column(String)
    consignment_unit_id = Column(String)
    consignment_date = Column(Date)
    consignment_amount = Column(Float)

    order = relationship("Order", back_populates="order_consignments")