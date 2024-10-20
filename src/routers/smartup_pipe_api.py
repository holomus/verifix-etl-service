from fastapi import APIRouter
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
def get_pipe_settings():
  with Session.begin() as session:
    dao = PipeSettingsDAO(session)
    return dao.get_all_pipe_settings()
  
@router.get('/{pipe_id}', response_model=SmartupCredentials)
def get_pipe_settings_by_id(pipe_id: int):
  with Session.begin() as session:
    dao = PipeSettingsDAO(session)
    return dao.delete_pipe_settings_by_id(pipe_id)
  
@router.put('/')
def update_pipe(settings: SmartupCredentials):
  with Session.begin() as session:
    dao = PipeSettingsDAO(session)
    dao.update_pipe_settings(settings)

@router.post('/', response_model=SmartupCreatePipeResponse)
def create_pipe(settings: NewSmartupCredentials):
  with Session.begin() as session:
    dao = PipeSettingsDAO(session)
    pipe_id = dao.insert_pipe_settings(settings)
    return SmartupCreatePipeResponse(id=pipe_id)

@router.delete('/{pipe_id}')
def delete_pipe(pipe_id: int):
  with Session.begin() as session:
    dao = PipeSettingsDAO(session)
    dao.delete_pipe_settings_by_id(pipe_id)  