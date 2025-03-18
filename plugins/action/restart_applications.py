# Copyright 2024, Itential Inc. All Rights Reserved

# GNU General Public License v3.0+ (see LICENSES/GPL-3.0-or-later.txt or https://www.gnu.org/licenses/gpl-3.0.txt)
# SPDX-License-Identifier: GPL-3.0-or-later

# Restarts one or more Platform applications.
# Parameters:
#   application_names: A single application name (str) or a list of application names (list).
#
# Examples:
#   - name: Restart a single application (string input)
#     itential.platform.restart_application:
#       application_names: "platform-core"
#
#   - name: Restart a single application (list input)
#     itential.platform.restart_application:
#       application_names:
#         - platform-core
#
#   - name: Restart multiple applications
#     itential.platform.restart_application:
#       application_names:
#         - platform-core
#         - ag-manager

from ansible.plugins.action import ActionBase
from ansible_collections.itential.platform.plugins.module_utils.request import make_request
from ansible.errors import AnsibleError

class ActionModule(ActionBase):

    _supports_check_mode = False
    _supports_async = False
    _requires_connection = False

    def run(self, tmp=None, task_vars=None):
        """Restart one or more Platform applications by making API requests."""

        application_names = self._task.args.get("application_names")
        if not application_names:
            raise AnsibleError("'application_names' must be provided.")

        # Normalize input: Convert a single string to a list
        if isinstance(application_names, str):
            application_names = [application_names]
        elif not isinstance(application_names, list):
            raise AnsibleError("'application_names' must be a string or a list of strings.")

        results = []
        for app in application_names:
            endpoint = f"/applications/{app}/restart"
            method = "PUT"
            response = make_request(task_vars, method, endpoint)
            results.append(response)

        return {"results": results}  # Always return a list
