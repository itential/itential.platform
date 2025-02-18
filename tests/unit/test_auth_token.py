import pytest
from unittest.mock import MagicMock, patch
from ansible.errors import AnsibleError
from ansible_collections.itential.platform.plugins.action.auth_token import ActionModule


@patch("ansible_collections.itential.core.plugins.module_utils.http.send_request")
@patch("ansible_collections.itential.core.plugins.module_utils.hosts.new")
@patch("ansible.module_utils.common.yaml.yaml_load")
def test_auth_token_success(mock_yaml_load, mock_host_new, mock_http_request, mock_task_vars):
    """Test successful authentication token retrieval."""

    mock_yaml_load.return_value = {"mock_schema": True}

    # Mock host object
    mock_host_instance = MagicMock()
    mock_host_instance.username = "mock_user"
    mock_host_instance.password = "mock_pass"
    mock_host_new.return_value = mock_host_instance

    # Define a proper mock response for send_request()
    mock_http_response = MagicMock()
    mock_http_response.status_code = 200
    mock_http_response.text = "mocked_auth_token"
    mock_http_request.return_value = mock_http_response

    mock_task = MagicMock()
    action_module = ActionModule(
        task=mock_task,
        connection=MagicMock(),
        play_context=MagicMock(),
        loader=MagicMock(),
        templar=MagicMock(),
        shared_loader_obj=MagicMock(),
    )

    result = action_module.run(task_vars=mock_task_vars)

    # Ensure send_request() was called once
    mock_http_request.assert_called_once()

    # Ensure the correct token is returned
    assert result == {"auth_token": "mocked_auth_token"}


@patch("ansible_collections.itential.core.plugins.module_utils.http.send_request")
@patch("ansible_collections.itential.core.plugins.module_utils.hosts.new")
@patch("ansible.module_utils.common.yaml.yaml_load")
def test_auth_token_login_failure(mock_yaml_load, mock_host_new, mock_http_request, mock_task_vars):
    """Test failure when login function raises an AnsibleError."""

    mock_yaml_load.return_value = {"mock_schema": True}

    mock_host_instance = MagicMock()
    mock_host_instance.username = "mock_user"
    mock_host_instance.password = "mock_pass"
    mock_host_new.return_value = mock_host_instance

    # Simulate login failure
    mock_http_response = MagicMock()
    mock_http_response.status_code = 401
    mock_http_response.text = "Unauthorized"
    mock_http_request.return_value = mock_http_response

    mock_task = MagicMock()
    action_module = ActionModule(
        task=mock_task,
        connection=MagicMock(),
        play_context=MagicMock(),
        loader=MagicMock(),
        templar=MagicMock(),
        shared_loader_obj=MagicMock(),
    )

    with pytest.raises(AnsibleError, match="Unexpected HTTP status code in response: 401 Unauthorized"):
        action_module.run(task_vars=mock_task_vars)
