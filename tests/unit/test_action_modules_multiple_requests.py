import pytest
import json
from unittest.mock import MagicMock, patch
from ansible.errors import AnsibleError
from ansible_collections.itential.platform.plugins.action.restart_adapters import ActionModule as RestartAdapter
from ansible_collections.itential.platform.plugins.action.restart_applications import ActionModule as RestartApplication

# Test cases for modules that send multiple API requests
@pytest.mark.parametrize("action_module_class, input_args, expected_endpoints", [
    (RestartAdapter, {"adapter_names": "netconf"}, ["/adapters/netconf/restart"]),
    (RestartAdapter, {"adapter_names": ["netconf", "restconf"]}, ["/adapters/netconf/restart", "/adapters/restconf/restart"]),
    (RestartApplication, {"application_names": "AGManager"}, ["/applications/AGManager/restart"]),
    (RestartApplication, {"application_names": ["AGManager", "ConfigManager"]}, ["/applications/AGManager/restart", "/applications/ConfigManager/restart"]),
])
@patch("ansible_collections.itential.core.plugins.module_utils.http.send_request")
def test_action_module_multiple_requests(mock_http_request, mock_http_login_response, mock_task_vars, action_module_class, input_args, expected_endpoints):
    """Test action modules that make multiple API requests based on input arguments."""

    api_response = MagicMock(status_code=200, text=json.dumps({"status": "success"}))
    api_response.json.return_value = {"status": "success"}

    # Since login is executed for each request, we expect (2 * len(expected_endpoints)) calls
    mock_http_request.side_effect = [mock_http_login_response, api_response] * len(expected_endpoints)

    # Mock task arguments
    mock_task = MagicMock()
    mock_task.args = input_args

    # Create the action module instance
    action_module = action_module_class(
        task=mock_task,
        connection=MagicMock(),
        play_context=MagicMock(),
        loader=MagicMock(),
        templar=MagicMock(),
        shared_loader_obj=MagicMock()
    )

    result = action_module.run(task_vars=mock_task_vars)

    assert isinstance(result, dict)
    assert "results" in result

    # Ensure all responses contain a "status" key inside "json"
    assert isinstance(result["results"], list)
    for res in result["results"]:
        assert "json" in res
        assert res["json"].get("status") == "success"

    # Verify that the number of calls matches the expected count (login + request per adapter/app)
    expected_call_count = len(expected_endpoints) * 2
    actual_call_count = len(mock_http_request.call_args_list)

    assert actual_call_count == expected_call_count, f"Expected {expected_call_count} calls but got {actual_call_count}"

    # Verify that the API requests match expected endpoints
    for i, expected_endpoint in enumerate(expected_endpoints):
        second_call_index = (i * 2) + 1  # The second call for each adapter/application is the actual request
        actual_call = mock_http_request.call_args_list[second_call_index]
        assert actual_call[1]["method"] == "PUT"
        assert actual_call[1]["url"].endswith(expected_endpoint)

    # Ensure each request includes an authentication token if `params` exist
    for call in mock_http_request.call_args_list:
        if "params" in call[1]:  # Ensure params exist before checking
            assert "token" in call[1]["params"]

# Test cases for missing required arguments and invalid types
@pytest.mark.parametrize("action_module_class, input_args, expected_exception", [
    (RestartAdapter, {}, pytest.raises(AnsibleError, match="'adapter_names' must be provided.")),
    (RestartAdapter, {"adapter_names": 123}, pytest.raises(AnsibleError, match="'adapter_names' must be a string or a list of strings.")),
    (RestartApplication, {}, pytest.raises(AnsibleError, match="'application_names' must be provided.")),
    (RestartApplication, {"application_names": {"invalid": "dict"}}, pytest.raises(AnsibleError, match="'application_names' must be a string or a list of strings.")),
])
@patch("ansible_collections.itential.core.plugins.module_utils.http.send_request")
def test_action_module_invalid_args(mock_http_request, mock_http_login_response, mock_task_vars, action_module_class, input_args, expected_exception):
    """Test action modules with missing or invalid required arguments."""

    api_response = MagicMock(status_code=200, text=json.dumps({"status": "success"}))
    api_response.json.return_value = {"status": "success"}

    mock_http_request.side_effect = [mock_http_login_response, api_response]

    mock_task = MagicMock()
    mock_task.args = input_args  # Passing invalid input

    action_module = action_module_class(
        task=mock_task,
        connection=MagicMock(),
        play_context=MagicMock(),
        loader=MagicMock(),
        templar=MagicMock(),
        shared_loader_obj=MagicMock()
    )

    with expected_exception:
        action_module.run(task_vars=mock_task_vars)
