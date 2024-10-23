from httpx import AsyncClient, Timeout

httpx_client = AsyncClient(timeout=Timeout(connect=5.0, write=5.0, pool=30.0, read=300.0))