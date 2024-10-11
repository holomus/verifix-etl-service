from pydantic import BaseModel
from datetime import date

class OrderConsignmentEntity(BaseModel):
    external_id: str
    consignment_unit_id: int
    consignment_date: date
    consignment_amount: float
