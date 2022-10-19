# Copyright (C) 2022 Internet Systems Consortium, Inc. ("ISC")
#
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

"""ISC_DHCP DHCPv6 Keywords"""

# pylint: disable=invalid-name,line-too-long

import pytest
from src import misc
from src import srv_control
from src import srv_msg

from src.softwaresupport.isc_dhcp6_server.functions import add_line_in_global


@pytest.mark.v6
@pytest.mark.dhcpd
def test_v6_dhcpd_keyword_server_duid_ll():
    """new-v6.dhcpd.keyword.server-duid-ll"""
    # Testing server-duid LL
    # #
    # Message details 		Client		Server
    # 						SOLICIT -->
    # 		   						<--	ADVERTISE
    # Pass Criteria:
    # #
    # server DUID matches the configured LL value
    # #
    misc.test_setup()
    srv_control.config_srv_subnet('2001:db8:1::/64', '2001:db8:1::1-2001:db8:1::2')
    add_line_in_global('server-duid LL ethernet 00:16:6f:49:7d:9b;')
    srv_control.build_and_send_config_files()
    srv_control.start_srv('DHCP', 'started')

    misc.test_procedure()
    srv_msg.client_does_include('Client', 'client-id')
    srv_msg.client_does_include('Client', 'IA_Address')
    srv_msg.client_does_include('Client', 'IA-NA')
    srv_msg.client_send_msg('SOLICIT')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', 'ADVERTISE')
    srv_msg.response_check_include_option(2)
    # Response option 2 must contain duid 00:03:00:01:00:16:6f:49:7d:9b;
    srv_msg.response_check_include_option(3)
    srv_msg.response_check_option_content(3, 'sub-option', 5)


@pytest.mark.v6
@pytest.mark.dhcpd
def test_v6_dhcpd_keyword_server_duid_llt():
    """new-v6.dhcpd.keyword.server-duid-llt"""
    # Testing server-duid LLT
    # #
    # Message details 		Client		Server
    # 						SOLICIT -->
    # 		   						<--	ADVERTISE
    # Pass Criteria:
    # #
    # server DUID matches the configured LLT value
    # #
    misc.test_setup()
    srv_control.config_srv_subnet('2001:db8:1::/64', '2001:db8:1::1-2001:db8:1::2')
    add_line_in_global('server-duid LLT ethernet 9999 00:16:6f:49:7d:9b;')
    srv_control.build_and_send_config_files()
    srv_control.start_srv('DHCP', 'started')

    misc.test_procedure()
    srv_msg.client_does_include('Client', 'client-id')
    srv_msg.client_does_include('Client', 'IA_Address')
    srv_msg.client_does_include('Client', 'IA-NA')
    srv_msg.client_send_msg('SOLICIT')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', 'ADVERTISE')
    srv_msg.response_check_include_option(2)
    # Response option 2 must contain duid 00:01:00:01:27:0f:00:16:6f:49:7d:9b;
    srv_msg.response_check_include_option(3)
    srv_msg.response_check_option_content(3, 'sub-option', 5)


@pytest.mark.v6
@pytest.mark.dhcpd
def test_v6_dhcpd_keyword_server_duid_en():
    """new-v6.dhcpd.keyword.server-duid-en"""
    # Testing server-duid EN
    # #
    # Message details 		Client		Server
    # 						SOLICIT -->
    # 		   						<--	ADVERTISE
    # Pass Criteria:
    # #
    # server DUID matches the configured EN value
    # #
    misc.test_setup()
    srv_control.config_srv_subnet('2001:db8:1::/64', '2001:db8:1::1-2001:db8:1::2')
    add_line_in_global('server-duid EN 2495 "peter-pan";')
    srv_control.build_and_send_config_files()
    srv_control.start_srv('DHCP', 'started')

    misc.test_procedure()
    srv_msg.client_does_include('Client', 'client-id')
    srv_msg.client_does_include('Client', 'IA_Address')
    srv_msg.client_does_include('Client', 'IA-NA')
    srv_msg.client_send_msg('SOLICIT')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', 'ADVERTISE')
    srv_msg.response_check_include_option(2)
    # Response option 2 must contain duid 00022495peter-pan.
    srv_msg.response_check_include_option(3)
    srv_msg.response_check_option_content(3, 'sub-option', 5)
