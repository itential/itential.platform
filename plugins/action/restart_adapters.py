# Copyright 2024, Itential Inc. All Rights Reserved

# GNU General Public License v3.0+ (see LICENSES/GPL-3.0-or-later.txt or https://www.gnu.org/licenses/gpl-3.0.txt)
# SPDX-License-Identifier: GPL-3.0-or-later

# Restarts one or more IAP adapters.
# Parameters:
#   adapter_names: A single adapter name (str) or a list of adapter names (list).
#
# Examples:
#   - name: Restart a single adapter (string input)
#     itential.platform.restart_adapter:
#       adapter_names: network-adapter
#
#   - name: Restart a single adapter (list input)
#     itential.platform.restart_adapter:
#       adapter_names:
#         - network-adapter
#
#   - name: Restart multiple adapters
#     itential.platform.restart_adapter:
#       adapter_names:
#         - network-adapter
#         - security-adapter

from ansible.plugins.action import ActionBase
from ansible_collections.itential.platform.plugins.module_utils.request import make_request
from ansible.errors import AnsibleError

class ActionModule(ActionBase):

    _supports_check_mode = False
    _supports_async = False
    _requires_connection = False

    def run(self, tmp=None, task_vars=None):
        """Restart one or more IAP adapters by making API requests."""

        adapter_names = self._task.args.get("adapter_names")
        if not adapter_names:
            raise AnsibleError("'adapter_names' must be provided.")

        # Normalize input: Convert a single string to a list
        if isinstance(adapter_names, str):
            adapter_names = [adapter_names]
        elif not isinstance(adapter_names, list):
            raise AnsibleError("'adapter_names' must be a string or a list of strings.")

        results = []
        for adapter in adapter_names:
            endpoint = f"/adapters/{adapter}/restart"
            method = "PUT"
            response = make_request(task_vars, method, endpoint)
            results.append(response)

        return {"results": results}  # Always return a list
