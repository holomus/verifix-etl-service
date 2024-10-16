
from datetime import datetime
from entities import SmartupCredentials
from clients import SmartupExtractionClient

class SmartupPipe:
  _credentials: SmartupCredentials
  _last_load_time: datetime

  def __init__(self, credentials: SmartupCredentials) -> None:
    self._credentials = credentials

  # load pipe settings from smartup_pipe_settings and you can work with this
  def extract_data(self):
    pass