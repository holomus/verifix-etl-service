import uvicorn
from fastapi import FastAPI
from routers import smartup_pipe_router

app = FastAPI()

app.include_router(smartup_pipe_router)

@app.get('/')
async def helloworld():
  return {
    'message': 'Hello World!!'
  }

if __name__ == "__main__":
  uvicorn.run(app, host="0.0.0.0", port=8000)