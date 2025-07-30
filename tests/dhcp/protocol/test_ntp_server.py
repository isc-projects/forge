# Copyright (C) 2025 Internet Systems Consortium, Inc. ("ISC")
#
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

"""Network Time Protocol (NTP) Server Option for DHCPv6"""

import pytest

from src import srv_control
from src import srv_msg
from src import misc
from src.forge_cfg import world
from src.protosupport.multi_protocol_functions import log_contains


@pytest.mark.v6
@pytest.mark.options
def test_v6_ntp():
    """
    Check if Kea return option Network Time Protocol as configured.
    """
    misc.test_setup()
    srv_control.config_srv_subnet(
        '2001:db8:a::/64', '2001:db8:a::1-2001:db8:a::10')

    option_data = [
        {
            "always-send": True,
            "code": 56,
            "name": "ntp-server",
            "space": "dhcp6"},
        {
            "space": "v6-ntp-server-suboptions",
            "name": "ntp-server-address",
            "data": "2001:db8:abcd::123"
        },
        {
            "space": "v6-ntp-server-suboptions",
            "name": "ntp-server-multicast",
            "data": "2001:db8:abcd::456"
        },
        {
            "space": "v6-ntp-server-suboptions",
            "name": "ntp-server-fqdn",
            "data": "ntp.example.com"
        }
    ]
    world.dhcp_cfg['option-data'] = option_data
    srv_control.build_and_send_config_files()
    srv_control.start_srv('DHCP', 'started')

    misc.test_procedure()
    srv_msg.client_does_include('Client', 'client-id')
    srv_msg.client_does_include('Client', 'IA-NA')
    srv_msg.client_requests_option(56)
    srv_msg.client_send_msg('SOLICIT')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', 'ADVERTISE')
    srv_msg.response_check_count_option(56, 3)
    srv_msg.response_check_suboption_content(1, 56, 'addr', '2001:db8:abcd::123')
    srv_msg.response_check_suboption_content(2, 56, 'addr', '2001:db8:abcd::456')
    srv_msg.response_check_suboption_content(3, 56, 'fqdn', 'ntp.example.com.')

    misc.test_procedure()
    srv_msg.client_copy_option('server-id')
    srv_msg.client_copy_option('IA_NA')
    srv_msg.client_does_include('Client', 'client-id')
    srv_msg.client_requests_option(56)
    srv_msg.client_send_msg('REQUEST')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', 'REPLY')
    srv_msg.response_check_count_option(56, 3)
    srv_msg.response_check_suboption_content(1, 56, 'addr', '2001:db8:abcd::123')
    srv_msg.response_check_suboption_content(2, 56, 'addr', '2001:db8:abcd::456')
    srv_msg.response_check_suboption_content(3, 56, 'fqdn', 'ntp.example.com.')


@pytest.mark.v6
@pytest.mark.options
def test_v6_ntp_negative():
    """
    Check if Kea discards wrong configuration.
    """
    option_data_template = [{
        "always-send": True,
        "code": 56,
        "name": "ntp-server",
        "space": "dhcp6"}]

    test_cases = [
        {'option_data': {
            "space": "v6-ntp-server-suboptions",
            "name": "ntp-server",
            "data": "2001:db8:abcd::123"
        },
            'log_message': 'definition for the option \'v6-ntp-server-suboptions.ntp-server\' '
            'having code \'0\' does not exist'
        },
        {'option_data': {
            "space": "v6-ntp-server-suboptions",
            "name": "ntp-server-address",
            "data": "lorem ipsum"
        },
            'log_message': 'Failed to convert string to address \'lorem ipsum\': Invalid argument'
        },
        {'option_data': {
            "space": "v6-ntp-server-suboptions",
            "name": "ntp-server-address",
            "data": ""
        },
            'log_message': 'Failed to convert string to address \'\': Invalid argument'
        }
    ]

    for test_case in test_cases:
        ic(test_case)
        srv_control.clear_some_data('logs')
        misc.test_setup()
        srv_control.config_srv_subnet(
            '2001:db8:a::/64', '2001:db8:a::1-2001:db8:a::10')
        ic(world.dhcp_cfg['option-data'])
        ic(option_data_template)
        world.dhcp_cfg['option-data'] = option_data_template
        ic(world.dhcp_cfg['option-data'])
        world.dhcp_cfg['option-data'].append(test_case['option_data'])
        srv_control.build_and_send_config_files()
        srv_control.start_srv('DHCP', 'started', should_succeed=False)

        misc.pass_criteria()
        log_contains(test_case['log_message'])
