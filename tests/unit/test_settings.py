"""Unit tests for configuration and settings."""

from app.config.settings import Settings, get_settings


def test_default_settings() -> None:
    settings = Settings(
        _env_file=None,  # type: ignore[call-arg]
        database_url="postgresql+psycopg://aima:aima@localhost:5432/aima",
    )
    assert settings.app_name == "Enterprise AI Modernization Architect"
    assert settings.environment == "local"
    assert settings.api_port == 8000
    assert settings.storage_backend == "filesystem"
    assert settings.llm_provider == "stub"
    assert "postgresql" in settings.database_url_str


def test_get_settings_cached() -> None:
    get_settings.cache_clear()
    a = get_settings()
    b = get_settings()
    assert a is b
    get_settings.cache_clear()


def test_is_production_flag() -> None:
    local = Settings(
        _env_file=None,  # type: ignore[call-arg]
        environment="local",
        database_url="postgresql+psycopg://aima:aima@localhost:5432/aima",
    )
    prod = Settings(
        _env_file=None,  # type: ignore[call-arg]
        environment="production",
        database_url="postgresql+psycopg://aima:aima@localhost:5432/aima",
    )
    assert local.is_production is False
    assert prod.is_production is True
