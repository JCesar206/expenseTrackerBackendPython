from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    app_name: str = "Expense Tracker API"
    app_env: str = "development"
    log_level: str = "INDO"

    db_host: str = "127.0.0.1"
    db_port: int = 3306
    db_name: str = "expense_tracker"
    db_user: str = "root"
    db_password: str = ""

    jwt_secret_key: str = "REPLACE_WITH_A_RANDOM_SECRET"
    jwt_algorithm: str = "HS256"
    access_token_expire_minutes: int = 30

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )

settings = Settings()