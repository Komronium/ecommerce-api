from contextlib import asynccontextmanager
from fastapi import FastAPI
from app.core.config import settings
from app.db.init_db import init_db
from app.api.v1 import users, categories, products


@asynccontextmanager
async def lifespan(application: FastAPI):
    await init_db()
    yield


app = FastAPI(
    title=settings.PROJECT_NAME,
    version=settings.PROJECT_VERSION,
    lifespan=lifespan
)


app.include_router(users.router, prefix='/api/v1', tags=['User'])
app.include_router(categories.router, prefix='/api/v1/categories', tags=['Category'])
app.include_router(products.router, prefix='/api/v1/products', tags=['Product'])
