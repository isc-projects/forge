# Copyright (C) 2025 Internet Systems Consortium, Inc. ("ISC")
#
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

"""Miscellaneous System/OS tests"""

import pytest

from src import srv_control
from src import misc

from src.forge_cfg import world
from src.softwaresupport.multi_server_functions import verify_file_permissions


@pytest.mark.v4
@pytest.mark.v6
@pytest.mark.logging
def test_pid_file_permissions(dhcp_version):
    """
    Test to check if Kea makes PID file with 640 permissions.
    :param dhcp_version: The DHCP version to use.
    :type dhcp_version: str
    """
    misc.test_setup()

    if dhcp_version == 'v4':
        srv_control.config_srv_subnet('192.168.50.0/24', '192.168.50.1-192.168.50.50')
    else:
        srv_control.config_srv_subnet('2001:db8:1::/64', '2001:db8:1::5-2001:db8:1::50')
        srv_control.config_srv_prefix('2001:db8:2::', 0, 90, 94)

    srv_control.build_and_send_config_files()
    srv_control.start_srv('DHCP', 'started')
    misc.test_procedure()

    assert verify_file_permissions(world.f_cfg.run_join(f'*dhcp{dhcp_version[1]}.pid'))
