# Copyright (C) 2022-2024 Internet Systems Consortium.
#
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

"""Kea Control channel TLS connection tests"""

from base64 import b64encode

import pytest

from src import misc
from src import srv_msg
from src import srv_control
from src.forge_cfg import world


@pytest.mark.v4
def test_ca_basic_authentication():
    misc.test_setup()
    srv_control.add_unix_socket()
    srv_control.add_http_control_channel()
    auth = {
        "authentication": {
            "type": "basic",
            "clients":
            [
                {
                    "comment": "admin is authorized",
                    "user": "admin",
                    "password": "1234"
                }
            ]
        }}
    if world.f_cfg.control_agent:
        world.ca_cfg["Control-agent"].update(auth)
    else:
        world.dhcp_cfg.update(auth)

    srv_control.build_and_send_config_files()
    srv_control.start_srv('DHCP', 'started')

    cmd = {"command": "config-get", "arguments": {}}

    headers = {'Authorization': f'Basic {b64encode(b"admin:1234").decode("ascii")}'}
    resp = srv_msg.send_ctrl_cmd(cmd, 'http', headers=headers)

    headers = {'Authorization': f'Basic {b64encode(b"admin:12345").decode("ascii")}'}
    resp = srv_msg.send_ctrl_cmd(cmd, 'http', headers=headers, exp_result=401)
    assert resp["text"] == "Unauthorized", f"Expected text is not 'Unauthorized' it's {resp['text']}"

    headers = {'Authorization': f'Basic {b64encode(b"asdmin:1234").decode("ascii")}'}
    resp = srv_msg.send_ctrl_cmd(cmd, 'http', headers=headers, exp_result=401)
    assert resp["text"] == "Unauthorized", f"Expected text is not 'Unauthorized' it's {resp['text']}"

    headers = {'Authorization': f'Basic {b64encode(b"admin:1234").decode("ascii")}'}
    resp = srv_msg.send_ctrl_cmd(cmd, 'http', service='agent', headers=headers)

    headers = {'Authorization': f'Basic {b64encode(b"admin:1234"*10000000).decode("ascii")}'}
    resp = srv_msg.send_ctrl_cmd(cmd, 'http', service='agent', headers=headers, exp_result=401)
    assert resp["text"] == "Unauthorized", f"Expected text is not 'Unauthorized' it's {resp['text']}"
