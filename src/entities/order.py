from datetime import date, datetime
from pydantic import BaseModel, ConfigDict, field_validator
from .order_product import OrderProductEntity

class OrderEntity(BaseModel):
  model_config = ConfigDict(from_attributes=True)

  deal_id: int
  filial_code: str | None
  external_id: str | None
  delivery_date: date | None
  booked_date: date | None
  total_amount: float | None
  room_name: str | None
  deal_time: datetime | None
  status: str | None
  currency_code: str | None
  delivery_number: str | None
  manager_code: str | None
  products: list[OrderProductEntity] | None = []

  @field_validator('deal_time', mode='before')
  @classmethod
  def parse_datetime(cls, value):
    if isinstance(value, str):
      # Parse string with the custom format "DD.MM.YYYY HH:MM:SS"
      return datetime.strptime(value, "%d.%m.%Y %H:%M:%S")
    return value

  @field_validator('booked_date', 'delivery_date', mode='before')
  @classmethod
  def parse_date(cls, value):
    if isinstance(value, str):
      # Parse string with the custom format "DD.MM.YYYY"
      return datetime.strptime(value, "%d.%m.%Y").date()
    return value
