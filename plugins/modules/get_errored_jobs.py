#!/usr/bin/python

# Copyright 2024, Itential Inc. All Rights Reserved
# GNU General Public License v3.0+ (see LICENSES/GPL-3.0-or-later.txt or https://www.gnu.org/licenses/gpl-3.0.txt)
# SPDX-License-Identifier: GPL-3.0-or-later

from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = """
---
module: itential.platform.get_errored_jobs
author: Itential

short_description: Get a list of active tasks from an IAP system

description:
  - The M(itential.platform.get_errored_jobs) module returns a list of errored 
  jobs from an IAP system.
"""


EXAMPLES = """
  - name: get a list of errored jobs
    itential.platform.get_errored_jobs:
"""
