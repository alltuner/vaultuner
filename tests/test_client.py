# ABOUTME: Tests for the client module.
# ABOUTME: Tests Bitwarden SDK wrapper functions.

from unittest.mock import MagicMock, patch

import pytest


class TestGetClient:
    @patch("vaultuner.client.BitwardenClient")
    @patch("vaultuner.client.client_settings_from_dict")
    @patch("vaultuner.client.get_settings")
    def test_creates_authenticated_client(self, mock_settings, mock_client_settings, mock_client_class):
        from vaultuner.client import get_client

        settings = MagicMock()
        settings.api_url = "https://api.example.com"
        settings.identity_url = "https://identity.example.com"
        settings.access_token.get_secret_value.return_value = "test-token"
        mock_settings.return_value = settings

        client = MagicMock()
        mock_client_class.return_value = client

        result = get_client()

        assert result == client
        client.auth().login_access_token.assert_called_once()


class TestGetOrCreateProject:
    @patch("vaultuner.client.get_settings")
    def test_returns_existing_project(self, mock_settings):
        from vaultuner.client import get_or_create_project

        mock_settings.return_value = MagicMock(organization_id="org-123")

        project = MagicMock()
        project.id = "project-id-123"
        project.name = "myproject"

        client = MagicMock()
        client.projects().list.return_value = MagicMock(
            data=MagicMock(data=[project])
        )

        result = get_or_create_project(client, "myproject")
        assert result == "project-id-123"
        client.projects().create.assert_not_called()

    @patch("vaultuner.client.get_settings")
    def test_creates_project_when_not_found(self, mock_settings):
        from vaultuner.client import get_or_create_project

        mock_settings.return_value = MagicMock(organization_id="org-123")

        client = MagicMock()
        client.projects().list.return_value = MagicMock(data=MagicMock(data=[]))

        new_project = MagicMock()
        new_project.id = "new-project-id"
        client.projects().create.return_value = MagicMock(data=new_project)

        result = get_or_create_project(client, "newproject")
        assert result == "new-project-id"
        client.projects().create.assert_called_once()

    @patch("vaultuner.client.get_settings")
    def test_raises_on_create_failure(self, mock_settings):
        from vaultuner.client import get_or_create_project

        mock_settings.return_value = MagicMock(organization_id="org-123")

        client = MagicMock()
        client.projects().list.return_value = MagicMock(data=MagicMock(data=[]))
        client.projects().create.return_value = MagicMock(data=None)

        with pytest.raises(RuntimeError, match="Failed to create project"):
            get_or_create_project(client, "newproject")


class TestFindSecretByKey:
    @patch("vaultuner.client.get_settings")
    def test_finds_secret(self, mock_settings):
        from vaultuner.client import find_secret_by_key

        mock_settings.return_value = MagicMock(organization_id="org-123")

        secret = MagicMock()
        secret.id = "secret-id-123"
        secret.key = "myproject/api-key"

        client = MagicMock()
        client.secrets().list.return_value = MagicMock(
            data=MagicMock(data=[secret])
        )

        result = find_secret_by_key(client, "myproject/api-key")
        assert result == {"id": "secret-id-123", "key": "myproject/api-key"}

    @patch("vaultuner.client.get_settings")
    def test_returns_none_when_not_found(self, mock_settings):
        from vaultuner.client import find_secret_by_key

        mock_settings.return_value = MagicMock(organization_id="org-123")

        client = MagicMock()
        client.secrets().list.return_value = MagicMock(data=MagicMock(data=[]))

        result = find_secret_by_key(client, "myproject/api-key")
        assert result is None

    @patch("vaultuner.client.get_settings")
    def test_returns_none_when_no_data(self, mock_settings):
        from vaultuner.client import find_secret_by_key

        mock_settings.return_value = MagicMock(organization_id="org-123")

        client = MagicMock()
        client.secrets().list.return_value = MagicMock(data=None)

        result = find_secret_by_key(client, "myproject/api-key")
        assert result is None
