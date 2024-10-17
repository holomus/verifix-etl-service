from sqlalchemy.orm import Session
from sqlalchemy import select, delete, and_
from sqlalchemy.dialects.postgresql import insert
from models.core import *
from entities import *

class OrderDAO:
  def __init__(self, session: Session):
    self.session = session

  def upsert_order(self, company_code: str, order: OrderEntity) -> None:
    order_data = order.model_dump(exclude_none=True, exclude_unset=True, exclude={
      "products"
    })

    upsert_order_stmt = insert(SmartupOrders).values(company_code=company_code).values(**order_data)
    upsert_order_stmt = upsert_order_stmt.on_conflict_do_update(constraint='smartup_orders_pk', set_={ 
      name: upsert_order_stmt.excluded[name] for name in SmartupOrders.nonprimary_columns()
    })

    self.session.execute(upsert_order_stmt)

    product_data_list = [
      {
        **product.model_dump(exclude_none=True, exclude_unset=True),
        'company_code': company_code,
        'deal_id': order.deal_id,
      } for product in order.products or []
    ]
    
    upsert_product_stmt = insert(SmartupOrderProducts).values(product_data_list)
    upsert_product_stmt = upsert_product_stmt.on_conflict_do_update(constraint='smartup_order_products_pk', set_={
      name: upsert_product_stmt.excluded[name] for name in SmartupOrderProducts.nonprimary_columns()
    })

    self.session.execute(upsert_product_stmt)

    product_ids = [
      product.product_unit_id for product in order.products or []
    ]

    delete_old_products_stmt = delete(SmartupOrderProducts).where(and_(
      SmartupOrderProducts.company_code == company_code,
      SmartupOrderProducts.deal_id == order.deal_id,
      SmartupOrderProducts.product_unit_id.not_in(product_ids)
    ))

    self.session.execute(delete_old_products_stmt)

  def bulk_upsert_orders(self, company_code: str, orders: list[OrderEntity]) -> None:
    order_data_list = [
      {
        **order.model_dump(exclude_none=True, exclude_unset=True, exclude={
          "products"
        }),
        'company_code': company_code
      }
      for order in orders
    ]
    
    upsert_order_stmt = insert(SmartupOrders).values(order_data_list)
    upsert_order_stmt = upsert_order_stmt.on_conflict_do_update(constraint='smartup_orders_pk', set_={ 
      name: upsert_order_stmt.excluded[name] for name in SmartupOrders.nonprimary_columns()
    })

    self.session.execute(upsert_order_stmt)

    product_data_list = [
      {
        **product.model_dump(exclude_none=True, exclude_unset=True),
        'company_code': company_code,
        'deal_id': order.deal_id,
      }
      for order in orders for product in (order.products or [])
    ]
    
    upsert_product_stmt = insert(SmartupOrderProducts).values(product_data_list)
    upsert_product_stmt = upsert_product_stmt.on_conflict_do_update(constraint='smartup_order_products_pk', set_={
      name: upsert_product_stmt.excluded[name] for name in SmartupOrderProducts.nonprimary_columns()
    })

    self.session.execute(upsert_product_stmt)

    deal_ids = [
      order.deal_id for order in orders
    ]

    product_ids = [
      product.product_unit_id for order in orders for product in (order.products or [])
    ]

    delete_old_products_stmt = delete(SmartupOrderProducts).where(and_(
      SmartupOrderProducts.company_code == company_code,
      SmartupOrderProducts.deal_id.in_(deal_ids),
      SmartupOrderProducts.product_unit_id.not_in(product_ids)
    ))

    self.session.execute(delete_old_products_stmt)

  def get_order_by_id(self, company_code: str, deal_id: int) -> OrderEntity:
    order = self.session.execute(
      select(SmartupOrders).where(and_(SmartupOrders.company_code == company_code, SmartupOrders.deal_id == deal_id))
    ).first() 
    return OrderEntity.model_validate(order)

  def delete_order(self, company_code: str, deal_id: int) -> None:
    self.session.execute(
      delete(SmartupOrders).where(and_(SmartupOrders.company_code == company_code, SmartupOrders.deal_id == deal_id))
    )
