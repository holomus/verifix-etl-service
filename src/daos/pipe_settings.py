from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload
from sqlalchemy.dialects.postgresql import insert
from sqlalchemy import select, update, delete, and_
from entities import SmartupCredentials, NewSmartupCredentials
from models import SmartupPipes, SmartupCursors

class PipeSettingsDAO:
  ORDERS_CURSOR_KEY = "orders"
  ORDER_PRODUCTS_CURSOR_KEY = "order_products"
  CLIENTS_CURSOR_KEY = "clients"
  PRODUCTS_CURSOR_KEY = "products"

  def __init__(self, session: AsyncSession):
    self.session = session
  
  async def insert_pipe_settings(self, credentials: NewSmartupCredentials) -> int:
    insert_stmt = insert(SmartupPipes).values(**credentials.model_dump(exclude_none=True))
    insert_stmt = insert_stmt.returning(SmartupPipes.id)

    pipe_id = await self.session.scalar(insert_stmt)

    if pipe_id is None:
      raise RuntimeError('Insert should always return id, but nothing was returned')

    return pipe_id

  async def update_pipe_settings(self, credentials: SmartupCredentials) -> int:
    update_stmt = (
      update(SmartupPipes).
       where(SmartupPipes.id == credentials.id).
      values(credentials.model_dump(exclude_none=True, exclude_unset=True, exclude={ 'id', 'cursors' }))
    )

    result = await self.session.execute(update_stmt)

    return result.rowcount

  async def upsert_pipe_cursor(self, pipe_id: int, extraction_key: str, cursor: int) -> None:
    upsert_stmt = insert(SmartupCursors).values(pipe_id=pipe_id, extraction_key=extraction_key, last_cursor=cursor)
    upsert_stmt = upsert_stmt.on_conflict_do_update(constraint='smartup_cursors_pk', set_={
      name: upsert_stmt.excluded[name] for name in SmartupCursors.nonprimary_columns()
    })

    await self.session.execute(upsert_stmt)

  async def get_pipe_settings_by_id(self, id: int) -> SmartupCredentials | None:
    select_stmt = (
      select(SmartupPipes).options(selectinload(SmartupPipes.cursors)).
       where(SmartupPipes.id == id)
    )

    pipe = await self.session.scalar(select_stmt)

    if pipe is None:
      return None

    return SmartupCredentials.model_validate(pipe)

  async def get_all_pipe_settings(self) -> list[SmartupCredentials]:
    select_stmt = (
      select(SmartupPipes).options(selectinload(SmartupPipes.cursors))
    )

    settings = await self.session.scalars(select_stmt)
    
    settings = settings.all()

    return [
      SmartupCredentials.model_validate(setting) for setting in settings
    ]

  async def delete_pipe_settings_by_id(self, id: int) -> None:
    delete_stmt = (
      delete(SmartupPipes).
       where(SmartupPipes.id == id)
    )

    await self.session.execute(delete_stmt)