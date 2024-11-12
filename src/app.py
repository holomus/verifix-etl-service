import uvicorn
import secrets
import config
from typing import Annotated
from fastapi import FastAPI, Request, Depends, HTTPException, status
from fastapi.responses import JSONResponse
from fastapi.security import HTTPBasic, HTTPBasicCredentials
from starlette.status import HTTP_500_INTERNAL_SERVER_ERROR
from routers import smartup_pipe_router, smartup_aggregates_router
from contextlib import asynccontextmanager
from jobs import start_extraction_on_all_pipes, scheduler
from async_client import httpx_client

@asynccontextmanager
async def lifespan(app:FastAPI):
  scheduler.add_job(start_extraction_on_all_pipes) # once right now
  scheduler.add_job(start_extraction_on_all_pipes, trigger='cron', hour=config.EXTRACTION_JOB_RUN_HOUR, minute=config.EXTRACTION_JOB_RUN_MINUTES)
  scheduler.start()
  yield
  scheduler.shutdown()
  await httpx_client.aclose()

security = HTTPBasic()

def verify_user(
  credentials: Annotated[HTTPBasicCredentials, Depends(security)],
):
  current_username_bytes = credentials.username.encode("utf8")
  correct_username_bytes = config.FASTAPI_AUTH_USERNAME.encode("utf8")
  is_correct_username = secrets.compare_digest(
    current_username_bytes, correct_username_bytes
  )
  current_password_bytes = credentials.password.encode("utf8")
  correct_password_bytes = config.FASTAPI_AUTH_PASSWORD.encode("utf8")
  is_correct_password = secrets.compare_digest(
    current_password_bytes, correct_password_bytes
  )
  if not (is_correct_username and is_correct_password):
    raise HTTPException(
      status_code=status.HTTP_401_UNAUTHORIZED,
      detail="Incorrect username or password",
      headers={"WWW-Authenticate": "Basic"},
    )

app = FastAPI(lifespan=lifespan, dependencies=[Depends(verify_user)])

app.include_router(smartup_pipe_router)
app.include_router(smartup_aggregates_router)

@app.exception_handler(Exception)
async def generic_exception_handler(request: Request, exc: Exception):
    # Change here to Logger
    return JSONResponse(
        status_code=HTTP_500_INTERNAL_SERVER_ERROR,
        content={
            "message": f"Failed method {request.method} at URL {request.url}.",
            "exception": f"{exc!r}"
        },
    )

@app.get('/')
async def helloworld():
  return {
    'message': 'Hello World!!'
  }

@app.get('/print_jobs')
async def print_jobs():
  jobs = scheduler.get_jobs()
  return [
    {
      'id': job.id,
      'next_run_time': str(job.next_run_time),
      'trigger': str(job.trigger),
      'name': job.name,
    } for job in jobs
  ]

if __name__ == "__main__":
  uvicorn.run(app, host="0.0.0.0", port=8000, log_config=config.LOGGING_CONFIG)