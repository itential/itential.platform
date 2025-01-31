import pytest
from unittest.mock import MagicMock, patch
import shutil
import os
from pathlib import Path
import json


@pytest.fixture(scope="session", autouse=True)
def cleanup():
    """Cleanup __pycache__ and unwanted local Ansible collections after tests."""
    yield  # Run tests first, then cleanup after session.

    # Define paths to clean
    project_root = Path(__file__).resolve().parents[1]
    collections_path = project_root / "collections"

    # Remove all __pycache__ directories
    for pycache in project_root.rglob("__pycache__"):
        try:
            shutil.rmtree(pycache)
            print(f"Removed: {pycache}")
        except Exception as e:
            print(f"Could not remove {pycache}: {e}")

    # Remove local Ansible collections folder if it exists
    if collections_path.exists():
        try:
            shutil.rmtree(collections_path)
            print(f"Removed local collections folder: {collections_path}")
        except Exception as e:
            print(f"Could not remove {collections_path}: {e}")

# Mock the inventory
@pytest.fixture
def mock_task_vars():
    """Fixture to provide a mock Ansible inventory structure."""
    return {
        "inventory_hostname": "platform",
        "hostvars": {
            "platform": {
                "ansible_host": "example.com",
                "ansible_user": "bob",
                "ansible_ssh_private_key_file": "key.pem",
                "itential_connection": "http",
                "itential_port": 3000,
                "itential_user": "admin",
                "itential_password": "admin",
                "itential_http_use_tls": False,
                "itential_http_verify": False,
            }
        }
    }

@pytest.fixture
def mock_http_login_response():
    """Fixture for a mocked successful login response."""
    login_response = MagicMock()
    login_response.status_code = 200
    login_response.json.return_value = {"token": "mocked_token"}
    login_response.text = json.dumps({"token": "mocked_token"})
    return login_response

@pytest.fixture
def mock_http_request():
    """Fixture to mock HTTP requests."""
    with pytest.patch("ansible_collections.itential.core.plugins.module_utils.http.send_request") as mock_request:
        yield mock_request