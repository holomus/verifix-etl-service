from async_client import httpx_client
from entities import OrderEntity, SmartupCredentials, SmartupOrderFilters

class SmartupExtractionClient:
  ACCESS_TOKEN_PATH = "{}/security/oauth/token"
  DEALS_EXPORT_PATH = "{}/b/trade/txs/tdeal/order$export"
  
  @classmethod
  async def _get_access_token(cls, credentials: SmartupCredentials) -> str:
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
  async def extractDeals(cls, credentials: SmartupCredentials, filters: SmartupOrderFilters) -> list[OrderEntity]:
    access_token = await cls._get_access_token(credentials)

    response = await httpx_client.post(
      cls.DEALS_EXPORT_PATH.format(credentials.host),
      headers={
        'Authorization': 'Bearer {}'.format(access_token),
        'project_code': 'trade',
      },
      data=filters.model_dump(exclude_none=True, exclude_unset=True)
    )

    if response.status_code != 200:
      raise Exception(response.text)

    orders = response.json()['order']

    return [
      OrderEntity(**order, products=order['order_products']) for order in orders
    ]
