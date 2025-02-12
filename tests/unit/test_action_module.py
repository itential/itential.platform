import pytest
import json
from unittest.mock import MagicMock, patch
from ansible_collections.itential.platform.plugins.action.deactivate_job_worker import ActionModule as DeactivateJobWorker
from ansible_collections.itential.platform.plugins.action.deactivate_task_worker import ActionModule as DeactivateTaskWorker
from ansible_collections.itential.platform.plugins.action.activate_job_worker import ActionModule as ActivateJobWorker
from ansible_collections.itential.platform.plugins.action.activate_task_worker import ActionModule as ActivateTaskWorker
from ansible_collections.itential.platform.plugins.action.get_system_health import ActionModule as GetSystemHealth
from ansible_collections.itential.platform.plugins.action.get_worker_status import ActionModule as GetWorkerStatus

# Test cases for action modules that follow the same request structure
@pytest.mark.parametrize("action_module_class, expected_endpoint, expected_method", [
    (DeactivateJobWorker, "/workflow_engine/jobWorker/deactivate", "POST"),
    (ActivateJobWorker, "/workflow_engine/jobWorker/activate", "POST"),
    (DeactivateTaskWorker, "/workflow_engine/deactivate", "POST"),
    (ActivateTaskWorker, "/workflow_engine/activate", "POST"),
    (GetSystemHealth, "/health/system", "GET"),
    (GetWorkerStatus, "/workflow_engine/workers/status", "GET")
])
@patch("ansible_collections.itential.core.plugins.module_utils.http.send_request")
def test_action_module_success(mock_http_request, mock_http_login_response, mock_task_vars, action_module_class, expected_endpoint, expected_method):
    """Test that each action module makes the correct API request and handles the response properly."""

    api_response = MagicMock(status_code=200, text=json.dumps({"status": "success"}))
    api_response.json.return_value = {"status": "success"}

    # Simulate the login response followed by the actual request response
    mock_http_request.side_effect = [mock_http_login_response, api_response]

    # Mock required arguments for creating the ActionModule instance
    mock_task = MagicMock()
    mock_connection = MagicMock()
    mock_play_context = MagicMock()
    mock_loader = MagicMock()
    mock_templar = MagicMock()
    mock_shared_loader_obj = MagicMock()

    # Create and execute the action module
    action_module = action_module_class(
        task=mock_task,
        connection=mock_connection,
        play_context=mock_play_context,
        loader=mock_loader,
        templar=mock_templar,
        shared_loader_obj=mock_shared_loader_obj
    )
    result = action_module.run(task_vars=mock_task_vars)

    assert not result["changed"]
    assert result["json"] == {"status": "success"}

    # Ensure `send_request` was called twice: once for login, once for the actual request
    assert mock_http_request.call_count == 2

    second_call = mock_http_request.call_args_list[1]
    assert second_call[1]["method"] == expected_method
    assert second_call[1]["url"].endswith(expected_endpoint)
