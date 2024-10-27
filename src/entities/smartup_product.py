from pydantic import BaseModel, ConfigDict, Field
from typing import Annotated

# Pydantic model for SmartupProductTypes
class SmartupProductTypeEntity(BaseModel):
  model_config = ConfigDict(from_attributes=True)

  group_code: Annotated[str | None, Field(alias='product_group_code')]
  type_code: Annotated[str | None, Field(alias='product_type_code')]

# Pydantic model for SmartupProducts
class SmartupProductEntity(BaseModel):
  model_config = ConfigDict(from_attributes=True)
  
  product_id: int
  code: str | None
  name: str
  weight_netto: float | None
  weight_brutto: float | None
  litr: float | None
  type_binds: list[SmartupProductTypeEntity] | None = []
