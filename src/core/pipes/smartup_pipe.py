
from datetime import datetime
from entities import SmartupCredentials, SmartupOrderFilters
from clients import SmartupExtractionClient
from daos import OrderDAO, PipeSettingsDAO
from db import Session

class SmartupPipe:
  _credentials: SmartupCredentials

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

  def extract_data_since_last(self):
    pass
