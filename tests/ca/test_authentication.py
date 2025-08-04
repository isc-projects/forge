# Copyright (C) 2022-2025 Internet Systems Consortium.
#
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

"""Kea Control channel TLS connection tests"""

from base64 import b64encode

import os
import pytest

from src import misc
from src import srv_msg
from src import srv_control
from src.forge_cfg import world

# pylint: disable=unused-argument


@pytest.mark.v6
@pytest.mark.v4
def test_ca_basic_authentication(dhcp_version):
    """Test basic authentication.

    :param dhcp_version: DHCP version
    :type dhcp_version: str
    """
    misc.test_setup()
    srv_control.add_unix_socket()
    srv_control.create_user_and_password_file("admin", "p@ssw0rd")
    auth = {
        "authentication": {
            "type": "basic",
            "directory": os.path.join(world.f_cfg.get_share_path(), "kea-creds"),
            "clients": [
                {
                    "user-file": "admin",
                    "password-file": "admin_password"
                }
            ]
        }}
    if world.f_cfg.control_agent:
        srv_control.add_http_control_channel()
        world.ca_cfg["Control-agent"].update(auth)
    else:
        srv_control.add_http_control_channel(auth=auth)

    srv_control.build_and_send_config_files()
    srv_control.start_srv('DHCP', 'started')

    cmd = {"command": "config-get", "arguments": {}}

    headers = {'Authorization': f'Basic {b64encode(b"admin:p@ssw0rd").decode("ascii")}'}
    srv_msg.send_ctrl_cmd(cmd, 'http', headers=headers)

    # password with extra character at the end
    headers = {'Authorization': f'Basic {b64encode(b"admin:p@ssw0rd5").decode("ascii")}'}
    resp = srv_msg.send_ctrl_cmd(cmd, 'http', headers=headers, exp_result=401)
    assert resp["text"] == "Unauthorized", f"Expected text is not 'Unauthorized' it's {resp['text']}"

    # password with extra character at the beginning
    headers = {'Authorization': f'Basic {b64encode(b"admin:5p@ssw0rd").decode("ascii")}'}
    resp = srv_msg.send_ctrl_cmd(cmd, 'http', headers=headers, exp_result=401)
    assert resp["text"] == "Unauthorized", f"Expected text is not 'Unauthorized' it's {resp['text']}"

    # wrong username
    headers = {'Authorization': f'Basic {b64encode(b"asdmin:p@ssw0rd").decode("ascii")}'}
    resp = srv_msg.send_ctrl_cmd(cmd, 'http', headers=headers, exp_result=401)
    assert resp["text"] == "Unauthorized", f"Expected text is not 'Unauthorized' it's {resp['text']}"

    # huge data set in auth header
    headers = {'Authorization': f'Basic {b64encode(b"admin:p@ssw0rd"*5000000).decode("ascii")}'}
    resp = srv_msg.send_ctrl_cmd(cmd, 'http', headers=headers, exp_result=401)
    assert resp["text"] == "Unauthorized", f"Expected text is not 'Unauthorized' it's {resp['text']}"

    if world.f_cfg.control_agent:
        headers = {'Authorization': f'Basic {b64encode(b"admin:p@ssw0rd").decode("ascii")}'}
        resp = srv_msg.send_ctrl_cmd(cmd, 'http', service='agent', headers=headers)

        headers = {'Authorization': f'Basic {b64encode(b"admin:p@ssw0rd"*5000000).decode("ascii")}'}
        resp = srv_msg.send_ctrl_cmd(cmd, 'http', service='agent', headers=headers, exp_result=401)
        assert resp["text"] == "Unauthorized", f"Expected text is not 'Unauthorized' it's {resp['text']}"

    # let's make sure that control channel is still working
    headers = {'Authorization': f'Basic {b64encode(b"admin:p@ssw0rd").decode("ascii")}'}
    srv_msg.send_ctrl_cmd(cmd, 'http', headers=headers)
