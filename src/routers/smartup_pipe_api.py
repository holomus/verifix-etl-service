from fastapi import APIRouter, HTTPException
from starlette.status import HTTP_204_NO_CONTENT,  HTTP_404_NOT_FOUND
from db import Session
from daos import PipeSettingsDAO
from entities import SmartupCredentials, NewSmartupCredentials
from pydantic import BaseModel

class SmartupCreatePipeResponse(BaseModel):
  id: int

router = APIRouter(
  prefix='/pipes/smartup',
  tags=['pipes']
)

@router.get('/', response_model=list[SmartupCredentials])
def get_pipe_settings() -> list[SmartupCredentials]:
  with Session.begin() as session:
    dao = PipeSettingsDAO(session)
    return dao.get_all_pipe_settings()
  
@router.get('/{pipe_id}', response_model=SmartupCredentials)
def get_pipe_settings_by_id(pipe_id: int) -> SmartupCredentials:
  with Session.begin() as session:
    dao = PipeSettingsDAO(session)
    settings = dao.get_pipe_settings_by_id(pipe_id)
    if settings is None:
      raise HTTPException(status_code=HTTP_404_NOT_FOUND, detail="Settings not found")
    return settings

@router.put('/', status_code=HTTP_204_NO_CONTENT)
def update_pipe(settings: SmartupCredentials) -> None:
  with Session.begin() as session:
    dao = PipeSettingsDAO(session)
    rowcount = dao.update_pipe_settings(settings)

    if rowcount == 0:
      raise HTTPException(status_code=HTTP_404_NOT_FOUND, detail="Settings not found")

@router.post('/', response_model=SmartupCreatePipeResponse)
def create_pipe(settings: NewSmartupCredentials) -> SmartupCreatePipeResponse:
  with Session.begin() as session:
    dao = PipeSettingsDAO(session)
    pipe_id = dao.insert_pipe_settings(settings)
    return SmartupCreatePipeResponse(id=pipe_id)

@router.delete('/{pipe_id}', status_code=HTTP_204_NO_CONTENT)
def delete_pipe(pipe_id: int) -> None:
  with Session.begin() as session:
    dao = PipeSettingsDAO(session)
    dao.delete_pipe_settings_by_id(pipe_id)  