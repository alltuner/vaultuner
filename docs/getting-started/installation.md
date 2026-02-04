# Installation

## Requirements

- Python 3.11 or 3.12 (bitwarden-sdk limitation)
- macOS (for Keychain credential storage)
- A [Bitwarden Secrets Manager](https://bitwarden.com/products/secrets-manager/) account

## Install with uv (Recommended)

The fastest way to install vaultuner is using [uv](https://docs.astral.sh/uv/):

```bash
uv tool install vaultuner
```

This installs vaultuner as a standalone tool with its own isolated environment.

## Run Without Installing

You can also run vaultuner directly without installing:

```bash
uvx vaultuner list
uvx vaultuner get myapp/api-key
```

This is useful for one-off commands or trying vaultuner before committing to an install.

## Verify Installation

```bash
vaultuner --version
```

## Next Steps

After installation, [configure your credentials](configuration.md).
