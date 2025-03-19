# Copyright 2024, Itential Inc. All Rights Reserved

# GNU General Public License v3.0+ (see LICENSES/GPL-3.0-or-later.txt or https://www.gnu.org/licenses/gpl-3.0.txt)
# SPDX-License-Identifier: GPL-3.0-or-later

# Activates the Itential Platform task worker. No parameters required.
# Example:
#   - name: Activate task worker
#     itential.platform.activate_task_worker:

from ansible.plugins.action import ActionBase
from ansible_collections.itential.platform.plugins.module_utils.request import make_request

class ActionModule(ActionBase):

    _supports_check_mode = False
    _supports_async = False
    _requires_connection = False

    def run(self, tmp=None, task_vars=None):

        endpoint = "/workflow_engine/activate"
        method = "POST"

        return make_request(task_vars, method, endpoint)
