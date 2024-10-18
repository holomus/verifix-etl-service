
from datetime import datetime, timedelta
from entities import SmartupCredentials, SmartupOrderFilters
from clients import SmartupExtractionClient
from daos import OrderDAO, PipeSettingsDAO
from db import Session

class SmartupPipe:
  _credentials: SmartupCredentials
  _pagination_timedelta: timedelta = timedelta(days=1)

  # load pipe settings from smartup_pipe_settings and you can work with this
  def extract_data_between(self, begin_load_time: datetime, end_load_time: datetime):
    if self._credentials.id is None:
      raise ValueError('when extracting data from SmartUp credentials must have an id')

    filters = SmartupOrderFilters(begin_modified_on=begin_load_time, end_modified_on=end_load_time)

    orders = SmartupExtractionClient.extractDeals(self._credentials, filters)

    with Session.begin() as session:
      orderDao = OrderDAO(session)
      pipeDao = PipeSettingsDAO(session)

      orderDao.bulk_upsert_orders(company_code=self._credentials.company_code, orders=orders)
      pipeDao.update_pipe_last_executed(id=self._credentials.id)

  def extract_data_since(self, start_load_time: datetime | None):
    start_load_time = start_load_time or self._credentials.last_update_time or datetime.now() - 2 * self._pagination_timedelta

    end_load_time = datetime.now()
    
    while start_load_time < end_load_time:
        # Extract data for each time window of _pagination_timedelta
        next_end_time = min(start_load_time + self._pagination_timedelta, end_load_time)
        
        self.extract_data_between(start_load_time, next_end_time)
        
        start_load_time = next_end_time
