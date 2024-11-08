from pydantic import BaseModel, ConfigDict, Field
from typing import Annotated

# Pydantic model for SmartupProductTypes
class SmartupProductTypeEntity(BaseModel):
  model_config = ConfigDict(from_attributes=True)

  group_id: Annotated[int, Field(serialization_alias='product_group_id')]
  type_id: Annotated[int, Field(serialization_alias='product_type_id')]

# Pydantic model for SmartupProducts
class SmartupProductEntity(BaseModel):
  model_config = ConfigDict(from_attributes=True)
  
  product_id: int
  name: str
  weight_netto: float | None
  weight_brutto: float | None
  litr: float | None
  type_binds: list[SmartupProductTypeEntity] | None = []
