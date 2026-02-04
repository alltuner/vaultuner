# list

List secrets in your organization.

## Usage

```bash
vaultuner list [OPTIONS]
```

## Options

| Option | Short | Description |
|--------|-------|-------------|
| `--project` | `-p` | Filter by project name |
| `--env` | `-e` | Filter by environment |
| `--deleted` | `-d` | Show deleted secrets |

## Examples

```bash
# List all secrets
vaultuner list

# List secrets for a project
vaultuner list -p myapp

# List production secrets
vaultuner list -p myapp -e prod

# Include deleted secrets
vaultuner list -d
```

## Output

Displays a table with columns:

- **Project**: The project name
- **Env**: The environment (or `-` if none)
- **Name**: The secret name
- **Status**: (only with `--deleted`) Shows if secret is active or deleted
