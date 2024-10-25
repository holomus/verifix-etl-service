from pydantic import BaseModel, ConfigDict

# Pydantic model for SmartupProducts
class SmartupProduct(BaseModel):
  model_config = ConfigDict(from_attributes=True)
  
  product_id: int
  code: str | None
  name: str
  weight_netto: float | None
  weight_brutto: float | None
  litr: float | None

# Pydantic model for SmartupProductTypes
class SmartupProductType(BaseModel):
  model_config = ConfigDict(from_attributes=True)

  product_group_code: str
  product_id: int
  product_type_code: str
