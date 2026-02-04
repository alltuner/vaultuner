# ABOUTME: Bitwarden Secrets Manager client wrapper.
# ABOUTME: Handles authentication and provides helper functions for secrets/projects.

import tempfile
from pathlib import Path

from bitwarden_sdk import BitwardenClient, DeviceType, client_settings_from_dict

from vaultuner.config import settings


def get_client() -> BitwardenClient:
    """Create and authenticate a Bitwarden client."""
    client = BitwardenClient(
        client_settings_from_dict(
            {
                "apiUrl": settings.api_url,
                "identityUrl": settings.identity_url,
                "deviceType": DeviceType.SDK,
                "userAgent": "vaultuner",
            }
        )
    )
    state_path = Path(tempfile.gettempdir()) / "vaultuner_state.json"
    client.auth().login_access_token(settings.access_token.get_secret_value(), str(state_path))
    return client


def get_or_create_project(client: BitwardenClient, project_name: str) -> str:
    """Get project ID by name, creating it if it doesn't exist."""
    response = client.projects().list(settings.organization_id)
    if response.data and response.data.data:
        for project in response.data.data:
            if project.name == project_name:
                return str(project.id)

    result = client.projects().create(settings.organization_id, project_name)
    if not result.data:
        raise RuntimeError(f"Failed to create project: {project_name}")
    return str(result.data.id)


def find_secret_by_key(client: BitwardenClient, key: str) -> dict | None:
    """Find a secret by its key name."""
    response = client.secrets().list(settings.organization_id)
    if not response.data or not response.data.data:
        return None
    for secret in response.data.data:
        if secret.key == key:
            return {"id": str(secret.id), "key": secret.key}
    return None
