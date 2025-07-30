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
    # Static part of option data configuration.
    option_data_template = [{
        "always-send": True,
        "code": 56,
        "name": "ntp-server",
        "space": "dhcp6"}]

    # Test cases of wrong configuration with expected error message.
    test_cases = [
        {  # wrong option name
            'option_data': {
                "space": "v6-ntp-server-suboptions",
                "name": "ntp-server",
                "data": "2001:db8:abcd::123"
            },
            'log_message': 'definition for the option \'v6-ntp-server-suboptions.ntp-server\' '
            'having code \'0\' does not exist'
        },
        {  # wrong address in ntp-server-address
            'option_data': {
                "space": "v6-ntp-server-suboptions",
                "name": "ntp-server-address",
                "data": "lorem ipsum"
            },
            'log_message': 'Failed to convert string to address \'lorem ipsum\': Invalid argument'
        },
        {  # empty address in ntp-server-address
            'option_data': {
                "space": "v6-ntp-server-suboptions",
                "name": "ntp-server-address",
                "data": ""
            },
            'log_message': 'option data does not match option definition '
            '(space: v6-ntp-server-suboptions, code: 1): no option value specified'
        },
        {  # wrong address in ntp-server-address
            'option_data': {
                "space": "v6-ntp-server-suboptions",
                "name": "ntp-server-address",
                "data": "2001:db8::abcd::123"
            },
            'log_message': 'Failed to convert string to address \'2001:db8::abcd::123\': Invalid argument'
        },
        {  # wrong address in ntp-server-multicast
            'option_data': {
                "space": "v6-ntp-server-suboptions",
                "name": "ntp-server-multicast",
                "data": "lorem ipsum"
            },
            'log_message': 'Failed to convert string to address \'lorem ipsum\': Invalid argument'
        },
        {  # empty address in ntp-server-multicast
            'option_data': {
                "space": "v6-ntp-server-suboptions",
                "name": "ntp-server-multicast",
                "data": ""
            },
            'log_message': 'option data does not match option definition '
            '(space: v6-ntp-server-suboptions, code: 2): no option value specified'
        },
        {  # wrong address in ntp-server-multicast
            'option_data': {
                "space": "v6-ntp-server-suboptions",
                "name": "ntp-server-multicast",
                "data": "2001:db8::abcd::123"
            },
            'log_message': 'Failed to convert string to address \'2001:db8::abcd::123\': Invalid argument'
        },
        {  # wrong fqdn in ntp-server-fqdn
            'option_data': {
                "space": "v6-ntp-server-suboptions",
                "name": "ntp-server-fqdn",
                "data": "lorem ipsum"
            },
            'log_message': 'option data does not match option definition '
            '(space: v6-ntp-server-suboptions, code: 3): option buffer truncated'
        },
        {  # empty address in ntp-server-fqdn
            'option_data': {
                "space": "v6-ntp-server-suboptions",
                "name": "ntp-server-fqdn",
                "data": ""
            },
            'log_message': 'option data does not match option definition '
            '(space: v6-ntp-server-suboptions, code: 3): no option value specified'
        }
    ]

    for test_case in test_cases:
        # Clear logs and setup test environment.
        srv_control.clear_some_data('logs')
        misc.test_setup()
        srv_control.config_srv_subnet('2001:db8:a::/64', '2001:db8:a::1-2001:db8:a::10')

        # Add static option data to the configuration.
        world.dhcp_cfg['option-data'] = option_data_template.copy()
        # Add test case specific option data to the configuration.
        world.dhcp_cfg['option-data'].append(test_case['option_data'])
        # Print test case in green for debugging.
        print(f'\033[92mOption test case: {test_case["option_data"]}\033[0m')

        srv_control.build_and_send_config_files()
        srv_control.start_srv('DHCP', 'started', should_succeed=False)

        misc.pass_criteria()
        log_contains(test_case['log_message'])
