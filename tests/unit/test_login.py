import pytest
import json
from unittest.mock import patch, MagicMock
from ansible.errors import AnsibleError
from ansible_collections.itential.platform.plugins.module_utils.login import login

@pytest.fixture
def mock_host():
    """Fixture to create a mock host object that mimics Ansible's hostvars."""
    mock = MagicMock()
    mock.username = "admin"
    mock.password = "admin"
    mock.host = "example.com"
    mock.port = 3000
    mock.use_tls = False
    mock.verify = False
    mock.disable_warnings = False
    mock.headers = {"custom": "header"}
    return mock

@pytest.fixture
def mock_http_response():
    """Fixture for a mock HTTP response used in `login()` tests."""
    with patch("ansible_collections.itential.core.plugins.module_utils.http.send_request") as mock_request:
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.text = "mocked_token"
        mock_response.json.return_value = {"token": "mocked_token"}
        mock_request.return_value = mock_response
        yield mock_request

def test_login_success(mock_host, mock_http_response):
    """Test that `login()` successfully retrieves an auth token."""
    assert mock_host is not None, "mock_host is None!"

    token = login(mock_host)
    assert token == "mocked_token"

    # Ensure `send_request` was called with the correct parameters
    mock_http_response.assert_called_once_with(
        method="POST",
        url="http://example.com:3000/login",
        headers={
            "custom": "header",
            "content-type": "application/json",
            "accept": "application/json"
        },
        data=json.dumps({"user": {"username": "admin", "password": "admin"}}).encode("utf-8"),
        verify=False,  # Matches `mock_host`
        disable_warnings=False
    )

def test_login_http_error(mock_host):
    """Test that `login()` raises an error on HTTP failure."""
    with patch("ansible_collections.itential.core.plugins.module_utils.http.send_request") as mock_request:
        mock_request.side_effect = Exception("HTTP Error")

        with pytest.raises(AnsibleError, match="HTTP request failed: HTTP Error"):
            login(mock_host)

def test_login_invalid_json(mock_host):
    """Test that `login()` handles non-JSON responses correctly."""
    with patch("ansible_collections.itential.core.plugins.module_utils.http.send_request") as mock_request:
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.text = "Invalid JSON"
        mock_response.json.side_effect = ValueError("Invalid JSON")
        mock_request.return_value = mock_response

        token = login(mock_host)

        assert token == "Invalid JSON"

def test_login_missing_credentials():
    """Test that `login()` fails gracefully when username or password is missing."""
    mock_host = MagicMock()
    mock_host.username = None
    mock_host.password = "admin"
    mock_host.host = "example.com"
    mock_host.port = 3000
    mock_host.use_tls = False
    mock_host.verify = False
    mock_host.disable_warnings = False

    with pytest.raises(AnsibleError, match="missing required property"):
        login(mock_host)

def test_login_missing_headers():
    """Test that `login()` correctly initializes headers when missing."""
    mock_host = MagicMock()
    mock_host.username = "admin"
    mock_host.password = "admin"
    mock_host.host = "example.com"
    mock_host.port = 3000
    mock_host.use_tls = False
    mock_host.verify = False
    mock_host.disable_warnings = False
    mock_host.headers = None

    with patch("ansible_collections.itential.core.plugins.module_utils.http.send_request") as mock_request:
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.text = "mocked_token"
        mock_request.return_value = mock_response

        token = login(mock_host)
        assert token == "mocked_token"

def test_login_non_200_response(mock_host):
    """Test that `login()` raises an error when the API returns a non-200 status code."""
    with patch("ansible_collections.itential.core.plugins.module_utils.http.send_request") as mock_request:
        mock_response = MagicMock()
        mock_response.status_code = 401
        mock_response.text = "Unauthorized"
        mock_request.return_value = mock_response

        with pytest.raises(AnsibleError, match="Unexpected HTTP status code in response:"):
            login(mock_host)


def test_login_timeout(mock_host):
    """Test that `login()` raises an error when a timeout occurs."""
    with patch("ansible_collections.itential.core.plugins.module_utils.http.send_request") as mock_request:
        mock_request.side_effect = TimeoutError("Request timed out")

        with pytest.raises(AnsibleError, match="HTTP request failed: Request timed out"):
            login(mock_host)