#!/usr/bin/python

# Copyright 2024, Itential Inc. All Rights Reserved
# GNU General Public License v3.0+ (see LICENSES/GPL-3.0-or-later.txt or https://www.gnu.org/licenses/gpl-3.0.txt)
# SPDX-License-Identifier: GPL-3.0-or-later

from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = """
---
module: itential.platform.activate_task_worker
author: Itential

short_description: Activate the task worker for an IAP system

description:
  - The M(itential.platform.activate_task_worker) module activates a
   task worker for an IAP system.
"""


EXAMPLES = """
  - name: activate iap task worker
    itential.platform.activate_task_worker:
"""
