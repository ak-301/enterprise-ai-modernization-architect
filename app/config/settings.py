"""Application configuration via environment variables.

All settings use the AIMA_ prefix. Secrets must never be hard-coded.
Cloud vs local backends are abstracted behind settings so Stage 1
runs entirely on Docker without Azure credentials.
"""

from functools import lru_cache
from typing import Literal

from pydantic import Field, PostgresDsn, field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Central configuration for Enterprise AI Modernization Architect.

    Local defaults target Docker Compose. Production (Azure) overrides
    the same keys without changing application code.
    """

    model_config = SettingsConfigDict(
        env_prefix="AIMA_",
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )

    # Application
    app_name: str = "Enterprise AI Modernization Architect"
    environment: Literal["local", "test", "staging", "production"] = "local"
    debug: bool = False
    log_level: Literal["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"] = "INFO"
    log_format: Literal["json", "console"] = "json"

    # API
    api_host: str = "0.0.0.0"
    api_port: int = 8000
    api_prefix: str = "/api/v1"

    # Database
    database_url: PostgresDsn = Field(default="postgresql+psycopg://aima:aima@localhost:5432/aima")
    database_pool_size: int = Field(default=5, ge=1, le=50)
    database_max_overflow: int = Field(default=10, ge=0, le=50)

    # Storage abstraction (filesystem local → Azure Blob later)
    storage_backend: Literal["filesystem", "azure_blob"] = "filesystem"
    storage_path: str = "./data/processed"

    # LLM abstraction (OpenAI-compatible → Azure OpenAI later)
    llm_provider: Literal["openai_compatible", "azure_openai", "stub"] = "stub"
    llm_base_url: str = "http://localhost:11434/v1"
    llm_api_key: str = ""
    llm_model: str = "gpt-4o-mini"
    embedding_model: str = "text-embedding-3-small"

    # Observability
    otel_enabled: bool = False
    service_name: str = "aima-api"

    @field_validator("database_url", mode="before")
    @classmethod
    def coerce_database_url(cls, value: object) -> object:
        """Accept plain strings from env and coerce to PostgresDsn."""
        return value

    @property
    def database_url_str(self) -> str:
        """SQLAlchemy-compatible connection string."""
        return str(self.database_url)

    @property
    def is_production(self) -> bool:
        return self.environment == "production"


@lru_cache
def get_settings() -> Settings:
    """Cached settings singleton for dependency injection."""
    return Settings()
