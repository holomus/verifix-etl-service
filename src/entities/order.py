from datetime import date, datetime
from pydantic import BaseModel, ConfigDict, field_validator
from .order_product import OrderProductEntity

class OrderEntity(BaseModel):
  model_config = ConfigDict(from_attributes=True)

  deal_id: int
  filial_id: int
  external_id: str | None
  subfilial_code: str | None
  deal_time: datetime
  delivery_number: str | None
  delivery_date: date
  booked_date: date
  total_amount: float
  room_id: int
  room_code: str | None
  room_name: str
  robot_code: str | None
  lap_code: str | None
  sales_manager_id: int
  sales_manager_code: str | None
  sales_manager_name: str
  expeditor_id: int | None
  expeditor_code: str | None
  expeditor_name: str | None
  person_id: int
  person_code: str | None
  person_name: str
  person_local_code: str | None
  person_latitude: float | None
  person_longitude: float | None
  person_tin: str | None
  currency_code: str | None
  owner_person_code: str | None
  manager_code: str | None
  van_code: str | None
  contract_code: str | None
  contract_number: str | None
  invoice_number: str | None
  payment_type_code: str | None
  visit_payment_type_code: str | None
  note: str | None
  deal_note: str | None
  status: str
  with_marking: bool
  self_shipment: bool
  total_weight_netto: float | None
  total_weight_brutto: float | None
  total_litre: float | None
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
