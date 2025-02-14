import pytest
import json
from unittest.mock import MagicMock, patch
from ansible_collections.itential.platform.plugins.action.generic_request import ActionModule as GenericRequest

# Test successful API request
@patch("ansible_collections.itential.core.plugins.module_utils.http.send_request")
def test_generic_request_success(mock_http_request, mock_task_vars, mock_http_login_response):
    """Test a successful API request with required arguments."""

    api_response = MagicMock(status_code=200, text=json.dumps({"success": True}))
    api_response.json.return_value = {"success": True}

    mock_http_request.side_effect = [mock_http_login_response, api_response]  # Mock login, then API request

    mock_task = MagicMock()
    mock_task.args = {
        "method": "GET",
        "endpoint": "/authorization/accounts"
    }

    action_module = GenericRequest(
        task=mock_task,
        connection=MagicMock(),
        play_context=MagicMock(),
        loader=MagicMock(),
        templar=MagicMock(),
        shared_loader_obj=MagicMock(),
    )

    result = action_module.run(task_vars=mock_task_vars)

    assert not result["changed"]
    assert result["json"] == {"success": True}  # Corrected assertion

# Test API request with query parameters
@patch("ansible_collections.itential.core.plugins.module_utils.http.send_request")
def test_generic_request_with_params(mock_http_request, mock_task_vars, mock_http_login_response):
    """Test an API request with query parameters."""

    api_response = MagicMock(status_code=200, text=json.dumps({"success": True}))
    api_response.json.return_value = {"success": True}

    mock_http_request.side_effect = [mock_http_login_response, api_response]

    mock_task = MagicMock()
    mock_task.args = {
        "method": "GET",
        "endpoint": "/authorization/accounts",
        "params": {"status": "active"}
    }

    action_module = GenericRequest(
        task=mock_task,
        connection=MagicMock(),
        play_context=MagicMock(),
        loader=MagicMock(),
        templar=MagicMock(),
        shared_loader_obj=MagicMock(),
    )

    result = action_module.run(task_vars=mock_task_vars)

    assert not result["changed"]
    assert result["json"] == {"success": True}  # Corrected assertion

# Test API request with JSON payload (POST request)
@patch("ansible_collections.itential.core.plugins.module_utils.http.send_request")
def test_generic_request_with_data(mock_http_request, mock_task_vars, mock_http_login_response):
    """Test an API request with a JSON payload (POST request)."""

    api_response = MagicMock(status_code=200, text=json.dumps({"created": True}))
    api_response.json.return_value = {"created": True}

    mock_http_request.side_effect = [mock_http_login_response, api_response]

    mock_task = MagicMock()
    mock_task.args = {
        "method": "POST",
        "endpoint": "/authorization/accounts",
        "data": {"username": "test_user"}
    }

    action_module = GenericRequest(
        task=mock_task,
        connection=MagicMock(),
        play_context=MagicMock(),
        loader=MagicMock(),
        templar=MagicMock(),
        shared_loader_obj=MagicMock(),
    )

    result = action_module.run(task_vars=mock_task_vars)

    assert not result["changed"]
    assert result["json"] == {"created": True}  # Corrected assertion

# Test missing required arguments
@patch("ansible_collections.itential.core.plugins.module_utils.http.send_request")
def test_generic_request_missing_args(mock_http_request, mock_task_vars, mock_http_login_response):
    """Test missing required arguments (method or endpoint)."""

    mock_task = MagicMock()
    mock_task.args = {}  # No arguments provided

    action_module = GenericRequest(
        task=mock_task,
        connection=MagicMock(),
        play_context=MagicMock(),
        loader=MagicMock(),
        templar=MagicMock(),
        shared_loader_obj=MagicMock(),
    )

    with pytest.raises(Exception, match="'method' must be provided."):
        action_module.run(task_vars=mock_task_vars)

    mock_task.args = {"method": "GET"}

    with pytest.raises(Exception, match="'endpoint' must be provided."):
        action_module.run(task_vars=mock_task_vars)

# Test unexpected errors
@patch("ansible_collections.itential.core.plugins.module_utils.http.send_request")
def test_generic_request_unexpected_error(mock_http_request, mock_task_vars, mock_http_login_response):
    """Test handling of unexpected errors during request execution."""

    mock_http_request.side_effect = Exception("Unexpected error occurred")

    mock_task = MagicMock()
    mock_task.args = {
        "method": "GET",
        "endpoint": "/authorization/accounts"
    }

    action_module = GenericRequest(
        task=mock_task,
        connection=MagicMock(),
        play_context=MagicMock(),
        loader=MagicMock(),
        templar=MagicMock(),
        shared_loader_obj=MagicMock(),
    )

    with pytest.raises(Exception, match="Unexpected error occurred"):
        action_module.run(task_vars=mock_task_vars)
