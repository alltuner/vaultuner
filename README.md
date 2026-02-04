# vaultuner

[![PyPI version](https://img.shields.io/github/v/release/alltuner/vaultuner)](https://github.com/alltuner/vaultuner/releases)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.12](https://img.shields.io/badge/python-3.12-blue.svg)](https://www.python.org/downloads/)

**A developer-friendly CLI for Bitwarden Secrets Manager** with intuitive `PROJECT/[ENV/]SECRET` naming.

Stop managing cryptic secret IDs. Vaultuner organizes your secrets the way you think about them: by project and environment.

## Features

- **Intuitive naming**: `myapp/prod/db-password` instead of UUIDs
- **Project organization**: Group secrets by project automatically
- **Environment support**: Separate dev, staging, and prod secrets
- **Soft delete**: Recover accidentally deleted secrets
- **Export/Import**: Sync with `.env` files for local development
- **Secure storage**: Credentials stored in macOS Keychain

## Quick Start

### Installation

```bash
uv tool install git+https://github.com/alltuner/vaultuner --python 3.12
```

### Configuration

```bash
vaultuner config set access-token <your-access-token>
vaultuner config set organization-id <your-org-id>
```

Get your access token from the [Bitwarden Secrets Manager](https://vault.bitwarden.com/).

### Basic Usage

```bash
# Create a secret
vaultuner set myapp/api-key "sk-abc123"

# Get a secret
vaultuner get myapp/api-key

# List all secrets
vaultuner list

# Export to .env for local development
vaultuner export -p myapp -o .env
```

## Documentation

Full documentation available at [alltuner.github.io/vaultuner](https://alltuner.github.io/vaultuner).

## Commands

| Command | Description |
|---------|-------------|
| `list` | List secrets (filter by project/env) |
| `get` | Retrieve a secret value |
| `set` | Create or update a secret |
| `delete` | Soft-delete a secret |
| `restore` | Restore a deleted secret |
| `export` | Export secrets to .env file |
| `import` | Import secrets from .env file |
| `projects` | List all projects |
| `config` | Manage credentials |

## Secret Naming Convention

Secrets follow the pattern `PROJECT/[ENV/]SECRET`:

```
myapp/api-key              # Project-level secret
myapp/prod/db-password     # Environment-specific secret
myapp/dev/db-password      # Different value per environment
```

## Requirements

- Python 3.12
- macOS (for Keychain support)
- Bitwarden Secrets Manager account

## License

MIT License - see [LICENSE](LICENSE) for details.
