# Copyright 2024, Itential Inc. All Rights Reserved

# GNU General Public License v3.0+ (see LICENSES/GPL-3.0-or-later.txt or https://www.gnu.org/licenses/gpl-3.0.txt)
# SPDX-License-Identifier: GPL-3.0-or-later

import json
import time
from ansible.errors import AnsibleError
from ansible.module_utils.common import yaml
from ansible_collections.itential.platform.plugins.module_utils.login import login
from ansible_collections.itential.core.plugins.module_utils import hosts
from ansible_collections.itential.core.plugins.module_utils import display
from ansible_collections.itential.core.plugins.module_utils import http
from ansible_collections.itential.platform.plugins.module_utils import host as spec

def make_request(task_vars, method, endpoint, params=None, data=None):
    inventory_hostname = task_vars["inventory_hostname"]
    hostvars = task_vars["hostvars"].get(inventory_hostname)

    if params is None:
        params = {}

    try:
        data_json = json.dumps(data) if data else None
    except (TypeError, ValueError) as e:
        raise AnsibleError(f"'data' must be JSON-serializable: {e}")

    if not isinstance(params, dict):
        raise AnsibleError(f"'params' must be a dictionary, got {type(params)}")

    schema = yaml.yaml_load(spec.DOCUMENTATION)
    host = hosts.new(schema, hostvars)

    token = login(host)
    params["token"] = token

    headers = host.headers or {}
    headers.update({
        "content-type": "application/json",
        "accept": "application/json"
    })

    url = http.make_url(host.host, endpoint, port=host.port, use_tls=host.use_tls)

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

    try:
        resp = http.send_request(
            method=method,
            url=url,
            params=params,
            headers=headers,
            data=data_json,
            verify=host.verify,
            disable_warnings=host.disable_warnings,
        )
        resp.raise_for_status()

    except Exception as exc:
        raise AnsibleError(f"HTTP request failed: {str(exc)} | Method: {method} | URL: {url} | Params: {params}")

    display.vvv(
        f"API Response:\n"
        f"  Status Code: {resp.status_code}\n"
        f"  Headers: {json.dumps(dict(resp.headers), indent=2)}\n"
        f"  Body: {resp.text}",
        host=task_vars["inventory_hostname"]
    )

    result = {"changed": False, "elapsed_time": time.perf_counter() - start_time}

    if resp.headers.get("Content-Type", "").startswith("application/json"):
        try:
            result["json"] = resp.json()
        except ValueError:
            raise AnsibleError(f"Failed to parse JSON response: {resp.text}")
    else:
        raise AnsibleError(f"Unexpected content type: {resp.headers.get('Content-Type')} | Response: {resp.text}")

    return result
