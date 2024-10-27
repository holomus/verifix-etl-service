from async_client import httpx_client
from httpx import Auth
from entities import (
  OrderEntity, 
  SmartupFilialCredentials, 
  SmartupFilters,
  SmartupLegalPersonEntity,
  SmartupProductEntity,
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
  DEALS_EXPORT_PATH = "{}/b/trade/txs/tdeal/order$export"
  CLIENTS_EXPORT_PATH = "{}/b/anor/mxsx/mr/legal_person$export"
  PRODUCTS_EXPORT_PATH = "{}/b/anor/mxsx/mr/inventory$export"

  @classmethod
  async def get_access_token(cls, host: str, credentials: SmartupFilialCredentials) -> str:
    response = await httpx_client.post(
      cls.ACCESS_TOKEN_PATH.format(host),
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
  async def extractDeals(cls, smartup_auth: SmartupAuth, filters: SmartupFilters) -> list[OrderEntity]:
    response = await httpx_client.post(
      cls.DEALS_EXPORT_PATH.format(smartup_auth.host),
      auth=smartup_auth,
      headers={
        'project_code': 'trade',
      },
      json=filters.model_dump(exclude_none=True, exclude_unset=True)
    )

    if response.status_code != 200:
      raise Exception(response.text)

    orders = response.json()['order']

    return [
      OrderEntity(**order, products=order['order_products']) for order in orders
    ]
  
  @classmethod
  async def extractClients(cls, smartup_auth: SmartupAuth, filters: SmartupFilters) -> list[SmartupLegalPersonEntity]:
    response = await httpx_client.post(
      cls.CLIENTS_EXPORT_PATH.format(smartup_auth.host),
      auth=smartup_auth,
      headers={
        'project_code': 'trade',
      },
      json=filters.model_dump(exclude_none=True, exclude_unset=True, include={
        'begin_modified_on',
        'end_modified_on'
      })
    )

    if response.status_code != 200:
      raise Exception(response.text)

    clients = response.json()['legal_person']

    return [
      SmartupLegalPersonEntity(**client, type_binds=client['groups']) for client in clients
    ]
  
  @classmethod
  async def extractProducts(cls, smartup_auth: SmartupAuth, filters: SmartupFilters) -> list[SmartupProductEntity]:
    response = await httpx_client.post(
      cls.PRODUCTS_EXPORT_PATH.format(smartup_auth.host),
      auth=smartup_auth,
      headers={
        'project_code': 'trade',
      },
      json=filters.model_dump(exclude_none=True, exclude_unset=True, include={
        'begin_modified_on',
        'end_modified_on'
      })
    )

    if response.status_code != 200:
      raise Exception(response.text)

    products = response.json()['inventory']

    return [
      SmartupProductEntity(**product, type_binds=product['groups']) for product in products
    ]
