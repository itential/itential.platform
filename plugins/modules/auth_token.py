#!/usr/bin/python

# Copyright 2024, Itential Inc. All Rights Reserved
# GNU General Public License v3.0+ (see LICENSES/GPL-3.0-or-later.txt or https://www.gnu.org/licenses/gpl-3.0.txt)
# SPDX-License-Identifier: GPL-3.0-or-later

from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = """
---
module: itential.platform.auth_token
author: Itential

short_description: Generate an authentication token for Platform.

description:
  - The M(itential.platform.auth_token) module generates an authentication token for a Platform system.
  - This token can be used to authenticate API requests within the platform.
  - The module does not require any input parameters.

options: {}

"""

EXAMPLES = """
  - name: Generate auth token
    itential.platform.auth_token:
"""

RETURN = """
auth_token:
  description: The generated authentication token.
  type: str
  returned: always
"""
