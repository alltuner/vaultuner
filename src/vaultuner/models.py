# ABOUTME: Data models for vaultuner.
# ABOUTME: SecretPath (plain and @org/repo scoped), SecretMetadata, and note frontmatter parsing.

from pydantic import BaseModel, ConfigDict

import yaml

DELETED_PREFIX = "_deleted_/"


def is_deleted(key: str) -> bool:
    """Check if a secret key is marked as deleted."""
    return key.startswith(DELETED_PREFIX)


def mark_deleted(key: str) -> str:
    """Mark a secret key as deleted by adding the prefix."""
    return f"{DELETED_PREFIX}{key}"


def unmark_deleted(key: str) -> str:
    """Remove the deleted prefix from a secret key."""
    return key.removeprefix(DELETED_PREFIX)


class SecretPath(BaseModel):
    project: str
    name: str
    env: str | None = None

    @classmethod
    def parse(cls, path: str) -> "SecretPath":
        """Parse a path like 'project/env/name' or '@org/repo/env/name'."""
        parts = path.split("/")

        if any(not part for part in parts):
            raise ValueError(
                f"Invalid path format: {path}. Path segments cannot be empty."
            )

        is_scoped = parts[0].startswith("@")

        if is_scoped and len(parts[0]) == 1:
            raise ValueError(
                f"Invalid path format: {path}. Path segments cannot be empty."
            )

        if is_scoped:
            if len(parts) == 4:
                return cls(project=f"{parts[0]}/{parts[1]}", env=parts[2], name=parts[3])
            elif len(parts) == 3:
                return cls(project=f"{parts[0]}/{parts[1]}", name=parts[2])
            else:
                raise ValueError(
                    f"Invalid path format: {path}. Expected @ORG/REPO/[ENV/]NAME"
                )
        else:
            if len(parts) == 3:
                return cls(project=parts[0], env=parts[1], name=parts[2])
            elif len(parts) == 2:
                return cls(project=parts[0], name=parts[1])
            else:
                raise ValueError(
                    f"Invalid path format: {path}. Expected PROJECT/[ENV/]NAME"
                )

    def to_key(self) -> str:
        """Convert to Bitwarden secret key format."""
        if self.env:
            return f"{self.project}/{self.env}/{self.name}"
        return f"{self.project}/{self.name}"

    def __str__(self) -> str:
        return self.to_key()


FRONTMATTER_SEPARATOR = "---"


class SecretMetadata(BaseModel):
    model_config = ConfigDict(extra="ignore")

    description: str | None = None

    def is_empty(self) -> bool:
        return all(v is None for v in self.model_dump().values())


def parse_note(note: str | None) -> tuple[SecretMetadata, str]:
    """Parse a note into metadata frontmatter and body text."""
    if not note:
        return SecretMetadata(), ""

    lines = note.split("\n")
    if lines[0] != FRONTMATTER_SEPARATOR:
        return SecretMetadata(), note

    try:
        end = lines.index(FRONTMATTER_SEPARATOR, 1)
    except ValueError:
        return SecretMetadata(), note

    frontmatter_lines = lines[1:end]
    raw = yaml.safe_load("\n".join(frontmatter_lines)) or {}
    metadata = SecretMetadata(**raw) if isinstance(raw, dict) else SecretMetadata()

    body_lines = lines[end + 1 :]
    body = "\n".join(body_lines)
    # Strip a single leading newline that separates frontmatter from body,
    # but preserve the body content if it's empty string
    if body == "\n":
        body = ""

    return metadata, body


def render_note(metadata: SecretMetadata, body: str) -> str | None:
    """Render metadata and body back into a note string."""
    if metadata.is_empty() and not body:
        return None

    if metadata.is_empty():
        return body

    data = {k: v for k, v in metadata.model_dump().items() if v is not None}
    frontmatter = yaml.dump(data, default_flow_style=False).rstrip("\n")

    parts = [FRONTMATTER_SEPARATOR, frontmatter, FRONTMATTER_SEPARATOR]
    if body:
        parts.append(body)

    return "\n".join(parts)
