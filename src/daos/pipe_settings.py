from sqlalchemy.orm import Session
from sqlalchemy import select, insert, update, delete
from entities import SmartupCredentials
from models import SmartupPipeSettings
from datetime import datetime

class PipeSettingsDAO:
  def __init__(self, session: Session):
    self.session = session
  
  def insert_pipe_setting(self, credentials: SmartupCredentials) -> int:
    insert_stmt = insert(SmartupPipeSettings).values(**credentials.model_dump(exclude_none=True, exclude_unset=True))
    insert_stmt = insert_stmt.returning(SmartupPipeSettings.id)

    user_id = self.session.scalar(insert_stmt)

    if user_id is None:
      raise RuntimeError('Insert should always return id, but nothing was returned')

    return user_id

  def update_pipe_last_executed(self, id: int) -> None:
    update_stmt = (
      update(SmartupPipeSettings).
       where(SmartupPipeSettings.id == id).
      values(last_update_time = datetime.now())
    )

    self.session.execute(update_stmt)

  def get_pipe_setting_by_id(self, id: int) -> SmartupCredentials | None:
    select_stmt = (
      select(SmartupPipeSettings).
       where(SmartupPipeSettings.id == id)
    )

    settings = self.session.scalar(select_stmt)

    if settings is None:
      return None

    return SmartupCredentials.model_validate(settings)

  def get_all_pipe_settings(self) -> list[SmartupCredentials]:
    select_stmt = (
      select(SmartupPipeSettings)
    )

    settings = self.session.scalars(select_stmt).all()

    return [
      SmartupCredentials.model_validate(setting) for setting in settings
    ]

  def delete_pipe_setting_by_id(self, id: int) -> None:
    delete_stmt = (
      delete(SmartupPipeSettings).
       where(SmartupPipeSettings.id == id)
    )

    self.session.execute(delete_stmt)