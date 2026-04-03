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
| `VALUE` | The secret value (omit when using `--generate`) |

## Options

| Option | Short | Description |
|--------|-------|-------------|
| `--note` | `-n` | Optional free-text note |
| `--description` | `-d` | Secret description (stored as [metadata](../concepts/metadata.md)) |
| `--generate` | `-g` | Generate a random value instead of providing one |

## Examples

```bash
# Create a project-level secret
vaultuner set myapp/api-key "sk-test-abc123"

# Create an environment-specific secret
vaultuner set myapp/prod/db-password "super-secret"

# Add a description
vaultuner set myapp/api-key "sk-test-abc123" --description "Stripe test key"

# Add a note
vaultuner set myapp/api-key "sk-test-abc123" -n "Rotated quarterly"

# Combine description and note
vaultuner set myapp/api-key "sk-test-abc123" -d "Stripe test key" -n "Rotated quarterly"

# Update an existing secret
vaultuner set myapp/api-key "new-value"

# Update only metadata (value unchanged)
vaultuner set myapp/api-key --description "Updated description"

# Generate and store a random secret
vaultuner set myapp/prod/api-key --generate
```

## Behavior

- If the secret doesn't exist, it's created (requires a value or `--generate`)
- If the secret exists, it's updated
- When only `--description` or `--note` is provided (no value), the existing value is preserved
- Metadata is stored as YAML frontmatter in the note field (see [metadata](../concepts/metadata.md))
- The secret is automatically associated with a project in Bitwarden
- When `--generate` is used, a 24-character random value is created and printed to the console
- Cannot combine `--generate` with an explicit value
