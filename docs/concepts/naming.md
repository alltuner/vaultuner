# Naming Convention

Vaultuner uses a hierarchical naming system: `PROJECT/[ENV/]SECRET`

## Path Format

### Two-Part Path: `PROJECT/SECRET`

For secrets that don't vary by environment:

```bash
myapp/api-key
myapp/encryption-key
backend/jwt-secret
```

### Three-Part Path: `PROJECT/ENV/SECRET`

For environment-specific secrets:

```bash
myapp/dev/db-password
myapp/staging/db-password
myapp/prod/db-password
```

## Naming Best Practices

### Project Names

- Use lowercase
- Match your repository or service name
- Examples: `myapp`, `backend-api`, `payment-service`

### Environment Names

Common patterns:

- `dev`, `staging`, `prod`
- `development`, `test`, `production`
- `local`, `ci`, `preview`

### Secret Names

- Use lowercase with dashes
- Be descriptive but concise
- Examples: `api-key`, `db-password`, `stripe-secret-key`

## Examples

```bash
# Web application
webapp/stripe-api-key           # Shared across environments
webapp/dev/database-url         # Development database
webapp/prod/database-url        # Production database

# Microservice
user-service/jwt-secret
user-service/prod/redis-url

# Infrastructure
infra/aws-access-key
infra/prod/cloudflare-api-token
```

## Name Conversion

When exporting to `.env`, names are converted:

| Secret Name | Environment Variable |
|-------------|---------------------|
| `api-key` | `API_KEY` |
| `db-password` | `DB_PASSWORD` |
| `stripe-secret-key` | `STRIPE_SECRET_KEY` |

When importing from `.env`, the reverse conversion happens.
