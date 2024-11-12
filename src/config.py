import os

EXTRACTION_JOB_RUN_HOUR='3'
EXTRACTION_JOB_RUN_MINUTES='0'

FASTAPI_AUTH_USERNAME=os.environ['FASTAPI_AUTH_USERNAME']
FASTAPI_AUTH_PASSWORD=os.environ['FASTAPI_AUTH_PASSWORD']

LOG_DIR = './logs'
if not os.path.exists(LOG_DIR):
  os.mkdir(LOG_DIR)

LOGGING_CONFIG = { 
  'version': 1,
  'disable_existing_loggers': True,
  'formatters': { 
    'standard': { 
      'format': '%(asctime)s [%(levelname)s] %(name)s: %(message)s'
    },
    'custom_formatter': { 
      'format': "%(asctime)s [%(levelname)s] %(name)s: %(message)s"
    },
  },
  'handlers': { 
    'default': { 
      'formatter': 'standard',
      'class': 'logging.StreamHandler',
      'stream': 'ext://sys.stdout',  # Default is stderr
    },
    'stream_handler': { 
      'formatter': 'custom_formatter',
      'class': 'logging.StreamHandler',
      'stream': 'ext://sys.stdout',  # Default is stderr
    },
    'default_file_handler': { 
      'class': 'logging.handlers.TimedRotatingFileHandler',
      'formatter': 'custom_formatter',
      'filename': f'{LOG_DIR}/app.log',
      'when': 'D',
      'utc': True,
      'backupCount': 60,
    },
    'access_log_file_handler': { 
      'class': 'logging.handlers.TimedRotatingFileHandler',
      'formatter': 'custom_formatter',
      'filename': f'{LOG_DIR}/access.log',
      'when': 'D',
      'utc': True,
      'backupCount': 60,
    },
    'job_file_handler': { 
      'class': 'logging.handlers.TimedRotatingFileHandler',
      'formatter': 'custom_formatter',
      'filename': f'{LOG_DIR}/job.log',
      'when': 'D',
      'utc': True,
      'backupCount': 60,
    },
    'httpx_file_handler': { 
      'class': 'logging.handlers.TimedRotatingFileHandler',
      'formatter': 'custom_formatter',
      'filename': f'{LOG_DIR}/outgoing-httpx.log',
      'when': 'D',
      'utc': True,
      'backupCount': 60,
    },
  },
  'loggers': {
    'uvicorn': {
      'handlers': ['default', 'default_file_handler'],
      'level': 'TRACE',
      'propagate': False
    },
    'uvicorn.access': {
      'handlers': ['stream_handler', 'access_log_file_handler'],
      'level': 'TRACE',
      'propagate': False
    },
    'uvicorn.error': { 
      'handlers': ['stream_handler', 'default_file_handler'],
      'level': 'TRACE',
      'propagate': False
    },
    'uvicorn.asgi': {
      'handlers': ['stream_handler', 'default_file_handler'],
      'level': 'TRACE',
      'propagate': False
    },
    'apscheduler': {
      'handlers': ['stream_handler', 'job_file_handler'],
      'level': 'TRACE',
      'propagate': False
    },
    'httpx': {
      'handlers': ['default', 'httpx_file_handler'],
      'level': 'DEBUG',
    },
    'httpcore': {
      'handlers': ['default', 'httpx_file_handler'],
      'level': 'DEBUG',
    },
  },
}
