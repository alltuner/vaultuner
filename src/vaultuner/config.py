# ABOUTME: Configuration settings for Bitwarden Secrets Manager.
# ABOUTME: Loads credentials from environment variables or .env file.

from pydantic import SecretStr
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", env_prefix="BWS_")

    access_token: SecretStr
    organization_id: str
    api_url: str = "https://vault.bitwarden.com/api"
    identity_url: str = "https://vault.bitwarden.com/identity"


settings = Settings()
