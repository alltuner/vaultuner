# Configuration

Vaultuner needs two pieces of information to connect to Bitwarden Secrets Manager:

1. **Access Token**: Authenticates your CLI
2. **Organization ID**: Identifies your Bitwarden organization

## Getting Your Credentials

### Access Token

1. Log in to [Bitwarden Vault](https://vault.bitwarden.com/)
2. Go to **Secrets Manager** > **Machine Accounts**
3. Create a new machine account or select an existing one
4. Generate an access token

### Organization ID

1. In Bitwarden Vault, go to **Organizations**
2. Click on your organization
3. Find the **Organization ID** in the settings

## Storing Credentials

Vaultuner stores credentials securely in your macOS Keychain:

```bash
vaultuner config set access-token <your-access-token>
vaultuner config set organization-id <your-org-id>
```

## Verify Configuration

```bash
vaultuner config show
```

You should see both settings marked as configured.

## Alternative: Environment Variables

If you prefer not to use the Keychain (or on non-macOS systems), set environment variables:

```bash
export BWS_ACCESS_TOKEN="your-access-token"
export BWS_ORGANIZATION_ID="your-org-id"
```

!!! note
    Keychain storage is only available on macOS. On other platforms, use environment variables.

## Next Steps

Once configured, try the [quick start guide](quickstart.md).
