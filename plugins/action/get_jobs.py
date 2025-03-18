# Copyright 2024, Itential Inc. All Rights Reserved

# GNU General Public License v3.0+ (see LICENSES/GPL-3.0-or-later.txt or https://www.gnu.org/licenses/gpl-3.0.txt)
# SPDX-License-Identifier: GPL-3.0-or-later

# Retrieves list of jobs from Platform. No parameters required.
# Returns: List of job objects with their status and details.
# Example:
#   - name: Get all jobs
#     itential.platform.get_jobs:
#     register: jobs_result

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

        endpoint = "/operations-manager/jobs"

        method = "GET"

        params["include"] = "name,status"

        return make_request(task_vars, method, endpoint, params=params)
