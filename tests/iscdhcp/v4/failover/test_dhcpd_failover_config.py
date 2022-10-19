# Copyright (C) 2022 Internet Systems Consortium, Inc. ("ISC")
#
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

"""ISC_DHCP DHCPv4 Failover Configuration"""

# pylint: disable=invalid-name,line-too-long

import pytest

from src import misc
from src import srv_control

from src.protosupport.multi_protocol_functions import log_contains
from src.protosupport.multi_protocol_functions import wait_for_message_in_log
from src.softwaresupport.isc_dhcp6_server.functions import build_log_path, add_line_in_global


@pytest.mark.v4
@pytest.mark.dhcpd
@pytest.mark.disabled
def test_v4_dhcpd_failover_sanity_check_good_config():
    """new-v4.dhcpd.failover.sanity_check.good_config"""
    wait_for_message_in_log('Pool threshold reset', count=1, log_file=build_log_path())
    # Verifies that failover config for two peers passes
    wait_for_message_in_log('Pool threshold reset', count=1, log_file=build_log_path())
    # sanity checking
    wait_for_message_in_log('Pool threshold reset', count=1, log_file=build_log_path())
    # #
    misc.test_setup()
    add_line_in_global(' failover peer "fonet" {')
    add_line_in_global('     primary;')
    add_line_in_global('     address 175.16.1.30;')
    add_line_in_global('     port 519;')
    add_line_in_global('     peer address 175.16.1.30;')
    add_line_in_global('     peer port 520;')
    add_line_in_global('     mclt 30;')
    add_line_in_global('     split 128;')
    add_line_in_global('     load balance max seconds 2;')
    add_line_in_global(' }')
    add_line_in_global(' failover peer "beebonet" {')
    add_line_in_global('     primary;')
    add_line_in_global('     address 175.16.1.30;')
    add_line_in_global('     port 521;')
    add_line_in_global('     peer address 175.16.1.30;')
    add_line_in_global('     peer port 522;')
    add_line_in_global('     mclt 30;')
    add_line_in_global('     split 128;')
    add_line_in_global('     load balance max seconds 2;')
    add_line_in_global(' }')
    add_line_in_global(' subnet 192.168.50.0 netmask 255.255.255.0 {')
    add_line_in_global('     pool {')
    add_line_in_global('       failover peer "fonet";')
    add_line_in_global('       range 192.168.50.50 192.168.50.50;')
    add_line_in_global('     }')
    add_line_in_global('     pool {')
    add_line_in_global('       failover peer "beebonet";')
    add_line_in_global('       range 192.168.50.150 192.168.50.200;')
    add_line_in_global('     }')
    add_line_in_global(' }')
    srv_control.build_and_send_config_files()
    srv_control.start_srv('DHCP', 'started')

    # No steps required
    misc.test_procedure()

    misc.pass_criteria()
    log_contains('failover peer fonet: I move from recover to startup',
                 log_file=build_log_path())
    log_contains('failover peer beebonet: I move from recover to startup',
                 log_file=build_log_path())
