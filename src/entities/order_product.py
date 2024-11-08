from pydantic import BaseModel, ConfigDict, field_validator
from datetime import date, datetime

class OrderProductEntity(BaseModel):
  model_config = ConfigDict(from_attributes=True)

  product_unit_id: int
  deal_id: int
  product_id: int
  product_name: str
  serial_number: str | None
  order_quant: float
  sold_quant: float
  return_quant: float
  inventory_kind: str | None
  on_balance: bool | None
  warehouse_id: int | None
  warehouse_name: str | None
  product_price: float
  margin_amount: float
  margin_amount_base: float
  margin_value: float
  margin_kind: str
  vat_amount: float
  vat_percent: float
  sold_amount: float
  sold_amount_base: float
  price_type_id: int
  price_type_name: str