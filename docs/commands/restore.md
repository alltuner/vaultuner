# restore

Restore a soft-deleted secret.

## Usage

```bash
vaultuner restore PATH
```

## Arguments

| Argument | Description |
|----------|-------------|
| `PATH` | Original secret path: `PROJECT/[ENV/]NAME` |

## Examples

```bash
# Restore a deleted secret
vaultuner restore myapp/api-key

# Check what's deleted first
vaultuner list -d
```

## Notes

- Only works for soft-deleted secrets (deleted without `--permanent`)
- Use `vaultuner list -d` to see deleted secrets
- The secret is restored to its original path

## See Also

- [delete](delete.md) - Delete a secret
- [Soft Delete concept](../concepts/soft-delete.md)
