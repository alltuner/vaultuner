# ABOUTME: Tests for the import_env module.
# ABOUTME: Tests env file parsing and secret path building.


from vaultuner.import_env import (
    build_secret_path,
    env_var_to_secret_name,
    parse_env_entries,
)


class TestEnvVarToSecretName:
    def test_keeps_name_unchanged(self):
        assert env_var_to_secret_name("API_KEY") == "API_KEY"

    def test_preserves_case(self):
        assert env_var_to_secret_name("DB_PASSWORD") == "DB_PASSWORD"

    def test_lowercase_unchanged(self):
        assert env_var_to_secret_name("secret") == "secret"

    def test_mixed_case_unchanged(self):
        assert env_var_to_secret_name("My_Api_Key") == "My_Api_Key"

    def test_empty_string(self):
        assert env_var_to_secret_name("") == ""


class TestParseEnvEntries:
    def test_nonexistent_file(self, tmp_path):
        path = tmp_path / "nonexistent.env"
        assert parse_env_entries(path) == []

    def test_empty_file(self, tmp_path):
        path = tmp_path / ".env"
        path.write_text("")
        assert parse_env_entries(path) == []

    def test_ignores_comments(self, tmp_path):
        path = tmp_path / ".env"
        path.write_text("# Comment\nAPI_KEY=value\n# Another")
        entries = parse_env_entries(path)
        assert len(entries) == 1
        assert entries[0] == ("API_KEY", "value")

    def test_ignores_blank_lines(self, tmp_path):
        path = tmp_path / ".env"
        path.write_text("A=1\n\n\nB=2\n")
        entries = parse_env_entries(path)
        assert len(entries) == 2

    def test_parses_simple_entries(self, tmp_path):
        path = tmp_path / ".env"
        path.write_text("API_KEY=secret123\nDB_HOST=localhost")
        entries = parse_env_entries(path)
        assert entries == [("API_KEY", "secret123"), ("DB_HOST", "localhost")]

    def test_strips_double_quotes(self, tmp_path):
        path = tmp_path / ".env"
        path.write_text('KEY="quoted value"')
        entries = parse_env_entries(path)
        assert entries == [("KEY", "quoted value")]

    def test_strips_single_quotes(self, tmp_path):
        path = tmp_path / ".env"
        path.write_text("KEY='quoted value'")
        entries = parse_env_entries(path)
        assert entries == [("KEY", "quoted value")]

    def test_handles_equals_in_value(self, tmp_path):
        path = tmp_path / ".env"
        path.write_text("KEY=val=ue=with=equals")
        entries = parse_env_entries(path)
        assert entries == [("KEY", "val=ue=with=equals")]

    def test_handles_spaces_around_equals(self, tmp_path):
        path = tmp_path / ".env"
        path.write_text("  KEY = value  ")
        entries = parse_env_entries(path)
        assert entries == [("KEY", "value")]


class TestBuildSecretPath:
    def test_with_env(self):
        assert build_secret_path("proj", "prod", "key") == "proj/prod/key"

    def test_without_env(self):
        assert build_secret_path("proj", None, "key") == "proj/key"

    def test_with_empty_env(self):
        assert build_secret_path("proj", "", "key") == "proj/key"
