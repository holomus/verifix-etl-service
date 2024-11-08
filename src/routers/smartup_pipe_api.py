from fastapi import APIRouter, HTTPException
from starlette.status import HTTP_204_NO_CONTENT,  HTTP_404_NOT_FOUND
from db import Session
from daos import PipeSettingsDAO
from entities import SmartupCredentials, NewSmartupCredentials, SmartupDealFilters, UpdateSmartupCredentials
from pydantic import BaseModel
from jobs import start_extraction_between
from datetime import datetime

class SmartupCreatePipeResponse(BaseModel):
  id: int

router = APIRouter(
  prefix='/pipes/smartup',
  tags=['pipes']
)

@router.get('/', response_model=list[SmartupCredentials])
async def get_pipe_settings() -> list[SmartupCredentials]:
  async with Session.begin() as session:
    dao = PipeSettingsDAO(session)
    return await dao.get_all_pipe_settings()
  
@router.get('/{pipe_id}', response_model=SmartupCredentials)
async def get_pipe_settings_by_id(pipe_id: int) -> SmartupCredentials:
  async with Session.begin() as session:
    dao = PipeSettingsDAO(session)
    settings = await dao.get_pipe_settings_by_id(pipe_id)
    if settings is None:
      raise HTTPException(status_code=HTTP_404_NOT_FOUND, detail="Settings not found")
    return settings

@router.delete('/{pipe_id}', status_code=HTTP_204_NO_CONTENT)
async def delete_pipe(pipe_id: int) -> None:
  async with Session.begin() as session:
    dao = PipeSettingsDAO(session)
    await dao.delete_pipe_settings_by_id(pipe_id)  

@router.put('/', status_code=HTTP_204_NO_CONTENT)
async def update_pipe(update_settings: UpdateSmartupCredentials) -> None:
  settings = SmartupCredentials(
    id=update_settings.id,
    company_code=update_settings.company_code,
    host=update_settings.host,
    client_id=update_settings.client_id,
    client_secret=update_settings.client_secret,
    cursors={}
  )

  async with Session.begin() as session:
    dao = PipeSettingsDAO(session)
    await dao.update_pipe_settings(settings)

@router.post('/', response_model=SmartupCreatePipeResponse)
async def create_pipe(settings: NewSmartupCredentials, filters: SmartupDealFilters) -> SmartupCreatePipeResponse:
  filters.begin_deal_month = filters.begin_deal_month or datetime.now()
  filters.end_deal_month = filters.end_deal_month or datetime.now()

  async with Session.begin() as session:
    dao = PipeSettingsDAO(session)
    pipe_id = await dao.insert_pipe_settings(settings)
  
    credentials = SmartupCredentials(
      id=pipe_id,
      company_code=settings.company_code,
      host=settings.host,
      client_id=settings.client_id,
      client_secret=settings.client_secret,
      cursors={}
    )

    start_extraction_between(credentials, filters, True, True)
    return SmartupCreatePipeResponse(id=pipe_id)

@router.post('/extract/{pipe_id}', status_code=HTTP_204_NO_CONTENT)
async def extract_deals(pipe_id: int, filters: SmartupDealFilters, reload_clients: bool = False, reload_products: bool = False):
  async with Session.begin() as session:
    dao = PipeSettingsDAO(session)
    settings = await dao.get_pipe_settings_by_id(pipe_id)

    if settings is None:
      return

    start_extraction_between(settings, filters, reload_clients, reload_products)