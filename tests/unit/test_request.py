import pytest
import json
import re
from unittest.mock import patch, MagicMock
from ansible.errors import AnsibleError
import requests
from ansible_collections.itential.platform.plugins.module_utils.request import make_request, VALID_HTTP_METHODS


@patch("ansible_collections.itential.core.plugins.module_utils.http.send_request")
def test_make_request_success(mock_http_request, mock_http_login_response, mock_task_vars):
    """Test successful execution of `make_request` when authentication succeeds."""

    api_response = MagicMock(status_code=200, text=json.dumps({"key": "value"}))
    api_response.json.return_value = {"key": "value"}

    mock_http_request.side_effect = [mock_http_login_response, api_response]

    result = make_request(
        mock_task_vars,
        "GET",
        "/api/endpoint",
        params={"param": "value"},
        data={"data": "test"}
    )

    assert not result["changed"]
    assert "elapsed_time" in result
    assert result["json"] == {"key": "value"}
    assert mock_http_request.call_count == 2  # Ensures both login and API requests were made


@patch("ansible_collections.itential.core.plugins.module_utils.http.send_request")
def test_make_request_invalid_json_data(mock_task_vars):
    """Test that `make_request` raises an error when given non-serializable JSON data."""

    class UnserializableObject:
        pass

    with pytest.raises(AnsibleError, match="'data' must be JSON-serializable"):
        make_request(mock_task_vars, "POST", "/api/endpoint", data=UnserializableObject())


@patch("ansible_collections.itential.core.plugins.module_utils.http.send_request")
def test_make_request_invalid_params(mock_task_vars):
    """Test that `make_request` raises an error when params is not a dictionary."""

    with pytest.raises(AnsibleError, match="'params' must be a dictionary"):
        make_request(mock_task_vars, "GET", "/api/endpoint", params="invalid")


@patch("ansible_collections.itential.core.plugins.module_utils.http.send_request")
def test_make_request_invalid_http_method(mock_task_vars):
    """Test that `make_request` raises an error when an invalid HTTP method is provided."""

    invalid_method = "INVALID"

    with pytest.raises(AnsibleError, match=f"Invalid HTTP method: {invalid_method}. Must be one of {VALID_HTTP_METHODS}"):
        make_request(mock_task_vars, invalid_method, "/api/endpoint")


@patch("ansible_collections.itential.core.plugins.module_utils.http.send_request")
@patch("ansible_collections.itential.platform.plugins.module_utils.login.login")
def test_make_request_with_manual_token(mock_login, mock_http_request, mock_task_vars):
    """Test that `make_request` does not call `login()` if a token is already provided in task_vars."""

    manual_token = "manual-token"

    # Add the manual token to the existing mock_task_vars
    mock_task_vars["hostvars"]["platform"]["platform_auth_token"] = manual_token

    # Mock HTTP response
    api_response = MagicMock(status_code=200, text=json.dumps({"key": "value"}))
    api_response.json.return_value = {"key": "value"}
    mock_http_request.return_value = api_response

    result = make_request(
        mock_task_vars,
        "GET",
        "/api/endpoint",
        params={}
    )

    # Ensure login() is never called since token is already provided
    mock_login.assert_not_called()

    # Ensure token is correctly used in request
    assert mock_http_request.call_args[1]["params"]["token"] == manual_token

    # Validate response
    assert not result["changed"]
    assert "elapsed_time" in result
    assert result["json"] == {"key": "value"}


# VALID URL TESTS
@pytest.mark.parametrize("valid_url", [
    "http://example.com/api",
    "https://example.com/api",
    "http://sub.domain.com/path",
    "https://www.example.com/?query=param",
    "http://localhost:8080/api",
    "https://127.0.0.1:443/api",
    "http://example.com/api/resource?key=value",
    "https://example.com/api#fragment",
])
@patch("ansible_collections.itential.core.plugins.module_utils.http.send_request")
def test_make_request_valid_urls(mock_http_request, mock_http_login_response, mock_task_vars, valid_url):
    """Test that `make_request` correctly accepts valid URLs."""
    
    api_response = MagicMock(status_code=200, text=json.dumps({"status": "success"}))
    api_response.json.return_value = {"status": "success"}

    mock_http_request.side_effect = [mock_http_login_response, api_response]

    # Patch `make_url` to return a valid URL
    with patch("ansible_collections.itential.core.plugins.module_utils.http.make_url", return_value=valid_url):
        result = make_request(mock_task_vars, "GET", "/api/endpoint")

        assert isinstance(result, dict)
        assert result["json"]["status"] == "success"
        assert mock_http_request.call_count == 2  # Login + actual request


# INVALID URL TESTS
@pytest.mark.parametrize("invalid_url", [
    "example.com/api",  # Missing http/https
    "ftp://example.com/api",  # Invalid scheme
    "http//example.com/api",  # Missing colon
    "://example.com/api",  # Missing scheme
    "https:/example.com/api",  # Single slash after scheme
    "http://",  # Incomplete URL
    "http://?query=param",  # No domain
    "https:///api",  # Triple slash issue
    "http://example .com/api",  # Space in URL
    "https://exa mple.com",  # Space in domain
    "http://example.com/ api",  # Space in path
    "http://.com/api",  # No domain before TLD
])
@patch("ansible_collections.itential.core.plugins.module_utils.http.send_request")
def test_make_request_invalid_urls(mock_http_request, mock_http_login_response, mock_task_vars, invalid_url):
    """Test that `make_request` raises an error for malformed URLs."""

    with patch("ansible_collections.itential.core.plugins.module_utils.http.make_url", return_value=invalid_url):
        with pytest.raises(AnsibleError, match=re.escape(f"Malformed URL: {invalid_url}")):
            make_request(mock_task_vars, "GET", "/api/endpoint")


@patch("ansible_collections.itential.core.plugins.module_utils.http.send_request")
def test_make_request_invalid_status_code(mock_http_request, mock_http_login_response, mock_task_vars):
    """Test that `make_request` raises an error when the API returns a non-200 response (400 Bad Request) for the non-login API request."""

    error_response = {
        "message": "Invalid query parameters provided :\nParameter 'equals' received invalid property paths. The following properties are not supported for this operator in the target document type: exclude",
        "data": None,
        "metadata": {}
    }

    # Mock API responses: First for login (successful), second for actual request (400 error)
    api_response = MagicMock(status_code=400, text=json.dumps(error_response))
    api_response.json.return_value = error_response

    mock_http_request.side_effect = [mock_http_login_response, api_response]  # First call is login, second is real API request

    with pytest.raises(AnsibleError, match=r"API request failed with status 400:.*Invalid query parameters provided.*exclude"):
        make_request(mock_task_vars, "GET", "/api/endpoint")

    assert mock_http_request.call_count == 2


@pytest.mark.parametrize("response_text, expected_json", [
    (json.dumps({"key": "value"}), {"key": "value"}),  # Valid JSON response
    ("Invalid JSON", None),  # Invalid JSON response
])
@patch("ansible_collections.itential.core.plugins.module_utils.http.send_request")
def test_make_request_json_response_handling(mock_http_request, mock_http_login_response, mock_task_vars, response_text, expected_json):
    """Test handling of valid and invalid JSON responses."""

    mock_response = MagicMock(status_code=200, text=response_text)
    mock_response.headers = {"Content-Type": "application/json"}

    if expected_json is not None:
        mock_response.json.return_value = expected_json
        mock_http_request.side_effect = [mock_http_login_response, mock_response]

        result = make_request(mock_task_vars, "GET", "/api/endpoint")
        assert result["json"] == expected_json
    else:
        mock_response.json.side_effect = ValueError("Invalid JSON")
        mock_http_request.side_effect = [mock_http_login_response, mock_response]

        with pytest.raises(AnsibleError, match="Failed to parse JSON response: Invalid JSON"):
            make_request(mock_task_vars, "GET", "/api/endpoint")
