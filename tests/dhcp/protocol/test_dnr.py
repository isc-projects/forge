# Copyright (C) 2023 Internet Systems Consortium, Inc. ("ISC")
#
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

"""DHCP Option for the Discovery of Network-designated Resolvers"""

import pytest

from src import srv_control
from src import srv_msg
from src import misc


@pytest.mark.v4
@pytest.mark.options
def test_v4_dnr():
    """
    Check if Kea return option Discovery of Network-designated Resolvers (162, DNR) as configured.
    Using example from documentation.
    """
    misc.test_setup()
    srv_control.config_srv_subnet('192.168.50.0/24', '192.168.50.50-192.168.50.50')
    srv_control.config_srv_opt('v4-dnr', '2, '
                               'example.some.host.org., '
                               '10.0.5.6, '
                               'alpn=dot\\,doq port=8530')
    srv_control.build_and_send_config_files()
    srv_control.start_srv('DHCP', 'started')

    misc.test_procedure()
    srv_msg.client_sets_value('Client', 'chaddr', 'ff:01:02:03:ff:04')
    srv_msg.client_requests_option(162)
    srv_msg.client_does_include_with_value('client_id', 'ff:01:02:03:ff:04:11:22')
    srv_msg.client_send_msg('DISCOVER')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', 'OFFER')
    srv_msg.response_check_include_option(162)
    srv_msg.response_check_option_content(162, 'value',
                                          b'\x001\x00\x02\x17\x07example\x04some\x04host\x03org\x00\x04\n\x00'
                                          b'\x05\x06\x00\x01\x00\x08\x03dot\x03doq\x00\x03\x00\x02!R')

    misc.test_procedure()
    srv_msg.client_copy_option('server_id')
    srv_msg.client_does_include_with_value('requested_addr', '192.168.50.50')
    srv_msg.client_requests_option(162)
    srv_msg.client_send_msg('REQUEST')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', 'ACK')
    srv_msg.response_check_content('yiaddr', '192.168.50.50')
    srv_msg.response_check_include_option(162)
    srv_msg.response_check_option_content(162, 'value',
                                          b'\x001\x00\x02\x17\x07example\x04some\x04host\x03org\x00\x04\n\x00'
                                          b'\x05\x06\x00\x01\x00\x08\x03dot\x03doq\x00\x03\x00\x02!R')


@pytest.mark.v6
@pytest.mark.options
def test_v6_dnr():
    """
    Check if Kea return option Discovery of Network-designated Resolvers (144, DNR) as configured.
    Using example from documentation.
    """
    misc.test_setup()
    srv_control.config_srv_subnet('2001:db8:a::/64', '2001:db8:a::1-2001:db8:a::10')
    srv_control.config_srv_opt('v6-dnr', '100, foo.org., 2001:db8::1 2001:db8::2, alpn=dot port=8530')

    srv_control.build_and_send_config_files()
    srv_control.start_srv('DHCP', 'started')

    misc.test_procedure()
    srv_msg.client_does_include('Client', 'client-id')
    srv_msg.client_does_include('Client', 'IA-NA')
    srv_msg.client_requests_option(144)
    srv_msg.client_send_msg('SOLICIT')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', 'ADVERTISE')
    srv_msg.response_check_include_option(144)
    srv_msg.response_check_option_content(144, 'optlen', 61)
    srv_msg.response_check_option_content(144, 'servicepriority', 100)
    srv_msg.response_check_option_content(144, 'adnlen', 9)
    srv_msg.response_check_option_content(144, 'adn', 'foo.org.')
    srv_msg.response_check_option_content(144, 'addrslen', 32)
    srv_msg.response_check_option_content(144, 'addrs', '2001:db8::1,2001:db8::2')
    srv_msg.response_check_option_content(144, 'svcparams', '0001000403646f74000300022152')

    misc.test_procedure()
    srv_msg.client_copy_option('server-id')
    srv_msg.client_copy_option('IA_NA')
    srv_msg.client_does_include('Client', 'client-id')
    srv_msg.client_requests_option(144)
    srv_msg.client_send_msg('REQUEST')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', 'REPLY')
    srv_msg.response_check_include_option(144)
    srv_msg.response_check_option_content(144, 'optlen', 61)
    srv_msg.response_check_option_content(144, 'servicepriority', 100)
    srv_msg.response_check_option_content(144, 'adnlen', 9)
    srv_msg.response_check_option_content(144, 'adn', 'foo.org.')
    srv_msg.response_check_option_content(144, 'addrslen', 32)
    srv_msg.response_check_option_content(144, 'addrs', '2001:db8::1,2001:db8::2')
    srv_msg.response_check_option_content(144, 'svcparams', '0001000403646f74000300022152')
