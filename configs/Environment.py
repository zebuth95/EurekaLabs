from functools import lru_cache
import os

from pydantic import BaseSettings


@lru_cache
def get_env_filename():
    runtime_env = os.getenv("ENV")
    return f".env.{runtime_env}" if runtime_env else ".env"


class EnvironmentSettings(BaseSettings):
    LOG_LEVEL: str = "info"
    LOG_FORMAT: str = "JSON"
    LOG_DIR: str = "/usr/src/app/"
    ALGORITHM: str = "HS256"
    API_KEY: str = "X86NOH6II01P7R24"
    API_VERSION: str = "1.0.0"
    APP_NAME: str = "jaes"
    ALPHA_URL: str = "https://www.alphavantage.co/query"
    DEBUG_MODE: bool = True
    DATABASE_URL: str = "sqlite:///./sqlite3.db"
    SECRET_KEY: str = "09d25e094faa6ca2556c818166b7a9563b93f7099f6f0f4caa6cf63b88e8d3e7"

    class Config:
        env_file = get_env_filename()
        env_file_encoding = "utf-8"


@lru_cache
def get_environment_variables():
    return EnvironmentSettings()
