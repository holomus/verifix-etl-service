
from daos import PipeSettingsDAO
from db import Session
from core.pipes import SmartupPipe
from entities import SmartupCredentials
from .scheduler_instance import scheduler

def start_extraction_on(credentials: SmartupCredentials):
  pipe = SmartupPipe(credentials)
  scheduler.add_job(pipe.extract_data_since, id=credentials.company_code)

async def start_extraction_on_all_pipes():
  async with Session.begin() as session:
    dao = PipeSettingsDAO(session)
    settings = await dao.get_all_pipe_settings()

  for setting in settings:
    start_extraction_on(setting)

