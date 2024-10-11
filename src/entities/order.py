from datetime import date, datetime
from typing import List, Optional
from pydantic import BaseModel
from .order_product import OrderProductEntity
from .order_gift import OrderGiftEntity
from .order_action import OrderActionEntity
from .order_consignment import OrderConsignmentEntity

class OrderEntity(BaseModel):
    filial_code: str
    external_id: str
    deal_id: int
    delivery_date: date
    booked_date: date
    total_amount: float
    room_name: str
    deal_time: datetime
    status: str
    currency_code: str
    delivery_number: str
    manager_code: str
    products: Optional[List[OrderProductEntity]] = []
    gifts: Optional[List[OrderGiftEntity]] = []
    actions: Optional[List[OrderActionEntity]] = []
    consignments: Optional[List[OrderConsignmentEntity]] = []
