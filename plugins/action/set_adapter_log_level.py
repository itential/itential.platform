# Copyright 2024, Itential Inc. All Rights Reserved

# GNU General Public License v3.0+ (see LICENSES/GPL-3.0-or-later.txt or https://www.gnu.org/licenses/gpl-3.0.txt)
# SPDX-License-Identifier: GPL-3.0-or-later

# Sets the logging level for a specific Itential Platform adapter.
# Parameters:
#   adapter_name: Name of the adapter
#   log_level: Desired log level (debug, info, warn, error)
# Example:
#   - name: Set adapter logging to debug
#     itential.platform.set_adapter_log_level:
#       adapter_name: network-adapter
#       log_level: debug

from ansible.plugins.action import ActionBase
from ansible_collections.itential.platform.plugins.module_utils.request import make_request
from ansible.errors import AnsibleError

class ActionModule(ActionBase):

    _supports_check_mode = False
    _supports_async = False
    _requires_connection = False

    def run(self, tmp=None, task_vars=None):
        adapter_name = self._task.args.get("adapter_name")
        log_level = self._task.args.get("log_level")
        transport = self._task.args.get("transport")

        if not adapter_name or not log_level or not transport:
            raise AnsibleError("adapter_name, log_level, and transport must be provided.")

        endpoint = f"/adapters/{adapter_name}/loglevel"
        method = "PUT"

        data = {
            "properties": {
                "transport": transport,
                "level": log_level
            }
        }

        return make_request(task_vars, method, endpoint, data=data)

