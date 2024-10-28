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
  filial_codes: list[str] = []
  room_ids: list[str] = []
  client_ids: list[int] = []
  product_codes: list[str] = []
  product_type_codes: list[str] = []
  product_group_code: str | None = None
  client_type_codes: list[str] = []
  client_group_code: str | None = None

  @field_validator('product_group_code', mode='before')
  @classmethod
  def validate_product_group_code(cls, value, info: ValidationInfo):
    if len(info.data['product_type_codes']) == 0:
      return None
    return value

  @field_validator('client_group_code', mode='before')
  @classmethod
  def validate_client_group_code(cls, value, info: ValidationInfo):
    if len(info.data['client_type_codes']) == 0:
      return None
    return value