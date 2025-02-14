# Copyright 2024, Itential Inc. All Rights Reserved

# GNU General Public License v3.0+ (see LICENSES/GPL-3.0-or-later.txt or https://www.gnu.org/licenses/gpl-3.0.txt)
# SPDX-License-Identifier: GPL-3.0-or-later

import time
import json

from ansible.plugins.action import ActionBase
from ansible.errors import AnsibleError

from ansible_collections.itential.lib.plugins.module_utils import display
from ansible_collections.itential.lib.plugins.module_utils import args
from ansible_collections.itential.lib.plugins.module_utils import hosts

from ansible_collections.itential.lib.plugins.module_utils import http


class ActionModule(ActionBase):

    _supports_check_mode = False
    _supports_async = False
    _requires_connection = False

    def run(self, tmp=None, task_vars=None):
        inventory_hostname = task_vars["inventory_hostname"]
        hostvars = task_vars["hostvars"].get(inventory_hostname)

        if not hostvars.get("itential_connection") == "http":
            return {"changed": False, "skipped": True}

        host = hosts.new("itential.http.host", hostvars)

        display.vvv(f"running task {self._task.action}", host=inventory_hostname)

        method = args.get("method", self._task).upper()
        query = args.get("query", self._task)
        path = args.get("path", self._task)
        data = args.get("data", self._task)
        timeout = args.get("timeout", self._task)

        headers = host.headers or {}
        headers.update(self._task.args.get("headers") or {})

        url = http.url(host, path)

        auth = None
        if host.auth_type == "basic":
            auth = http.basic_auth(host.username, host.password)

        if isinstance(data, str):
            data = bytes(data, "utf-8")

        display.vvv(f"{method} {url}", host=inventory_hostname)

        resp = http.request(**{
            "method": method,
            "url": url,
            "headers": headers,
            "data": json.dumps(data),
            "params": query,
            "auth": auth,
            "timeout": timeout,
            "verify": host.verify,
            "disable_warnings": host.disable_warnings,
        })


        result = {"changed": False}

        start = time.perf_counter()

        try:
            resp.raise_for_status()
        except Exception as exc:
            raise AnsibleError(str(exc))

        if resp.json():
            result["json"] = resp.json()

        end = time.perf_counter()
        result["elapsed_time"] = end - start

        return result
