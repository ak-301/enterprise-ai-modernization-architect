"""Configuration package — re-exports settings for clean imports."""

from app.config.settings import Settings, get_settings

__all__ = ["Settings", "get_settings"]
