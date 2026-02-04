# vaultuner

Bitwarden Secrets Manager CLI with `PROJECT/[ENV/]SECRET` naming convention.

## Requirements

- Python 3.12

## Installation

```bash
uv tool install git+https://github.com/alltuner/vaultuner --python 3.12
```

## Configuration

Store your Bitwarden Secrets Manager credentials:

```bash
vaultuner config set access-token <your-access-token>
vaultuner config set organization-id <your-org-id>
```

Credentials are stored securely in your system keychain.

## Usage

### List secrets

```bash
vaultuner list
vaultuner list -p myproject
vaultuner list -p myproject -e prod
```

### Get a secret

```bash
vaultuner get myproject/api-key
vaultuner get myproject/prod/db-password
vaultuner get myproject/api-key --value  # value only
```

### Set a secret

```bash
vaultuner set myproject/api-key "secret-value"
vaultuner set myproject/prod/db-password "password" --note "Production DB"
```

### Delete a secret

```bash
vaultuner delete myproject/api-key           # soft delete
vaultuner delete myproject/api-key --permanent  # hard delete
```

### Restore a deleted secret

```bash
vaultuner restore myproject/api-key
```

### Export to .env file

```bash
vaultuner export                    # uses current directory name as project
vaultuner export -p myproject       # specify project
vaultuner export -p myproject -e prod  # filter by environment
vaultuner export -o secrets.env     # custom output file
```

### List projects

```bash
vaultuner projects
```

## Secret naming convention

Secrets follow the pattern `PROJECT/[ENV/]SECRET`:

- `myapp/api-key` - project-level secret (no environment)
- `myapp/prod/db-password` - environment-specific secret
