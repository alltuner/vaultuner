# export

Export secrets to a `.env` file.

## Usage

```bash
vaultuner export [OPTIONS]
```

## Options

| Option | Short | Description |
|--------|-------|-------------|
| `--project` | `-p` | Project name (defaults to current directory name) |
| `--env` | `-e` | Filter by environment |
| `--output` | `-o` | Output file path (default: `.env`) |

## Examples

```bash
# Export using current directory as project name
vaultuner export

# Export specific project
vaultuner export -p myapp

# Export only production secrets
vaultuner export -p myapp -e prod

# Custom output file
vaultuner export -p myapp -o secrets.env
```

## Output Format

Secrets are exported in standard `.env` format:

```bash
API_KEY="sk-test-abc123"
DB_PASSWORD="super-secret"
```

### Name Conversion

Secret names are converted to environment variable format:

| Secret Name | Environment Variable |
|-------------|---------------------|
| `api-key` | `API_KEY` |
| `db-password` | `DB_PASSWORD` |

## Behavior

- If the output file exists, new secrets are **appended**
- Existing variables in the file are **not overwritten**
- Skipped variables are noted in comments

## See Also

- [import](import.md) - Import secrets from .env file
