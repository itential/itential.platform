#!/usr/bin/python

# Copyright 2024, Itential Inc. All Rights Reserved
# GNU General Public License v3.0+ (see LICENSES/GPL-3.0-or-later.txt or https://www.gnu.org/licenses/gpl-3.0.txt)
# SPDX-License-Identifier: GPL-3.0-or-later

from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = """
---
module: itential.iap.system
author: Itential

short_description: Get the health of an IAP system

description:
  - The M(itential.iap.system) module returns the health of the
    IAP system.

options:
  name:
    type: str

  tags:
    type: list

  pass_rule:
    type: bool
    default: true

  ignore_warnings:
    type: bool
    default: false

  commands:
    type: list
    suboptions:
      command:
        type: string
      pass_rule:
        type: bool
      rules:
        type: list
        suboptions:
          rule:
            type: str
          eval:
            type: str
          severity:
            type: str

"""


EXAMPLES = """
  - name: get the health of a system
    itential.iap.system:
"""
