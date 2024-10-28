from datetime import date, datetime
from pydantic import BaseModel, field_serializer

class SmartupFilialFilters(BaseModel):
  filial_code: str

class SmartupFilters(BaseModel):
  filial_codes: list[SmartupFilialFilters] | None = None
  begin_created_on: datetime | None = None
  end_created_on: datetime | None = None
  begin_modified_on: datetime | None = None
  end_modified_on: datetime | None = None

  @field_serializer('begin_created_on', 'end_created_on', 'begin_modified_on', 'end_modified_on')
  def serialize_datetime(self, dt: datetime):
    return dt.strftime("%d.%m.%Y")
