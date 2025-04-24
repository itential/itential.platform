#!/usr/bin/python

# Copyright 2024, Itential Inc. All Rights Reserved
# GNU General Public License v3.0+ (see LICENSES/GPL-3.0-or-later.txt or https://www.gnu.org/licenses/gpl-3.0.txt)
# SPDX-License-Identifier: GPL-3.0-or-later

from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = """
---
module: set_adapter_log_level
author: Itential
short_description: Set the logging level for a specific Itential Platform adapter

description:
  - The C(set_adapter_log_level) module configures the log level and transport
    method (file or console) for a specific adapter running on the Itential Platform.

options:
  adapter_name:
    description:
      - Name of the adapter to update the logging level for.
    required: true
    type: str

  log_level:
    description:
      - Logging level to set for the adapter.
      - Common values include C(debug), C(info), C(warn), C(error).
    required: true
    type: str

  transport:
    description:
      - Output transport to apply the log level to.
      - Valid values are C(file) and C(console).
    required: true
    type: str
"""

EXAMPLES = """
- name: Set adapter logging to debug using file transport
  itential.platform.set_adapter_log_level:
    adapter_name: network-adapter
    log_level: debug
    transport: file
"""

RETURN = """
changed:
  description: Whether the log level was successfully updated.
  returned: always
  type: bool
  sample: true
"""
