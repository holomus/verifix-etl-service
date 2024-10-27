from sqlalchemy import delete, and_
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.dialects.postgresql import insert
from models import SmartupLegalPersons, SmartupLegalPersonTypes
from entities import SmartupLegalPersonEntity

class ClientDAO:
  def __init__(self, session: AsyncSession):
    self.session = session

  async def bulk_upsert_clients(self, pipe_id: int, clients: list[SmartupLegalPersonEntity]) -> None:
    if len(clients) == 0: 
      return

    client_data_list = [
      {
        **client.model_dump(exclude={
          "type_binds"
        }),
        'pipe_id': pipe_id
      }
      for client in clients
    ]
    
    upsert_order_stmt = insert(SmartupLegalPersons)
    upsert_order_stmt = upsert_order_stmt.on_conflict_do_update(constraint='smartup_legal_persons_pk', set_={ 
      name: upsert_order_stmt.excluded[name] for name in SmartupLegalPersons.nonprimary_columns()
    })

    await self.session.execute(upsert_order_stmt, client_data_list)

    type_bind_data_list = [
      {
        **type_bind.model_dump(by_alias=True),
        'pipe_id': pipe_id,
        'person_id': client.person_id,
      }
      for client in clients for type_bind in (client.type_binds or []) 
      if type_bind.group_code is not None and type_bind.type_code is not None
    ]

    if len(type_bind_data_list) > 0:
      upsert_product_stmt = insert(SmartupLegalPersonTypes)
      upsert_product_stmt = upsert_product_stmt.on_conflict_do_update(constraint='smartup_legal_person_types_pk', set_={
        name: upsert_product_stmt.excluded[name] for name in SmartupLegalPersonTypes.nonprimary_columns()
      })

      await self.session.execute(upsert_product_stmt, type_bind_data_list)

      person_ids = [
        client.person_id for client in clients
      ]

      person_group_codes = [
        type_bind.group_code for client in clients for type_bind in (client.type_binds or [])
        if type_bind.group_code is not None
      ]

      delete_old_products_stmt = delete(SmartupLegalPersonTypes).where(and_(
        SmartupLegalPersonTypes.pipe_id == pipe_id,
        SmartupLegalPersonTypes.person_id.in_(person_ids),
        SmartupLegalPersonTypes.person_group_code.not_in(person_group_codes)
      ))

      await self.session.execute(delete_old_products_stmt)