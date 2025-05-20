# Copyright (C) 2025 Internet Systems Consortium.
#
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

# Author: Marcin Godzina

import os
import pytest

from src import misc
from src import srv_msg
from src import srv_control

from src.forge_cfg import world
from src.protosupport.multi_protocol_functions import log_contains, wait_for_message_in_log
from src.softwaresupport.multi_server_functions import verify_file_permissions, fabric_sudo_command


@pytest.mark.v4
@pytest.mark.v6
def test_leasefile_path_configfile(dhcp_version):
    """Test if Kea accepts correct lease file path.

    :param dhcp_version: DHCP version
    :type dhcp_version: str
    """

    illegal_paths = [
        ['', True, 'DHCPSRV_MEMFILE_LEASE_FILE_LOAD loading leases from file'],
        ['/tmp/', False, 'DHCPSRV_MEMFILE_FAILED_TO_OPEN Could not open lease file: invalid path specified:'],
        ['~/', False, 'DHCPSRV_MEMFILE_FAILED_TO_OPEN Could not open lease file: invalid path specified:'],
        ['/var/', False, 'DHCPSRV_MEMFILE_FAILED_TO_OPEN Could not open lease file: invalid path specified:'],
        ['/srv/', False, 'DHCPSRV_MEMFILE_FAILED_TO_OPEN Could not open lease file: invalid path specified:'],
        ['/etc/kea/', False, 'DHCPSRV_MEMFILE_FAILED_TO_OPEN Could not open lease file: invalid path specified:'],
    ]
    misc.test_setup()
    for path, should_succeed, message in illegal_paths:

        srv_msg.remove_file_from_server(path + 'leasefile.csv')

        if dhcp_version == 'v4':
            srv_control.config_srv_subnet('192.168.50.0/24', '192.168.50.1-192.168.50.50')
        else:
            srv_control.config_srv_subnet('2001:db8:1::/64', '2001:db8:1::5-2001:db8:1::50')

        srv_control.define_temporary_lease_db_backend('memfile')
        world.dhcp_cfg["lease-database"] = {"type": "memfile",
                                            "name": path + 'leasefile.csv',
                                            "lfc-interval": 5,
                                            }
        srv_control.build_and_send_config_files()
        srv_control.clear_some_data('logs')
        srv_control.start_srv('DHCP', 'started', should_succeed=should_succeed)

        misc.test_procedure()
        # Check if file is created and has proper permissions when legal path is used.
        if should_succeed:
            if path == '':
                path = os.path.dirname(world.f_cfg.get_leases_path())
            verify_file_permissions(os.path.join(path, 'leasefile.csv'))  # file may not exist yet
            if dhcp_version == 'v4':
                srv_msg.DORA('192.168.50.1')
            else:
                srv_msg.SARR('2001:db8:1::5')
            assert verify_file_permissions(os.path.join(path, 'leasefile.csv'))  # also confirm that file is created

            # Check if LFC is assiginig proper permissions to the file.
            wait_for_message_in_log("DHCPSRV_MEMFILE_LFC_EXECUTE")
            srv_msg.forge_sleep(1, 'seconds')
            assert verify_file_permissions(os.path.join(path, 'leasefile.csv'))
            assert verify_file_permissions(os.path.join(path, 'leasefile.csv.2'))

        log_contains(message)


@pytest.mark.v4
@pytest.mark.v6
def test_leasefile_path_config_set(dhcp_version):
    """Test if Kea accepts correct lease file path using config commands.

    :param dhcp_version: DHCP version
    :type dhcp_version: str
    """

    illegal_paths = [
        ['', 0, 'Configuration successful'],
        ['/tmp/', 1, 'Unable to open database: invalid path specified:'],
        ['~/', 1, 'Unable to open database: invalid path specified:'],
        ['/var/', 1, 'Unable to open database: invalid path specified:'],
        ['/srv/', 1, 'Unable to open database: invalid path specified:'],
        ['/etc/kea/', 1, 'Unable to open database: invalid path specified:'],
    ]
    misc.test_setup()

    if dhcp_version == 'v4':
        srv_control.config_srv_subnet('192.168.50.0/24', '192.168.50.1-192.168.50.50')
    else:
        srv_control.config_srv_subnet('2001:db8:1::/64', '2001:db8:1::5-2001:db8:1::50')

    srv_control.open_control_channel()
    srv_control.agent_control_channel()

    srv_control.build_and_send_config_files()
    srv_control.clear_some_data('logs')
    srv_control.start_srv('DHCP', 'started')

    # Get current config
    cmd = {"command": "config-get", "arguments": {}}
    response = srv_msg.send_ctrl_cmd(cmd, 'http')
    config_set = response['arguments']
    del config_set['hash']

    for path, exp_result, message in illegal_paths:
        full_path = os.path.join(path, 'leasefile.csv')
        srv_msg.remove_file_from_server(full_path)
        fabric_sudo_command(f'touch {full_path}')
        config_set[f"Dhcp{dhcp_version[1]}"]["lease-database"]['persist'] = True
        config_set[f"Dhcp{dhcp_version[1]}"]["lease-database"]['name'] = full_path
        cmd = {"command": "config-set", "arguments": config_set}
        resp = srv_msg.send_ctrl_cmd(cmd, 'http', exp_result=exp_result)
        assert message in resp['text'], f"Expected message: {message} not found in response: {resp['text']}"
        if exp_result == 0:
            verify_file_permissions(full_path)
