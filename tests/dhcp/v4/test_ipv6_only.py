# Copyright (C) 2023 Internet Systems Consortium, Inc. ("ISC")
#
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

"""DHCPv4 IPv6-only-preferred option tests"""

import pytest

from src import misc
from src import srv_control
from src import srv_msg

from src.forge_cfg import world


@pytest.mark.v4
@pytest.mark.options
def test_ipv6_only_preferred():
    """
    Basic test to verify IPv6-only-preferred option
    """
    misc.test_setup()
    srv_control.config_srv_subnet('192.168.50.0/24', '192.168.50.1-192.168.50.10')

    option = {"name": "v6-only-preferred", "data": "1800"}
    world.dhcp_cfg["option-data"].append(option)

    srv_control.build_and_send_config_files()
    srv_control.start_srv('DHCP', 'started')

    # Verify that option 108 is NOT returned if not requested.
    misc.test_procedure()
    srv_msg.client_sets_value('Client', 'chaddr', '00:00:00:00:00:22')
    srv_msg.client_does_include_with_value('client_id', 'ff:01:02:03:ff:04:f1:f2')
    srv_msg.client_send_msg('DISCOVER')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', 'OFFER')
    srv_msg.response_check_content('yiaddr', '192.168.50.1')
    srv_msg.response_check_include_option(108, expect_include=False)

    misc.test_procedure()
    srv_msg.client_copy_option('server_id')
    srv_msg.client_sets_value('Client', 'chaddr', '00:00:00:00:00:22')
    srv_msg.client_does_include_with_value('client_id', 'ff:01:02:03:ff:04:f1:f2')
    srv_msg.client_does_include_with_value('requested_addr', '192.168.50.1')
    srv_msg.client_requests_option(1)
    srv_msg.client_send_msg('REQUEST')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', 'ACK')
    srv_msg.response_check_include_option(108, expect_include=False)
    srv_msg.response_check_content('yiaddr', '192.168.50.1')
    srv_msg.response_check_include_option(1)
    srv_msg.response_check_option_content(1, 'value', '255.255.255.0')

    # Verify that option 108 IS returned if not requested.
    misc.test_procedure()
    srv_msg.client_sets_value('Client', 'chaddr', '00:00:00:00:00:33')
    srv_msg.client_does_include_with_value('client_id', 'ff:01:02:03:ff:04:f1:f3')
    srv_msg.client_requests_option(108)
    srv_msg.client_send_msg('DISCOVER')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', 'OFFER')
    srv_msg.response_check_content('yiaddr', '192.168.50.2')
    srv_msg.response_check_include_option(108)
    srv_msg.response_check_option_content(108, 'value', '1800')

    misc.test_procedure()
    srv_msg.client_copy_option('server_id')
    srv_msg.client_sets_value('Client', 'chaddr', '00:00:00:00:00:33')
    srv_msg.client_does_include_with_value('client_id', 'ff:01:02:03:ff:04:f1:f3')
    srv_msg.client_does_include_with_value('requested_addr', '192.168.50.2')
    srv_msg.client_requests_option(108)
    srv_msg.client_requests_option(1)
    srv_msg.client_send_msg('REQUEST')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', 'ACK')
    srv_msg.response_check_include_option(108)
    srv_msg.response_check_option_content(108, 'value', '1800')
    srv_msg.response_check_content('yiaddr', '192.168.50.2')
    srv_msg.response_check_include_option(1)
    srv_msg.response_check_option_content(1, 'value', '255.255.255.0')
