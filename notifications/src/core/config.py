from logging import config as logging_config
from datetime import timedelta

from core.logger import LOGGING
from pydantic_settings import BaseSettings
from pydantic import Field

logging_config.dictConfig(LOGGING)

env_file = ".env.example"


class Settings(BaseSettings):
    service_name: str = Field(default="Notifications", env="SERVICE_NAME")
    api_key: str = Field(env="API_KEY")
    api_secret: str = Field(env="API_SECRET")

    class Config:
        env_file = env_file


settings = Settings()
