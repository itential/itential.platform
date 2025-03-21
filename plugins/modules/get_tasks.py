#!/usr/bin/python

# Copyright 2024, Itential Inc. All Rights Reserved
# GNU General Public License v3.0+ (see LICENSES/GPL-3.0-or-later.txt or https://www.gnu.org/licenses/gpl-3.0.txt)
# SPDX-License-Identifier: GPL-3.0-or-later

from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = """
---
module: itential.platform.get_tasks
author: Itential

short_description: Retrieve a list of tasks from an Itential Platform system with
optional filtering.

description:
  - The M(itential.platform.get_tasks) module retrieves a list of tasks from an 
    Itential Platform system.
  - Users can provide key-value pairs as arguments to filter the results based on task attributes.
  - Filters are dynamically converted to query parameters, allowing for flexible task retrieval.
  - The response includes the task name and status by default.

options:
  <key>:
    description:
      - Any key-value pair can be provided as an argument to filter the task list.
      - The key corresponds to a task attribute, and the value restricts results to matching entries.
    required: false
    type: str

"""

EXAMPLES = """
  - name: Get all tasks
    itential.platform.get_tasks:

  - name: Get active tasks filtered by name
    itential.platform.get_tasks:
      name: "Example Task"
      status: active
"""

