from datetime import date, datetime
from typing import List, Optional
from .order_product import OrderProductEntity
from .order_gift import OrderGiftEntity
from .order_action import OrderActionEntity
from .order_consignment import OrderConsignmentEntity

class OrderEntity:
    def __init__(
        self,
        filial_code: str,
        external_id: str,
        deal_id: int,
        delivery_date: date,
        booked_date: date,
        total_amount: float,
        room_name: str,
        deal_time: datetime,
        status: str,
        currency_code: str,
        delivery_number: str,
        manager_code: str,
        order_products: Optional[List[OrderProductEntity]] = None,
        order_gifts: Optional[List[OrderGiftEntity]] = None,
        order_actions: Optional[List[OrderActionEntity]] = None,
        order_consignments: Optional[List[OrderConsignmentEntity]] = None,
    ):
        self.filial_code = filial_code
        self.external_id = external_id
        self.deal_id = deal_id
        self.delivery_date = delivery_date
        self.booked_date = booked_date
        self.total_amount = total_amount
        self.room_name = room_name
        self.deal_time = deal_time
        self.status = status
        self.currency_code = currency_code
        self.delivery_number = delivery_number
        self.manager_code = manager_code
        self.order_products = order_products if order_products else []
        self.order_gifts = order_gifts if order_gifts else []
        self.order_actions = order_actions if order_actions else []
        self.order_consignments = order_consignments if order_consignments else []
