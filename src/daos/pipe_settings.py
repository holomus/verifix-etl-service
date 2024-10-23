from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, insert, update, delete
from entities import SmartupCredentials, NewSmartupCredentials
from models import SmartupPipeSettings
from datetime import datetime

class PipeSettingsDAO:
  def __init__(self, session: AsyncSession):
    self.session = session
  
  async def insert_pipe_settings(self, credentials: NewSmartupCredentials) -> int:
    insert_stmt = insert(SmartupPipeSettings).values(**credentials.model_dump(exclude_none=True))
    insert_stmt = insert_stmt.returning(SmartupPipeSettings.id)

    user_id = await self.session.scalar(insert_stmt)

    if user_id is None:
      raise RuntimeError('Insert should always return id, but nothing was returned')

    return user_id

  async def update_pipe_settings(self, credentials: SmartupCredentials) -> int:
    update_stmt = (
      update(SmartupPipeSettings).
       where(SmartupPipeSettings.id == credentials.id).
      values(credentials.model_dump(exclude_none=True, exclude_unset=True, exclude={ 'id' }))
    )

    result = await self.session.execute(update_stmt)

    return result.rowcount

  async def update_pipe_last_executed(self, id: int, execution_time: datetime) -> None:
    update_stmt = (
      update(SmartupPipeSettings).
       where(SmartupPipeSettings.id == id).
      values(last_execution_time = execution_time)
    )

    await self.session.execute(update_stmt)

  async def get_pipe_settings_by_id(self, id: int) -> SmartupCredentials | None:
    select_stmt = (
      select(SmartupPipeSettings).
       where(SmartupPipeSettings.id == id)
    )

    settings = await self.session.scalar(select_stmt)

    if settings is None:
      return None

    return SmartupCredentials.model_validate(settings)

  async def get_all_pipe_settings(self) -> list[SmartupCredentials]:
    select_stmt = (
      select(SmartupPipeSettings)
    )

    settings = await self.session.scalars(select_stmt)
    
    settings = settings.all()

    return [
      SmartupCredentials.model_validate(setting) for setting in settings
    ]

  async def delete_pipe_settings_by_id(self, id: int) -> None:
    delete_stmt = (
      delete(SmartupPipeSettings).
       where(SmartupPipeSettings.id == id)
    )

    await self.session.execute(delete_stmt)