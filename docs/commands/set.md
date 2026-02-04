# set

Create or update a secret.

## Usage

```bash
vaultuner set PATH VALUE [OPTIONS]
```

## Arguments

| Argument | Description |
|----------|-------------|
| `PATH` | Secret path: `PROJECT/[ENV/]NAME` |
| `VALUE` | The secret value |

## Options

| Option | Short | Description |
|--------|-------|-------------|
| `--note` | `-n` | Optional note/description |

## Examples

```bash
# Create a project-level secret
vaultuner set myapp/api-key "sk-test-abc123"

# Create an environment-specific secret
vaultuner set myapp/prod/db-password "super-secret"

# Add a note
vaultuner set myapp/api-key "sk-test-abc123" -n "Stripe test key"

# Update an existing secret
vaultuner set myapp/api-key "new-value"
```

## Behavior

- If the secret doesn't exist, it's created
- If the secret exists, it's updated
- The secret is automatically associated with a project in Bitwarden
