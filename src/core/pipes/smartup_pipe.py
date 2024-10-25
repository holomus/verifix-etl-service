
from datetime import datetime, timedelta
from entities import SmartupCredentials, SmartupOrderFilters
from clients import SmartupExtractionClient, SmartupAuth
from daos import OrderDAO, PipeSettingsDAO
from db import Session
from sqlalchemy.ext.asyncio import AsyncSession

class SmartupPipe:
  _credentials: SmartupCredentials
  _pagination_timedelta: timedelta = timedelta(days=1)

  def __init__(self, credentials: SmartupCredentials):
    self._credentials = credentials

  # load pipe settings from smartup_pipe_settings and you can work with this
  async def extract_data_between(self, auth: SmartupAuth, session: AsyncSession, begin_load_time: datetime, end_load_time: datetime):
    if self._credentials.id is None:
      raise ValueError('when extracting data from SmartUp credentials must have an id')

    filters = SmartupOrderFilters(begin_modified_on=begin_load_time, end_modified_on=end_load_time)

    orders = await SmartupExtractionClient.extractDeals(auth, filters)

    orderDao = OrderDAO(session)

    await orderDao.bulk_upsert_orders(pipe_id=self._credentials.id, orders=orders)

  async def extract_data_since(self, start_load_time: datetime | None = None):
    if len(self._credentials.filials) == 0:
      raise RuntimeError('when extracting data from SmartUp at least one filial credential should be provided')

    filial_tokens = []
    head_token = ""

    for filial in self._credentials.filials:
      token = await SmartupExtractionClient.get_access_token(self._credentials.host, filial)
      filial_tokens.append(token)

      if filial.is_head_filial:
        head_token = token
    
    if head_token == "":
      head_token = filial_tokens[0]

    start_load_time = start_load_time or self._credentials.last_execution_time or datetime.utcnow() - 2 * self._pagination_timedelta

    end_load_time = datetime.utcnow()

    while start_load_time < end_load_time:
      # Extract data for each time window of _pagination_timedelta
      next_end_time = min(start_load_time + self._pagination_timedelta, end_load_time)
      
      async with Session.begin() as session:
        pipeDao = PipeSettingsDAO(session)

        for token in filial_tokens:
          auth = SmartupAuth(self._credentials.host, token)
          await self.extract_data_between(auth, session, start_load_time, next_end_time)
        
        await pipeDao.update_pipe_last_executed(self._credentials.id, next_end_time)
      
      start_load_time = next_end_time
