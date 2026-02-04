# ABOUTME: Tests for the config module.
# ABOUTME: Tests keyring operations and settings loading.

from unittest.mock import patch

import pytest

from vaultuner.config import (
    SERVICE_NAME,
    delete_keyring_value,
    get_keyring_value,
    set_keyring_value,
)


class TestGetKeyringValue:
    @patch("vaultuner.config.keyring.get_password")
    def test_returns_value(self, mock_get):
        mock_get.return_value = "secret-value"
        result = get_keyring_value("test_key")
        assert result == "secret-value"
        mock_get.assert_called_once_with(SERVICE_NAME, "test_key")

    @patch("vaultuner.config.keyring.get_password")
    def test_returns_none_when_missing(self, mock_get):
        mock_get.return_value = None
        result = get_keyring_value("missing_key")
        assert result is None


class TestSetKeyringValue:
    @patch("vaultuner.config.keyring.set_password")
    def test_stores_value(self, mock_set):
        set_keyring_value("test_key", "test_value")
        mock_set.assert_called_once_with(SERVICE_NAME, "test_key", "test_value")


class TestDeleteKeyringValue:
    @patch("vaultuner.config.keyring.delete_password")
    def test_deletes_value(self, mock_delete):
        delete_keyring_value("test_key")
        mock_delete.assert_called_once_with(SERVICE_NAME, "test_key")

    @patch("vaultuner.config.keyring.delete_password")
    def test_ignores_missing_key(self, mock_delete):
        import keyring.errors

        mock_delete.side_effect = keyring.errors.PasswordDeleteError()
        delete_keyring_value("missing_key")


class TestPlatformCheck:
    @patch("vaultuner.config.sys.platform", "linux")
    def test_get_keyring_returns_none_on_non_darwin(self):
        from vaultuner.config import get_keyring_value

        result = get_keyring_value("test_key")
        assert result is None

    @patch("vaultuner.config.sys.platform", "linux")
    def test_set_keyring_fails_on_non_darwin(self):
        from vaultuner.config import set_keyring_value

        with pytest.raises(SystemExit, match="macOS"):
            set_keyring_value("test_key", "value")

    @patch("vaultuner.config.sys.platform", "linux")
    def test_delete_keyring_fails_on_non_darwin(self):
        from vaultuner.config import delete_keyring_value

        with pytest.raises(SystemExit, match="macOS"):
            delete_keyring_value("test_key")

    @patch("vaultuner.config.sys.platform", "darwin")
    @patch("vaultuner.config.keyring.get_password")
    def test_get_keyring_works_on_darwin(self, mock_get):
        from vaultuner.config import get_keyring_value

        mock_get.return_value = "value"
        result = get_keyring_value("test_key")
        assert result == "value"
