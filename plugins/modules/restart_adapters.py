#!/usr/bin/python

# Copyright 2024, Itential Inc. All Rights Reserved
# GNU General Public License v3.0+ (see LICENSES/GPL-3.0-or-later.txt or https://www.gnu.org/licenses/gpl-3.0.txt)
# SPDX-License-Identifier: GPL-3.0-or-later

from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = """
---
module: itential.platform.restart_adapters
author: Itential

short_description: Restart one or more adapters in the Itential Platform system.

description:
  - The M(itential.platform.restart_adapters) module restarts one or more adapters in the 
    Itential Platform system using the names provided via the C(adapter_names) argument. 
  - This module communicates with the Itential Platform API to perform the restart operation.
  - The C(adapter_names) parameter supports both a single adapter name (as a string) and 
    multiple adapter names (as a list).

options:
  adapter_names:
    description:
      - The name of the adapter to restart or a list of adapter names.
    required: true
    type: list
    elements: str
"""

EXAMPLES = """
  - name: Restart a single adapter (string input)
    itential.platform.restart_adapters:
      adapter_names: network-adapter
    delegate_to: localhost

  - name: Restart a single adapter (list input)
    itential.platform.restart_adapters:
      adapter_names:
        - network-adapter
    delegate_to: localhost

  - name: Restart multiple adapters
    itential.platform.restart_adapters:
      adapter_names:
        - network-adapter
        - security-adapter
    delegate_to: localhost
"""
