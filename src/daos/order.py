from sqlalchemy.orm import Session
from sqlalchemy import select, update, delete
from sqlalchemy.dialects.postgresql import insert
from typing import List
from models.core import *
from entities import *

class OrderDAO:
  def __init__(self, session: Session):
    self.session = session

  def upsert_order(self, order: OrderEntity):
    order_data = order.model_dump(exclude_none=True, exclude_unset=True, exclude={
      "order_products": True,
      "order_gifts": True,
      "order_actions": True,
      "order_consignments": True,
    })
    
    upsert_order_stmt = insert(Order).values(**order_data)
    upsert_order_stmt = upsert_order_stmt.on_conflict_do_update(constraint='orders_pk', set_={ 
      name: upsert_order_stmt.excluded[name] for name in OrderEntity.model_fields.keys() 
    })

    self.session.execute(upsert_order_stmt)

    upsert_product_stmt = insert(OrderProduct)

    product_data_list = [
      product.model_dump(exclude_none=True, exclude_unset=True) for product in order.products or []
    ]
    
    upsert_product_stmt = upsert_product_stmt.values(product_data_list)
    upsert_product_stmt = upsert_product_stmt.on_conflict_do_update(constraint='order_products_pk', set_={
      name: upsert_product_stmt.excluded[name] for name in OrderProductEntity.model_fields.keys() 
    })

    # TODO: add delete ununused products

    self.session.execute(upsert_product_stmt)

  def bulk_upsert_order(self, orders: List[OrderEntity]):
    order_data_list = [
      order.model_dump(exclude_none=True, exclude_unset=True, exclude={
        "order_products": True,
        "order_gifts": True,
        "order_actions": True,
        "order_consignments": True,
      }) for order in orders
    ]
    
    upsert_order_stmt = insert(Order).values(order_data_list)
    upsert_order_stmt = upsert_order_stmt.on_conflict_do_update(constraint='orders_pk', set_={ 
      name: upsert_order_stmt.excluded[name] for name in OrderEntity.model_fields.keys() 
    })

    self.session.execute(upsert_order_stmt)

    upsert_product_stmt = insert(OrderProduct)

    product_data_list = [
      product.model_dump(exclude_none=True, exclude_unset=True)
      for order in orders for product in (order.products or [])
    ]
    
    upsert_product_stmt = upsert_product_stmt.values(product_data_list)
    upsert_product_stmt = upsert_product_stmt.on_conflict_do_update(constraint='order_products_pk', set_={
      name: upsert_product_stmt.excluded[name] for name in OrderProductEntity.model_fields.keys() 
    })

    # TODO: add delete ununused products

    self.session.execute(upsert_product_stmt)

  def get_order_by_id(self, order_id: Integer):
    return self.session.execute(
      select(Order).where(Order.id == order_id)
    ).first()

  def update_order(self, order: OrderEntity):
    pass
    # self.session.execute(
    #   update(Order)
    #     .where(Order.id == order.deal_id)
    # )
    # order = self.session.query(Order).filter(Order.id == order_id).first()
    # if order:
    #   for key, value in update_data.items():
    #     setattr(order, key, value)
    #   self.session.commit()

  def delete_order(self, order_id: Integer):
    self.session.execute(
      delete(Order).where(Order.id == order_id)
    )
