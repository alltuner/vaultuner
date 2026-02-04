# ABOUTME: Import secrets from .env file to Bitwarden Secrets Manager.
# ABOUTME: Parses .env files and interactively stores secrets.

from pathlib import Path


def env_var_to_secret_name(var_name: str) -> str:
    """Convert an environment variable name to a secret name."""
    return var_name


def parse_env_entries(path: Path) -> list[tuple[str, str]]:
    """Parse a .env file and return list of (name, value) tuples."""
    entries: list[tuple[str, str]] = []
    if not path.exists():
        return entries

    for line in path.read_text().splitlines():
        line = line.strip()
        if not line or line.startswith("#"):
            continue
        if "=" not in line:
            continue

        var_name, _, value = line.partition("=")
        var_name = var_name.strip()
        value = value.strip()

        # Remove surrounding quotes if present
        if len(value) >= 2 and value[0] == value[-1] and value[0] in ('"', "'"):
            value = value[1:-1]

        entries.append((var_name, value))

    return entries


def build_secret_path(project: str, env: str | None, name: str) -> str:
    """Build a secret path from components."""
    if env:
        return f"{project}/{env}/{name}"
    return f"{project}/{name}"
