# Installation

## Requirements

- Python 3.12
- macOS (for Keychain credential storage)
- A [Bitwarden Secrets Manager](https://bitwarden.com/products/secrets-manager/) account

## Install with uv (Recommended)

The fastest way to install vaultuner is using [uv](https://docs.astral.sh/uv/):

```bash
uv tool install git+https://github.com/alltuner/vaultuner --python 3.12
```

This installs vaultuner as a standalone tool with its own isolated environment.

## Install with pip

```bash
pip install git+https://github.com/alltuner/vaultuner
```

## Verify Installation

```bash
vaultuner --version
```

## Next Steps

After installation, [configure your credentials](configuration.md).
