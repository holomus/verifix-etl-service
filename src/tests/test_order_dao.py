from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from datetime import date, datetime
from daos import OrderDAO
from entities import OrderEntity, OrderProductEntity

# Replace with your actual PostgreSQL credentials
DATABASE_URL = "postgresql://verifix:verifix@localhost:5432/verifix_etl_db"

# Set up the engine and create all tables
engine = create_engine(DATABASE_URL)

# Set up a session for interacting with the database
Session = sessionmaker(bind=engine)

def test_insert(dao: OrderDAO, company_code: str):
  order = OrderEntity(
    deal_id=1001,
    filial_code="HELLO",
    external_id="WORLD",
    delivery_date=date(2024, 10, 20),
    booked_date=date(2024, 10, 15),
    total_amount=2500.75,
    room_name="Conference Hall 1",
    deal_time=datetime(2024, 10, 15, 14, 30),
    status="Confirmed",
    currency_code="USD",
    delivery_number="DLV20241020",
    manager_code="MGR123",
    products=[
        OrderProductEntity(
          product_unit_id=101,
          external_id="EXT987654",
          product_code="HELLO",
          product_name="WORLD",
          order_quant=2.0,
          product_price=500.00,
          margin_amount=50.00,
          margin_kind="fixed",
          margin_value=10.0,
          vat_percent=12.0,
          vat_amount=120.00,
          sold_amount=1120.00,
          inventory_kind="stock",
          price_type_code="PCT123",
          on_balance=True,
          card_code="CARD789",
          warehouse_code="WH001"
        )
    ]
  )

  dao.upsert_order(company_code, order)

def test_bulk_insert(dao: OrderDAO, company_code: str):
  order = OrderEntity(
    deal_id=10011,
    filial_code="FIL0011",
    external_id="EXT456789",
    delivery_date=date(2024, 10, 20),
    booked_date=date(2024, 10, 15),
    total_amount=2500.75,
    room_name="Conference Hall 1",
    deal_time=datetime(2024, 10, 15, 14, 30),
    status="Confirmed",
    currency_code="USD",
    delivery_number="DLV20241020",
    manager_code="MGR123",
    products=[
        OrderProductEntity(
          product_unit_id=2001223,
          external_id="EXT987654",
          product_code="PROD001",
          product_name="Projector",
          order_quant=2.0,
          product_price=500.00,
          margin_amount=50.00,
          margin_kind="fixe22d",
          margin_value=10.0,
          vat_percent=123.01,
          vat_amount=120.00,
          sold_amount=1120.00,
          inventory_kind="stock",
          price_type_code="PCT123",
          on_balance=True,
          card_code="CARD789",
          warehouse_code="WH001"
        )
    ]
  )

  dao.bulk_upsert_order(company_code, [order])

company_code = "ABC1234"

def test_delete(dao: OrderDAO, company_code: str):
  dao.delete_order(company_code, 10011)

with Session.begin() as session:
  dao = OrderDAO(session)

  # Run the test
  test_insert(dao, company_code)

  test_bulk_insert(dao, company_code)

  test_delete(dao, company_code)
