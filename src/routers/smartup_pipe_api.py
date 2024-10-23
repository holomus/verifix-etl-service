from fastapi import APIRouter, HTTPException
from starlette.status import HTTP_204_NO_CONTENT,  HTTP_404_NOT_FOUND
from db import Session
from daos import PipeSettingsDAO
from entities import SmartupCredentials, NewSmartupCredentials
from pydantic import BaseModel
from jobs import start_extraction_on

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
async def update_pipe(settings: SmartupCredentials) -> None:
  async with Session.begin() as session:
    dao = PipeSettingsDAO(session)
    await dao.update_pipe_settings(settings)
    credentials= await dao.get_pipe_settings_by_id(settings.id)
  
  if credentials is not None and settings.last_execution_time is not None:
    start_extraction_on(credentials)

@router.post('/', response_model=SmartupCreatePipeResponse)
async def create_pipe(settings: NewSmartupCredentials) -> SmartupCreatePipeResponse:
  async with Session.begin() as session:
    dao = PipeSettingsDAO(session)
    pipe_id = await dao.insert_pipe_settings(settings)
  
    credentials = SmartupCredentials(
      id=pipe_id,
      company_code=settings.company_code,
      host=settings.host,
      client_id=settings.client_id,
      client_secret=settings.client_secret,
      last_execution_time=settings.last_execution_time
    )

  start_extraction_on(credentials)
  return SmartupCreatePipeResponse(id=pipe_id)