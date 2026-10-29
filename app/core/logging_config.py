import logging
from app.core.config import settings

def configure_logging() -> None:
    log_level = settings.log_level.upper()
    logging.basicConfig(level=log_level, format=("%(asctime)s | %(levelname)-8s | %(name)s | %(message)s"),
    datefmt="%Y-%m-%d %H:%M:%S", force=True)

    logging.getLogger("sqlalchemy.engine").setLevel(logging.WARNING)