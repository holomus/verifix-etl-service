from datetime import date, datetime
from typing import List, Optional
from pydantic import BaseModel
from .order_product import OrderProductEntity

class OrderEntity(BaseModel):
    deal_id: int
    filial_code: str
    external_id: str
    delivery_date: date
    booked_date: date
    total_amount: float
    room_name: str
    deal_time: datetime
    status: str
    currency_code: str
    delivery_number: str
    manager_code: str
    products: List[OrderProductEntity] | None = []
