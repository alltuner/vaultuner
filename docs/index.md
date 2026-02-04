# Vaultuner

**Human-readable secrets for Bitwarden Secrets Manager.**

Vaultuner replaces cryptic UUIDs with intuitive paths. Your secrets, organized the way you actually think about them.

## Why Vaultuner?

Bitwarden Secrets Manager is excellent for secure credential storage, but its CLI requires UUIDs to reference secrets:

```bash
# What you have to type today
bws secret get 550e8400-e29b-41d4-a716-446655440000
```

Nobody memorizes UUIDs. You end up searching through dashboards or keeping a mapping file. Vaultuner fixes this:

```bash
# What you type with vaultuner
vaultuner get myapp/prod/db-password
```

Secrets organized by project and environment. Instantly memorable. Zero cognitive overhead.

## Key Features

### Path-Based Naming
Reference secrets by meaning, not by ID:
```bash
vaultuner get myapp/prod/api-key
vaultuner set myapp/dev/db-password "localpass"
```

### Environment Isolation
Keep dev, staging, and prod secrets cleanly separated:
```bash
vaultuner list -p myapp -e prod    # Only production secrets
vaultuner export -p myapp -e dev   # Export dev secrets to .env
```

### `.env` Integration
Sync secrets with your local development workflow:
```bash
# Pull secrets into your project
vaultuner export -p myapp -o .env

# Push local secrets to the vault
vaultuner import -p myapp -i .env
```

### Soft Delete & Recovery
Accidentally deleted something? No problem:
```bash
vaultuner delete myapp/api-key     # Soft delete
vaultuner restore myapp/api-key    # Bring it back
vaultuner delete myapp/api-key --permanent  # Actually delete
```

### Secure Credential Storage
Your Bitwarden access token is stored in macOS Keychain, not in plaintext config files.

## Quick Example

```bash
# Install (--python 3.12 required for bitwarden-sdk compatibility)
uv tool install --python 3.12 vaultuner

# Configure once
vaultuner config set access-token <your-token>
vaultuner config set organization-id <your-org-id>

# Start using
vaultuner set myapp/prod/stripe-key "sk-live-abc123"
vaultuner get myapp/prod/stripe-key --value
vaultuner export -p myapp -e prod -o .env.production
```

## Getting Started

1. [Install vaultuner](getting-started/installation.md)
2. [Configure your credentials](getting-started/configuration.md)
3. [Try the quick start guide](getting-started/quickstart.md)

---

Built at [All Tuner Labs](https://alltuner.com) by [David Poblador i Garcia](https://davidpoblador.com)
