# Installation

## Requirements

- Python 3.11 or 3.12 (bitwarden-sdk limitation)
- macOS (for Keychain credential storage)
- A [Bitwarden Secrets Manager](https://bitwarden.com/products/secrets-manager/) account

## Install with uv (Recommended)

The fastest way to install vaultuner is using [uv](https://docs.astral.sh/uv/):

```bash
uv tool install --python 3.12 vaultuner
```

This installs vaultuner as a standalone tool with its own isolated environment.

!!! note "Why `--python 3.12`?"
    The bitwarden-sdk dependency only provides pre-built wheels for Python 3.11 and 3.12. Without this flag, uv may attempt to use a newer Python version and fail to install.

## Run Without Installing

You can also run vaultuner directly without installing:

```bash
uvx --python 3.12 vaultuner list
uvx --python 3.12 vaultuner get myapp/api-key
```

This is useful for one-off commands or trying vaultuner before committing to an install.

## Verify Installation

```bash
vaultuner --version
```

## Next Steps

After installation, [configure your credentials](configuration.md).
