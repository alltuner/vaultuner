# ABOUTME: Tests for the models module.
# ABOUTME: Tests SecretPath parsing and key generation.

import pytest

from vaultuner.models import SecretPath


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

    def test_parse_with_special_characters(self):
        path = SecretPath.parse("my_project/dev/api-key_v2")
        assert path.project == "my_project"
        assert path.env == "dev"
        assert path.name == "api-key_v2"


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
