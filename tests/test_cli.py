# ABOUTME: Tests for the CLI module.
# ABOUTME: Tests helper functions and CLI commands.

from unittest.mock import MagicMock, patch

import pytest
from typer.testing import CliRunner

from vaultuner.cli import (
    app,
    is_deleted,
    mark_deleted,
    unmark_deleted,
)

runner = CliRunner()


class TestIsDeleted:
    def test_deleted_prefix(self):
        assert is_deleted("_deleted_/project/name") is True

    def test_not_deleted(self):
        assert is_deleted("project/name") is False


class TestMarkDeleted:
    def test_adds_prefix(self):
        assert mark_deleted("project/name") == "_deleted_/project/name"

    def test_already_deleted(self):
        assert mark_deleted("_deleted_/project/name") == "_deleted_/_deleted_/project/name"


class TestUnmarkDeleted:
    def test_removes_prefix(self):
        assert unmark_deleted("_deleted_/project/name") == "project/name"

    def test_not_deleted(self):
        assert unmark_deleted("project/name") == "project/name"


class TestConfigSet:
    @patch("vaultuner.cli.set_keyring_value")
    def test_stores_access_token(self, mock_set):
        result = runner.invoke(app, ["config", "set", "access-token", "my-token"])
        assert result.exit_code == 0
        mock_set.assert_called_once_with("bws_access_token", "my-token")
        assert "Stored" in result.stdout

    @patch("vaultuner.cli.set_keyring_value")
    def test_stores_organization_id(self, mock_set):
        result = runner.invoke(app, ["config", "set", "organization-id", "org-123"])
        assert result.exit_code == 0
        mock_set.assert_called_once_with("bws_organization_id", "org-123")


class TestConfigShow:
    @patch("vaultuner.cli.get_keyring_value")
    def test_shows_configured(self, mock_get):
        mock_get.side_effect = lambda key: "value" if key == "access_token" else "org-123"
        result = runner.invoke(app, ["config", "show"])
        assert result.exit_code == 0
        assert "configured" in result.stdout

    @patch("vaultuner.cli.get_keyring_value")
    def test_shows_not_set(self, mock_get):
        mock_get.return_value = None
        result = runner.invoke(app, ["config", "show"])
        assert result.exit_code == 0
        assert "not set" in result.stdout


class TestConfigDelete:
    @patch("vaultuner.cli.delete_keyring_value")
    def test_deletes_key(self, mock_delete):
        result = runner.invoke(app, ["config", "delete", "access-token"])
        assert result.exit_code == 0
        mock_delete.assert_called_once_with("bws_access_token")
        assert "Deleted" in result.stdout


class TestListSecrets:
    @patch("vaultuner.cli.get_client")
    @patch("vaultuner.cli.get_settings")
    def test_lists_secrets(self, mock_settings, mock_client):
        mock_settings.return_value = MagicMock(organization_id="org-123")

        secret = MagicMock(key="myproject/prod/api-key")
        client = MagicMock()
        client.secrets().list.return_value = MagicMock(
            data=MagicMock(data=[secret])
        )
        mock_client.return_value = client

        result = runner.invoke(app, ["list"])
        assert result.exit_code == 0
        assert "myproject" in result.stdout
        assert "prod" in result.stdout
        assert "api-key" in result.stdout

    @patch("vaultuner.cli.get_client")
    @patch("vaultuner.cli.get_settings")
    def test_filters_by_project(self, mock_settings, mock_client):
        mock_settings.return_value = MagicMock(organization_id="org-123")

        secret1 = MagicMock(key="myproject/api-key")
        secret2 = MagicMock(key="other/api-key")
        client = MagicMock()
        client.secrets().list.return_value = MagicMock(
            data=MagicMock(data=[secret1, secret2])
        )
        mock_client.return_value = client

        result = runner.invoke(app, ["list", "-p", "myproject"])
        assert result.exit_code == 0
        assert "myproject" in result.stdout
        assert "other" not in result.stdout

    @patch("vaultuner.cli.get_client")
    @patch("vaultuner.cli.get_settings")
    def test_empty_response(self, mock_settings, mock_client):
        mock_settings.return_value = MagicMock(organization_id="org-123")
        client = MagicMock()
        client.secrets().list.return_value = MagicMock(data=None)
        mock_client.return_value = client

        result = runner.invoke(app, ["list"])
        assert result.exit_code == 0
        assert "No secrets found" in result.stdout


class TestGetSecret:
    @patch("vaultuner.cli.get_client")
    @patch("vaultuner.cli.find_secret_by_key")
    def test_get_secret(self, mock_find, mock_client):
        mock_find.return_value = {"id": "secret-id", "key": "myproject/api-key"}
        client = MagicMock()
        client.secrets().get.return_value = MagicMock(
            data=MagicMock(key="myproject/api-key", value="secret-value", note=None)
        )
        mock_client.return_value = client

        result = runner.invoke(app, ["get", "myproject/api-key"])
        assert result.exit_code == 0
        assert "secret-value" in result.stdout

    @patch("vaultuner.cli.get_client")
    @patch("vaultuner.cli.find_secret_by_key")
    def test_get_value_only(self, mock_find, mock_client):
        mock_find.return_value = {"id": "secret-id", "key": "myproject/api-key"}
        client = MagicMock()
        client.secrets().get.return_value = MagicMock(
            data=MagicMock(key="myproject/api-key", value="secret-value", note=None)
        )
        mock_client.return_value = client

        result = runner.invoke(app, ["get", "myproject/api-key", "--value"])
        assert result.exit_code == 0
        assert result.stdout.strip() == "secret-value"

    @patch("vaultuner.cli.get_client")
    @patch("vaultuner.cli.find_secret_by_key")
    def test_get_not_found(self, mock_find, mock_client):
        mock_find.return_value = None
        mock_client.return_value = MagicMock()

        result = runner.invoke(app, ["get", "myproject/api-key"])
        assert result.exit_code == 1
        assert "not found" in result.output


class TestSetSecret:
    @patch("vaultuner.cli.get_or_create_project")
    @patch("vaultuner.cli.find_secret_by_key")
    @patch("vaultuner.cli.get_client")
    @patch("vaultuner.cli.get_settings")
    def test_creates_secret(self, mock_settings, mock_client, mock_find, mock_project):
        mock_settings.return_value = MagicMock(organization_id="org-123")
        mock_find.return_value = None
        mock_project.return_value = "project-id"
        client = MagicMock()
        client.secrets().create.return_value = MagicMock(data=MagicMock())
        mock_client.return_value = client

        result = runner.invoke(app, ["set", "myproject/api-key", "secret-value"])
        assert result.exit_code == 0
        assert "Created" in result.stdout

    @patch("vaultuner.cli.find_secret_by_key")
    @patch("vaultuner.cli.get_client")
    @patch("vaultuner.cli.get_settings")
    def test_updates_existing(self, mock_settings, mock_client, mock_find):
        mock_settings.return_value = MagicMock(organization_id="org-123")
        mock_find.return_value = {"id": "secret-id", "key": "myproject/api-key"}
        client = MagicMock()
        client.secrets().update.return_value = MagicMock(data=MagicMock())
        mock_client.return_value = client

        result = runner.invoke(app, ["set", "myproject/api-key", "new-value"])
        assert result.exit_code == 0
        assert "Updated" in result.stdout


class TestDeleteSecret:
    @patch("vaultuner.cli.find_secret_by_key")
    @patch("vaultuner.cli.get_client")
    @patch("vaultuner.cli.get_settings")
    def test_soft_deletes(self, mock_settings, mock_client, mock_find):
        mock_settings.return_value = MagicMock(organization_id="org-123")
        mock_find.return_value = {"id": "secret-id", "key": "myproject/api-key"}
        client = MagicMock()
        client.secrets().get.return_value = MagicMock(
            data=MagicMock(value="value", note=None, project_id="proj-id")
        )
        client.secrets().update.return_value = MagicMock(data=MagicMock())
        mock_client.return_value = client

        result = runner.invoke(app, ["delete", "myproject/api-key", "--force"])
        assert result.exit_code == 0
        assert "Deleted" in result.stdout
        client.secrets().update.assert_called_once()

    @patch("vaultuner.cli.find_secret_by_key")
    @patch("vaultuner.cli.get_client")
    @patch("vaultuner.cli.get_settings")
    def test_permanent_deletes(self, mock_settings, mock_client, mock_find):
        mock_settings.return_value = MagicMock(organization_id="org-123")
        mock_find.return_value = {"id": "secret-id", "key": "myproject/api-key"}
        client = MagicMock()
        mock_client.return_value = client

        result = runner.invoke(app, ["delete", "myproject/api-key", "--force", "--permanent"])
        assert result.exit_code == 0
        assert "Permanently deleted" in result.stdout
        client.secrets().delete.assert_called_once()

    @patch("vaultuner.cli.find_secret_by_key")
    @patch("vaultuner.cli.get_client")
    @patch("vaultuner.cli.get_settings")
    def test_not_found(self, mock_settings, mock_client, mock_find):
        mock_settings.return_value = MagicMock(organization_id="org-123")
        mock_find.return_value = None
        mock_client.return_value = MagicMock()

        result = runner.invoke(app, ["delete", "myproject/api-key", "--force"])
        assert result.exit_code == 1
        assert "not found" in result.output


class TestRestoreSecret:
    @patch("vaultuner.cli.find_secret_by_key")
    @patch("vaultuner.cli.get_client")
    @patch("vaultuner.cli.get_settings")
    def test_restores(self, mock_settings, mock_client, mock_find):
        mock_settings.return_value = MagicMock(organization_id="org-123")
        mock_find.return_value = {"id": "secret-id", "key": "_deleted_/myproject/api-key"}
        client = MagicMock()
        client.secrets().get.return_value = MagicMock(
            data=MagicMock(value="value", note=None, project_id="proj-id")
        )
        client.secrets().update.return_value = MagicMock(data=MagicMock())
        mock_client.return_value = client

        result = runner.invoke(app, ["restore", "myproject/api-key"])
        assert result.exit_code == 0
        assert "Restored" in result.stdout

    @patch("vaultuner.cli.find_secret_by_key")
    @patch("vaultuner.cli.get_client")
    @patch("vaultuner.cli.get_settings")
    def test_not_found(self, mock_settings, mock_client, mock_find):
        mock_settings.return_value = MagicMock(organization_id="org-123")
        mock_find.return_value = None
        mock_client.return_value = MagicMock()

        result = runner.invoke(app, ["restore", "myproject/api-key"])
        assert result.exit_code == 1
        assert "not found" in result.output


class TestProjects:
    @patch("vaultuner.cli.get_client")
    @patch("vaultuner.cli.get_settings")
    def test_lists_projects(self, mock_settings, mock_client):
        mock_settings.return_value = MagicMock(organization_id="org-123")
        project = MagicMock()
        project.name = "myproject"
        client = MagicMock()
        client.projects().list.return_value = MagicMock(
            data=MagicMock(data=[project])
        )
        mock_client.return_value = client

        result = runner.invoke(app, ["projects"])
        assert result.exit_code == 0
        assert "myproject" in result.output

    @patch("vaultuner.cli.get_client")
    @patch("vaultuner.cli.get_settings")
    def test_empty(self, mock_settings, mock_client):
        mock_settings.return_value = MagicMock(organization_id="org-123")
        client = MagicMock()
        client.projects().list.return_value = MagicMock(data=None)
        mock_client.return_value = client

        result = runner.invoke(app, ["projects"])
        assert result.exit_code == 0
        assert "No projects found" in result.stdout


class TestExportCommand:
    @patch("vaultuner.export.export_secrets")
    def test_exports(self, mock_export, tmp_path):
        mock_export.return_value = (3, 1)

        result = runner.invoke(app, ["export", "-p", "myproject", "-o", str(tmp_path / ".env")])
        assert result.exit_code == 0
        assert "3 added" in result.output
        assert "1 already present" in result.output

    @patch("vaultuner.export.export_secrets")
    def test_no_secrets(self, mock_export):
        mock_export.return_value = (0, 0)

        result = runner.invoke(app, ["export", "-p", "myproject"])
        assert result.exit_code == 0
        assert "No secrets found" in result.output
