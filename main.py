# ABOUTME: CLI for Bitwarden Secrets Manager.
# ABOUTME: Provides commands to list and retrieve secrets.

import tempfile
from pathlib import Path

import typer
from bitwarden_sdk import BitwardenClient, DeviceType, client_settings_from_dict

from config import settings

app = typer.Typer()


def get_client() -> BitwardenClient:
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
    client.auth().login_access_token(settings.access_token, str(state_path))
    return client


@app.command()
def list_secrets():
    """List all secrets in the organization."""
    client = get_client()
    response = client.secrets().list(settings.organization_id)
    if not response.data or not response.data.data:
        typer.echo("No secrets found.")
        return
    for secret in response.data.data:
        typer.echo(f"{secret.key} ({secret.id})")


@app.command()
def get(secret_id: str):
    """Get a secret by ID."""
    client = get_client()
    response = client.secrets().get(secret_id)
    if not response.data:
        typer.echo(f"Secret {secret_id} not found.")
        raise typer.Exit(1)
    typer.echo(f"Key:   {response.data.key}")
    typer.echo(f"Value: {response.data.value}")
    if response.data.note:
        typer.echo(f"Note:  {response.data.note}")


@app.command()
def list_projects():
    """List all projects in the organization."""
    client = get_client()
    response = client.projects().list(settings.organization_id)
    if not response.data or not response.data.data:
        typer.echo("No projects found.")
        return
    for project in response.data.data:
        typer.echo(f"{project.name} ({project.id})")


@app.command()
def create_project(name: str):
    """Create a new project."""
    client = get_client()
    response = client.projects().create(settings.organization_id, name)
    if not response.data:
        typer.echo("Failed to create project.")
        raise typer.Exit(1)
    typer.echo(f"Created project: {response.data.name} ({response.data.id})")


@app.command()
def create(key: str, value: str, note: str | None = None, project_id: str | None = None):
    """Create a new secret."""
    client = get_client()
    project_ids = [project_id] if project_id else None
    response = client.secrets().create(
        organization_id=settings.organization_id,
        key=key,
        value=value,
        note=note,
        project_ids=project_ids,
    )
    if not response.data:
        typer.echo("Failed to create secret.")
        raise typer.Exit(1)
    typer.echo(f"Created secret: {response.data.key} ({response.data.id})")


if __name__ == "__main__":
    app()
