from fastapi import APIRouter
from db import Session
from daos import OrderDAO
from entities import SmartupAggregateResult, SmartupAggregateFilter

router = APIRouter(
  prefix='/aggregates/smartup',
  tags=['aggregates']
)

@router.post('/', response_model=list[SmartupAggregateResult])
async def load_smartup_order_aggregate_results(filters: SmartupAggregateFilter) -> list[SmartupAggregateResult]:
  async with Session.begin() as session:
    dao = OrderDAO(session)
    return await dao.get_order_aggregates(filters)