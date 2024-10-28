
from datetime import datetime, timedelta
from entities import SmartupCredentials, SmartupFilters
from clients import SmartupExtractionClient, SmartupAuth
from daos import OrderDAO, PipeSettingsDAO, ProductDAO, ClientDAO
from db import Session
from sqlalchemy.ext.asyncio import AsyncSession

class SmartupPipe:
  _credentials: SmartupCredentials
  _pagination_timedelta: timedelta = timedelta(days=1)

  def __init__(self, credentials: SmartupCredentials):
    self._credentials = credentials

  # load pipe settings from smartup_pipe_settings and you can work with this
  async def extract_data_between(self, auth: SmartupAuth, session: AsyncSession, filters: SmartupFilters):
    orders = await SmartupExtractionClient.extractDeals(auth, filters)

    orderDao = OrderDAO(session)

    await orderDao.bulk_upsert_orders(pipe_id=self._credentials.id, orders=orders)

  async def _initial_data_extraction(self, head_token: str):
    end_load_time = datetime.utcnow()

    filters = SmartupFilters(end_modified_on=end_load_time)
    auth = SmartupAuth(self._credentials.host, head_token)

    async with Session.begin() as session:
      productDao = ProductDAO(session)
      clientDao = ClientDAO(session)

      products = await SmartupExtractionClient.extractProducts(auth, filters)
      await productDao.bulk_upsert_products(pipe_id=self._credentials.id, products=products)
      
      clients = await SmartupExtractionClient.extractClients(auth, filters)
      await clientDao.bulk_upsert_clients(pipe_id=self._credentials.id, clients=clients)

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

    is_initial_load = start_load_time or self._credentials.last_execution_time is None
    start_load_time = start_load_time or self._credentials.last_execution_time or datetime.utcnow() - 2 * self._pagination_timedelta

    end_load_time = datetime.utcnow()

    if is_initial_load:
      await self._initial_data_extraction(head_token)

    while start_load_time < end_load_time:
      # Extract data for each time window of _pagination_timedelta
      next_end_time = min(start_load_time + self._pagination_timedelta, end_load_time)
      
      filters = SmartupFilters(begin_modified_on=start_load_time, end_modified_on=next_end_time)

      async with Session.begin() as session:
        pipeDao = PipeSettingsDAO(session)
        productDao = ProductDAO(session)
        clientDao = ClientDAO(session)

        for token in filial_tokens:
          auth = SmartupAuth(self._credentials.host, token)
          await self.extract_data_between(auth, session, filters)
        
        if not is_initial_load:
          auth = SmartupAuth(self._credentials.host, head_token)

          products = await SmartupExtractionClient.extractProducts(auth, filters)
          await productDao.bulk_upsert_products(pipe_id=self._credentials.id, products=products)
          
          clients = await SmartupExtractionClient.extractClients(auth, filters)
          await clientDao.bulk_upsert_clients(pipe_id=self._credentials.id, clients=clients)

        await pipeDao.update_pipe_last_executed(self._credentials.id, next_end_time)
      
      start_load_time = next_end_time

    print(f'End Extration Job {datetime.now()}')