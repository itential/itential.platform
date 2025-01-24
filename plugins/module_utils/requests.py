# Copyright 2024, Itential Inc. All Rights Reserved

# GNU General Public License v3.0+ (see LICENSES/GPL-3.0-or-later.txt or https://www.gnu.org/licenses/gpl-3.0.txt)
# SPDX-License-Identifier: GPL-3.0-or-later
from ansible.errors import AnsibleError
from ansible.module_utils.common import yaml
from ansible_collections.itential.platform.plugins.module_utils.iap import login
from ansible_collections.itential.core.plugins.module_utils import hosts
import time
from ansible_collections.itential.core.plugins.module_utils import http

def initialize_request(task_vars, spec):
    """
    Initialize the host object, login to get a token, and prepare headers.
    Returns the host, headers, and token.
    """
    inventory_hostname = task_vars["inventory_hostname"]
    hostvars = task_vars["hostvars"].get(inventory_hostname)

    if not hostvars.get("itential_connection") == "http":
        return None, {"changed": False, "skipped": True}

    schema = yaml.yaml_load(spec.DOCUMENTATION)
    host = hosts.new(schema, hostvars)

    token = login(host)
    headers = host.headers or {}
    headers.update({
        "content-type": "application/json",
        "accept": "application/json"
    })

    return host, headers, token

def execute_request(host, method, url, params=None, headers=None):
    """
    Execute the HTTP request, measure elapsed time, and process the response.
    """
    start_time = time.perf_counter()

    try:
        resp = http.send_request(**{
            "method": method,
            "url": url,
            "params": params or {},
            "headers": headers or {},
            "verify": host.verify,
            "disable_warnings": host.disable_warnings,
        })
        resp.raise_for_status()
    except Exception as exc:
        raise AnsibleError(f"HTTP request failed: {str(exc)}")

    result = {"changed": False, "elapsed_time": time.perf_counter() - start_time}

    # Process JSON response if available
    if resp.headers.get("Content-Type", "").startswith("application/json"):
        try:
            result["json"] = resp.json()
        except ValueError:
            raise AnsibleError("Failed to parse JSON response")

    return result
