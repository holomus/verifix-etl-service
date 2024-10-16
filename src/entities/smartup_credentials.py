from pydantic import BaseModel

class SmartupCredentials(BaseModel):
  host: str
  client_id: str
  client_secret: str