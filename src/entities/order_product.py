from pydantic import BaseModel

class OrderProductEntity(BaseModel):
  product_unit_id: int
  external_id: str | None
  product_code: str | None
  product_name: str | None
  order_quant: float | None
  product_price: float | None
  margin_amount: float | None
  margin_kind: str | None
  margin_value: float | None
  vat_percent: float | None
  vat_amount: float | None
  sold_amount: float | None
  inventory_kind: str | None
  price_type_code: str | None
  on_balance: bool | None
  card_code: str | None
  warehouse_code: str | None
