import pytest
import json
from unittest.mock import MagicMock, patch
from ansible.errors import AnsibleError
from ansible_collections.itential.platform.plugins.action.get_jobs import ActionModule as GetJobs
from ansible_collections.itential.platform.plugins.action.get_tasks import ActionModule as GetTasks

# Test cases for action modules that construct parameters dynamically
@pytest.mark.parametrize("action_module_class, input_args, expected_endpoint, expected_method, expected_params", [
    (GetJobs, {"status": "running", "name": "greg"}, "/operations-manager/jobs", "GET", {
        "equals[status]": "running",
        "equals[name]": "greg",
        "include": "name,status"
    }),
    (GetTasks, {"status": "running", "name": "greg"}, "/operations-manager/tasks", "GET", {
        "equals[status]": "running",
        "equals[name]": "greg",
        "include": "name,status"
    }),
])
@patch("ansible_collections.itential.core.plugins.module_utils.http.send_request")
def test_action_module_with_inputs(mock_http_request, mock_http_login_response, mock_task_vars, action_module_class, input_args, expected_endpoint, expected_method, expected_params):
    """Test action modules that construct parameters dynamically based on input arguments."""

    api_response = MagicMock(status_code=200, text=json.dumps({"status": "success"}))
    api_response.json.return_value = {"status": "success"}

    # Simulate login response followed by API request response
    mock_http_request.side_effect = [mock_http_login_response, api_response]

    # Mock task arguments
    mock_task = MagicMock()
    mock_task.args = input_args

    # Create the action module instance with required Ansible arguments
    action_module = action_module_class(
        task=mock_task,
        connection=MagicMock(),
        play_context=MagicMock(),
        loader=MagicMock(),
        templar=MagicMock(),
        shared_loader_obj=MagicMock()
    )

    result = action_module.run(task_vars=mock_task_vars)

    assert not result["changed"]
    assert result["json"] == {"status": "success"}

    # Ensure send_request was called twice (once for login, once for API request)
    assert mock_http_request.call_count == 2

    second_call = mock_http_request.call_args_list[1]
    assert second_call[1]["method"] == expected_method
    assert second_call[1]["url"].endswith(expected_endpoint)

    # Ensure expected parameters are included in the request
    if expected_params:
        for key, value in expected_params.items():
            assert second_call[1]["params"].get(key) == value

    assert "token" in second_call[1]["params"]

# Test cases for missing required arguments
@pytest.mark.parametrize("action_module_class, missing_args_behavior", [
    (GetJobs, None),
    (GetTasks, None),
])
@patch("ansible_collections.itential.core.plugins.module_utils.http.send_request")
def test_action_module_missing_args(mock_http_request, mock_http_login_response, mock_task_vars, action_module_class, missing_args_behavior):
    """Test action modules with missing required arguments."""

    api_response = MagicMock(status_code=200, text=json.dumps({"status": "success"}))
    api_response.json.return_value = {"status": "success"}

    mock_http_request.side_effect = [mock_http_login_response, api_response]

    mock_task = MagicMock()
    mock_task.args = {}  # No arguments provided

    action_module = action_module_class(
        task=mock_task,
        connection=MagicMock(),
        play_context=MagicMock(),
        loader=MagicMock(),
        templar=MagicMock(),
        shared_loader_obj=MagicMock()
    )

    if missing_args_behavior:
        with missing_args_behavior:
            action_module.run(task_vars=mock_task_vars)
    else:
        result = action_module.run(task_vars=mock_task_vars)
        assert not result["changed"]
        assert result["json"] == {"status": "success"}
