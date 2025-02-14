# Copyright 2024, Itential Inc. All Rights Reserved

# GNU General Public License v3.0+ (see LICENSES/GPL-3.0-or-later.txt or https://www.gnu.org/licenses/gpl-3.0.txt)
# SPDX-License-Identifier: GPL-3.0-or-later

# Generates an auth token. No parameters required.
# Example:
#   - name: Generate auth token
#     itential.platform.auth_token:

from ansible.plugins.action import ActionBase
from ansible.module_utils.common import yaml
from ansible_collections.itential.platform.plugins.module_utils.login import login
from ansible_collections.itential.platform.plugins.module_utils import host as spec
from ansible_collections.itential.core.plugins.module_utils import hosts

class ActionModule(ActionBase):

    _supports_check_mode = False
    _supports_async = False
    _requires_connection = False

    def run(self, tmp=None, task_vars=None):
        inventory_hostname = task_vars["inventory_hostname"]
        hostvars = task_vars["hostvars"].get(inventory_hostname)

        schema = yaml.yaml_load(spec.DOCUMENTATION)
        host = hosts.new(schema, hostvars)

        auth_token = login(host)

        return {"auth_token": auth_token}
