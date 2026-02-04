# get

Retrieve a secret by its path.

## Usage

```bash
vaultuner get PATH [OPTIONS]
```

## Arguments

| Argument | Description |
|----------|-------------|
| `PATH` | Secret path: `PROJECT/[ENV/]NAME` |

## Options

| Option | Short | Description |
|--------|-------|-------------|
| `--value` | `-v` | Print only the secret value |

## Examples

```bash
# Get a project-level secret
vaultuner get myapp/api-key

# Get an environment-specific secret
vaultuner get myapp/prod/db-password

# Get just the value (for scripts)
vaultuner get myapp/api-key -v

# Use in shell scripts
DB_PASS=$(vaultuner get myapp/prod/db-password -v)
```

## Output

Without `--value`:

```
Path   myapp/api-key
Value  sk-test-abc123
Note   API key for external service
```

With `--value`:

```
sk-test-abc123
```
