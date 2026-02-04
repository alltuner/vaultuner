# Soft Delete

Vaultuner implements soft delete to protect against accidental data loss.

## How It Works

When you delete a secret without `--permanent`:

1. The secret is **renamed** with a `_deleted_/` prefix
2. It's **hidden** from normal `list` output
3. It can be **restored** at any time

```bash
# Original secret
myapp/api-key

# After soft delete
_deleted_/myapp/api-key
```

## Viewing Deleted Secrets

```bash
vaultuner list -d
```

This shows both active and deleted secrets with their status.

## Restoring a Secret

```bash
vaultuner restore myapp/api-key
```

The secret is renamed back to its original path.

## Permanent Delete

To bypass soft delete and permanently remove a secret:

```bash
vaultuner delete myapp/api-key --permanent
```

!!! warning
    Permanent deletes cannot be undone. The secret is removed from Bitwarden entirely.

## Why Soft Delete?

Soft delete provides a safety net:

- **Accidental deletion**: Recover secrets deleted by mistake
- **Audit trail**: See what was deleted and when
- **No downtime**: Restore quickly without recreating secrets

## Cleaning Up

To permanently remove all deleted secrets, delete them again with `--permanent`:

```bash
# List deleted secrets
vaultuner list -d

# Permanently remove specific ones
vaultuner delete myapp/old-key --permanent
```
