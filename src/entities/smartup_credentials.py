from pydantic import BaseModel, ConfigDict
from datetime import datetime

class SmartupCredentials(BaseModel):
  model_config = ConfigDict(from_attributes=True)

  id: int | None = None
  company_code: str
  host: str
  client_id: str
  client_secret: str
  last_update_time: datetime | None = None