# ABOUTME: Typer CLI for Bitwarden Secrets Manager.
# ABOUTME: Commands for listing, getting, setting, and deleting secrets.

import typer
from rich.console import Console
from rich.table import Table

from vaultuner.client import find_secret_by_key, get_client, get_or_create_project
from vaultuner.config import settings
from vaultuner.models import SecretPath

DELETED_PREFIX = "_deleted_/"

app = typer.Typer(
    help="Bitwarden Secrets Manager CLI with PROJECT/[ENV/]SECRET naming.",
    no_args_is_help=True,
)
console = Console()
err_console = Console(stderr=True)


def is_deleted(key: str) -> bool:
    return key.startswith(DELETED_PREFIX)


def mark_deleted(key: str) -> str:
    return f"{DELETED_PREFIX}{key}"


def unmark_deleted(key: str) -> str:
    return key.removeprefix(DELETED_PREFIX)


@app.command("list")
def list_secrets(
    project: str | None = typer.Option(None, "--project", "-p", help="Filter by project"),
    env: str | None = typer.Option(None, "--env", "-e", help="Filter by environment"),
    deleted: bool = typer.Option(False, "--deleted", "-d", help="Show deleted secrets"),
):
    """List secrets. Optionally filter by project and/or environment."""
    client = get_client()
    response = client.secrets().list(settings.organization_id)
    if not response.data or not response.data.data:
        console.print("[dim]No secrets found.[/dim]")
        return

    table = Table(show_header=True, header_style="bold")
    table.add_column("Project", style="cyan")
    table.add_column("Env", style="yellow")
    table.add_column("Name", style="green")
    if deleted:
        table.add_column("Status", style="red")

    count = 0
    for secret in response.data.data:
        key = secret.key
        secret_deleted = is_deleted(key)

        if secret_deleted and not deleted:
            continue

        display_key = unmark_deleted(key) if secret_deleted else key

        try:
            path = SecretPath.parse(display_key)
        except ValueError:
            continue

        if project and path.project != project:
            continue
        if env and path.env != env:
            continue

        if deleted:
            status = "[red]deleted[/red]" if secret_deleted else "[green]active[/green]"
            table.add_row(path.project, path.env or "-", path.name, status)
        else:
            table.add_row(path.project, path.env or "-", path.name)
        count += 1

    if count == 0:
        console.print("[dim]No secrets found.[/dim]")
    else:
        console.print(table)


@app.command()
def get(
    path: str = typer.Argument(..., help="Secret path: PROJECT/[ENV/]NAME"),
    value_only: bool = typer.Option(False, "--value", "-v", help="Print only the value"),
):
    """Get a secret by path."""
    client = get_client()
    secret_info = find_secret_by_key(client, path)
    if not secret_info:
        err_console.print(f"[red]Secret not found:[/red] {path}")
        raise typer.Exit(1)

    response = client.secrets().get(secret_info["id"])
    if not response.data:
        err_console.print(f"[red]Failed to retrieve secret:[/red] {path}")
        raise typer.Exit(1)

    if value_only:
        console.print(response.data.value)
    else:
        table = Table(show_header=False, box=None)
        table.add_column("Label", style="dim")
        table.add_column("Value")
        table.add_row("Path", f"[cyan]{response.data.key}[/cyan]")
        table.add_row("Value", f"[green]{response.data.value}[/green]")
        if response.data.note:
            table.add_row("Note", f"[dim]{response.data.note}[/dim]")
        console.print(table)


@app.command()
def set(
    path: str = typer.Argument(..., help="Secret path: PROJECT/[ENV/]NAME"),
    value: str = typer.Argument(..., help="Secret value"),
    note: str | None = typer.Option(None, "--note", "-n", help="Optional note"),
):
    """Create or update a secret."""
    secret_path = SecretPath.parse(path)
    client = get_client()

    existing = find_secret_by_key(client, path)
    if existing:
        response = client.secrets().update(
            organization_id=settings.organization_id,
            id=existing["id"],
            key=path,
            value=value,
            note=note,
            project_ids=None,
        )
        if not response.data:
            err_console.print("[red]Failed to update secret.[/red]")
            raise typer.Exit(1)
        console.print(f"[yellow]Updated:[/yellow] {path}")
    else:
        project_id = get_or_create_project(client, secret_path.project)
        response = client.secrets().create(
            organization_id=settings.organization_id,
            key=path,
            value=value,
            note=note,
            project_ids=[project_id],
        )
        if not response.data:
            err_console.print("[red]Failed to create secret.[/red]")
            raise typer.Exit(1)
        console.print(f"[green]Created:[/green] {path}")


@app.command()
def delete(
    path: str = typer.Argument(..., help="Secret path: PROJECT/[ENV/]NAME"),
    force: bool = typer.Option(False, "--force", "-f", help="Skip confirmation"),
    permanent: bool = typer.Option(False, "--permanent", help="Permanently delete"),
):
    """Delete a secret (soft-delete by default)."""
    client = get_client()
    secret_info = find_secret_by_key(client, path)
    if not secret_info:
        err_console.print(f"[red]Secret not found:[/red] {path}")
        raise typer.Exit(1)

    if not force:
        action = "permanently delete" if permanent else "delete"
        confirm = typer.confirm(f"{action.capitalize()} secret '{path}'?")
        if not confirm:
            raise typer.Abort()

    if permanent:
        client.secrets().delete([secret_info["id"]])
        console.print(f"[red]Permanently deleted:[/red] {path}")
    else:
        response = client.secrets().get(secret_info["id"])
        if not response.data:
            err_console.print("[red]Failed to get secret for deletion.[/red]")
            raise typer.Exit(1)

        deleted_key = mark_deleted(path)
        project_ids = [str(response.data.project_id)] if response.data.project_id else None
        client.secrets().update(
            organization_id=settings.organization_id,
            id=secret_info["id"],
            key=deleted_key,
            value=response.data.value,
            note=response.data.note,
            project_ids=project_ids,
        )
        console.print(f"[red]Deleted:[/red] {path}")


@app.command()
def restore(
    path: str = typer.Argument(..., help="Secret path: PROJECT/[ENV/]NAME"),
):
    """Restore a soft-deleted secret."""
    client = get_client()
    deleted_key = mark_deleted(path)
    secret_info = find_secret_by_key(client, deleted_key)
    if not secret_info:
        err_console.print(f"[red]Deleted secret not found:[/red] {path}")
        raise typer.Exit(1)

    response = client.secrets().get(secret_info["id"])
    if not response.data:
        err_console.print("[red]Failed to get secret for restoration.[/red]")
        raise typer.Exit(1)

    project_ids = [str(response.data.project_id)] if response.data.project_id else None
    client.secrets().update(
        organization_id=settings.organization_id,
        id=secret_info["id"],
        key=path,
        value=response.data.value,
        note=response.data.note,
        project_ids=project_ids,
    )
    console.print(f"[green]Restored:[/green] {path}")


@app.command()
def projects():
    """List all projects."""
    client = get_client()
    response = client.projects().list(settings.organization_id)
    if not response.data or not response.data.data:
        console.print("[dim]No projects found.[/dim]")
        return

    table = Table(show_header=True, header_style="bold")
    table.add_column("Project", style="cyan")

    for project in response.data.data:
        table.add_row(project.name)

    console.print(table)


def main():
    app()


if __name__ == "__main__":
    main()
