# Copyright 2024, Itential Inc. All Rights Reserved

# GNU General Public License v3.0+ (see LICENSES/GPL-3.0-or-later.txt or https://www.gnu.org/licenses/gpl-3.0.txt)
# SPDX-License-Identifier: GPL-3.0-or-later
from ansible.plugins.action import ActionBase
from ansible_collections.itential.platform.plugins.module_utils.request import make_request
from ansible.errors import AnsibleError

class ActionModule(ActionBase):

    _supports_check_mode = False
    _supports_async = False
    _requires_connection = False

    def run(self, tmp=None, task_vars=None):

        application_name = self._task.args.get("application_name")
        if not application_name:
            raise AnsibleError("'application_name' must be provided.")

        endpoint = f"/applications/{application_name}/restart"
        method = "PUT"

        return make_request(task_vars, method, endpoint)
