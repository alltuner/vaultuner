# Quick Start

This guide walks you through common vaultuner workflows.

## Create Your First Secret

```bash
vaultuner set myapp/api-key "sk-test-abc123"
```

This creates a secret named `api-key` in the `myapp` project.

## Retrieve a Secret

```bash
# Full output with metadata
vaultuner get myapp/api-key

# Just the value (useful for scripts)
vaultuner get myapp/api-key --value
```

## Environment-Specific Secrets

Use the three-part path for environment-specific secrets:

```bash
# Development
vaultuner set myapp/dev/db-password "dev-password"

# Production
vaultuner set myapp/prod/db-password "prod-password"
```

## List Secrets

```bash
# All secrets
vaultuner list

# Filter by project
vaultuner list -p myapp

# Filter by project and environment
vaultuner list -p myapp -e prod
```

## Export to .env

Export secrets for local development:

```bash
# Export all secrets for a project
vaultuner export -p myapp

# Export only production secrets
vaultuner export -p myapp -e prod -o .env.prod
```

## Import from .env

Import secrets from an existing .env file:

```bash
# Interactive import (confirms each secret)
vaultuner import -p myapp -i .env

# Import all without prompting
vaultuner import -p myapp -i .env -y
```

## Delete and Restore

```bash
# Soft delete (can be restored)
vaultuner delete myapp/api-key

# Restore a deleted secret
vaultuner restore myapp/api-key

# Permanent delete
vaultuner delete myapp/api-key --permanent
```

## Next Steps

- Learn about the [naming convention](../concepts/naming.md)
- Explore all [commands](../commands/list.md)
