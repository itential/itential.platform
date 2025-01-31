import pytest
import json
from unittest.mock import patch, MagicMock
from ansible.errors import AnsibleError
import requests
from ansible_collections.itential.platform.plugins.module_utils.request import make_request

@patch("ansible_collections.itential.core.plugins.module_utils.http.send_request")
def test_make_request_success(mock_http_request, mock_http_login_response, mock_task_vars):
    """Test successful execution of `make_request` when authentication succeeds."""

    # Mock API response for a successful request
    api_response = MagicMock()
    api_response.status_code = 200
    api_response.json.return_value = {"key": "value"}
    api_response.text = json.dumps({"key": "value"})

    # Simulate login followed by the actual request
    mock_http_request.side_effect = [mock_http_login_response, api_response]

    # Execute `make_request`
    result = make_request(
        mock_task_vars,
        "GET",
        "/api/endpoint",
        params={"param": "value"},
        data={"data": "test"}
    )

    # Validate response
    assert not result["changed"]
    assert "elapsed_time" in result
    assert result["json"] == {"key": "value"}
    assert mock_http_request.call_count == 2

    # Verify first call (Login request)
    first_call = mock_http_request.call_args_list[0]
    assert first_call[1]["method"] == "POST"
    assert "/login" in first_call[1]["url"]

    # Verify second call (Actual API request)
    second_call = mock_http_request.call_args_list[1]
    assert second_call[1]["method"] == "GET"
    assert "/api/endpoint" in second_call[1]["url"]
    assert second_call[1]["params"]["token"] == json.dumps({"token": "mocked_token"})


@patch("ansible_collections.itential.core.plugins.module_utils.http.send_request")
def test_make_request_invalid_json_data(mock_http_request, mock_task_vars):
    """Test that `make_request` raises an error when given non-serializable JSON data."""

    class UnserializableObject:
        pass

    with pytest.raises(AnsibleError, match="'data' must be JSON-serializable"):
        make_request(mock_task_vars, "POST", "/api/endpoint", data=UnserializableObject())


@patch("ansible_collections.itential.core.plugins.module_utils.http.send_request")
def test_make_request_timeout(mock_http_request, mock_task_vars):
    """Test handling of timeout errors when making a request."""

    mock_http_request.side_effect = TimeoutError("Request timed out")

    with pytest.raises(AnsibleError, match="HTTP request failed: Request timed out"):
        make_request(mock_task_vars, "GET", "/api/endpoint")


@patch("ansible_collections.itential.core.plugins.module_utils.http.send_request")
def test_make_request_invalid_params(mock_http_request, mock_task_vars):
    """Test that `make_request` raises an error when params is not a dictionary."""

    with pytest.raises(AnsibleError, match="'params' must be a dictionary"):
        make_request(mock_task_vars, "GET", "/api/endpoint", params="invalid")


@patch("ansible_collections.itential.core.plugins.module_utils.http.send_request")
def test_make_request_skipped_due_to_invalid_connection(mock_http_request, mock_task_vars):
    """Test that `make_request` skips execution when `itential_connection` is not 'http'."""

    mock_task_vars["hostvars"]["platform"]["itential_connection"] = "ssh"  # Invalid connection type

    result = make_request(mock_task_vars, "GET", "/api/endpoint")

    assert result == (None, {"changed": False, "skipped": True})
    mock_http_request.assert_not_called()  # Ensure no request was made


@patch("ansible_collections.itential.core.plugins.module_utils.http.send_request")
def test_make_request_request_exception(mock_http_request, mock_task_vars):
    """Test handling of various request exceptions."""

    # Simulate a connection failure
    mock_http_request.side_effect = requests.exceptions.ConnectionError("Connection failed")
    with pytest.raises(AnsibleError, match="HTTP request failed: Connection failed"):
        make_request(mock_task_vars, "GET", "/api/endpoint")

    # Simulate an invalid URL error
    mock_http_request.side_effect = requests.exceptions.InvalidURL("Invalid URL")
    with pytest.raises(AnsibleError, match="HTTP request failed: Invalid URL"):
        make_request(mock_task_vars, "GET", "/api/endpoint")

    # Simulate a timeout
    mock_http_request.side_effect = requests.exceptions.Timeout("Request timed out")
    with pytest.raises(AnsibleError, match="HTTP request failed: Request timed out"):
        make_request(mock_task_vars, "GET", "/api/endpoint")


@patch("ansible_collections.itential.core.plugins.module_utils.http.send_request")
def test_make_request_invalid_json_response(mock_http_request, mock_task_vars):
    """Test handling of an API response that claims to be JSON but is invalid."""

    # Mock login response
    login_response = MagicMock(status_code=200, text=json.dumps({"token": "mocked_token"}))
    login_response.json.return_value = {"token": "mocked_token"}

    # Mock API response with invalid JSON
    invalid_json_response = MagicMock(status_code=200, text="Invalid JSON")
    invalid_json_response.headers = {"Content-Type": "application/json"}
    invalid_json_response.json.side_effect = ValueError("Invalid JSON")  # Simulate JSON parsing failure

    mock_http_request.side_effect = [login_response, invalid_json_response]

    # Ensure error is raised due to invalid JSON parsing
    with pytest.raises(AnsibleError, match="Failed to parse JSON response: Invalid JSON"):
        make_request(mock_task_vars, "GET", "/api/endpoint")


@patch("ansible_collections.itential.core.plugins.module_utils.http.send_request")
def test_make_request_unexpected_content_type(mock_http_request, mock_task_vars):
    """Test handling of a response with an unexpected content type."""

    # Mock login response
    login_response = MagicMock(status_code=200, text=json.dumps({"token": "mocked_token"}))
    login_response.json.return_value = {"token": "mocked_token"}

    # Mock API response with a non-JSON content type
    unexpected_content_response = MagicMock(status_code=200, text="This is plain text, not JSON.")
    unexpected_content_response.headers = {"Content-Type": "text/plain"}

    mock_http_request.side_effect = [login_response, unexpected_content_response]

    # Ensure error is raised due to unexpected content type
    with pytest.raises(AnsibleError, match="Unexpected content type: text/plain"):
        make_request(mock_task_vars, "GET", "/api/endpoint")
