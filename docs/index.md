# Vaultuner

**A developer-friendly CLI for Bitwarden Secrets Manager** with intuitive `PROJECT/[ENV/]SECRET` naming.

Stop managing cryptic secret IDs. Vaultuner organizes your secrets the way you think about them: by project and environment.

## Why Vaultuner?

Bitwarden Secrets Manager is powerful, but its default CLI uses UUIDs to reference secrets. Vaultuner gives you a human-friendly naming system:

```bash
# Instead of this:
bws secret get 550e8400-e29b-41d4-a716-446655440000

# You get this:
vaultuner get myapp/prod/db-password
```

## Features

- **Intuitive naming**: `myapp/prod/db-password` instead of UUIDs
- **Project organization**: Group secrets by project automatically
- **Environment support**: Separate dev, staging, and prod secrets
- **Soft delete**: Recover accidentally deleted secrets
- **Export/Import**: Sync with `.env` files for local development
- **Secure storage**: Credentials stored in macOS Keychain

## Quick Example

```bash
# Store a secret
vaultuner set myapp/prod/api-key "sk-live-abc123"

# Retrieve it
vaultuner get myapp/prod/api-key --value

# Export all prod secrets to .env
vaultuner export -p myapp -e prod -o .env
```

## Getting Started

1. [Install vaultuner](getting-started/installation.md)
2. [Configure your credentials](getting-started/configuration.md)
3. [Try the quick start guide](getting-started/quickstart.md)
