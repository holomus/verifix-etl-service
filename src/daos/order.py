from sqlalchemy import select, delete, and_, case
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.sql import func, distinct
from sqlalchemy.dialects.postgresql import insert
from models import (
  SmartupOrders, 
  SmartupOrderProducts, 
  SmartupOrderProductAggregates, 
  SmartupProducts, 
  SmartupProductTypes, 
  SmartupPipes,
  SmartupLegalPersons,
  SmartupLegalPersonTypes
)
from entities import OrderEntity, SmartupAggregateFilter, SmartupAggregateResult

class OrderDAO:
  SMARTUP_ORDER_STATUS_ARCHIVED = 'A'

  def __init__(self, session: AsyncSession):
    self.session = session

  async def _aggregate_order_products(self, pipe_id: int, product_unit_ids: list[int]):
    upsert_stmt = insert(SmartupOrderProductAggregates)
    upsert_stmt = upsert_stmt.on_conflict_do_update(constraint='smartup_order_product_aggregates_pk', set_={
      name: upsert_stmt.excluded[name] for name in SmartupOrderProductAggregates.nonprimary_columns()
    })

    subquery_stmt = (
      select(
        SmartupProducts.weight_netto
      ).where(
        and_(
          SmartupOrderProducts.pipe_id == SmartupProducts.pipe_id,
          SmartupOrderProducts.product_id == SmartupProducts.product_id
        )
       ).scalar_subquery()
    )

    select_stmt = select(
      SmartupOrders.pipe_id,
      SmartupOrders.sales_manager_id,
      SmartupOrders.filial_id,
      SmartupOrders.room_id,
      SmartupOrders.person_id,
      SmartupOrderProducts.product_id,
      SmartupOrders.delivery_date,
      func.count(distinct(case((SmartupOrderProducts.sold_amount > 0, SmartupOrders.deal_id), else_=None))),
      func.sum(SmartupOrderProducts.sold_amount),
      func.sum(SmartupOrderProducts.sold_quant),
      func.coalesce(func.sum(SmartupOrderProducts.sold_quant * subquery_stmt), 0),
    ).where(
      and_(
        SmartupOrderProducts.pipe_id == pipe_id,
        SmartupOrderProducts.product_unit_id.in_(product_unit_ids),
        SmartupOrders.status == self.SMARTUP_ORDER_STATUS_ARCHIVED
      )
    ).join(SmartupOrders, 
      and_(
        SmartupOrders.pipe_id == pipe_id,
        SmartupOrders.deal_id == SmartupOrderProducts.deal_id
      )
    ).group_by(
      SmartupOrders.pipe_id,
      SmartupOrders.sales_manager_id,
      SmartupOrders.filial_id,
      SmartupOrders.room_id,
      SmartupOrders.person_id,
      SmartupOrderProducts.product_id,
      SmartupOrders.delivery_date
    )

    upsert_stmt = upsert_stmt.from_select([
      SmartupOrderProductAggregates.pipe_id,
      SmartupOrderProductAggregates.sales_manager_id,
      SmartupOrderProductAggregates.filial_id,
      SmartupOrderProductAggregates.room_id,
      SmartupOrderProductAggregates.person_id,
      SmartupOrderProductAggregates.product_id,
      SmartupOrderProductAggregates.delivery_date,
      SmartupOrderProductAggregates.deal_count,
      SmartupOrderProductAggregates.sold_amount,
      SmartupOrderProductAggregates.sold_quantity,
      SmartupOrderProductAggregates.sold_weight
    ], select=select_stmt)

    await self.session.execute(upsert_stmt)

  async def upsert_order(self, pipe_id: int, order: OrderEntity) -> None:
    order_data = order.model_dump(exclude={
      "products"
    })

    upsert_order_stmt = insert(SmartupOrders).values(pipe_id=pipe_id).values(**order_data)
    upsert_order_stmt = upsert_order_stmt.on_conflict_do_update(constraint='smartup_orders_pk', set_={ 
      name: upsert_order_stmt.excluded[name] for name in SmartupOrders.nonprimary_columns()
    })

    await self.session.execute(upsert_order_stmt)

    if order.products is not None and len(order.products) > 0:
      product_data_list = [
        {
          **product.model_dump(),
          'pipe_id': pipe_id,
          'deal_id': order.deal_id,
        } for product in order.products or []
      ]
      
      upsert_product_stmt = insert(SmartupOrderProducts)
      upsert_product_stmt = upsert_product_stmt.on_conflict_do_update(constraint='smartup_order_products_pk', set_={
        name: upsert_product_stmt.excluded[name] for name in SmartupOrderProducts.nonprimary_columns()
      })

      await self.session.execute(upsert_product_stmt, product_data_list)

      product_unit_ids = [
        product.product_unit_id for product in order.products or []
      ]

      delete_old_products_stmt = delete(SmartupOrderProducts).where(and_(
        SmartupOrderProducts.pipe_id == pipe_id,
        SmartupOrderProducts.deal_id == order.deal_id,
        SmartupOrderProducts.product_unit_id.not_in(product_unit_ids)
      ))

      await self.session.execute(delete_old_products_stmt)

      await self._aggregate_order_products(pipe_id, product_unit_ids)

  async def bulk_upsert_orders(self, pipe_id: int, orders: list[OrderEntity]) -> None:
    if len(orders) == 0: 
      return

    order_data_list = [
      {
        **order.model_dump(exclude={
          "products"
        }),
        'pipe_id': pipe_id
      }
      for order in orders
    ]
    
    upsert_order_stmt = insert(SmartupOrders)
    upsert_order_stmt = upsert_order_stmt.on_conflict_do_update(constraint='smartup_orders_pk', set_={ 
      name: upsert_order_stmt.excluded[name] for name in SmartupOrders.nonprimary_columns()
    })

    await self.session.execute(upsert_order_stmt, order_data_list)

    product_data_list = [
      {
        **product.model_dump(),
        'pipe_id': pipe_id,
        'deal_id': order.deal_id,
      }
      for order in orders for product in (order.products or [])
    ]

    if len(product_data_list) > 0:
      upsert_product_stmt = insert(SmartupOrderProducts)
      upsert_product_stmt = upsert_product_stmt.on_conflict_do_update(constraint='smartup_order_products_pk', set_={
        name: upsert_product_stmt.excluded[name] for name in SmartupOrderProducts.nonprimary_columns()
      })

      await self.session.execute(upsert_product_stmt, product_data_list)

      deal_ids = [
        order.deal_id for order in orders
      ]

      product_unit_ids = [
        product.product_unit_id for order in orders for product in (order.products or [])
      ]

      delete_old_products_stmt = delete(SmartupOrderProducts).where(and_(
        SmartupOrderProducts.pipe_id == pipe_id,
        SmartupOrderProducts.deal_id.in_(deal_ids),
        SmartupOrderProducts.product_unit_id.not_in(product_unit_ids)
      ))

      await self.session.execute(delete_old_products_stmt)

      await self._aggregate_order_products(pipe_id, product_unit_ids)

  async def get_order_by_id(self, pipe_id: int, deal_id: int) -> OrderEntity:
    order = await self.session.execute(
      select(SmartupOrders).where(and_(SmartupOrders.pipe_id == pipe_id, SmartupOrders.deal_id == deal_id))
    )
    order = order.first()
    return OrderEntity.model_validate(order)

  async def delete_order(self, pipe_id: int, deal_id: int) -> None:
    await self.session.execute(
      delete(SmartupOrders).where(and_(SmartupOrders.pipe_id == pipe_id, SmartupOrders.deal_id == deal_id))
    )

  async def get_order_aggregates(self, filter: SmartupAggregateFilter) -> list[SmartupAggregateResult]:
    pipe_select_stmt = (
      select(
        SmartupPipes.id
      ).where(and_(
          SmartupPipes.company_code == filter.company_code,
          SmartupPipes.host == filter.host
        )
      ).scalar_subquery()
    )

    select_stmt = (
      select(
        SmartupOrderProductAggregates.sales_manager_id,
        func.sum(SmartupOrderProductAggregates.deal_count).label('deal_count'),
        func.sum(SmartupOrderProductAggregates.sold_amount).label('sold_amount'),
        func.sum(SmartupOrderProductAggregates.sold_quantity).label('sold_quantity'),
        func.sum(SmartupOrderProductAggregates.sold_weight).label('sold_weight'),
        func.count(distinct(case(
          (SmartupOrderProductAggregates.sold_amount > 0, SmartupOrderProductAggregates.person_id),
          else_=None
        ))).label('active_clients_count')
      ).where(
        and_(
          SmartupOrderProductAggregates.pipe_id == pipe_select_stmt,
          SmartupOrderProductAggregates.delivery_date >= filter.period_begin,
          SmartupOrderProductAggregates.delivery_date <= filter.period_end
        )
      ).group_by(
        SmartupOrderProductAggregates.sales_manager_id
      )
    )

    if len(filter.filial_ids) > 0:
      select_stmt = select_stmt.where(SmartupOrderProductAggregates.filial_id.in_(filter.filial_ids))

    if len(filter.room_ids) > 0:
      select_stmt = select_stmt.where(SmartupOrderProductAggregates.room_id.in_(filter.room_ids))

    if len(filter.sales_manager_ids) > 0:
      select_stmt = select_stmt.where(SmartupOrderProductAggregates.sales_manager_id.in_(filter.sales_manager_ids))

    if len(filter.client_ids) > 0:
      select_stmt = select_stmt.where(SmartupOrderProductAggregates.person_id.in_(filter.client_ids))

    if len(filter.product_ids) > 0:
      select_stmt = select_stmt.where(SmartupOrderProductAggregates.product_id.in_(filter.product_ids))

    if len(filter.product_type_ids) > 0 and filter.product_group_id is not None:
      product_filter_smtm = (
        select(
          SmartupProducts.code
        ).where(
          and_(
            SmartupProductTypes.pipe_id == pipe_select_stmt,
            SmartupProductTypes.product_group_id == filter.product_group_id,
            SmartupProductTypes.product_type_id.in_(filter.product_type_ids)
          )
        )
      )

      select_stmt = select_stmt.where(SmartupOrderProductAggregates.product_id.in_(product_filter_smtm))

    if len(filter.client_type_ids) > 0 and filter.client_group_id is not None:
      client_filter_smtm = (
        select(
          SmartupLegalPersons.code
        ).where(
          and_(
            SmartupLegalPersonTypes.pipe_id == pipe_select_stmt,
            SmartupLegalPersonTypes.person_group_id == filter.client_group_id,
            SmartupLegalPersonTypes.person_type_id.in_(filter.client_type_ids)
          )
        )
      )

      select_stmt = select_stmt.where(SmartupOrderProductAggregates.person_id.in_(client_filter_smtm))

    aggregate_results = await self.session.execute(select_stmt)

    aggregate_results = aggregate_results.mappings().all()

    return [
      SmartupAggregateResult.model_validate(result) for result in aggregate_results
    ]
