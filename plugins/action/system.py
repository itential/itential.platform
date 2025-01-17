# Copyright 2024, Itential Inc. All Rights Reserved

# GNU General Public License v3.0+ (see LICENSES/GPL-3.0-or-later.txt or https://www.gnu.org/licenses/gpl-3.0.txt)
# SPDX-License-Identifier: GPL-3.0-or-later

import time
import json

from ansible.plugins.action import ActionBase
from ansible.errors import AnsibleError

from ansible.module_utils.common import yaml

from ansible_collections.itential.core.plugins.module_utils import display
from ansible_collections.itential.core.plugins.module_utils import args
from ansible_collections.itential.core.plugins.module_utils import hosts
from ansible_collections.itential.core.plugins.module_utils import http

from ansible_collections.itential.platform.plugins.module_utils.iap import login
from ansible_collections.itential.platform.plugins.module_utils import host as spec


class ActionModule(ActionBase):

    _supports_check_mode = False
    _supports_async = False
    _requires_connection = False

    def run(self, tmp=None, task_vars=None):
        inventory_hostname = task_vars["inventory_hostname"]
        hostvars = task_vars["hostvars"].get(inventory_hostname)

        if not hostvars.get("itential_connection") == "http":
            return {"changed": False, "skipped": True}


        schema = yaml.yaml_load(spec.DOCUMENTATION)
        host = hosts.new(schema, hostvars)

        display.vvv(f"running task {self._task.action}", host=inventory_hostname)

        headers = host.headers or {}
        headers.update({
            "content-type": "application/json",
            "accept": "application/json"
        })

        token = login(host)
        params = {"token": token}

        url = http.make_url(host.host, "/health/system", port=host.port, use_tls=host.use_tls)

        method = "GET"

        display.vvv(f"{method} {url}", host=inventory_hostname)

        result = {"changed": False}

        start = time.perf_counter()

        resp = http.send_request(**{
            "method": method,
            "url": url,
            "params": params,
            "headers": headers,
            "verify": host.verify,
            "disable_warnings": host.disable_warnings,
        })

        try:
            resp.raise_for_status()
        except Exception as exc:
            raise AnsibleError(str(exc))

        if resp.json():
            result["json"] = resp.json()

        end = time.perf_counter()
        result["elapsed_time"] = end - start

        return result

