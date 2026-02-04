# ABOUTME: Configuration settings for Bitwarden Secrets Manager.
# ABOUTME: Loads credentials from keychain (preferred) or environment variables.

import keyring
from pydantic import SecretStr
from pydantic_settings import BaseSettings, SettingsConfigDict

SERVICE_NAME = "vaultuner"


def get_keyring_value(key: str) -> str | None:
    """Get a value from the system keychain."""
    return keyring.get_password(SERVICE_NAME, key)


def set_keyring_value(key: str, value: str) -> None:
    """Store a value in the system keychain."""
    keyring.set_password(SERVICE_NAME, key, value)


def delete_keyring_value(key: str) -> None:
    """Delete a value from the system keychain."""
    try:
        keyring.delete_password(SERVICE_NAME, key)
    except keyring.errors.PasswordDeleteError:
        pass


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_prefix="BWS_")

    access_token: SecretStr
    organization_id: str
    api_url: str = "https://vault.bitwarden.com/api"
    identity_url: str = "https://vault.bitwarden.com/identity"

    @classmethod
    def settings_customise_sources(
        cls,
        settings_cls,
        init_settings,
        env_settings,
        dotenv_settings,
        file_secret_settings,
    ):
        """Load from keychain first, then fall back to env vars."""
        return (
            init_settings,
            KeyringSettingsSource(settings_cls),
            env_settings,
            dotenv_settings,
            file_secret_settings,
        )


class KeyringSettingsSource:
    """Custom settings source that reads from system keychain."""

    def __init__(self, settings_cls):
        self.settings_cls = settings_cls

    def __call__(self):
        values = {}
        access_token = get_keyring_value("bws_access_token")
        if access_token:
            values["access_token"] = access_token
        org_id = get_keyring_value("bws_organization_id")
        if org_id:
            values["organization_id"] = org_id
        return values


_settings: Settings | None = None


def get_settings() -> Settings:
    """Load settings lazily, with helpful error message if not configured."""
    global _settings
    if _settings is None:
        try:
            _settings = Settings()
        except Exception:
            raise SystemExit(
                "Credentials not configured. Run:\n"
                "  vaultuner config set access-token <token>\n"
                "  vaultuner config set organization-id <org-id>"
            )
    return _settings
