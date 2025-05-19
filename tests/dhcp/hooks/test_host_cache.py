# Copyright (C) 2025 Internet Systems Consortium, Inc. ("ISC")
#
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

"""Kea Host Cache Reservations hook"""

import pytest

from src import misc
from src import srv_control
from src import srv_msg
from src.forge_cfg import world
from src.softwaresupport.multi_server_functions import verify_file_permissions, fabric_is_file


# v4 disabled for time saving:
# @pytest.mark.v4
@pytest.mark.v6
@pytest.mark.legal_logging
def test_host_cache_path_config_set(dhcp_version):
    """
    Test to check if Kea writes host cache reservations to custom path.
    :param dhcp_version: The DHCP version to use.
    :type dhcp_version: str
    """
    misc.test_procedure()

    misc.test_setup()
    srv_control.set_time('renew-timer', 100)
    srv_control.set_time('rebind-timer', 200)
    srv_control.set_time('valid-lifetime', 600)
    if dhcp_version == 'v4':
        srv_control.config_srv_subnet('192.168.50.0/24', '192.168.50.1-192.168.50.50')
    else:
        srv_control.config_srv_subnet('2001:db8:1::/64', '2001:db8:1::5-2001:db8:1::50')

    srv_control.add_hooks('libdhcp_host_cache.so')
    # set custom name
    srv_control.add_parameter_to_hook("libdhcp_host_cache.so", 'maximum', '1000')

    srv_control.add_unix_socket()
    srv_control.add_http_control_channel()
    srv_control.build_and_send_config_files()
    srv_control.start_srv('DHCP', 'started')

    srv_msg.remove_file_from_server(world.f_cfg.data_join("kea-host-cache.json"))
    cmd = {"command": "cache-write", "arguments": world.f_cfg.data_join("kea-host-cache.json")}
    response = srv_msg.send_ctrl_cmd(cmd, 'http')
    # example response:
    # "0 entries dumped to '/home/usr/installed/keapriv/var/lib/kea/kea-host-cache.json'."
    verify_file_permissions(response['text'].split("'")[1])

    illegal_paths = [
        ['/tmp/kea-host-cache.json', 1, 'parameter is invalid: invalid path specified:'],
        ['~/kea-host-cache.json', 1, 'parameter is invalid: invalid path specified:'],
        ['/var/kea-host-cache.json', 1, 'parameter is invalid: invalid path specified:'],
        ['/srv/kea-host-cache.json', 1, 'parameter is invalid: invalid path specified:'],
        ['/etc/kea/kea-host-cache', 1, 'parameter is invalid: invalid path specified:'],
    ]

    for path, exp_result, exp_text in illegal_paths:
        srv_msg.remove_file_from_server(path)
        cmd = {"command": "cache-write", "arguments": path}
        response = srv_msg.send_ctrl_cmd(cmd, 'http', exp_result=exp_result)
        assert exp_text in response['text'], f"Expected {exp_text} in response, got {response['text']}"
        assert fabric_is_file(path) is False, f"File {path} should not exist"
