# Copyright 2024, Itential Inc. All Rights Reserved

# GNU General Public License v3.0+ (see LICENSES/GPL-3.0-or-later.txt or https://www.gnu.org/licenses/gpl-3.0.txt)
# SPDX-License-Identifier: GPL-3.0-or-later

# Retrieves list of tasks from IAP. Supports filtering via parameters.
# Returns: List of task objects with their status, details, and type.
# Example:
#   - name: Get tasks by status
#     itential.platform.get_tasks:
#       status: completed
#     register: completed_tasks

from ansible.plugins.action import ActionBase
from ansible_collections.itential.platform.plugins.module_utils.request import make_request


class ActionModule(ActionBase):

    _supports_check_mode = False
    _supports_async = False
    _requires_connection = False

    def run(self, tmp=None, task_vars=None):

        module_args = self._task.args

        params = {}
        for key, value in module_args.items():
            params[f"equals[{key}]"] = value

        endpoint = "/operations-manager/tasks"

        method = "GET"

        params["include"] = "name,status,type"

        return make_request(task_vars, method, endpoint, params=params)
