from sqlalchemy.orm import sessionmaker
from sqlalchemy import select, insert, update, delete
from typing import List
from models.core import *
from entities import *

class OrderDAO:
  def __init__(self, engine):
    Session = sessionmaker(bind=engine)
    self.session = Session()

  def add_order(self, order: OrderEntity):
    order = Order()
    self.session.add(order)
    self.session.commit()
    return order

  def bulk_add_order(self, orders: List[OrderEntity]):
    pass

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

  def delete_order(self, order_id):
    self.session.execute(
      delete(Order).where(Order.id == order_id)
    )
    self.session.commit()
