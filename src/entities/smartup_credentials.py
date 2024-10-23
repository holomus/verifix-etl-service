from pydantic import BaseModel, ConfigDict
from datetime import datetime

class NewSmartupCredentials(BaseModel):
  model_config = ConfigDict(from_attributes=True)

  company_code: str
  filial_codes: list[str] = []
  host: str
  client_id: str
  client_secret: str
  last_execution_time: datetime | None = None

class SmartupCredentials(NewSmartupCredentials):
  id: int