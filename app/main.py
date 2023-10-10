import os
from mangum import Mangum
from fastapi.middleware.cors import CORSMiddleware
from app.routes.buscalibre.api import router as buscalibre_router
from fastapi import Body, BackgroundTasks, FastAPI, Depends


app = FastAPI()
os.environ["PLAYWRIGHT_BROWSERS_PATH"] = "pw-browsers"


@app.get("/")
async def root():
  return {"response": "Hello World"}


app.include_router(buscalibre_router, prefix="/api/book")
#app.include_router(celery_router, prefix="/api/celery", tags=["Celery"])


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Handler to aws lambda
handler = Mangum(app)


