import logging
from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.core.config import settings
from app.core.logging_config import configure_logging
from app.routes.auth import router as auth_router
from app.routes.categories import router as categories_router
from app.routes.transactions import router as transactions_router
from app.routes.reports import router as reports_router

configure_logging()
logger = logging.getLogger(__name__)

@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info("%s iniciada", settings.app_name)
    yield
    logger.info("%s detenida", settings.app_name)

app = FastAPI(
    title=settings.app_name,
    lifespan=lifespan,
)

# Permitir la comunicación con el frontend de vite.
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://127.0.0.1:5173",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth_router)
app.include_router(categories_router)
app.include_router(transactions_router)
app.include_router(reports_router)

@app.get("/health", tags=["Health"])
def health_check():
    return {"status": "ok"}