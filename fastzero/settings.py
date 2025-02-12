from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):  # pragma no cover
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", extra="ignore")

    ALGORITHM: str
    SECRET_KEY: str
    DATABASE_URL: str
    ACCESSTOKENEXPIRE: str
