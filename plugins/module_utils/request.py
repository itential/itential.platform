import json
import time
import re
from ansible.errors import AnsibleError
from ansible.module_utils.common import yaml
from ansible_collections.itential.platform.plugins.module_utils.login import login
from ansible_collections.itential.core.plugins.module_utils import hosts
from ansible_collections.itential.core.plugins.module_utils import display
from ansible_collections.itential.core.plugins.module_utils import http
from ansible_collections.itential.platform.plugins.module_utils import host as spec

VALID_HTTP_METHODS = {"GET", "POST", "PUT", "PATCH", "DELETE"}

def make_request(task_vars, method, endpoint, params=None, data=None):
    """Send an authenticated API request to the specified endpoint."""

    inventory_hostname = task_vars["inventory_hostname"]
    hostvars = task_vars["hostvars"].get(inventory_hostname)

    if params is None:
        params = {}

    # Ensure `data` is JSON-serializable
    try:
        data_json = json.dumps(data) if data else None
    except (TypeError, ValueError) as e:
        raise AnsibleError(f"'data' must be JSON-serializable: {e}")

    # Validate that `params` is a dictionary
    if not isinstance(params, dict):
        raise AnsibleError(f"'params' must be a dictionary, got {type(params)}")

    # Validate HTTP method before sending request
    if method not in VALID_HTTP_METHODS:
        raise AnsibleError(f"Invalid HTTP method: {method}. Must be one of {VALID_HTTP_METHODS}")

    # Load schema and construct the host object
    schema = yaml.yaml_load(spec.DOCUMENTATION)
    host = hosts.new(schema, hostvars)

    headers = host.headers or {}
    headers.update({
        "content-type": "application/json",
        "accept": "application/json"
    })

    # Construct and validate the request URL
    url = http.make_url(host.host, endpoint, port=host.port, use_tls=host.use_tls)
    if not re.match(r"^https?://[^\s/$.?#].[^\s]*$", url):
        raise AnsibleError(f"Malformed URL: {url}")

    # Check if iap_auth_token is provided in task vars
    auth_token = hostvars.get("iap_auth_token")

    # If auth_token is already provided, add it to params. Otherwise call the login function
    if auth_token:
        display.vvv("Using Provided IAP Auth Token")
        params["token"] = auth_token
    else:
        display.vvv("Generating new IAP Auth Token")
        params["token"] = login(host)

    display.vvv(
        f"API Request:\n"
        f"  Method: {method}\n"
        f"  URL: {url}\n"
        f"  Headers: {json.dumps(headers, indent=2)}\n"
        f"  Params: {json.dumps(params, indent=2)}\n"
        f"  Data: {data_json or 'None'}",
        host=task_vars["inventory_hostname"]
    )

    start_time = time.perf_counter()

    # Send the request
    resp = http.send_request(
        method=method,
        url=url,
        params=params,
        headers=headers,
        data=data_json,
        verify=host.verify,
        disable_warnings=host.disable_warnings,
    )

    display.vvv(
        f"API Response:\n"
        f"  Status Code: {resp.status_code}\n"
        f"  Headers: {json.dumps(dict(resp.headers), indent=2)}\n"
        f"  Body: {resp.text}",
        host=task_vars["inventory_hostname"]
    )

    # Raise an error for any non-200 response
    if resp.status_code != 200:
        raise AnsibleError(f"API request failed with status {resp.status_code}: {resp.text}")

    result = {"changed": False, "elapsed_time": time.perf_counter() - start_time}

    # Attempt to parse JSON response if applicable
    if resp.headers.get("Content-Type", "").startswith("application/json"):
        try:
            result["json"] = resp.json()
        except ValueError:
            raise AnsibleError(f"Failed to parse JSON response: {resp.text}")

    return result
