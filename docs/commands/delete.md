# delete

Delete a secret.

## Usage

```bash
vaultuner delete PATH [OPTIONS]
```

## Arguments

| Argument | Description |
|----------|-------------|
| `PATH` | Secret path: `PROJECT/[ENV/]NAME` |

## Options

| Option | Short | Description |
|--------|-------|-------------|
| `--force` | `-f` | Skip confirmation prompt |
| `--permanent` | | Permanently delete (cannot be restored) |

## Examples

```bash
# Soft delete (can be restored)
vaultuner delete myapp/api-key

# Skip confirmation
vaultuner delete myapp/api-key -f

# Permanent delete
vaultuner delete myapp/api-key --permanent
```

## Soft Delete vs Permanent Delete

By default, `delete` performs a **soft delete**:

- The secret is renamed with a `_deleted_/` prefix
- It's hidden from normal `list` output
- It can be recovered with `vaultuner restore`

With `--permanent`, the secret is **permanently removed** from Bitwarden and cannot be recovered.

!!! warning
    Permanent deletes cannot be undone. Use with caution.

## See Also

- [restore](restore.md) - Restore a soft-deleted secret
