
from daos import PipeSettingsDAO
from db import Session
from core.pipes import SmartupPipe
from entities import SmartupCredentials, SmartupDealFilters
from .scheduler_instance import scheduler

def start_extraction_between(credentials: SmartupCredentials, filters: SmartupDealFilters, reload_clients: bool = False, reload_products: bool = False):
  pipe = SmartupPipe(credentials)
  scheduler.add_job(pipe.extract_deals_between, args=[filters, reload_clients, reload_products], id=str(credentials.id))

def start_extraction_on(credentials: SmartupCredentials):
  pipe = SmartupPipe(credentials)
  scheduler.add_job(pipe.extract_data, id=str(credentials.id))

async def start_extraction_on_all_pipes():
  async with Session.begin() as session:
    dao = PipeSettingsDAO(session)
    settings = await dao.get_all_pipe_settings()

  for setting in settings:
    start_extraction_on(setting)

