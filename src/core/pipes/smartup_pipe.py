
from entities import SmartupCredentials, SmartupDealFilters
from clients import SmartupExtractionClient, SmartupAuth
from daos import OrderDAO, PipeSettingsDAO, ProductDAO, ClientDAO
from datetime import datetime
from db import Session

class SmartupPipe:
  _credentials: SmartupCredentials

  def __init__(self, credentials: SmartupCredentials):
    self._credentials = credentials
    
  async def _extract_deal_products(self, auth: SmartupAuth, filters: SmartupDealFilters, cursor: int | None, update_pipe_cursor: bool = True):
    next_cursor = max(cursor or 1, 1)
    last_cursor = next_cursor

    while next_cursor > 0:
      last_cursor = next_cursor

      async with Session.begin() as session:
        dao = OrderDAO(session)

        order_products, next_cursor = await SmartupExtractionClient.extractDealProducts(auth, filters, next_cursor)

        await dao.bulk_upsert_order_products(pipe_id=self._credentials.id, order_products=order_products)

    if update_pipe_cursor:
      async with Session.begin() as session:
        pipe_dao = PipeSettingsDAO(session)

        await pipe_dao.upsert_pipe_cursor(pipe_id=self._credentials.id, extraction_key=PipeSettingsDAO.ORDER_PRODUCTS_CURSOR_KEY, cursor=last_cursor)

  async def _extract_deals(self, auth: SmartupAuth, filters: SmartupDealFilters, cursor: int | None, update_pipe_cursor: bool = True):
    next_cursor = max(cursor or 1, 1)
    last_cursor = next_cursor

    while next_cursor > 0:
      last_cursor = next_cursor
      
      async with Session.begin() as session:
        dao = OrderDAO(session)

        orders, next_cursor = await SmartupExtractionClient.extractDeals(auth, filters, next_cursor)

        await dao.bulk_upsert_orders(pipe_id=self._credentials.id, orders=orders)

      deal_ids = [
        order.deal_id for order in orders
      ]

      if len(deal_ids) > 0:
        product_filters = SmartupDealFilters(deal_ids=deal_ids)

        await self._extract_deal_products(auth, product_filters, None, update_pipe_cursor)

    if update_pipe_cursor:
      async with Session.begin() as session:
        pipe_dao = PipeSettingsDAO(session)

        await pipe_dao.upsert_pipe_cursor(pipe_id=self._credentials.id, extraction_key=PipeSettingsDAO.ORDERS_CURSOR_KEY, cursor=last_cursor)
  
  async def _extract_clients(self, auth: SmartupAuth, cursor: int | None):
    next_cursor = max(cursor or 1, 1)
    last_cursor = next_cursor

    while next_cursor > 0:
      last_cursor = next_cursor

      async with Session.begin() as session:
        dao = ClientDAO(session)

        clients, next_cursor = await SmartupExtractionClient.extractClients(auth, next_cursor)

        await dao.bulk_upsert_clients(pipe_id=self._credentials.id, clients=clients)

    async with Session.begin() as session:
      pipe_dao = PipeSettingsDAO(session)

      await pipe_dao.upsert_pipe_cursor(pipe_id=self._credentials.id, extraction_key=PipeSettingsDAO.CLIENTS_CURSOR_KEY, cursor=last_cursor)
  
  async def _extract_products(self, auth: SmartupAuth, cursor: int | None):
    next_cursor = max(cursor or 1, 1)
    last_cursor = next_cursor

    while next_cursor > 0:
      last_cursor = next_cursor

      async with Session.begin() as session:
        dao = ProductDAO(session)

        products, next_cursor = await SmartupExtractionClient.extractProducts(auth, next_cursor)

        await dao.bulk_upsert_products(pipe_id=self._credentials.id, products=products)

    async with Session.begin() as session:
      pipe_dao = PipeSettingsDAO(session)

      await pipe_dao.upsert_pipe_cursor(pipe_id=self._credentials.id, extraction_key=PipeSettingsDAO.PRODUCTS_CURSOR_KEY, cursor=last_cursor)

  async def extract_deals_between(self, filters: SmartupDealFilters, reload_clients: bool = False, reload_products: bool = False):
    token = await SmartupExtractionClient.get_access_token(self._credentials)

    auth = SmartupAuth(self._credentials.host, token)
    
    update_pipe_cursor = filters.end_deal_month is None or filters.end_deal_month >= datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)

    if reload_clients:
      await self._extract_clients(auth, None)
    if reload_products:
      await self._extract_products(auth, None)

    await self._extract_deals(auth, filters, None, update_pipe_cursor)

  async def extract_data(self):
    token = await SmartupExtractionClient.get_access_token(self._credentials)

    auth = SmartupAuth(self._credentials.host, token)

    filters = SmartupDealFilters()

    await self._extract_clients(auth, self._credentials.cursors.get(PipeSettingsDAO.CLIENTS_CURSOR_KEY))
    await self._extract_products(auth, self._credentials.cursors.get(PipeSettingsDAO.PRODUCTS_CURSOR_KEY))
    await self._extract_deals(auth, filters, self._credentials.cursors.get(PipeSettingsDAO.ORDERS_CURSOR_KEY))