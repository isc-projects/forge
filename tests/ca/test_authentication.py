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
from src.protosupport.multi_protocol_functions import fabric_sudo_command

# pylint: disable=unused-argument


def create_user_and_passowrd_file(user, password):
    """create_user_and_passowrd_file Create a user and password file
    for the RBAC tests that are using basic authentication.
    Usulally basic authentication uses one file with username
    and password. Let's use separate files for each user in those tests.

    :param user: The user to create in the file
    :type user: str
    :param password: The password to use
    :type password: str
    """
    fabric_sudo_command(f'echo "{user}" > {os.path.join(world.f_cfg.get_share_path(), "kea-creds-tmp", user)}',
                        hide_all=not world.f_cfg.forge_verbose)
    fabric_sudo_command(f'echo "{password}" > {os.path.join(world.f_cfg.get_share_path(),
                        "kea-creds-tmp", f"{user}_password")}',
                        hide_all=not world.f_cfg.forge_verbose)

    if world.f_cfg.install_method != 'make':
        if world.server_system in ['alpine', 'redhat', 'fedora']:
            fabric_sudo_command(f'chown -R kea:kea {os.path.join(world.f_cfg.get_share_path(), "kea-creds-tmp")}',
                                hide_all=not world.f_cfg.forge_verbose)
        else:
            fabric_sudo_command(f'chown -R _kea:_kea {os.path.join(world.f_cfg.get_share_path(), "kea-creds-tmp")}',
                                hide_all=not world.f_cfg.forge_verbose)


# fixture to remove authentication files after the test
@pytest.fixture()
def remove_authentication_files():
    """remove_authentication_files Remove authentication files after the test.
    This fixture is used to create authentiaction directory and files before the test.
    It is used to avoid conflicts with other tests.
    """
    fabric_sudo_command(f'mkdir -m 750 -p {os.path.join(world.f_cfg.get_share_path(), "kea-creds-tmp")}',
                        hide_all=not world.f_cfg.forge_verbose)
    yield
    fabric_sudo_command(f'rm -rf {os.path.join(world.f_cfg.get_share_path(), "kea-creds-tmp")}',
                        hide_all=not world.f_cfg.forge_verbose)


@pytest.mark.usefixtures('remove_authentication_files')
@pytest.mark.v6
@pytest.mark.v4
def test_ca_basic_authentication(dhcp_version):
    """Test basic authentication.

    :param dhcp_version: DHCP version
    :type dhcp_version: str
    """
    misc.test_setup()
    srv_control.add_unix_socket()
    create_user_and_passowrd_file("admin", "p@ssw0rd")
    auth = {
        "authentication": {
            "type": "basic",
            "directory": os.path.join(world.f_cfg.get_share_path(), "kea-creds-tmp"),
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
