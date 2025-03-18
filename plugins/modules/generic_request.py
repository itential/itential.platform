#!/usr/bin/python

# Copyright 2024, Itential Inc. All Rights Reserved
# GNU General Public License v3.0+ (see LICENSES/GPL-3.0-or-later.txt or https://www.gnu.org/licenses/gpl-3.0.txt)
# SPDX-License-Identifier: GPL-3.0-or-later

from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = """
---
module: itential.platform.api_request
author: Itential

short_description: Send a generic API request to a Platform system.

description:
  - The M(itential.platform.api_request) module allows users to send generic API requests to a Platform system.
  - It supports specifying the HTTP method, endpoint, query parameters, and request body data.
  - This module is useful for interacting with various Platform API endpoints without creating dedicated modules.

options:
    method:
    description:
      - The HTTP method to use for the request.
    required: true
    type: str
    choices: [GET, PUT, POST, DELETE]
    default: GET

  endpoint:
    description:
      - The API endpoint to send the request to (e.g., "/applications/list").
    required: true
    type: str

  params:
    description:
      - Query parameters to include in the request.
      - These will be appended as URL parameters.
    required: false
    type: dict

  data:
    description:
      - The request body data to send (used for methods like POST or PUT).
      - This should be a JSON-serializable dictionary.
    required: false
    type: dict

"""

EXAMPLES = """
  - name: Retrieve a list of applications
    itential.platform.api_request:
      method: GET
      endpoint: "/applications/list"

  - name: Restart an application
    itential.platform.api_request:
      method: PUT
      endpoint: "/applications/AGManager/restart"

  - name: Create a new user with specific attributes
    itential.platform.api_request:
      method: POST
      endpoint: "/users"
      data:
        username: "newuser"
        role: "admin"

  - name: Retrieve jobs with filtering
    itential.platform.api_request:
      method: GET
      endpoint: "/operations-manager/jobs"
      params:
        status: running
        owner: "admin"

"""
