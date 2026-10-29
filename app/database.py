import logging
from sqlalchemy import URL, create_engine, text
from sqlalchemy.orm import sessionmaker

from app.core.config import settings
from app.models import Base

logger = logging.getLogger(__name__)
DATABASE_URL = URL.create(
    drivername="mysql+pymysql",
    username=settings.db_user,
    password=settings.db_password,
    host=settings.db_host,
    port=settings.db_port,
    database=settings.db_name,
    query={"charset": "utf8mb4"},
)

engine = create_engine(
    DATABASE_URL,
    pool_pre_ping=True,
    pool_recycle=1800,
)

SessionLocal = sessionmaker(
    bind=engine,
    autoflush=False,
    autocommit=False,
)

def create_tables() -> None:
    Base.metadata.create_all(bind=engine)
def check_database_connection() -> None:
    with engine.connect() as connection:
        connection.execute(text("SELECT 1"))
    logger.info("Conexicón con MariaDB verficada.")
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()