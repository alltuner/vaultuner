# ABOUTME: Export project secrets to .env file format.
# ABOUTME: Handles parsing existing .env files and appending new secrets.

from pathlib import Path

from vaultuner.client import get_client
from vaultuner.config import get_settings
from vaultuner.models import SecretPath


def secret_name_to_env_var(name: str) -> str:
    """Convert a secret name to an environment variable name."""
    return name.upper().replace("-", "_")


def parse_env_file(path: Path) -> set[str]:
    """Parse a .env file and return the set of defined variable names."""
    defined_vars: set[str] = set()
    if not path.exists():
        return defined_vars

    for line in path.read_text().splitlines():
        line = line.strip()
        if not line or line.startswith("#"):
            continue
        if "=" in line:
            var_name = line.split("=", 1)[0].strip()
            defined_vars.add(var_name)
    return defined_vars


def is_deleted(key: str) -> bool:
    """Check if a secret key is marked as deleted."""
    return key.startswith("_deleted_/")


def export_secrets(
    project_name: str,
    output: Path,
    env: str | None = None,
) -> tuple[int, int]:
    """
    Export secrets for a project to a .env file.

    Returns a tuple of (added_count, skipped_count).
    """
    settings = get_settings()
    client = get_client()
    response = client.secrets().list(settings.organization_id)

    if not response.data or not response.data.data:
        return 0, 0

    # Find secrets matching the project (and optionally env)
    matching_secrets: list[tuple[SecretPath, str]] = []
    for secret in response.data.data:
        key = secret.key
        if is_deleted(key):
            continue

        try:
            path = SecretPath.parse(key)
        except ValueError:
            continue

        if path.project != project_name:
            continue
        if path.env != env:
            continue

        # Fetch the actual value
        secret_response = client.secrets().get(secret.id)
        if secret_response.data:
            matching_secrets.append((path, secret_response.data.value))

    if not matching_secrets:
        return 0, 0

    # Parse existing .env to find already-defined variables
    existing_vars = parse_env_file(output)

    # Build the lines to append
    lines_to_append: list[str] = []
    added_count = 0
    skipped_count = 0

    for path, value in matching_secrets:
        env_var = secret_name_to_env_var(path.name)
        env_line = f'{env_var}="{value}"'

        if env_var in existing_vars:
            lines_to_append.append(f"# Already defined above, from {path}:")
            lines_to_append.append(f"# {env_line}")
            skipped_count += 1
        else:
            lines_to_append.append(env_line)
            existing_vars.add(env_var)
            added_count += 1

    # Append to file
    if lines_to_append:
        with output.open("a") as f:
            if output.exists() and output.stat().st_size > 0:
                # Ensure we start on a new line
                f.write("\n")
            f.write("\n".join(lines_to_append))
            f.write("\n")

    return added_count, skipped_count
