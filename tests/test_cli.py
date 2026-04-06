# ABOUTME: Tests for the CLI module.
# ABOUTME: Tests helper functions and CLI commands.

from unittest.mock import MagicMock, patch

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
        assert (
            mark_deleted("_deleted_/project/name") == "_deleted_/_deleted_/project/name"
        )


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
        mock_get.side_effect = (
            lambda key: "value" if key == "bws_access_token" else "org-123"
        )
        result = runner.invoke(app, ["config", "show"])
        assert result.exit_code == 0
        assert "configured" in result.stdout

    @patch("vaultuner.cli.get_keyring_value")
    def test_shows_not_set(self, mock_get):
        mock_get.return_value = None
        result = runner.invoke(app, ["config", "show"])
        assert result.exit_code == 0
        assert "not set" in result.stdout

    @patch("vaultuner.cli.get_keyring_value")
    def test_uses_correct_keyring_keys(self, mock_get):
        """Verify config show uses the same keyring keys as config set."""
        mock_get.return_value = None
        runner.invoke(app, ["config", "show"])
        # Should use keys from KEYRING_MAP (bws_access_token, bws_organization_id)
        called_keys = [call.args[0] for call in mock_get.call_args_list]
        assert "bws_access_token" in called_keys
        assert "bws_organization_id" in called_keys

    @patch("vaultuner.cli.get_keyring_value")
    def test_hides_org_id_value(self, mock_get):
        """Org ID should show 'configured' not the actual value."""
        mock_get.return_value = "some-org-uuid-12345"
        result = runner.invoke(app, ["config", "show"])
        assert "some-org-uuid-12345" not in result.stdout
        assert "configured" in result.stdout

    @patch("vaultuner.cli.is_keyring_accessible")
    @patch("vaultuner.cli.get_keyring_value")
    def test_warns_when_keyring_inaccessible(self, mock_get, mock_accessible):
        mock_accessible.return_value = False
        mock_get.return_value = None
        result = runner.invoke(app, ["config", "show"])
        assert result.exit_code == 0
        assert "keychain is not accessible" in result.stdout.lower()
        assert "regular" in result.stdout.lower()


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
        client.secrets().list.return_value = MagicMock(data=MagicMock(data=[secret]))
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
    def test_filters_by_scoped_project(self, mock_settings, mock_client):
        mock_settings.return_value = MagicMock(organization_id="org-123")

        secrets = [
            MagicMock(key="@dpoblador/vaultuner/prod/api-key"),
            MagicMock(key="@dpoblador/vaultuner/dev/db-pass"),
            MagicMock(key="myproject/api-key"),
        ]
        client = MagicMock()
        client.secrets().list.return_value = MagicMock(
            data=MagicMock(data=secrets)
        )
        mock_client.return_value = client

        result = runner.invoke(app, ["list", "-p", "@dpoblador/vaultuner"])
        assert result.exit_code == 0
        assert "@dpoblador/vaultuner" in result.stdout
        assert "myproject" not in result.stdout

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


class TestSetGenerate:
    @patch("vaultuner.cli.get_or_create_project")
    @patch("vaultuner.cli.find_secret_by_key")
    @patch("vaultuner.cli.get_client")
    @patch("vaultuner.cli.get_settings")
    def test_creates_with_generated_value(
        self, mock_settings, mock_client, mock_find, mock_project
    ):
        mock_settings.return_value = MagicMock(organization_id="org-123")
        mock_find.return_value = None
        mock_project.return_value = "project-id"
        client = MagicMock()
        client.secrets().create.return_value = MagicMock(data=MagicMock())
        mock_client.return_value = client

        result = runner.invoke(app, ["set", "myproject/api-key", "--generate"])
        assert result.exit_code == 0
        assert "Created" in result.output
        assert "Generated value:" in result.output

    @patch("vaultuner.cli.get_or_create_project")
    @patch("vaultuner.cli.find_secret_by_key")
    @patch("vaultuner.cli.get_client")
    @patch("vaultuner.cli.get_settings")
    def test_generate_prints_value(
        self, mock_settings, mock_client, mock_find, mock_project
    ):
        mock_settings.return_value = MagicMock(organization_id="org-123")
        mock_find.return_value = None
        mock_project.return_value = "project-id"
        client = MagicMock()
        client.secrets().create.return_value = MagicMock(data=MagicMock())
        mock_client.return_value = client

        result = runner.invoke(app, ["set", "myproject/api-key", "--generate"])
        assert result.exit_code == 0
        # Verify the value passed to create matches what was printed
        call_args = client.secrets().create.call_args
        stored_value = call_args.kwargs.get("value") or call_args[1].get("value")
        assert stored_value in result.output

    @patch("vaultuner.cli.find_secret_by_key")
    @patch("vaultuner.cli.get_client")
    @patch("vaultuner.cli.get_settings")
    def test_generate_updates_existing(self, mock_settings, mock_client, mock_find):
        mock_settings.return_value = MagicMock(organization_id="org-123")
        mock_find.return_value = {"id": "secret-id", "key": "myproject/api-key"}
        client = MagicMock()
        client.secrets().update.return_value = MagicMock(data=MagicMock())
        mock_client.return_value = client

        result = runner.invoke(app, ["set", "myproject/api-key", "--generate"])
        assert result.exit_code == 0
        assert "Updated" in result.output
        # Should still print the generated value
        call_args = client.secrets().update.call_args
        stored_value = call_args.kwargs.get("value") or call_args[1].get("value")
        assert stored_value in result.output

    def test_generate_and_value_conflict(self):
        result = runner.invoke(
            app, ["set", "myproject/api-key", "my-value", "--generate"]
        )
        assert result.exit_code == 1
        assert "Cannot use --generate with an explicit value" in result.output

    def test_missing_value_and_no_generate(self):
        result = runner.invoke(app, ["set", "myproject/api-key"])
        assert result.exit_code != 0


class TestSetDescription:
    @patch("vaultuner.cli.get_or_create_project")
    @patch("vaultuner.cli.find_secret_by_key")
    @patch("vaultuner.cli.get_client")
    @patch("vaultuner.cli.get_settings")
    def test_creates_with_description(
        self, mock_settings, mock_client, mock_find, mock_project
    ):
        mock_settings.return_value = MagicMock(organization_id="org-123")
        mock_find.return_value = None
        mock_project.return_value = "project-id"
        client = MagicMock()
        client.secrets().create.return_value = MagicMock(data=MagicMock())
        mock_client.return_value = client

        result = runner.invoke(
            app,
            ["set", "myproject/api-key", "secret-value", "--description", "My API key"],
        )
        assert result.exit_code == 0
        call_args = client.secrets().create.call_args
        note = call_args.kwargs.get("note") or call_args[1].get("note")
        assert "description: My API key" in note
        assert "---" in note

    @patch("vaultuner.cli.find_secret_by_key")
    @patch("vaultuner.cli.get_client")
    @patch("vaultuner.cli.get_settings")
    def test_updates_description_preserves_body(
        self, mock_settings, mock_client, mock_find
    ):
        """Updating description on a secret with an existing plain note preserves the note as body."""
        mock_settings.return_value = MagicMock(organization_id="org-123")
        mock_find.return_value = {"id": "secret-id", "key": "myproject/api-key"}
        client = MagicMock()
        client.secrets().get.return_value = MagicMock(
            data=MagicMock(
                key="myproject/api-key",
                value="existing-value",
                note="Existing plain note.",
                project_id="proj-id",
            )
        )
        client.secrets().update.return_value = MagicMock(data=MagicMock())
        mock_client.return_value = client

        result = runner.invoke(
            app,
            [
                "set",
                "myproject/api-key",
                "new-value",
                "--description",
                "Added description",
            ],
        )
        assert result.exit_code == 0
        call_args = client.secrets().update.call_args
        note = call_args.kwargs.get("note") or call_args[1].get("note")
        assert "description: Added description" in note
        assert "Existing plain note." in note

    @patch("vaultuner.cli.find_secret_by_key")
    @patch("vaultuner.cli.get_client")
    @patch("vaultuner.cli.get_settings")
    def test_metadata_only_update(self, mock_settings, mock_client, mock_find):
        """Update just metadata without changing the secret value."""
        mock_settings.return_value = MagicMock(organization_id="org-123")
        mock_find.return_value = {"id": "secret-id", "key": "myproject/api-key"}
        client = MagicMock()
        client.secrets().get.return_value = MagicMock(
            data=MagicMock(
                key="myproject/api-key",
                value="keep-this-value",
                note=None,
                project_id="proj-id",
            )
        )
        client.secrets().update.return_value = MagicMock(data=MagicMock())
        mock_client.return_value = client

        result = runner.invoke(
            app,
            ["set", "myproject/api-key", "--description", "Just adding metadata"],
        )
        assert result.exit_code == 0
        call_args = client.secrets().update.call_args
        value = call_args.kwargs.get("value") or call_args[1].get("value")
        note = call_args.kwargs.get("note") or call_args[1].get("note")
        assert value == "keep-this-value"
        assert "description: Just adding metadata" in note

    @patch("vaultuner.cli.find_secret_by_key")
    @patch("vaultuner.cli.get_client")
    @patch("vaultuner.cli.get_settings")
    def test_metadata_only_update_not_found(self, mock_settings, mock_client, mock_find):
        """Cannot update metadata on a secret that doesn't exist without providing a value."""
        mock_settings.return_value = MagicMock(organization_id="org-123")
        mock_find.return_value = None
        mock_client.return_value = MagicMock()

        result = runner.invoke(
            app,
            ["set", "myproject/api-key", "--description", "No value provided"],
        )
        assert result.exit_code != 0


class TestGetDescription:
    @patch("vaultuner.cli.get_client")
    @patch("vaultuner.cli.find_secret_by_key")
    def test_displays_description_and_note_body(self, mock_find, mock_client):
        mock_find.return_value = {"id": "secret-id", "key": "myproject/api-key"}
        client = MagicMock()
        client.secrets().get.return_value = MagicMock(
            data=MagicMock(
                key="myproject/api-key",
                value="secret-value",
                note="---\ndescription: My API key\n---\nSome extra note.",
            )
        )
        mock_client.return_value = client

        result = runner.invoke(app, ["get", "myproject/api-key"])
        assert result.exit_code == 0
        assert "My API key" in result.stdout
        assert "Some extra note." in result.stdout

    @patch("vaultuner.cli.get_client")
    @patch("vaultuner.cli.find_secret_by_key")
    def test_displays_plain_note_without_frontmatter(self, mock_find, mock_client):
        mock_find.return_value = {"id": "secret-id", "key": "myproject/api-key"}
        client = MagicMock()
        client.secrets().get.return_value = MagicMock(
            data=MagicMock(
                key="myproject/api-key",
                value="secret-value",
                note="Just a plain note.",
            )
        )
        mock_client.return_value = client

        result = runner.invoke(app, ["get", "myproject/api-key"])
        assert result.exit_code == 0
        assert "Just a plain note." in result.stdout


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

        result = runner.invoke(
            app, ["delete", "myproject/api-key", "--force", "--permanent"]
        )
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
        mock_find.return_value = {
            "id": "secret-id",
            "key": "_deleted_/myproject/api-key",
        }
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
    def test_lists_semantic_projects(self, mock_settings, mock_client):
        mock_settings.return_value = MagicMock(organization_id="org-123")

        secrets = [
            MagicMock(key="myproject/api-key"),
            MagicMock(key="myproject/prod/db-pass"),
            MagicMock(key="other/secret"),
        ]
        client = MagicMock()
        client.secrets().list.return_value = MagicMock(data=MagicMock(data=secrets))
        mock_client.return_value = client

        result = runner.invoke(app, ["projects"])
        assert result.exit_code == 0
        assert "myproject" in result.output
        assert "other" in result.output

    @patch("vaultuner.cli.get_client")
    @patch("vaultuner.cli.get_settings")
    def test_lists_scoped_projects(self, mock_settings, mock_client):
        mock_settings.return_value = MagicMock(organization_id="org-123")

        secrets = [
            MagicMock(key="@dpoblador/vaultuner/prod/api-key"),
            MagicMock(key="@dpoblador/vaultuner/dev/api-key"),
            MagicMock(key="myproject/api-key"),
        ]
        client = MagicMock()
        client.secrets().list.return_value = MagicMock(data=MagicMock(data=secrets))
        mock_client.return_value = client

        result = runner.invoke(app, ["projects"])
        assert result.exit_code == 0
        assert "@dpoblador/vaultuner" in result.output
        assert "myproject" in result.output

    @patch("vaultuner.cli.get_client")
    @patch("vaultuner.cli.get_settings")
    def test_deduplicates_projects(self, mock_settings, mock_client):
        mock_settings.return_value = MagicMock(organization_id="org-123")

        secrets = [
            MagicMock(key="myproject/api-key"),
            MagicMock(key="myproject/prod/db-pass"),
            MagicMock(key="myproject/dev/db-pass"),
        ]
        client = MagicMock()
        client.secrets().list.return_value = MagicMock(data=MagicMock(data=secrets))
        mock_client.return_value = client

        result = runner.invoke(app, ["projects"])
        assert result.exit_code == 0
        # Should appear once, not three times
        assert result.output.count("myproject") == 1

    @patch("vaultuner.cli.get_client")
    @patch("vaultuner.cli.get_settings")
    def test_ignores_deleted_secrets(self, mock_settings, mock_client):
        mock_settings.return_value = MagicMock(organization_id="org-123")

        secrets = [
            MagicMock(key="myproject/api-key"),
            MagicMock(key="_deleted_/oldproject/secret"),
        ]
        client = MagicMock()
        client.secrets().list.return_value = MagicMock(data=MagicMock(data=secrets))
        mock_client.return_value = client

        result = runner.invoke(app, ["projects"])
        assert result.exit_code == 0
        assert "myproject" in result.output
        assert "oldproject" not in result.output

    @patch("vaultuner.cli.get_client")
    @patch("vaultuner.cli.get_settings")
    def test_empty(self, mock_settings, mock_client):
        mock_settings.return_value = MagicMock(organization_id="org-123")
        client = MagicMock()
        client.secrets().list.return_value = MagicMock(data=None)
        mock_client.return_value = client

        result = runner.invoke(app, ["projects"])
        assert result.exit_code == 0
        assert "No projects found" in result.stdout


class TestExportCommand:
    @patch("vaultuner.export.export_secrets")
    def test_exports(self, mock_export, tmp_path):
        mock_export.return_value = (3, 1)

        result = runner.invoke(
            app, ["export", "-p", "myproject", "-o", str(tmp_path / ".env")]
        )
        assert result.exit_code == 0
        assert "3 added" in result.output
        assert "1 already present" in result.output

    @patch("vaultuner.export.export_secrets")
    def test_no_secrets(self, mock_export):
        mock_export.return_value = (0, 0)

        result = runner.invoke(app, ["export", "-p", "myproject"])
        assert result.exit_code == 0
        assert "No secrets found" in result.output


class TestImportCommand:
    @patch("vaultuner.cli.get_or_create_project")
    @patch("vaultuner.cli.find_secret_by_key")
    @patch("vaultuner.cli.get_client")
    @patch("vaultuner.cli.get_settings")
    def test_preview_shows_length_not_value(
        self, mock_settings, mock_client, mock_find, mock_project, tmp_path
    ):
        """Import preview should not leak partial secret values."""
        mock_settings.return_value = MagicMock(organization_id="org-123")
        mock_find.return_value = None
        mock_project.return_value = "project-id"
        client = MagicMock()
        client.secrets().create.return_value = MagicMock(data=MagicMock())
        mock_client.return_value = client

        env_file = tmp_path / ".env"
        env_file.write_text("MY_SECRET=supersecretvalue12345\n")

        # Run with prompting (no -y flag) and answer "n" to abort
        result = runner.invoke(
            app,
            ["import", "-i", str(env_file), "-p", "testproj"],
            input="n\n",
        )

        # Value should NOT appear in output
        assert "supersecret" not in result.output
        # Length info should appear instead (value is 21 chars)
        assert "21 chars" in result.output
