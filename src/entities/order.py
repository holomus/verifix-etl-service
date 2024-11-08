from datetime import date, datetime
from pydantic import BaseModel, ConfigDict, field_validator
from .order_product import OrderProductEntity

class OrderEntity(BaseModel):
  model_config = ConfigDict(from_attributes=True)

  deal_id: int
  filial_id: int
  deal_time: datetime
  delivery_date: date
  booked_date: date
  room_id: int
  room_name: str
  robot_id: int
  robot_name: str
  sales_manager_id: int
  sales_manager_name: str
  expeditor_id: int | None
  expeditor_name: str | None
  person_id: int
  person_name: str
  currency_id: int
  currency_code: str
  currency_name: str
  owner_person_id: int | None
  owner_person_name: str | None
  manager_id: int | None
  manager_name: str | None
  status: str
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
