#!/usr/bin/python

# Copyright 2024, Itential Inc. All Rights Reserved
# GNU General Public License v3.0+ (see LICENSES/GPL-3.0-or-later.txt or https://www.gnu.org/licenses/gpl-3.0.txt)
# SPDX-License-Identifier: GPL-3.0-or-later

from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = """
---
module: itential.platform.restart_adapter
author: Itential

short_description: Restart a specified adapter in the IAP system.

description:
  - The M(itential.platform.restart_adapter) module restarts an adapter in the 
    IAP system using the name provided via the C(adapter_name) argument. 
  - This module communicates with the IAP API to perform the restart operation.

options:
  adapter_name:
    description:
      - The name of the adapter to restart.
    required: true
    type: str
"""

EXAMPLES = """
  - name: Restart a specific adapter
    itential.platform.restart_adapter:
      adapter_name: example_adapter
    delegate_to: localhost
"""

