#!/usr/bin/python

# Copyright 2024, Itential Inc. All Rights Reserved
# GNU General Public License v3.0+ (see LICENSES/GPL-3.0-or-later.txt or https://www.gnu.org/licenses/gpl-3.0.txt)
# SPDX-License-Identifier: GPL-3.0-or-later

from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = """
---
module: itential.platform.activate_job_worker
author: Itential

short_description: Activate the job worker for an Itential Platform system

description:
  - The M(itential.platform.activate_job_worker) module activates a
   job worker for an Itential Platform system.
"""


EXAMPLES = """
  - name: activate platform job worker
    itential.platform.activate_job_worker:
"""
