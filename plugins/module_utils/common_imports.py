# Copyright 2024, Itential Inc. All Rights Reserved

# GNU General Public License v3.0+ (see LICENSES/GPL-3.0-or-later.txt or https://www.gnu.org/licenses/gpl-3.0.txt)
# SPDX-License-Identifier: GPL-3.0-or-later

from ansible.plugins.action import ActionBase
from ansible_collections.itential.platform.plugins.module_utils.requests import (
    initialize_request,
    execute_request,
)
from ansible_collections.itential.platform.plugins.module_utils import host as spec
from ansible_collections.itential.core.plugins.module_utils import display
from ansible_collections.itential.core.plugins.module_utils import http
