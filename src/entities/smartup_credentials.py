from pydantic import BaseModel, ConfigDict, field_validator

class NewSmartupCredentials(BaseModel):
  model_config = ConfigDict(from_attributes=True)

  company_code: str
  host: str
  client_id: str
  client_secret: str

class UpdateSmartupCredentials(NewSmartupCredentials):
  id: int

class SmartupCredentials(NewSmartupCredentials):
  id: int
  cursors: dict[str, int]

  @field_validator('cursors', mode='before')
  @classmethod
  def convert_cursors(cls, value):
      if isinstance(value, list):
          return {
            cursor.extraction_key: cursor.last_cursor
            for cursor in value
          }
      return value