# ABOUTME: Data models for vaultuner.
# ABOUTME: SecretPath represents the PROJECT/[ENV/]SECRET naming convention.

from pydantic import BaseModel


class SecretPath(BaseModel):
    project: str
    name: str
    env: str | None = None

    @classmethod
    def parse(cls, path: str) -> "SecretPath":
        """Parse a path like 'project/env/name' or 'project/name'."""
        parts = path.split("/")
        if len(parts) == 3:
            return cls(project=parts[0], env=parts[1], name=parts[2])
        elif len(parts) == 2:
            return cls(project=parts[0], name=parts[1])
        else:
            raise ValueError(f"Invalid path format: {path}. Expected PROJECT/[ENV/]NAME")

    def to_key(self) -> str:
        """Convert to Bitwarden secret key format."""
        if self.env:
            return f"{self.project}/{self.env}/{self.name}"
        return f"{self.project}/{self.name}"

    def __str__(self) -> str:
        return self.to_key()
