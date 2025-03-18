# Copyright 2024, Itential Inc. All Rights Reserved

# GNU General Public License v3.0+ (see LICENSES/GPL-3.0-or-later.txt or https://www.gnu.org/licenses/gpl-3.0.txt)
# SPDX-License-Identifier: GPL-3.0-or-later

import json
from ansible.errors import AnsibleError
from ansible_collections.itential.core.plugins.module_utils import display
from ansible_collections.itential.core.plugins.module_utils import http

def login(host):
    if not host.username or not host.password:
        raise AnsibleError("missing required property: username or password")

    user = {
        "username": host.username,
        "password": host.password,
    }

    headers = host.headers or {}
    headers.update({
        "content-type": "application/json",
        "accept": "application/json"
    })

    url = http.make_url(host.host, "/login", port=host.port, use_tls=host.use_tls)

    data = json.dumps({"user": user}).encode("utf-8")
    display.v(f"Request URL: {url}")
    display.v(type(data))

    try:
        resp = http.send_request(
            method="POST",
            url=url,
            headers=headers,
            data=data,
            verify=host.verify,
            disable_warnings=host.disable_warnings,
        )
        if resp.status_code != 200:
            raise AnsibleError(f"Unexpected HTTP status code in response: {resp.status_code} {resp.text}")
    except Exception as exc:
        raise AnsibleError(f"HTTP request failed: {str(exc)}")

    return resp.text
