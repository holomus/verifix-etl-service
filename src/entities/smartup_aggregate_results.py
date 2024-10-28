from pydantic import BaseModel

class SmartupAggregateResult(BaseModel):
  sales_manager_id: int
  deal_count: float
  sold_amount: float
  sold_quantity: float
  sold_weight: float
  active_clients_count: float