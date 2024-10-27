from pydantic import BaseModel, ConfigDict, Field
from typing import Annotated

# Pydantic model for SmartupLegalPersonTypes
class SmartupLegalPersonTypeEntity(BaseModel):
  model_config = ConfigDict(from_attributes=True)

  group_code: Annotated[str | None, Field(alias='person_group_code')]
  type_code: Annotated[str | None, Field(alias='person_type_code')]

# Pydantic model for SmartupLegalPersons
class SmartupLegalPersonEntity(BaseModel):
  model_config = ConfigDict(from_attributes=True)
  
  person_id: int
  name: str
  short_name: str
  code: str | None
  region_code: str | None
  type_binds: list[SmartupLegalPersonTypeEntity] | None = []

