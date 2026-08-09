from functools import lru_cache

from pydantic import AliasChoices, Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    app_name: str = "investment-wizard API"
    api_prefix: str = "/api"
    cboe_base_url: str = "https://cdn.cboe.com"
    cache_ttl_seconds: int = 30
    request_timeout_seconds: float = 9.0
    frontend_origin: str = "http://localhost:5173"
    openai_api_key: str | None = Field(
        default=None,
        validation_alias=AliasChoices(
            "OPENAI_API_KEY",
            "INVESTMENT_WIZARD_OPENAI_API_KEY",
            "OPTIONSCOPE_OPENAI_API_KEY",
        ),
    )
    openai_model: str = "gpt-5.6-sol"

    model_config = SettingsConfigDict(
        env_prefix="INVESTMENT_WIZARD_",
        env_file=(".env", "backend/.env"),
        env_file_encoding="utf-8",
    )


@lru_cache
def get_settings() -> Settings:
    return Settings()
