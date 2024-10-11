from pydantic import BaseModel

class OrderActionEntity(BaseModel):
    external_id: str
    product_unit_id: str
    product_code: str
    product_name: str
    order_quant: float
    bonus_id: int
    action_name: str
