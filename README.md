<h1 align="center">vaultuner</h1>

<p align="center">
  <strong>Human-readable secrets for Bitwarden Secrets Manager.</strong><br>
  Replace cryptic UUIDs with intuitive paths like <code>myapp/prod/db-password</code>.
</p>

<p align="center">
  <a href="https://vaultuner.alltuner.com">Docs</a> &middot;
  <a href="https://github.com/sponsors/alltuner">Sponsor</a>
</p>

<p align="center">
  <img src="https://img.shields.io/pypi/v/vaultuner?color=5B2333" alt="PyPI">
  <img src="https://img.shields.io/github/license/alltuner/vaultuner?color=5B2333" alt="License">
  <img src="https://img.shields.io/github/stars/alltuner/vaultuner?color=5B2333" alt="Stars">
</p>

---

## Get Started

```bash
uv tool install vaultuner
```

Or run without installing:

```bash
uvx vaultuner list
```

Configure once:

```bash
vaultuner config set access-token <your-token>
vaultuner config set organization-id <your-org-id>
```

Credentials come from [Bitwarden Secrets Manager](https://vault.bitwarden.com/).

---

## What is vaultuner?

Bitwarden Secrets Manager addresses every secret by UUID. Looking one up means digging through the dashboard or memorising hex strings. vaultuner sits on top and lets you address secrets by readable paths organised by project and environment, so retrieving a secret feels like reading a config file:

```bash
# Bitwarden CLI
bws secret get 550e8400-e29b-41d4-a716-446655440000

# vaultuner
vaultuner get myapp/prod/db-password
```

### Features

- **Path-based naming** — `project/env/secret` instead of UUIDs.
- **Environment isolation** — keep dev, staging, and prod secrets separate.
- **`.env` sync** — export to and import from `.env` files seamlessly.
- **Secret metadata** — attach descriptions via `--description`.
- **Soft delete** — recover accidentally deleted secrets.
- **Keychain storage** — credentials secured in the macOS Keychain.

## Usage

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

### Commands

| Command    | Description                                  |
|------------|----------------------------------------------|
| `list`     | List secrets with project/env filtering      |
| `get`      | Retrieve a secret value                      |
| `set`      | Create or update a secret                    |
| `delete`   | Soft-delete (recoverable)                    |
| `restore`  | Recover a deleted secret                     |
| `export`   | Export to `.env` file                        |
| `import`   | Import from `.env` file                      |
| `projects` | List all projects                            |
| `config`   | Manage stored credentials                    |

### Naming convention

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

- Python 3.11+
- macOS (Keychain integration)
- Bitwarden Secrets Manager account

## Documentation

Full docs at [vaultuner.alltuner.com](https://vaultuner.alltuner.com).

## Support the project

vaultuner is an open source project built by [David Poblador i Garcia](https://davidpoblador.com/) through [All Tuner Labs](https://www.alltuner.com/).

If this project was useful to you, consider supporting its development.

❤️ **Sponsor development**
https://github.com/sponsors/alltuner

☕ **One-time support**
https://buymeacoffee.com/alltuner

Your support helps fund the continued development of vaultuner and other open source developer tools such as [Factory Floor](https://github.com/alltuner/factoryfloor).

## License

[MIT](LICENSE)

---

<p align="center">
  Built by <a href="https://davidpoblador.com">David Poblador i Garcia</a> with the support of <a href="https://alltuner.com">All Tuner Labs</a>.<br>
  Made with ❤️ in Poblenou, Barcelona.
</p>
