from pydantic import BaseModel, ConfigDict, Field
from typing import Annotated

# Pydantic model for SmartupLegalPersonTypes
class SmartupLegalPersonTypeEntity(BaseModel):
  model_config = ConfigDict(from_attributes=True)

  group_id: Annotated[int, Field(serialization_alias='person_group_id')]
  type_id: Annotated[int, Field(serialization_alias='person_type_id')]

# Pydantic model for SmartupLegalPersons
class SmartupLegalPersonEntity(BaseModel):
  model_config = ConfigDict(from_attributes=True)
  
  person_id: int
  name: str
  short_name: str
  region_id: int | None
  type_binds: list[SmartupLegalPersonTypeEntity] | None = []

