# config

Manage vaultuner credentials.

## Usage

```bash
vaultuner config COMMAND [OPTIONS]
```

## Commands

### config set

Store a credential in the system keychain.

```bash
vaultuner config set KEY VALUE
```

**Keys:**

- `access-token` - Your Bitwarden access token
- `organization-id` - Your Bitwarden organization ID

**Examples:**

```bash
vaultuner config set access-token "0.abc123..."
vaultuner config set organization-id "550e8400-e29b-..."
```

### config show

Show current configuration status.

```bash
vaultuner config show
```

**Output:**

```
┏━━━━━━━━━━━━━━━━━━┳━━━━━━━━━━━━━━┓
┃ Setting          ┃ Status       ┃
┡━━━━━━━━━━━━━━━━━━╇━━━━━━━━━━━━━━┩
│ access-token     │ configured   │
│ organization-id  │ configured   │
└──────────────────┴──────────────┘
```

### config delete

Remove a credential from the system keychain.

```bash
vaultuner config delete KEY
```

**Examples:**

```bash
vaultuner config delete access-token
vaultuner config delete organization-id
```

## Storage

Credentials are stored securely in the macOS Keychain under the service name `vaultuner`.

!!! note
    Keychain storage is only available on macOS. On other platforms, use environment variables `BWS_ACCESS_TOKEN` and `BWS_ORGANIZATION_ID`.
