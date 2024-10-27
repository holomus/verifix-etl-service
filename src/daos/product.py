from sqlalchemy import delete, and_
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.dialects.postgresql import insert
from models import SmartupProducts, SmartupProductTypes
from entities import SmartupProductEntity

class ProductDAO:
  def __init__(self, session: AsyncSession):
    self.session = session

  async def bulk_upsert_products(self, pipe_id: int, products: list[SmartupProductEntity]) -> None:
    if len(products) == 0: 
      return

    product_data_list = [
      {
        **client.model_dump(exclude={
          "type_binds"
        }),
        'pipe_id': pipe_id
      }
      for client in products
    ]
    
    upsert_order_stmt = insert(SmartupProducts)
    upsert_order_stmt = upsert_order_stmt.on_conflict_do_update(constraint='smartup_products_pk', set_={ 
      name: upsert_order_stmt.excluded[name] for name in SmartupProducts.nonprimary_columns()
    })

    await self.session.execute(upsert_order_stmt, product_data_list)

    type_bind_data_list = [
      {
        **type_bind.model_dump(by_alias=True),
        'pipe_id': pipe_id,
        'product_id': product.product_id,
      }
      for product in products for type_bind in (product.type_binds or []) 
      if type_bind.group_code is not None and type_bind.type_code is not None
    ]

    if len(type_bind_data_list) > 0:
      upsert_product_stmt = insert(SmartupProductTypes)
      upsert_product_stmt = upsert_product_stmt.on_conflict_do_update(constraint='smartup_product_types_pk', set_={
        name: upsert_product_stmt.excluded[name] for name in SmartupProductTypes.nonprimary_columns()
      })

      await self.session.execute(upsert_product_stmt, type_bind_data_list)

      product_ids = [
        product.product_id for product in products
      ]

      product_group_codes = [
        type_bind.group_code for product in products for type_bind in (product.type_binds or [])
        if type_bind.group_code is not None
      ]

      delete_old_products_stmt = delete(SmartupProductTypes).where(and_(
        SmartupProductTypes.pipe_id == pipe_id,
        SmartupProductTypes.product_id.in_(product_ids),
        SmartupProductTypes.product_group_code.not_in(product_group_codes)
      ))

      await self.session.execute(delete_old_products_stmt)