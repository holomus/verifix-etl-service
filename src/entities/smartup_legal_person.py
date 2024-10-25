from pydantic import BaseModel, ConfigDict

# Pydantic model for SmartupLegalPersons
class SmartupLegalPerson(BaseModel):
  model_config = ConfigDict(from_attributes=True)
  
  person_id: int
  name: str
  short_name: str
  code: str | None
  region_code: str | None

# Pydantic model for SmartupLegalPersonTypes
class SmartupLegalPersonType(BaseModel):
  model_config = ConfigDict(from_attributes=True)

  person_group_code: str
  person_id: int
  person_type_code: str
