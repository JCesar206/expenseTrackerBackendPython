import logging
import re
import sys
import pymysql
from sqlalchemy import select
from app.core.config import settings
from app.database import (
    SessionLocal,
    check_database_connection,
    create_tables,
)
from app.models import Category
logger = logging.getLogger(__name__)
DEFAULT_CATEGORIES = [
    ("Salary", "income"),
    ("Freelance", "income"),
    ("Other income", "income"),
    ("Food", "expense"),
    ("Transport", "expense"),
    ("Housing", "expense"),
    ("Health", "expense"),
    ("Entertainment", "expense"),
    ("Other expense", "expense"),
]

def validate_database_name() -> None:
    if not re.fullmatch(r"[A-Za-z0-9_]+", settings.db_name):
        raise ValueError("DB_NAME solo puede contener letras, números y guion bajo.")
    if settings.db_name.lower() in {"mysql", "information_schema", "performance_schema", "sys"}:
        raise ValueError(
            "No se permite utilizar una base de datos del sistema."
        )

def create_database() -> None:
    validate_database_name()

    connection = pymysql.connect(
        host=settings.db_host,
        port=settings.db_port,
        user=settings.db_user,
        password=settings.db_password,
        charset="utf8mb4",
        autocommit=True,
    )

    try:
        with connection.cursor() as cursor:
            cursor.execute(f"CREATE DATABASE IF NOT EXISTS "f"`{settings.db_name}` ""CHARACTER SET utf8mb4 " "COLLATE utf8mb4_unicode_ci")

        logger.info("Base de datos preparada: %s", settings.db_name)
    finally:
        connection.close()

def seed_categories() -> None:
    with SessionLocal() as db:
        try:
            for name, kind in DEFAULT_CATEGORIES:
                existing = db.scalar(
                    select(Category.id).where(
                        Category.name == name,
                        Category.kind == kind,
                        Category.user_id.is_(None),
                    )
                )

                if existing is None:
                    db.add(
                        Category(
                            name=name,
                            kind=kind,
                            user_id=None,
                        )
                    )

            db.commit()
            logger.info("Categorías predeterminadas verificadas")
        except Exception:
            db.rollback()
            logger.exception("Error al cargar categorías")
            raise

def reset_database() -> None:
    if settings.app_env.lower() != "development":
        raise RuntimeError(
            "db reset solo está permitido en desarrollo."
        )

    validate_database_name()

    confirmation = input(
        f"Esto eliminará TODOS los datos de "
        f"'{settings.db_name}'. Escribe RESET para continuar: "
    )

    if confirmation != "RESET":
        logger.warning("Restablecimiento cancelado")
        return

    connection = pymysql.connect(
        host=settings.db_host,
        port=settings.db_port,
        user=settings.db_user,
        password=settings.db_password,
        charset="utf8mb4",
        autocommit=True,
    )

    try:
        with connection.cursor() as cursor:
            cursor.execute(
                f"DROP DATABASE IF EXISTS `{settings.db_name}`"
            )
    finally:
        connection.close()

    logger.warning("Base de datos de desarrollo eliminada")
    initialize_database()
    seed_categories()

def initialize_database() -> None:
    create_database()
    check_database_connection()
    create_tables()
    logger.info("Estructura de tablas preparada")

def main() -> None:
    logging.basicConfig(
        level=settings.log_level.upper(),
        format="%(asctime)s | %(levelname)s | %(name)s | %(message)s",
    )

    if len(sys.argv) != 2:
        print(
            "Uso: python -m app.db_tasks "
            "{init|seed|reset}"
        )
        raise SystemExit(2)

    command = sys.argv[1].lower()

    try:
        if command == "init":
            initialize_database()
        elif command == "seed":
            seed_categories()
        elif command == "reset":
            reset_database()
        else:
            print(f"Comando desconocido: {command}")
            raise SystemExit(2)
    except Exception:
        logger.exception("Falló la tarea de base de datos")
        raise SystemExit(1)

if __name__ == "__main__":
    main()