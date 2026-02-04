# ABOUTME: Tests for the export module.
# ABOUTME: Tests env file parsing, variable naming, and secret export.

from unittest.mock import MagicMock, patch


from vaultuner.export import (
    export_secrets,
    parse_env_file,
    secret_name_to_env_var,
)
from vaultuner.models import is_deleted


class TestSecretNameToEnvVar:
    def test_converts_to_uppercase(self):
        assert secret_name_to_env_var("my-secret") == "MY_SECRET"

    def test_replaces_dashes_with_underscores(self):
        assert secret_name_to_env_var("api-key") == "API_KEY"

    def test_already_uppercase(self):
        assert secret_name_to_env_var("API_KEY") == "API_KEY"

    def test_mixed_case_with_dashes(self):
        assert secret_name_to_env_var("my-Api-Key") == "MY_API_KEY"

    def test_single_word(self):
        assert secret_name_to_env_var("secret") == "SECRET"

    def test_empty_string(self):
        assert secret_name_to_env_var("") == ""


class TestParseEnvFile:
    def test_nonexistent_file(self, tmp_path):
        path = tmp_path / "nonexistent.env"
        assert parse_env_file(path) == set()

    def test_empty_file(self, tmp_path):
        path = tmp_path / ".env"
        path.write_text("")
        assert parse_env_file(path) == set()

    def test_ignores_comments(self, tmp_path):
        path = tmp_path / ".env"
        path.write_text("# This is a comment\nAPI_KEY=value\n# Another comment")
        assert parse_env_file(path) == {"API_KEY"}

    def test_ignores_blank_lines(self, tmp_path):
        path = tmp_path / ".env"
        path.write_text("API_KEY=value\n\n\nDB_HOST=localhost\n")
        assert parse_env_file(path) == {"API_KEY", "DB_HOST"}

    def test_extracts_variable_names(self, tmp_path):
        path = tmp_path / ".env"
        path.write_text("API_KEY=secret123\nDB_PASSWORD=pass")
        assert parse_env_file(path) == {"API_KEY", "DB_PASSWORD"}

    def test_handles_spaces_around_equals(self, tmp_path):
        path = tmp_path / ".env"
        path.write_text("  API_KEY = value  \n")
        assert parse_env_file(path) == {"API_KEY"}

    def test_handles_equals_in_value(self, tmp_path):
        path = tmp_path / ".env"
        path.write_text('KEY="val=ue=with=equals"\n')
        assert parse_env_file(path) == {"KEY"}

    def test_multiple_variables(self, tmp_path):
        path = tmp_path / ".env"
        path.write_text("A=1\nB=2\nC=3\n")
        assert parse_env_file(path) == {"A", "B", "C"}


class TestIsDeleted:
    def test_deleted_prefix(self):
        assert is_deleted("_deleted_/project/name") is True

    def test_not_deleted(self):
        assert is_deleted("project/name") is False

    def test_incomplete_prefix(self):
        assert is_deleted("_deleted_") is False

    def test_prefix_not_at_start(self):
        assert is_deleted("project/_deleted_/name") is False


class TestExportSecrets:
    @patch("vaultuner.export.get_client")
    @patch("vaultuner.export.get_settings")
    def test_no_secrets_found(self, mock_settings, mock_client, tmp_path):
        mock_settings.return_value = MagicMock(organization_id="org-123")
        client = MagicMock()
        client.secrets().list.return_value = MagicMock(data=None)
        mock_client.return_value = client

        output = tmp_path / ".env"
        added, skipped = export_secrets("myproject", output)

        assert added == 0
        assert skipped == 0
        assert not output.exists()

    @patch("vaultuner.export.get_client")
    @patch("vaultuner.export.get_settings")
    def test_filters_by_project(self, mock_settings, mock_client, tmp_path):
        mock_settings.return_value = MagicMock(organization_id="org-123")

        secret1 = MagicMock(id="1", key="myproject/api-key")
        secret2 = MagicMock(id="2", key="otherproject/api-key")

        client = MagicMock()
        client.secrets().list.return_value = MagicMock(
            data=MagicMock(data=[secret1, secret2])
        )
        client.secrets().get.return_value = MagicMock(
            data=MagicMock(value="secret-value")
        )
        mock_client.return_value = client

        output = tmp_path / ".env"
        added, skipped = export_secrets("myproject", output)

        assert added == 1
        assert skipped == 0
        assert output.read_text() == 'API_KEY="secret-value"\n'

    @patch("vaultuner.export.get_client")
    @patch("vaultuner.export.get_settings")
    def test_filters_by_env(self, mock_settings, mock_client, tmp_path):
        mock_settings.return_value = MagicMock(organization_id="org-123")

        secret1 = MagicMock(id="1", key="myproject/prod/api-key")
        secret2 = MagicMock(id="2", key="myproject/dev/api-key")

        client = MagicMock()
        client.secrets().list.return_value = MagicMock(
            data=MagicMock(data=[secret1, secret2])
        )
        client.secrets().get.return_value = MagicMock(
            data=MagicMock(value="prod-secret")
        )
        mock_client.return_value = client

        output = tmp_path / ".env"
        added, skipped = export_secrets("myproject", output, env="prod")

        assert added == 1
        assert skipped == 0

    @patch("vaultuner.export.get_client")
    @patch("vaultuner.export.get_settings")
    def test_ignores_deleted_secrets(self, mock_settings, mock_client, tmp_path):
        mock_settings.return_value = MagicMock(organization_id="org-123")

        secret1 = MagicMock(id="1", key="_deleted_/myproject/api-key")
        secret2 = MagicMock(id="2", key="myproject/db-pass")

        client = MagicMock()
        client.secrets().list.return_value = MagicMock(
            data=MagicMock(data=[secret1, secret2])
        )
        client.secrets().get.return_value = MagicMock(data=MagicMock(value="value"))
        mock_client.return_value = client

        output = tmp_path / ".env"
        added, skipped = export_secrets("myproject", output)

        assert added == 1
        assert "API_KEY" not in output.read_text()
        assert "DB_PASS" in output.read_text()

    @patch("vaultuner.export.get_client")
    @patch("vaultuner.export.get_settings")
    def test_skips_existing_vars(self, mock_settings, mock_client, tmp_path):
        mock_settings.return_value = MagicMock(organization_id="org-123")

        secret = MagicMock(id="1", key="myproject/api-key")

        client = MagicMock()
        client.secrets().list.return_value = MagicMock(data=MagicMock(data=[secret]))
        client.secrets().get.return_value = MagicMock(data=MagicMock(value="new-value"))
        mock_client.return_value = client

        output = tmp_path / ".env"
        output.write_text("API_KEY=existing-value\n")

        added, skipped = export_secrets("myproject", output)

        assert added == 0
        assert skipped == 1
        content = output.read_text()
        assert "# Already defined above" in content
        assert '# API_KEY="new-value"' in content

    @patch("vaultuner.export.get_client")
    @patch("vaultuner.export.get_settings")
    def test_appends_to_existing_file(self, mock_settings, mock_client, tmp_path):
        mock_settings.return_value = MagicMock(organization_id="org-123")

        secret = MagicMock(id="1", key="myproject/new-key")

        client = MagicMock()
        client.secrets().list.return_value = MagicMock(data=MagicMock(data=[secret]))
        client.secrets().get.return_value = MagicMock(data=MagicMock(value="new-value"))
        mock_client.return_value = client

        output = tmp_path / ".env"
        output.write_text("EXISTING=value\n")

        added, skipped = export_secrets("myproject", output)

        assert added == 1
        content = output.read_text()
        assert content.startswith("EXISTING=value\n")
        assert 'NEW_KEY="new-value"' in content
