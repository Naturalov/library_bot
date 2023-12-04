from typing import Optional

from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    bot_token: Optional[str]

    DATABASE_DNS: Optional[str] = "sqlite://db.sqlite"

    DOMAIN: str

    class Config:
        env_file = '.env'
        env_file_encoding = 'utf-8'
        env_nested_delimiter = '__'


config = Settings()
