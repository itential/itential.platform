# Copyright 2024, Itential Inc. All Rights Reserved

# GNU General Public License v3.0+ (see LICENSES/GPL-3.0-or-later.txt or https://www.gnu.org/licenses/gpl-3.0.txt)
# SPDX-License-Identifier: GPL-3.0-or-later

from ansible.plugins.action import ActionBase
from ansible.errors import AnsibleError
from ansible_collections.itential.platform.plugins.module_utils.request import make_request

class ActionModule(ActionBase):

    _supports_check_mode = False
    _supports_async = False
    _requires_connection = False

    def run(self, tmp=None, task_vars=None):

        module_args = self._task.args

        # Validate required arguments
        method = module_args.get("method")
        endpoint = module_args.get("endpoint")
        if not method:
            raise AnsibleError("'method' must be provided.")
        if not endpoint:
            raise AnsibleError("'endpoint' must be provided.")

        # Optional arguments
        params = module_args.get("params", None)
        data = module_args.get("data", None)

        # Execute the request
        return make_request(task_vars, method, endpoint, params=params, data=data)


