import uvicorn
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from starlette.status import HTTP_500_INTERNAL_SERVER_ERROR
from routers import smartup_pipe_router

app = FastAPI()

app.include_router(smartup_pipe_router)

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

if __name__ == "__main__":
  uvicorn.run(app, host="0.0.0.0", port=8000)