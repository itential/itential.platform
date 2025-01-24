# Copyright 2024, Itential Inc. All Rights Reserved

# GNU General Public License v3.0+ (see LICENSES/GPL-3.0-or-later.txt or https://www.gnu.org/licenses/gpl-3.0.txt)
# SPDX-License-Identifier: GPL-3.0-or-later
from ansible_collections.itential.platform.plugins.module_utils.common_imports import *

class ActionModule(ActionBase):

    _supports_check_mode = False
    _supports_async = False
    _requires_connection = False

    def run(self, tmp=None, task_vars=None):
        host, headers, token = initialize_request(task_vars, spec)
        if not host:
            return headers
        
        params = {
            "token": token,
            "equals[status]": "canceled"
        }

        url = http.make_url(host.host, "/operations-manager/jobs", port=host.port, use_tls=host.use_tls)

        method = "GET"

        display.vvv(f"{method} {url}", host=task_vars["inventory_hostname"])

        return execute_request(host, method, url, params=params, headers=headers)
