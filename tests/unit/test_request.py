import pytest
import json
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
def test_make_request_with_manual_token(mock_http_request, mock_task_vars):
    """Test that `make_request` does not call `login()` if a token is already provided."""

    manual_token = "manual-token"

    api_response = MagicMock(status_code=200, text=json.dumps({"key": "value"}))
    api_response.json.return_value = {"key": "value"}
    mock_http_request.return_value = api_response

    result = make_request(
        mock_task_vars,
        "GET",
        "/api/endpoint",
        params={"token": manual_token}
    )

    # Ensures login is skipped
    assert mock_http_request.call_args[1]["params"]["token"] == manual_token
    assert not result["changed"]
    assert "elapsed_time" in result
    assert result["json"] == {"key": "value"}


@patch("ansible_collections.itential.core.plugins.module_utils.http.send_request")
def test_make_request_malformed_url(mock_http_request, mock_task_vars):
    """Test that `make_request` raises an error for a malformed URL."""

    with patch("ansible_collections.itential.core.plugins.module_utils.http.make_url", return_value="invalid_url"):
        with pytest.raises(AnsibleError, match="Malformed URL: invalid_url"):
            make_request(mock_task_vars, "GET", "/api/endpoint")


@patch("ansible_collections.itential.core.plugins.module_utils.http.send_request")
def test_make_request_empty_response(mock_http_request, mock_http_login_response, mock_task_vars):
    """Test that `make_request` raises an error when the API returns an empty response."""

    empty_response = MagicMock(status_code=200, text="")

    mock_http_request.side_effect = [mock_http_login_response, empty_response]

    with pytest.raises(AnsibleError, match="Empty response from API"):
        make_request(mock_task_vars, "GET", "/api/endpoint")


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
