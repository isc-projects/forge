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


def _check_ipv6_only_response(ip_address, client, send108, expect_include, send_rapid_commit=False):
    """
    Function makes DORA exchange with IPv6-only-preferred request and checks server response.
    """
    misc.test_procedure()
    srv_msg.client_sets_value('Client', 'chaddr', f'00:00:00:00:00:{client}')
    if send108:
        srv_msg.client_requests_option(108)
    if send_rapid_commit:
        srv_msg.client_does_include_with_value('rapid-commit', '')
    srv_msg.client_send_msg('DISCOVER')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', 'OFFER')
    srv_msg.response_check_content('yiaddr', ip_address)
    srv_msg.response_check_include_option(108, expect_include=expect_include)
    if expect_include:
        srv_msg.response_check_option_content(108, 'value', '1800')

    misc.test_procedure()
    srv_msg.client_copy_option('server_id')
    srv_msg.client_sets_value('Client', 'chaddr', f'00:00:00:00:00:{client}')
    srv_msg.client_does_include_with_value('requested_addr', ip_address)
    if send108:
        srv_msg.client_requests_option(108)
    srv_msg.client_requests_option(1)
    srv_msg.client_send_msg('REQUEST')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', 'ACK')
    srv_msg.response_check_include_option(108, expect_include=expect_include)
    if expect_include:
        srv_msg.response_check_option_content(108, 'value', '1800')
    srv_msg.response_check_content('yiaddr', ip_address)
    if ip_address != '0.0.0.0':
        srv_msg.response_check_include_option(1)
        srv_msg.response_check_option_content(1, 'value', '255.255.255.0')


@pytest.mark.v4
@pytest.mark.options
@pytest.mark.parametrize("level", ['global', 'pool', 'subnet', 'shared_network', 'reservation', 'class'])
def test_ipv6_only_preferred(level):
    """
    Tests to verify IPv6-only-preferred option.
    Forge creates set of shared networks, subnets and pools with one subnet guarded by host reservation.
    According to selected level, DORA exchanges are performed to verify that IPv6-only-preferred is
    sent by server only when necessary.
    If rapid-commit AND IPv6-only-preferred are included Kea should ignore rapid-commit.
    """
    misc.test_setup()
    # Define option for tests
    option = {"name": "v6-only-preferred", "data": "1800"}
    # Create first subnet guarded by "50" class
    srv_control.config_srv_subnet('192.168.50.0/24', '192.168.50.1-192.168.50.2', client_classes=['50'], id=1)
    # Create second subnet with two pools
    srv_control.config_srv_another_subnet_no_interface('192.168.51.0/24', '192.168.51.1-192.168.51.2', id=2)
    srv_control.new_pool('192.168.51.11-192.168.51.11', 1)
    # Create third subnet
    srv_control.config_srv_another_subnet_no_interface('192.168.52.0/24', '192.168.52.1-192.168.52.1', id=3)

    # Create shared network with subnet 2 and 3
    srv_control.shared_subnet('192.168.51.0/24', 0)
    srv_control.shared_subnet('192.168.52.0/24', 0)
    srv_control.set_conf_parameter_shared_subnet('name', '"sharedsubnet"', 0)
    # Create shared network with subnet 1
    srv_control.shared_subnet('192.168.50.0/24', 1)
    srv_control.set_conf_parameter_shared_subnet('name', '"sharedsubnetclass"', 1)

    # Create class and host reservation for subnet selection
    srv_control.create_new_class('50')
    reservations = [{"hw-address": "00:00:00:00:00:05",
                     "client-classes": ["50"]}]
    world.dhcp_cfg.update({'reservations': reservations})
    # Enable Early Global Host Reservation Lookup.
    world.dhcp_cfg['early-global-reservations-lookup'] = True
    # Required to apply reservation options
    world.dhcp_cfg['reservations-global'] = True

    if level == 'global':
        # Add v6-only-preferred on global level
        world.dhcp_cfg["option-data"].append(option)
        # Start server
        srv_control.build_and_send_config_files()
        srv_control.start_srv('DHCP', 'started')

        # Verify that IPv6-only-preferred is not returned if not requested
        _check_ipv6_only_response('192.168.51.1', '01', send108=False, expect_include=False)
        # shared network, second subnet, first pool
        _check_ipv6_only_response('192.168.51.2', '02', send108=True, expect_include=True)
        _check_ipv6_only_response('192.168.51.2', '02', send108=True, expect_include=True, send_rapid_commit=True)
        _check_ipv6_only_response('192.168.51.2', '02', send108=False, expect_include=False)
        # shared network, second subnet, second pool
        _check_ipv6_only_response('192.168.51.11', '03', send108=True, expect_include=True)
        _check_ipv6_only_response('192.168.51.11', '03', send108=True, expect_include=True, send_rapid_commit=True)
        _check_ipv6_only_response('192.168.51.11', '03', send108=False, expect_include=False)
        # shared network, third subnet
        _check_ipv6_only_response('192.168.52.1', '04', send108=True, expect_include=True)
        _check_ipv6_only_response('192.168.52.1', '04', send108=True, expect_include=True, send_rapid_commit=True)
        _check_ipv6_only_response('192.168.52.1', '04', send108=False, expect_include=False)
        # first subnet - host reservation
        _check_ipv6_only_response('192.168.50.1', '05', send108=True, expect_include=True)
        _check_ipv6_only_response('192.168.50.1', '05', send108=True, expect_include=True, send_rapid_commit=True)
        _check_ipv6_only_response('192.168.50.1', '05', send108=False, expect_include=False)

    if level == 'pool':
        # Add v6-only-preferred on pool level
        world.dhcp_cfg["shared-networks"][0]["subnet4"][0]["pools"][1]["option-data"] = [option]
        # Start server
        srv_control.build_and_send_config_files()
        srv_control.start_srv('DHCP', 'started')

        # Verify that IPv6-only-preferred is not returned if not requested
        _check_ipv6_only_response('192.168.51.1', '01', send108=False, expect_include=False)
        # shared network, second subnet, first pool
        _check_ipv6_only_response('192.168.51.2', '02', send108=True, expect_include=False)
        # shared network, second subnet, second pool
        _check_ipv6_only_response('192.168.51.11', '03', send108=True, expect_include=True)
        _check_ipv6_only_response('192.168.51.11', '03', send108=True, expect_include=True, send_rapid_commit=True)
        _check_ipv6_only_response('192.168.51.11', '03', send108=False, expect_include=False)
        # shared network, third subnet
        _check_ipv6_only_response('192.168.52.1', '04', send108=True, expect_include=False)
        # first subnet - host reservation
        _check_ipv6_only_response('192.168.50.1', '05', send108=True, expect_include=False)

    if level == 'subnet':
        # Add v6-only-preferred on subnet level
        world.dhcp_cfg["shared-networks"][0]["subnet4"][1]["option-data"] = [option]
        # Start server
        srv_control.build_and_send_config_files()
        srv_control.start_srv('DHCP', 'started')

        # Verify that IPv6-only-preferred is not returned if not requested
        _check_ipv6_only_response('192.168.51.1', '01', send108=False, expect_include=False)
        # shared network, second subnet, first pool
        _check_ipv6_only_response('0.0.0.0', '02', send108=True, expect_include=True)
        _check_ipv6_only_response('192.168.51.2', '02', send108=False, expect_include=False)
        # shared network, second subnet, second pool
        _check_ipv6_only_response('0.0.0.0', '03', send108=True, expect_include=True)
        _check_ipv6_only_response('192.168.51.11', '03', send108=False, expect_include=False)
        # shared network, third subnet
        _check_ipv6_only_response('0.0.0.0', '04', send108=True, expect_include=True)
        _check_ipv6_only_response('0.0.0.0', '04', send108=True, expect_include=True, send_rapid_commit=True)
        _check_ipv6_only_response('192.168.52.1', '04', send108=False, expect_include=False)
        # first subnet - host reservation
        _check_ipv6_only_response('192.168.50.1', '05', send108=True, expect_include=False)

    if level == 'shared_network':
        # Add v6-only-preferred on shared network level
        world.dhcp_cfg["shared-networks"][0]["option-data"] = [option]
        # Start server
        srv_control.build_and_send_config_files()
        srv_control.start_srv('DHCP', 'started')

        # Verify that IPv6-only-preferred is not returned if not requested
        _check_ipv6_only_response('192.168.51.1', '01', send108=False, expect_include=False)
        # shared network, second subnet, first pool
        _check_ipv6_only_response('0.0.0.0', '02', send108=True, expect_include=True)
        _check_ipv6_only_response('0.0.0.0', '02', send108=True, expect_include=True, send_rapid_commit=True)
        _check_ipv6_only_response('192.168.51.2', '02', send108=False, expect_include=False)
        # shared network, second subnet, second pool
        _check_ipv6_only_response('0.0.0.0', '03', send108=True, expect_include=True)
        _check_ipv6_only_response('0.0.0.0', '03', send108=True, expect_include=True, send_rapid_commit=True)
        _check_ipv6_only_response('192.168.51.11', '03', send108=False, expect_include=False)
        # shared network, third subnet
        _check_ipv6_only_response('0.0.0.0', '04', send108=True, expect_include=True)
        _check_ipv6_only_response('0.0.0.0', '04', send108=True, expect_include=True, send_rapid_commit=True)
        _check_ipv6_only_response('192.168.52.1', '04', send108=False, expect_include=False)
        # first subnet - host reservation
        _check_ipv6_only_response('192.168.50.1', '05', send108=True, expect_include=False)

    if level == 'reservation':
        # Add v6-only-preferred on additional reservation
        reservation = {"hw-address": "00:00:00:00:00:06",
                       "client-classes": ["50"],
                       "option-data": [
                           {
                               "name": "v6-only-preferred",
                               "data": "1800"
                           }
                       ]
                       }
        world.dhcp_cfg['reservations'].append(reservation)

        # Start server
        srv_control.build_and_send_config_files()
        srv_control.start_srv('DHCP', 'started')

        # Verify that IPv6-only-preferred is not returned if not requested
        _check_ipv6_only_response('192.168.51.1', '01', send108=False, expect_include=False)
        # shared network, second subnet, first pool
        _check_ipv6_only_response('192.168.51.2', '02', send108=True, expect_include=False)
        # shared network, second subnet, second pool
        _check_ipv6_only_response('192.168.51.11', '03', send108=True, expect_include=False)
        # shared network, third subnet
        _check_ipv6_only_response('192.168.52.1', '04', send108=True, expect_include=False)
        # first subnet - host reservation
        _check_ipv6_only_response('192.168.50.1', '05', send108=True, expect_include=False)
        # first subnet - host reservation with v6-only-preferred
        _check_ipv6_only_response('192.168.50.2', '06', send108=True, expect_include=True)
        _check_ipv6_only_response('192.168.50.2', '06', send108=True, expect_include=True, send_rapid_commit=True)
        _check_ipv6_only_response('192.168.50.2', '06', send108=False, expect_include=False)

    if level == 'class':
        # Add v6-only-preferred to "50" class
        srv_control.add_option_to_defined_class(1, 'v6-only-preferred', "1800")
        # Start server
        srv_control.build_and_send_config_files()
        srv_control.start_srv('DHCP', 'started')

        # Verify that IPv6-only-preferred is not returned if not requested
        _check_ipv6_only_response('192.168.51.1', '01', send108=False, expect_include=False)
        # shared network, second subnet, first pool
        _check_ipv6_only_response('192.168.51.2', '02', send108=True, expect_include=False)
        # shared network, second subnet, second pool
        _check_ipv6_only_response('192.168.51.11', '03', send108=True, expect_include=False)
        # shared network, third subnet
        _check_ipv6_only_response('192.168.52.1', '04', send108=True, expect_include=False)
        # first subnet - host reservation with class
        _check_ipv6_only_response('192.168.50.1', '05', send108=True, expect_include=True)
        _check_ipv6_only_response('192.168.50.1', '05', send108=True, expect_include=True, send_rapid_commit=True)
        _check_ipv6_only_response('192.168.50.1', '05', send108=False, expect_include=False)
