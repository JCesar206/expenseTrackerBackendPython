import logging
from contextlib import asynccontextmanager
from fastapi import FastAPI

from app.core.config import settings
from app.core.logging_config import configure_logging
from app.routes.auth import router as auth_router
from app.routes.categories import router as categories_router
from app.routes.transactions import router as transactions_router

configure_logging()
logger = logging.getLogger(__name__)

@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info("%s iniciada", settings.app_name)
    yield
    logger.info("%d detenida", settings.app_name)

app = FastAPI(
    title=settings.app_name,
    lifespan=lifespan,
)

app.include_router(auth_router)
app.include_router(categories_router)
app.include_router(transactions_router)

@app.get("/health", tags=["Health"])
def health_check():
    return {"status": "ok"}