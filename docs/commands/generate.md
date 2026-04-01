# generate

Generate a cryptographically secure random secret value.

## Usage

```bash
vaultuner generate [OPTIONS]
```

## Options

| Option | Short | Description | Default |
|--------|-------|-------------|---------|
| `--length` | `-l` | Length of generated secret | `24` |
| `--no-lowercase` | | Exclude lowercase letters | Off |
| `--no-uppercase` | | Exclude uppercase letters | Off |
| `--no-numbers` | | Exclude digits | Off |
| `--no-special` | | Exclude special characters (`!@#$%^&*`) | Off |
| `--allow-ambiguous` | | Allow ambiguous characters (`I`, `O`, `l`, `0`, `1`) | Off |

## Examples

```bash
# Generate a 24-character secret (default)
vaultuner generate

# Generate a longer secret
vaultuner generate --length 64

# Letters and numbers only
vaultuner generate --no-special

# Alphanumeric lowercase only
vaultuner generate --no-uppercase --no-special
```

## Behavior

- Uses Python's `secrets` module for cryptographically secure randomness
- Ambiguous characters (`I`, `O`, `l`, `0`, `1`) are excluded by default to avoid confusion when copying values manually
- At least one character set must be enabled
- Output is printed to stdout with no extra formatting, making it easy to pipe into other commands

!!! tip
    Use `vaultuner set PATH --generate` to generate and store a secret in one step. See [set](set.md) for details.
