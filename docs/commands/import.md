# import

Import secrets from a `.env` file.

## Usage

```bash
vaultuner import [OPTIONS]
```

## Options

| Option | Short | Description |
|--------|-------|-------------|
| `--project` | `-p` | Project name (defaults to current directory name) |
| `--env` | `-e` | Environment for imported secrets |
| `--input` | `-i` | Input file path (default: `.env`) |
| `--yes` | `-y` | Import all without prompting |

## Examples

```bash
# Interactive import from .env
vaultuner import

# Import to specific project
vaultuner import -p myapp

# Import as production secrets
vaultuner import -p myapp -e prod

# Custom input file
vaultuner import -p myapp -i secrets.env

# Import all without confirmation
vaultuner import -p myapp -y
```

## Interactive Mode

By default, import runs interactively:

```
API_KEY = sk-test-abc...
  → myapp/api-key
Store this secret? [Y/n]:
```

Use `-y` to skip confirmations and import all secrets.

## Name Conversion

Environment variable names are converted to secret names:

| Environment Variable | Secret Name |
|---------------------|-------------|
| `API_KEY` | `api-key` |
| `DB_PASSWORD` | `db-password` |

## Behavior

- Existing secrets are **skipped** (not overwritten)
- Blank lines and comments are ignored
- Quoted values have quotes stripped

## See Also

- [export](export.md) - Export secrets to .env file
