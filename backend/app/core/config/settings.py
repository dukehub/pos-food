from pydantic import AliasChoices, Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    app_name: str = Field(
        default="restaurant-pos",
        validation_alias=AliasChoices("APP_NAME", "APP_TITLE", "APP_APP_NAME"),
    )
    env: str = Field(default="dev", validation_alias=AliasChoices("APP_ENV", "ENV"))
    database_url: str = Field(
        default="sqlite+aiosqlite:///./data.db",
        validation_alias=AliasChoices("DATABASE_URL", "DB_URL"),
    )
    tenant_header: str = Field(
        default="X-Tenant-Id",
        validation_alias=AliasChoices("TENANT_HEADER", "X_TENANT_HEADER"),
    )
    api_prefix: str = Field(default="/api", validation_alias=AliasChoices("API_PREFIX"))
    app_secret: str = Field(default="dev-secret", validation_alias=AliasChoices("APP_SECRET", "SECRET_KEY"))

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )


settings = Settings()
