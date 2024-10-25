from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload
from sqlalchemy.dialects.postgresql import insert
from sqlalchemy import select, update, delete
from entities import SmartupCredentials, NewSmartupCredentials
from models import SmartupPipes, SmartupFilialCredentials
from datetime import datetime

class PipeSettingsDAO:
  def __init__(self, session: AsyncSession):
    self.session = session
  
  async def insert_pipe_settings(self, credentials: NewSmartupCredentials) -> int:
    if len(credentials.filials) == 0:
      raise RuntimeError('Filial credentials list must have at least one entry')

    insert_stmt = insert(SmartupPipes).values(**credentials.model_dump(exclude_none=True, exclude={
      'filials': True
    }))
    insert_stmt = insert_stmt.returning(SmartupPipes.id)

    pipe_id = await self.session.scalar(insert_stmt)

    if pipe_id is None:
      raise RuntimeError('Insert should always return id, but nothing was returned')

    filial_credentials = [
      {
        'pipe_id': pipe_id,
        **filial.model_dump()
      }
      for filial in credentials.filials
    ]

    insert_stmt = insert(SmartupFilialCredentials)

    await self.session.execute(insert_stmt, filial_credentials)

    return pipe_id

  async def update_pipe_settings(self, credentials: SmartupCredentials) -> int:
    if len(credentials.filials) == 0:
      raise RuntimeError('Filial credentials list must have at least one entry')

    update_stmt = (
      update(SmartupPipes).
       where(SmartupPipes.id == credentials.id).
      values(credentials.model_dump(exclude_none=True, exclude_unset=True, exclude={ 'id', 'filials' }))
    )

    result = await self.session.execute(update_stmt)

    filial_credentials = [
      {
        'pipe_id': credentials.id,
        **filial.model_dump()
      }
      for filial in credentials.filials
    ]

    upsert_stmt = insert(SmartupFilialCredentials)
    upsert_stmt = upsert_stmt.on_conflict_do_update(constraint='smartup_pipe_credentials_pk', set_={
      name: upsert_stmt.excluded[name] for name in SmartupFilialCredentials.nonprimary_columns()
    })

    await self.session.execute(upsert_stmt, filial_credentials)

    return result.rowcount

  async def update_pipe_last_executed(self, id: int, execution_time: datetime) -> None:
    update_stmt = (
      update(SmartupPipes).
       where(SmartupPipes.id == id).
      values(last_execution_time = execution_time)
    )

    await self.session.execute(update_stmt)

  async def get_pipe_settings_by_id(self, id: int) -> SmartupCredentials | None:
    select_stmt = (
      select(SmartupPipes).options(selectinload(SmartupPipes.filials)).
       where(SmartupPipes.id == id)
    )

    pipe = await self.session.scalar(select_stmt)

    if pipe is None:
      return None

    return SmartupCredentials.model_validate(pipe)

  async def get_all_pipe_settings(self) -> list[SmartupCredentials]:
    select_stmt = (
      select(SmartupPipes).options(selectinload(SmartupPipes.filials))
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