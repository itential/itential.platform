import pytest
import json
from unittest.mock import patch, MagicMock
from ansible.errors import AnsibleError
import requests
from ansible_collections.itential.platform.plugins.module_utils.request import make_request

@patch("ansible_collections.itential.core.plugins.module_utils.http.send_request")
def test_make_request_success(mock_http_request, mock_http_login_response, mock_task_vars):
    """Test successful execution of `make_request` when authentication succeeds."""

    api_response = MagicMock()
    api_response.status_code = 200
    api_response.json.return_value = {"key": "value"}
    api_response.text = json.dumps({"key": "value"})

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
    assert mock_http_request.call_count == 2

    first_call = mock_http_request.call_args_list[0]
    assert first_call[1]["method"] == "POST"
    assert "/login" in first_call[1]["url"]

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
def test_make_request_invalid_params(mock_http_request, mock_task_vars):
    """Test that `make_request` raises an error when params is not a dictionary."""

    with pytest.raises(AnsibleError, match="'params' must be a dictionary"):
        make_request(mock_task_vars, "GET", "/api/endpoint", params="invalid")


@patch("ansible_collections.itential.core.plugins.module_utils.http.send_request")
def test_make_request_request_exceptions(mock_http_request, mock_task_vars):
    """Test handling of various request-related exceptions."""

    exception_cases = [
        (requests.exceptions.ConnectionError("Connection failed"), "HTTP request failed: Connection failed"),
        (requests.exceptions.InvalidURL("Invalid URL"), "HTTP request failed: Invalid URL"),
        (requests.exceptions.Timeout("Request timed out"), "HTTP request failed: Request timed out"),
        (TimeoutError("Request timed out"), "HTTP request failed: Request timed out"),
    ]

    for side_effect, expected_message in exception_cases:
        mock_http_request.side_effect = side_effect
        with pytest.raises(AnsibleError, match=expected_message):
            make_request(mock_task_vars, "GET", "/api/endpoint")


@patch("ansible_collections.itential.core.plugins.module_utils.http.send_request")
def test_make_request_invalid_response_handling(mock_http_request, mock_task_vars):
    """Test handling of invalid API responses including invalid JSON and unexpected content types."""

    login_response = MagicMock(status_code=200, text=json.dumps({"token": "mocked_token"}))
    login_response.json.return_value = {"token": "mocked_token"}

    invalid_cases = [
        (
            MagicMock(status_code=200, text="Invalid JSON", headers={"Content-Type": "application/json"}, json=MagicMock(side_effect=ValueError("Invalid JSON"))),
            "Failed to parse JSON response: Invalid JSON"
        ),
        (
            MagicMock(status_code=200, text="This is plain text, not JSON.", headers={"Content-Type": "text/plain"}),
            "Unexpected content type: text/plain"
        )
    ]

    for response_mock, expected_message in invalid_cases:
        mock_http_request.side_effect = [login_response, response_mock]
        with pytest.raises(AnsibleError, match=expected_message):
            make_request(mock_task_vars, "GET", "/api/endpoint")
