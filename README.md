# vaultuner

[![PyPI version](https://img.shields.io/pypi/v/vaultuner)](https://pypi.org/project/vaultuner/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.11-3.12](https://img.shields.io/badge/python-3.11--3.12-blue.svg)](https://www.python.org/downloads/)

**Human-readable secrets for Bitwarden Secrets Manager.**

Vaultuner replaces cryptic UUIDs with intuitive paths like `myapp/prod/db-password`. Your secrets, organized the way you actually think about them.

## The Problem

```bash
# Bitwarden's default CLI
bws secret get 550e8400-e29b-41d4-a716-446655440000
```

You shouldn't need to memorize UUIDs or dig through dashboards to find secrets.

## The Solution

```bash
# With vaultuner
vaultuner get myapp/prod/db-password
```

Secrets organized by project and environment. Instantly memorable. Zero cognitive overhead.

## Features

- **Path-based naming** - `project/env/secret` instead of UUIDs
- **Environment isolation** - Keep dev, staging, and prod secrets separate
- **`.env` sync** - Export to and import from `.env` files seamlessly
- **Soft delete** - Recover accidentally deleted secrets
- **Keychain storage** - Credentials secured in macOS Keychain

## Quick Start

### Install

```bash
uv tool install vaultuner
```

Or run without installing:

```bash
uvx vaultuner list
```

### Configure

```bash
vaultuner config set access-token <your-token>
vaultuner config set organization-id <your-org-id>
```

Get credentials from [Bitwarden Secrets Manager](https://vault.bitwarden.com/).

### Use

```bash
# Create secrets
vaultuner set myapp/api-key "sk-abc123"
vaultuner set myapp/prod/db-password "hunter2"

# Retrieve
vaultuner get myapp/prod/db-password -v

# List everything
vaultuner list

# Export for local dev
vaultuner export -p myapp -e dev -o .env
```

## Commands

| Command | Description |
|---------|-------------|
| `list` | List secrets with project/env filtering |
| `get` | Retrieve a secret value |
| `set` | Create or update a secret |
| `delete` | Soft-delete (recoverable) |
| `restore` | Recover a deleted secret |
| `export` | Export to `.env` file |
| `import` | Import from `.env` file |
| `projects` | List all projects |
| `config` | Manage stored credentials |

## Naming Convention

```
PROJECT/SECRET           # Project-level secret
PROJECT/ENV/SECRET       # Environment-specific secret
```

Examples:
```
myapp/api-key            # Shared across environments
myapp/prod/db-password   # Production only
myapp/dev/db-password    # Development only
```

## Requirements

- Python 3.11 or 3.12 (bitwarden-sdk limitation)
- macOS (Keychain integration)
- Bitwarden Secrets Manager account

## Documentation

Full docs at [alltuner.github.io/vaultuner](https://alltuner.github.io/vaultuner)

## License

MIT

---

Built at [All Tuner Labs](https://alltuner.com) by [David Poblador i Garcia](https://davidpoblador.com)
