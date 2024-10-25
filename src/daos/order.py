from sqlalchemy import select, delete, and_
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.sql import func, distinct
from sqlalchemy.dialects.postgresql import insert
from models.core import *
from entities import *

class OrderDAO:
  SMARTUP_ORDER_STATUS_ARCHIVED = 'A'

  def __init__(self, session: AsyncSession):
    self.session = session

  async def aggregate_order_products(self, company_code: str, product_unit_ids: list[int]):
    upsert_stmt = insert(SmartupOrderProductAggregates)
    upsert_stmt = upsert_stmt.on_conflict_do_update(constraint='smartup_order_product_aggregates_pk', set_={
      name: upsert_stmt.excluded[name] for name in SmartupOrderProductAggregates.nonprimary_columns()
    })

    select_stmt = select(
      SmartupOrders.company_code,
      SmartupOrders.sales_manager_id,
      SmartupOrders.filial_code,
      SmartupOrders.room_id,
      SmartupOrders.person_id,
      SmartupOrderProducts.product_code,
      SmartupOrders.delivery_date,
      func.count(distinct(SmartupOrders.deal_id)),
      func.sum(SmartupOrderProducts.sold_amount),
      func.sum(SmartupOrderProducts.sold_quant),
      func.sum(SmartupOrderProducts.sold_quant), # TODO: multiply by product weight
    ).where(
      and_(
        SmartupOrderProducts.company_code == company_code,
        SmartupOrderProducts.product_unit_id.in_(product_unit_ids),
        SmartupOrders.status == self.SMARTUP_ORDER_STATUS_ARCHIVED,
        SmartupOrders.filial_code.is_not(None),
        SmartupOrderProducts.product_code.is_not(None)
      )
    ).join(SmartupOrders, 
      and_(
        SmartupOrders.company_code == company_code,
        SmartupOrders.deal_id == SmartupOrderProducts.deal_id
      )
    ).group_by(
      SmartupOrders.company_code,
      SmartupOrders.sales_manager_id,
      SmartupOrders.filial_code,
      SmartupOrders.room_id,
      SmartupOrders.person_id,
      SmartupOrderProducts.product_code,
      SmartupOrders.delivery_date
    )

    upsert_stmt = upsert_stmt.from_select([
      SmartupOrderProductAggregates.company_code,
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

  async def upsert_order(self, company_code: str, order: OrderEntity) -> None:
    order_data = order.model_dump(exclude={
      "products"
    })

    upsert_order_stmt = insert(SmartupOrders).values(company_code=company_code).values(**order_data)
    upsert_order_stmt = upsert_order_stmt.on_conflict_do_update(constraint='smartup_orders_pk', set_={ 
      name: upsert_order_stmt.excluded[name] for name in SmartupOrders.nonprimary_columns()
    })

    await self.session.execute(upsert_order_stmt)

    if order.products is not None and len(order.products) > 0:
      product_data_list = [
        {
          **product.model_dump(),
          'company_code': company_code,
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
        SmartupOrderProducts.company_code == company_code,
        SmartupOrderProducts.deal_id == order.deal_id,
        SmartupOrderProducts.product_unit_id.not_in(product_unit_ids)
      ))

      await self.session.execute(delete_old_products_stmt)

      await self.aggregate_order_products(company_code, product_unit_ids)

  async def bulk_upsert_orders(self, company_code: str, orders: list[OrderEntity]) -> None:
    if len(orders) == 0: 
      return

    order_data_list = [
      {
        **order.model_dump(exclude={
          "products"
        }),
        'company_code': company_code
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
        'company_code': company_code,
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
        SmartupOrderProducts.company_code == company_code,
        SmartupOrderProducts.deal_id.in_(deal_ids),
        SmartupOrderProducts.product_unit_id.not_in(product_unit_ids)
      ))

      await self.session.execute(delete_old_products_stmt)

      await self.aggregate_order_products(company_code, product_unit_ids)

  async def get_order_by_id(self, company_code: str, deal_id: int) -> OrderEntity:
    order = await self.session.execute(
      select(SmartupOrders).where(and_(SmartupOrders.company_code == company_code, SmartupOrders.deal_id == deal_id))
    )
    order = order.first()
    return OrderEntity.model_validate(order)

  async def delete_order(self, company_code: str, deal_id: int) -> None:
    await self.session.execute(
      delete(SmartupOrders).where(and_(SmartupOrders.company_code == company_code, SmartupOrders.deal_id == deal_id))
    )
