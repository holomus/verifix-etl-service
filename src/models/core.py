from sqlalchemy import (
    Column, String, BigInteger, DateTime, Date, Numeric, Boolean, ForeignKeyConstraint
)
from sqlalchemy.orm import relationship
from .base import Base

# Model for the verifix.smartup_orders table
class SmartupOrders(Base):
  __tablename__ = 'smartup_orders'

  company_code = Column(String(100), primary_key=True, nullable=False)
  deal_id = Column(BigInteger, primary_key=True, nullable=False)      
  filial_code = Column(String(500))                                   
  external_id = Column(String(500))                                   
  subfilial_code = Column(String(500))                                
  deal_time = Column(DateTime, nullable=False)                        
  delivery_number = Column(String(500))                               
  delivery_date = Column(Date, nullable=False)                        
  booked_date = Column(Date, nullable=False)                          
  total_amount = Column(Numeric(20, 6), nullable=False)               
  room_id = Column(BigInteger, nullable=False)                        
  room_code = Column(String(500))                                     
  room_name = Column(String(500), nullable=False)                     
  robot_code = Column(String(500))                                    
  lap_code = Column(String(500))                                      
  sales_manager_id = Column(BigInteger, nullable=False)               
  sales_manager_code = Column(String(500))                            
  sales_manager_name = Column(String(1000), nullable=False)           
  expeditor_id = Column(BigInteger)                                   
  expeditor_code = Column(String(500))                                
  expeditor_name = Column(String(1000))                               
  person_id = Column(BigInteger, nullable=False)                      
  person_code = Column(String(500))                                   
  person_name = Column(String(1000), nullable=False)                  
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
  status = Column(String(10), nullable=False)            
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

  company_code = Column(String(100), primary_key=True, nullable=False)
  product_unit_id = Column(BigInteger, primary_key=True, nullable=False)
  deal_id = Column(BigInteger, nullable=False)                          
  external_id = Column(String(500))                                     
  product_code = Column(String(500))                                    
  product_local_code = Column(String(500))                              
  product_name = Column(String(500), nullable=False)                    
  serial_number = Column(String(500))                                   
  expiry_date = Column(Date)                                            
  order_quant = Column(Numeric(20, 6), nullable=False)                  
  sold_quant = Column(Numeric(20, 6), nullable=False)                   
  return_quant = Column(Numeric(20, 6), nullable=False)                 
  inventory_kind = Column(String(500))                                  
  on_balance = Column(Boolean)                                          
  card_code = Column(String(500))                                       
  warehouse_code = Column(String(500))                                  
  product_price = Column(Numeric(20, 6), nullable=False)                
  margin_amount = Column(Numeric(20, 6), nullable=False)                
  margin_value = Column(Numeric(20, 6), nullable=False)                 
  margin_kind = Column(String(500), nullable=False)                     
  vat_amount = Column(Numeric(20, 6), nullable=False)                   
  vat_percent = Column(Numeric(20, 6), nullable=False)                  
  sold_amount = Column(Numeric(20, 6), nullable=False)                  
  price_type_code = Column(String(500))                 

  # Foreign Key to SmartupOrders
  order = relationship('SmartupOrders', back_populates='products')
  __table_args__ = (
      ForeignKeyConstraint(['company_code', 'deal_id'], ['smartup_orders.company_code', 'smartup_orders.deal_id'], ondelete='CASCADE'),
  )

class SmartupOrderProductAggregates(Base):
  __tablename__ = 'smartup_order_product_aggregates'
  
  company_code = Column(String(100), primary_key=True, nullable=False)
  sales_manager_id = Column(BigInteger, primary_key=True, nullable=False)
  filial_code = Column(String(500), primary_key=True, nullable=False)
  room_id = Column(BigInteger, primary_key=True, nullable=False)
  person_id = Column(BigInteger, primary_key=True, nullable=False)
  product_code = Column(String(500), primary_key=True, nullable=False)
  delivery_date = Column(Date, primary_key=True, nullable=False)
  deal_id = Column(BigInteger, nullable=False)
  sold_amount = Column(Numeric(20, 6),nullable=False)
  sold_quantity = Column(Numeric(20, 6), nullable=False)
  sold_weight = Column(Numeric(20, 6), nullable=False)