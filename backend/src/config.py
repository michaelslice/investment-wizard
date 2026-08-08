from functools import lru_cache

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    app_name: str = "OptionScope API"
    api_prefix: str = "/api"
    cboe_base_url: str = "https://cdn.cboe.com"
    cache_ttl_seconds: int = 30
    request_timeout_seconds: float = 9.0
    frontend_origin: str = "http://localhost:5173"

    model_config = SettingsConfigDict(env_prefix="OPTIONSCOPE_", env_file=".env")


@lru_cache
def get_settings() -> Settings:
    return Settings()
