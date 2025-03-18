#!/usr/bin/python

# Copyright 2024, Itential Inc. All Rights Reserved
# GNU General Public License v3.0+ (see LICENSES/GPL-3.0-or-later.txt or https://www.gnu.org/licenses/gpl-3.0.txt)
# SPDX-License-Identifier: GPL-3.0-or-later

from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = """
---
module: itential.platform.restart_applications
author: Itential

short_description: Restart one or more applications in the Platform system.

description:
  - The M(itential.platform.restart_applications) module restarts one or more applications in the 
    Platform system using the names provided via the C(application_names) argument.
  - This module communicates with the Platform API to perform the restart operation.
  - The C(application_names) parameter supports both a single application name (as a string) and multiple application names (as a list).

options:
  application_names:
    description:
      - The name of the application to restart or a list of application names.
    required: true
    type: list
    elements: str
"""

EXAMPLES = """
  - name: Restart a single application (string input)
    itential.platform.restart_applications:
      application_names: OperationsManager
    delegate_to: localhost

  - name: Restart a single application (list input)
    itential.platform.restart_applications:
      application_names:
        - OperationsManager
    delegate_to: localhost

  - name: Restart multiple applications
    itential.platform.restart_applications:
      application_names:
        - OperationsManager
        - ag-manager
    delegate_to: localhost
"""
