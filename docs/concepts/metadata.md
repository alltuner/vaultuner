# Secret Metadata

Vaultuner supports storing structured metadata alongside each secret using the note field. Metadata is stored as YAML frontmatter at the beginning of the note.

## Format

```
---
description: Production database credentials
---
Optional free-text note content here.
```

The frontmatter block is delimited by `---` lines. Any text after the closing `---` is preserved as the note body.

## Available Fields

| Field | Type | Description |
|-------|------|-------------|
| `description` | string | A human-readable description of the secret |

## How It Works

Metadata is stored inside Bitwarden's `note` field using YAML frontmatter. This means:

- **No extra API calls** — metadata is read and written alongside the secret
- **Backward compatible** — existing secrets without frontmatter continue to work normally
- **Non-destructive** — adding metadata to a secret with an existing plain-text note preserves the note as the body

## Examples

### Add a description when creating a secret

```bash
vaultuner set myapp/api-key "sk-abc123" --description "Stripe test key"
```

### Add a description to an existing secret (without changing its value)

```bash
vaultuner set myapp/api-key --description "Stripe test key"
```

### View metadata

```bash
vaultuner get myapp/api-key
```

```
Path         myapp/api-key
Value        sk-abc123
Description  Stripe test key
```

### Combine description and note

```bash
vaultuner set myapp/api-key "sk-abc123" \
  --description "Stripe test key" \
  --note "Rotated quarterly"
```

```bash
vaultuner get myapp/api-key
```

```
Path         myapp/api-key
Value        sk-abc123
Description  Stripe test key
Note         Rotated quarterly
```
