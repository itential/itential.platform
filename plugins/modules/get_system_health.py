#!/usr/bin/python

# Copyright 2024, Itential Inc. All Rights Reserved
# GNU General Public License v3.0+ (see LICENSES/GPL-3.0-or-later.txt or https://www.gnu.org/licenses/gpl-3.0.txt)
# SPDX-License-Identifier: GPL-3.0-or-later

from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = """
---
module: itential.iap.get_system_health
author: Itential

short_description: Get the health of an IAP system

description:
  - The M(itential.iap.get_system_health) module returns the health of the
    IAP system.
"""


EXAMPLES = """
  - name: get the health of a system
    itential.iap.get_system_health:
"""
