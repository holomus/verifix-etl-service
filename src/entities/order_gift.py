from pydantic import BaseModel

class OrderGiftEntity(BaseModel):
    external_id: str
    product_unit_id: int
    product_code: str
    product_name: str
    order_quant: float
    warehouse_code: str
