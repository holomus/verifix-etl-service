from datetime import date, datetime
from pydantic import BaseModel, field_validator, ValidationInfo
from typing import Annotated
from annotated_types import Len

class SmartupAggregateFilter(BaseModel):
  period_begin: date
  period_end: date
  host: str
  company_code: str
  sales_manager_ids: Annotated[list[int], Len(min_length=1)]
  filial_ids: list[int] = []
  room_ids: list[int] = []
  client_ids: list[int] = []
  product_ids: list[int] = []
  product_type_ids: list[int] = []
  product_group_id: int | None = None
  client_type_ids: list[int] = []
  client_group_id: int | None = None

  @field_validator('product_group_id', mode='before')
  @classmethod
  def validate_product_group_code(cls, value, info: ValidationInfo):
    if len(info.data['product_type_ids']) == 0:
      return None
    return value

  @field_validator('client_group_id', mode='before')
  @classmethod
  def validate_client_group_code(cls, value, info: ValidationInfo):
    if len(info.data['client_type_ids']) == 0:
      return None
    return value
  
  @field_validator('period_begin', 'period_end', mode='before')
  @classmethod
  def parse_date(cls, value):
    if isinstance(value, str):
      # Parse string with the custom format "DD.MM.YYYY"
      return datetime.strptime(value, "%d.%m.%Y").date()
    return value