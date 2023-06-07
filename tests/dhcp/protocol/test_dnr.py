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
    srv_control.config_srv_opt('v4-dnr', '54, 3234, 23, example.some.host.org., '
                                         '08 c0 a8 00 01 c0 a8 00 02 6b 65 79 31 3d 76 61 6c 31 20 6b 65 79 32 3d 76 '
                                         '61 6c 32 00 34 10 e1 15 07 6D 79 68 6F 73 74 31 07 65 78 61 6D 70 6C 65 03 '
                                         '63 6F 6D 00 08 c0 a9 00 01 c0 a9 00 02 6b 65 79 33 3d 76 61 6c 33 20 6b 65 '
                                         '79 34 3d 76 61 6c 34')
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
    srv_msg.response_check_option_content(162, 'value', 'HEX:00360CA217076578616D706C6504736F6D6504686F7374036F72670008'
                                                        'C0A80001C0A800026B6579313D76616C31206B6579323D76616C32003410E1'
                                                        '15076D79686F737431076578616D706C6503636F6D0008C0A90001C0A90002'
                                                        '6B6579333D76616C33206B6579343D76616C34')

    misc.test_procedure()
    srv_msg.client_copy_option('server_id')
    srv_msg.client_does_include_with_value('requested_addr', '192.168.50.50')
    srv_msg.client_requests_option(162)
    srv_msg.client_send_msg('REQUEST')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', 'ACK')
    srv_msg.response_check_content('yiaddr', '192.168.50.50')
    srv_msg.response_check_include_option(162)
    srv_msg.response_check_option_content(162, 'value', 'HEX:00360CA217076578616D706C6504736F6D6504686F7374036F72670008'
                                                        'C0A80001C0A800026B6579313D76616C31206B6579323D76616C32003410E1'
                                                        '15076D79686F737431076578616D706C6503636F6D0008C0A90001C0A90002'
                                                        '6B6579333D76616C33206B6579343D76616C34')


@pytest.mark.v6
@pytest.mark.options
def test_v6_dnr():
    """
    Check if Kea return option Discovery of Network-designated Resolvers (144, DNR) as configured.
    Using example from documentation.
    """
    misc.test_setup()
    srv_control.config_srv_subnet('2001:db8:a::/64', '2001:db8:a::1-2001:db8:a::10')
    srv_control.config_srv_opt('v6-dnr', '3234, 23, example.some.host.org., 00 20 20 01 0d b8 00 01 00 00 00 00 00 00 '
                                         'de ad be ef ff 02 00 00 00 00 00 00 00 00 00 00 fa ce b0 0c 6b 65 79 31 3d '
                                         '76 61 6c 31 20 6b 65 79 32 3d 76 61 6c 32')

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
    srv_msg.response_check_option_content(144, 'svcprio', 3234)
    srv_msg.response_check_option_content(144, 'adnlen', 23)
    srv_msg.response_check_option_content(144, 'adn', 'example.some.host.org.')
    srv_msg.response_check_option_content(144, 'address', '2001:db8:1::dead:beef,ff02::face:b00c')
    srv_msg.response_check_option_content(144, 'svcparams', 'key1=val1 key2=val2')

    misc.test_procedure()
    srv_msg.client_copy_option('server-id')
    srv_msg.client_copy_option('IA_NA')
    srv_msg.client_does_include('Client', 'client-id')
    srv_msg.client_requests_option(144)
    srv_msg.client_send_msg('REQUEST')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', 'REPLY')
    srv_msg.response_check_include_option(144)
    srv_msg.response_check_include_option(144)
    srv_msg.response_check_option_content(144, 'svcprio', 3234)
    srv_msg.response_check_option_content(144, 'adnlen', 23)
    srv_msg.response_check_option_content(144, 'adn', 'example.some.host.org.')
    srv_msg.response_check_option_content(144, 'address', '2001:db8:1::dead:beef,ff02::face:b00c')
    srv_msg.response_check_option_content(144, 'svcparams', 'key1=val1 key2=val2')
