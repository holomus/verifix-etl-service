from pydantic import BaseModel, field_validator
from datetime import date, datetime

class OrderProductEntity(BaseModel):
  product_unit_id: int
  external_id: str | None
  product_code: str | None
  product_local_code: str | None
  product_name: str
  serial_number: str | None
  expiry_date: date | None
  order_quant: float
  sold_quant: float
  return_quant: float
  inventory_kind: str | None
  on_balance: bool | None
  card_code: str | None
  warehouse_code: str | None
  product_price: float
  margin_amount: float
  margin_value: float
  margin_kind: str
  vat_amount: float
  vat_percent: float
  sold_amount: float
  price_type_code: str | None

  @field_validator('expiry_date', mode='before')
  @classmethod
  def parse_date(cls, value):
    if isinstance(value, str):
      # Parse string with the custom format "DD.MM.YYYY"
      return datetime.strptime(value, "%d.%m.%Y").date()
    return value