#!/usr/bin/python

# Copyright 2024, Itential Inc. All Rights Reserved
# GNU General Public License v3.0+ (see LICENSES/GPL-3.0-or-later.txt or https://www.gnu.org/licenses/gpl-3.0.txt)
# SPDX-License-Identifier: GPL-3.0-or-later

from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = """
---
module: itential.platform.get_jobs
author: Itential

short_description: Retrieve a list of jobs from an IAP system with optional filtering.

description:
  - The M(itential.platform.get_jobs) module retrieves a list of jobs from an IAP system.
  - Users can provide key-value pairs as arguments to filter the results based on job attributes.
  - Filters are dynamically converted to query parameters, allowing for flexible job retrieval.
  - The response includes the job name and status by default.

options:
  <key>:
    description:
      - Any key-value pair can be provided as an argument to filter the job list.
      - The key corresponds to a job attribute, and the value restricts results to matching entries.
    required: false
    type: str

"""

EXAMPLES = """
  - name: Get all jobs
    itential.platform.get_jobs:

  - name: Get only running jobs
    itential.platform.get_jobs:
      status: running

  - name: Get jobs filtered by name and status
    itential.platform.get_jobs:
      name: "Example Job"
      status: completed
"""

