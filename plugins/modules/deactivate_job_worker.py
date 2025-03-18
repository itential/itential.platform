#!/usr/bin/python

# Copyright 2024, Itential Inc. All Rights Reserved
# GNU General Public License v3.0+ (see LICENSES/GPL-3.0-or-later.txt or https://www.gnu.org/licenses/gpl-3.0.txt)
# SPDX-License-Identifier: GPL-3.0-or-later

from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = """
---
module: itential.platform.deactivate_job_worker
author: Itential

short_description: deactivate the job worker for a Platform system

description:
  - The M(itential.platform.deactivate_job_worker) module deactivates a
   job worker for a Platform system.
"""


EXAMPLES = """
  - name: deactivate platform job worker
    itential.platform.deactivate_job_worker:
"""
