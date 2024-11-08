from datetime import datetime
from pydantic import BaseModel, field_serializer

class SmartupDealFilters(BaseModel):
  begin_deal_month: datetime | None = None
  end_deal_month: datetime | None = None
  deal_ids: list[int] | None = None

  @field_serializer('begin_deal_month', 'end_deal_month')
  def serialize_datetime(self, dt: datetime):
    return dt.strftime("%d.%m.%Y")
