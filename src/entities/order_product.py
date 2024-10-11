from pydantic import BaseModel

class OrderProductEntity(BaseModel):
    external_id: str
    product_unit_id: int
    product_code: str
    product_name: str
    order_quant: float
    product_price: float
    margin_amount: float
    margin_kind: str
    margin_value: float
    vat_percent: float
    vat_amount: float
    sold_amount: float
    inventory_kind: str
    price_type_code: str
    on_balance: bool
    card_code: str
    warehouse_code: str
