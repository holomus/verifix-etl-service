from pydantic import BaseModel, ConfigDict
from datetime import datetime
from typing import Annotated
from annotated_types import Len

class SmartupFilialCredentials(BaseModel):
  model_config = ConfigDict(from_attributes=True)

  filial_code: str
  client_id: str
  client_secret: str
  is_head_filial: bool = False

class NewSmartupCredentials(BaseModel):
  model_config = ConfigDict(from_attributes=True)

  company_code: str
  host: str
  filials: Annotated[list[SmartupFilialCredentials], Len(min_length=1)]
  last_execution_time: datetime | None = None

class SmartupCredentials(NewSmartupCredentials):
  id: int