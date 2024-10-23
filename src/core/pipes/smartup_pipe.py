
from datetime import datetime, timedelta
from entities import SmartupCredentials, SmartupOrderFilters
from clients import SmartupExtractionClient
from daos import OrderDAO, PipeSettingsDAO
from db import Session
import asyncio

class SmartupPipe:
  _credentials: SmartupCredentials
  _pagination_timedelta: timedelta = timedelta(days=1)

  def __init__(self, credentials: SmartupCredentials):
    self._credentials = credentials

  # load pipe settings from smartup_pipe_settings and you can work with this
  async def extract_data_between(self, begin_load_time: datetime, end_load_time: datetime):
    if self._credentials.id is None:
      raise ValueError('when extracting data from SmartUp credentials must have an id')

    filters = SmartupOrderFilters(begin_modified_on=begin_load_time, end_modified_on=end_load_time)

    orders = await SmartupExtractionClient.extractDeals(self._credentials, filters)

    async with Session.begin() as session:
      orderDao = OrderDAO(session)
      pipeDao = PipeSettingsDAO(session)

      await orderDao.bulk_upsert_orders(company_code=self._credentials.company_code, orders=orders)
      await pipeDao.update_pipe_last_executed(id=self._credentials.id, execution_time=end_load_time)

  async def extract_data_since(self, start_load_time: datetime | None = None):
    start_load_time = start_load_time or self._credentials.last_execution_time or datetime.utcnow() - 2 * self._pagination_timedelta

    end_load_time = datetime.utcnow()

    while start_load_time < end_load_time:
      # Extract data for each time window of _pagination_timedelta
      next_end_time = min(start_load_time + self._pagination_timedelta, end_load_time)
      
      await self.extract_data_between(start_load_time, next_end_time)
      
      start_load_time = next_end_time
