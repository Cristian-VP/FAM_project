import os
import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from motor.motor_asyncio import AsyncIOMotorClient
from starlette.responses import RedirectResponse
from contextlib import asynccontextmanager
from config import settings
from routers import router

app = FastAPI()

origins = ['http://localhost:3000']

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=['*'],
    allow_headers=['*']
)

@asynccontextmanager
async def lifespan(app: FastAPI):
    app.mongodb_client = AsyncIOMotorClient(settings.MONGODB_URL)
    app.mongodb = app.mongodb_client[settings.MONGODB_NAME]
    yield
    app.mongodb_client.close()

app = FastAPI(lifespan=lifespan)

@app.get('/', include_in_schema=False)
async def get_root():
    root_url = os.environ.get('ROOT_URL')
    return RedirectResponse(url=f"{root_url}/docs")

app.include_router(router, tags=["Todo"], prefix="/api/v1/task")


if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host=settings.HOST,
        reload=settings.DEBUG_MODE,
        port=settings.PORT,
    )