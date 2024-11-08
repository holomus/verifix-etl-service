from async_client import httpx_client
from httpx import Auth
from entities import (
  OrderEntity, 
  OrderProductEntity,
  SmartupCredentials,
  SmartupLegalPersonEntity,
  SmartupProductEntity,
  SmartupDealFilters
)

class SmartupAuth(Auth):
  def __init__(self, host: str, token: str):
    self._token = token
    self.host = host

  def auth_flow(self, request):
    request.headers["Authorization"] = f"Bearer {self._token}"
    yield request

class SmartupExtractionClient:
  ACCESS_TOKEN_PATH = "{}/security/oauth/token"
  DEALS_PAGINATED_EXPORT_PATH = "{}/b/anor/api/v2/mdeal/order$list"
  DEAL_PRODUCTS_PAGINATED_EXPORT_PATH = "{}/b/anor/api/v2/mdeal/order$list_products"
  CLIENTS_PAGINATED_EXPORT_PATH="{}/b/anor/api/v2/mr/legal_person$list"
  PRODUCT_PAGINATED_EXPORT_PATH="{}/b/anor/api/v2/mr/inventory$list"

  @classmethod
  async def get_access_token(cls, credentials: SmartupCredentials) -> str:
    response = await httpx_client.post(
      cls.ACCESS_TOKEN_PATH.format(credentials.host),
      json={
        'grant_type': 'client_credentials',
        'client_id': credentials.client_id,
        'client_secret': credentials.client_secret,
        'scope': 'read',
      }
    )

    if response.status_code != 200:
      raise Exception(response.text)
    
    response = response.json()

    return response['access_token']

  @classmethod
  async def extractDeals(cls, smartup_auth: SmartupAuth, filters: SmartupDealFilters, cursor: int | None) -> tuple[list[OrderEntity], int]:
    response = await httpx_client.post(
      cls.DEALS_PAGINATED_EXPORT_PATH.format(smartup_auth.host),
      auth=smartup_auth,
      headers={
        'project_code': 'trade',
        'cursor': str(cursor) if cursor is not None else ""
      },
      json=filters.model_dump(exclude_none=True, exclude_unset=True)
    )

    if response.status_code != 200:
      raise Exception(response.text)

    result = response.json()

    orders = result['data']
    meta = result['meta']

    return [
      OrderEntity(**order) for order in orders
    ], int(meta['next_cursor'])
  
  @classmethod
  async def extractDealProducts(cls, smartup_auth: SmartupAuth, filters: SmartupDealFilters, cursor: int | None) -> tuple[list[OrderProductEntity], int]:
    response = await httpx_client.post(
      cls.DEAL_PRODUCTS_PAGINATED_EXPORT_PATH.format(smartup_auth.host),
      auth=smartup_auth,
      headers={
        'project_code': 'trade',
        'cursor': str(cursor) if cursor is not None else ""
      },
      json=filters.model_dump(exclude_none=True, exclude_unset=True)
    )

    if response.status_code != 200:
      raise Exception(response.text)

    result = response.json()

    order_products = result['data']
    meta = result['meta']

    return [
      OrderProductEntity(**product) for product in order_products
    ], int(meta['next_cursor'])
  
  @classmethod
  async def extractClients(cls, smartup_auth: SmartupAuth, cursor: int | None) -> tuple[list[SmartupLegalPersonEntity], int]:
    response = await httpx_client.post(
      cls.CLIENTS_PAGINATED_EXPORT_PATH.format(smartup_auth.host),
      auth=smartup_auth,
      headers={
        'project_code': 'trade',
        'cursor': str(cursor) if cursor is not None else ""
      },
      json={}
    )

    if response.status_code != 200:
      raise Exception(response.text)
    
    result = response.json()

    clients = result['data']
    meta = result['meta']

    return [
      SmartupLegalPersonEntity(**client, type_binds=client['groups']) for client in clients
    ], int(meta['next_cursor'])
  
  @classmethod
  async def extractProducts(cls, smartup_auth: SmartupAuth, cursor: int | None) -> tuple[list[SmartupProductEntity], int]:
    response = await httpx_client.post(
      cls.PRODUCT_PAGINATED_EXPORT_PATH.format(smartup_auth.host),
      auth=smartup_auth,
      headers={
        'project_code': 'trade',
        'cursor': str(cursor) if cursor is not None else ""
      },
      json={}
    )

    if response.status_code != 200:
      raise Exception(response.text)

    result = response.json()

    products = result['data']
    meta = result['meta']

    return [
      SmartupProductEntity(**product, type_binds=product['groups']) for product in products
    ], int(meta['next_cursor'])
