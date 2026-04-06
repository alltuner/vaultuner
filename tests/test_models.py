# ABOUTME: Tests for the models module.
# ABOUTME: Tests SecretPath parsing, key generation, and note metadata.

import pytest

from vaultuner.models import SecretMetadata, SecretPath, parse_note, render_note


class TestSecretPathParse:
    def test_parse_three_parts(self):
        path = SecretPath.parse("myproject/prod/db-password")
        assert path.project == "myproject"
        assert path.env == "prod"
        assert path.name == "db-password"

    def test_parse_two_parts(self):
        path = SecretPath.parse("myproject/api-key")
        assert path.project == "myproject"
        assert path.env is None
        assert path.name == "api-key"

    def test_parse_one_part_raises(self):
        with pytest.raises(ValueError, match="Invalid path format"):
            SecretPath.parse("myproject")

    def test_parse_four_parts_raises(self):
        with pytest.raises(ValueError, match="Invalid path format"):
            SecretPath.parse("a/b/c/d")

    def test_parse_empty_raises(self):
        with pytest.raises(ValueError, match="Invalid path format"):
            SecretPath.parse("")

    def test_parse_double_slash_raises(self):
        with pytest.raises(ValueError, match="cannot be empty"):
            SecretPath.parse("project//name")

    def test_parse_leading_slash_raises(self):
        with pytest.raises(ValueError, match="cannot be empty"):
            SecretPath.parse("/project/name")

    def test_parse_trailing_slash_raises(self):
        with pytest.raises(ValueError, match="cannot be empty"):
            SecretPath.parse("project/name/")

    def test_parse_empty_env_raises(self):
        with pytest.raises(ValueError, match="cannot be empty"):
            SecretPath.parse("project//env/name")

    def test_parse_with_special_characters(self):
        path = SecretPath.parse("my_project/dev/api-key_v2")
        assert path.project == "my_project"
        assert path.env == "dev"
        assert path.name == "api-key_v2"


class TestSecretPathParseScoped:
    """Tests for @org/repo scoped paths."""

    def test_parse_at_org_repo_name(self):
        path = SecretPath.parse("@dpoblador/vaultuner/api-key")
        assert path.project == "@dpoblador/vaultuner"
        assert path.env is None
        assert path.name == "api-key"

    def test_parse_at_org_repo_env_name(self):
        path = SecretPath.parse("@dpoblador/vaultuner/prod/api-key")
        assert path.project == "@dpoblador/vaultuner"
        assert path.env == "prod"
        assert path.name == "api-key"

    def test_parse_at_org_repo_only_raises(self):
        with pytest.raises(ValueError, match="Invalid path format"):
            SecretPath.parse("@dpoblador/vaultuner")

    def test_parse_at_org_only_raises(self):
        with pytest.raises(ValueError, match="Invalid path format"):
            SecretPath.parse("@dpoblador")

    def test_parse_at_five_parts_raises(self):
        with pytest.raises(ValueError, match="Invalid path format"):
            SecretPath.parse("@dpoblador/vaultuner/prod/api-key/extra")

    def test_parse_at_empty_org_raises(self):
        with pytest.raises(ValueError, match="cannot be empty"):
            SecretPath.parse("@/repo/name")

    def test_parse_at_empty_repo_raises(self):
        with pytest.raises(ValueError, match="cannot be empty"):
            SecretPath.parse("@org//name")

    def test_to_key_roundtrip_without_env(self):
        path = SecretPath.parse("@dpoblador/vaultuner/api-key")
        assert path.to_key() == "@dpoblador/vaultuner/api-key"

    def test_to_key_roundtrip_with_env(self):
        path = SecretPath.parse("@dpoblador/vaultuner/prod/api-key")
        assert path.to_key() == "@dpoblador/vaultuner/prod/api-key"

    def test_str_delegates_to_to_key(self):
        path = SecretPath(project="@dpoblador/vaultuner", env="staging", name="key")
        assert str(path) == "@dpoblador/vaultuner/staging/key"

    def test_special_chars_in_org_repo(self):
        path = SecretPath.parse("@my-org/my_repo.v2/prod/secret")
        assert path.project == "@my-org/my_repo.v2"
        assert path.env == "prod"
        assert path.name == "secret"


class TestSecretPathToKey:
    def test_to_key_with_env(self):
        path = SecretPath(project="proj", env="prod", name="secret")
        assert path.to_key() == "proj/prod/secret"

    def test_to_key_without_env(self):
        path = SecretPath(project="proj", env=None, name="secret")
        assert path.to_key() == "proj/secret"


class TestSecretPathStr:
    def test_str_delegates_to_to_key(self):
        path = SecretPath(project="proj", env="staging", name="key")
        assert str(path) == "proj/staging/key"

    def test_str_without_env(self):
        path = SecretPath(project="proj", env=None, name="key")
        assert str(path) == "proj/key"


class TestDeletedHelpers:
    def test_is_deleted_with_prefix(self):
        from vaultuner.models import is_deleted

        assert is_deleted("_deleted_/project/name") is True

    def test_is_deleted_without_prefix(self):
        from vaultuner.models import is_deleted

        assert is_deleted("project/name") is False

    def test_is_deleted_incomplete_prefix(self):
        from vaultuner.models import is_deleted

        assert is_deleted("_deleted_") is False

    def test_is_deleted_prefix_not_at_start(self):
        from vaultuner.models import is_deleted

        assert is_deleted("project/_deleted_/name") is False

    def test_mark_deleted(self):
        from vaultuner.models import mark_deleted

        assert mark_deleted("project/name") == "_deleted_/project/name"

    def test_unmark_deleted(self):
        from vaultuner.models import unmark_deleted

        assert unmark_deleted("_deleted_/project/name") == "project/name"

    def test_unmark_deleted_without_prefix(self):
        from vaultuner.models import unmark_deleted

        assert unmark_deleted("project/name") == "project/name"

    def test_deleted_prefix_constant(self):
        from vaultuner.models import DELETED_PREFIX

        assert DELETED_PREFIX == "_deleted_/"


class TestSecretMetadata:
    def test_all_fields_optional(self):
        meta = SecretMetadata()
        assert meta.description is None

    def test_description(self):
        meta = SecretMetadata(description="A secret")
        assert meta.description == "A secret"

    def test_unknown_fields_ignored(self):
        meta = SecretMetadata(owner="team-x", rotated="2026-01-01")
        assert not hasattr(meta, "owner")
        assert meta.description is None


class TestParseNote:
    def test_none_note(self):
        meta, body = parse_note(None)
        assert meta == SecretMetadata()
        assert body == ""

    def test_empty_note(self):
        meta, body = parse_note("")
        assert meta == SecretMetadata()
        assert body == ""

    def test_plain_text_no_frontmatter(self):
        meta, body = parse_note("Just a plain note.")
        assert meta == SecretMetadata()
        assert body == "Just a plain note."

    def test_multiline_plain_text(self):
        note = "Line one.\nLine two.\nLine three."
        meta, body = parse_note(note)
        assert meta == SecretMetadata()
        assert body == note

    def test_frontmatter_only(self):
        note = "---\ndescription: My secret\n---"
        meta, body = parse_note(note)
        assert meta.description == "My secret"
        assert body == ""

    def test_frontmatter_with_body(self):
        note = "---\ndescription: My secret\n---\nSome extra info."
        meta, body = parse_note(note)
        assert meta.description == "My secret"
        assert body == "Some extra info."

    def test_frontmatter_with_multiline_body(self):
        note = "---\ndescription: My secret\n---\nLine one.\nLine two."
        meta, body = parse_note(note)
        assert meta.description == "My secret"
        assert body == "Line one.\nLine two."

    def test_frontmatter_unknown_fields_ignored(self):
        note = "---\ndescription: My secret\nowner: team-x\n---\nBody."
        meta, body = parse_note(note)
        assert meta.description == "My secret"
        assert body == "Body."

    def test_dashes_in_body_not_treated_as_frontmatter(self):
        note = "Some text with\n---\ndashes in it."
        meta, body = parse_note(note)
        assert meta == SecretMetadata()
        assert body == note

    def test_frontmatter_with_trailing_newline(self):
        note = "---\ndescription: My secret\n---\n"
        meta, body = parse_note(note)
        assert meta.description == "My secret"
        assert body == ""


class TestRenderNote:
    def test_empty_metadata_no_body(self):
        result = render_note(SecretMetadata(), "")
        assert result is None

    def test_empty_metadata_with_body(self):
        result = render_note(SecretMetadata(), "Just a note.")
        assert result == "Just a note."

    def test_metadata_no_body(self):
        result = render_note(SecretMetadata(description="My secret"), "")
        assert result == "---\ndescription: My secret\n---"

    def test_metadata_with_body(self):
        result = render_note(SecretMetadata(description="My secret"), "Extra info.")
        assert result == "---\ndescription: My secret\n---\nExtra info."

    def test_roundtrip_plain_text(self):
        original = "Just a plain note."
        meta, body = parse_note(original)
        assert render_note(meta, body) == original

    def test_roundtrip_with_frontmatter(self):
        original = "---\ndescription: My secret\n---\nSome body text."
        meta, body = parse_note(original)
        assert render_note(meta, body) == original

    def test_roundtrip_frontmatter_only(self):
        original = "---\ndescription: My secret\n---"
        meta, body = parse_note(original)
        assert render_note(meta, body) == original

    def test_adding_frontmatter_preserves_body(self):
        """Existing note content becomes the body when adding metadata."""
        original = "This was the original note."
        meta, body = parse_note(original)
        meta.description = "Now with metadata"
        result = render_note(meta, body)
        assert result == "---\ndescription: Now with metadata\n---\nThis was the original note."
