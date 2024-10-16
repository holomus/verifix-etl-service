from datetime import date, datetime
from pydantic import BaseModel, field_serializer

class SmartupOrderFilialFilters(BaseModel):
  filial_code: str

class SmartupOrderFilters(BaseModel):
  filial_codes: list[SmartupOrderFilialFilters] | None = None
  begin_deal_date: date | None = None
  end_deal_date: date | None = None
  delivery_date: date | None = None
  begin_created_on: datetime | None = None
  end_created_on: datetime | None = None
  begin_modified_on: datetime | None = None
  end_modified_on: datetime | None = None

  @field_serializer('begin_created_on', 'end_created_on', 'begin_modified_on', 'end_modified_on', when_used='json')
  def serialize_datetime(self, dt: datetime):
      return dt.strftime("%d.%m.%Y %H:%M:%S")
  
  @field_serializer('begin_deal_date', 'end_deal_date', 'delivery_date', when_used='json')
  def serialize_date(self, dt: date):
      return dt.strftime("%d.%m.%Y")
