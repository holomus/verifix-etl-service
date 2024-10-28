from sqlalchemy import select, delete, and_
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.sql import func, distinct
from sqlalchemy.dialects.postgresql import insert
from models import SmartupOrders, SmartupOrderProducts, SmartupOrderProductAggregates, SmartupProducts
from entities import *

class OrderDAO:
  SMARTUP_ORDER_STATUS_ARCHIVED = 'A'

  def __init__(self, session: AsyncSession):
    self.session = session

  async def aggregate_order_products(self, pipe_id: int, product_unit_ids: list[int]):
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
          SmartupOrderProducts.product_code == SmartupProducts.code
        )
       ).scalar_subquery()
    )

    select_stmt = select(
      SmartupOrders.pipe_id,
      SmartupOrders.sales_manager_id,
      SmartupOrders.filial_code,
      SmartupOrders.room_id,
      SmartupOrders.person_id,
      SmartupOrderProducts.product_code,
      SmartupOrders.delivery_date,
      func.count(distinct(SmartupOrders.deal_id)),
      func.sum(SmartupOrderProducts.sold_amount),
      func.sum(SmartupOrderProducts.sold_quant),
      func.coalesce(func.sum(SmartupOrderProducts.sold_quant * subquery_stmt), 0),
    ).where(
      and_(
        SmartupOrderProducts.pipe_id == pipe_id,
        SmartupOrderProducts.product_unit_id.in_(product_unit_ids),
        SmartupOrders.status == self.SMARTUP_ORDER_STATUS_ARCHIVED,
        SmartupOrders.filial_code.is_not(None),
        SmartupOrderProducts.product_code.is_not(None)
      )
    ).join(SmartupOrders, 
      and_(
        SmartupOrders.pipe_id == pipe_id,
        SmartupOrders.deal_id == SmartupOrderProducts.deal_id
      )
    ).group_by(
      SmartupOrders.pipe_id,
      SmartupOrders.sales_manager_id,
      SmartupOrders.filial_code,
      SmartupOrders.room_id,
      SmartupOrders.person_id,
      SmartupOrderProducts.product_code,
      SmartupOrders.delivery_date
    )

    upsert_stmt = upsert_stmt.from_select([
      SmartupOrderProductAggregates.pipe_id,
      SmartupOrderProductAggregates.sales_manager_id,
      SmartupOrderProductAggregates.filial_code,
      SmartupOrderProductAggregates.room_id,
      SmartupOrderProductAggregates.person_id,
      SmartupOrderProductAggregates.product_code,
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

      await self.aggregate_order_products(pipe_id, product_unit_ids)

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

    # get unique products from order list
    # product_data_list = [*product_data_list.values()]

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

      await self.aggregate_order_products(pipe_id, product_unit_ids)

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
