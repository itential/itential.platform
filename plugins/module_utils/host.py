# Copyright 2024, Itential Inc. All Rights Reserved

# GNU General Public License v3.0+ (see LICENSES/GPL-3.0-or-later.txt or https://www.gnu.org/licenses/gpl-3.0.txt)
# SPDX-License-Identifier: GPL-3.0-or-later


DOCUMENTATION = """
---
name: itential.http.host
author: Itential

short_description: Represents a remote HTTP host

description:
  - The `itential.http.host` represents an API service that can uses HTTP as
    the connection transport.

options:
  host:
    description:
      - The hostname or IP host used to connect to the remote host
    type: str
    required: true
    vars:
      - itential_host
      - ansible_host

  port:
    description:
      - The port used to connect to the remote host
    type: int
    vars:
      - itential_port
      - ansible_port
      - iap_port

  username:
    description:
      - The username to use when authenticating to the remote device
    type: str
    vars:
      - itential_http_user
      - itential_user
      - ansible_user
      - iap_username
      - iap_user

  password:
    description:
      - The password to use when authenticating to the remote device
    type: str
    vars:
      - itential_http_password
      - itential_password
      - ansible_password
      - iap_password
      - iap_pass

  iap_auth_token:
    description:
      - The authentication token to use for IAP requests (optional)
    type: str
    vars:
      - iap_auth_token

  use_tls:
    description:
      - Enable or disable the use of TLS for the connection
    type: bool
    default: true
    vars:
      - itential_http_use_tls

  headers:
    description:
      - The set of key/value pairs to include in the header on every request
    type: dict
    vars:
      - intential_http_headers

  base_path:
    description:
      - The API base path to prepend for every request
    type: str
    vars:
      - itential_http_base_path

  auth_type:
    description:
      - The HTTP authorization type to use
    type: str
    choices: [ "basic", "token" ]
    vars:
      - itential_http_auth_type

  verify:
    description:
      - Enable or disable the validataion of certificates when using TLS
    type: bool
    default: true
    vars:
      - itential_http_verify

  disable_warnings:
    description:
      - Enable or disable warning messages
    type: bool
    default: false
    vars:
      - itential_http_disable_warnings
"""
