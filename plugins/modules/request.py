#!/usr/bin/python

# Copyright 2024, Itential Inc. All Rights Reserved
# GNU General Public License v3.0+ (see LICENSES/GPL-3.0-or-later.txt or https://www.gnu.org/licenses/gpl-3.0.txt)
# SPDX-License-Identifier: GPL-3.0-or-later

from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = """
---
module: itential.http.request
author: Itential

short_description: Send a request to a remote host over HTTP

description:
  - The M(itential.http.request) module provides a way to send API
    requests to remote hosts using HTTP.

options:
  method:
    description:
      - The HTTP method for the request.  This option accepts one of GET,
         POST, PUT, DELETE, PATCH, OPTION.   The default value is GET.
    type: str
    required: false
    default: get
    choices: [ "get", "put", "post", "delete", "patch", "option" ]

  data:
    description:
      - The body to send in the HTTP request.
    type: dict

  path:
    description:
      - The URI path to send the request to.  If the host is configured using
        `base_path`, the value of path will be combined with `base_path` to
        generate the full URI
    type: str
    required: true

  query:
    description:
      - One or more key=value pairs to be used to generate a query string
        that will be send to the remote host when the request is initiated.
    type: dict
    required: false

  timeout:
    description:
      - The amount of time in seconds to wait for a response from the remote
        host for a request
    type: int
    required: false
"""


EXAMPLES = """
  - name: send a http request to a remote host
    itential.http.request:
      path: "/search"
"""
