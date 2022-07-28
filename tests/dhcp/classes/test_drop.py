# Copyright (C) 2022 Internet Systems Consortium, Inc. ("ISC")
#
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

# Author: Marcin Godzina

"""DROP Class tests"""

# pylint: disable=invalid-name,line-too-long

import copy
import pytest

from src import srv_control
from src import srv_msg
from src import misc
from src.forge_cfg import world


def _get_address_v4(yiaddr, chaddr, drop=False):
    """
    Helper function to get v4 lease or check for DROP
    :param yiaddr: desired ip address
    :param chaddr: MAC address
    :param drop: If request should be dropped by Kea
    """
    misc.test_procedure()
    srv_msg.client_sets_value('Client', 'chaddr', chaddr)
    srv_msg.client_send_msg('DISCOVER')

    misc.pass_criteria()
    if drop is True:
        srv_msg.send_wait_for_message('MUST', 'OFFER', expect_response=False)
        return 0
    srv_msg.send_wait_for_message('MUST', 'OFFER')
    srv_msg.response_check_content('yiaddr', yiaddr)

    misc.test_procedure()
    srv_msg.client_copy_option('server_id')
    srv_msg.client_does_include_with_value('requested_addr', yiaddr)
    srv_msg.client_sets_value('Client', 'chaddr', chaddr)
    srv_msg.client_send_msg('REQUEST')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', 'ACK')
    srv_msg.response_check_content('yiaddr', yiaddr)
    srv_msg.response_check_include_option(1)
    srv_msg.response_check_option_content(1, 'value', '255.255.255.0')

    return 0


def _get_address_v6(ia_na, duid, drop=False):
    """
    Helper function to get v6 lease or check for DROP
    :param ia_na: desired ip address
    :param duid: MAC address
    :param drop: If request should be dropped by Kea
    """
    misc.test_procedure()
    srv_msg.client_sets_value('Client', 'DUID', duid)
    srv_msg.client_does_include('Client', 'client-id')
    srv_msg.client_does_include('Client', 'IA-NA')
    srv_msg.client_send_msg('SOLICIT')

    misc.pass_criteria()
    if drop is True:
        srv_msg.send_wait_for_message('MUST', 'ADVERTISE', expect_response=False)
        return 0

    srv_msg.send_wait_for_message('MUST', 'ADVERTISE')
    misc.test_procedure()
    srv_msg.client_copy_option('server-id')
    srv_msg.client_copy_option('IA_NA')
    srv_msg.client_sets_value('Client', 'DUID', duid)
    srv_msg.client_does_include('Client', 'client-id')
    srv_msg.client_send_msg('REQUEST')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', 'REPLY')
    srv_msg.response_check_include_option(3)
    srv_msg.response_check_option_content(3, 'sub-option', 5)
    srv_msg.response_check_suboption_content(5, 3, 'addr', ia_na)

    return 0


@pytest.mark.v4
@pytest.mark.v6
@pytest.mark.host_reservation
def test_drop_subnet_reservation(dhcp_version):
    """
    Test to check if Kea assigns DROP class from subnet reservation and drops packets.
    """
    misc.test_setup()
    # Define subnet.
    subnets_v4 = [
        {
            'id': 1,
            'interface': world.f_cfg.server_iface,
            'pools': [
                {
                    'pool': '192.168.50.1-192.168.50.50'
                }
            ],
            'subnet': '192.168.50.0/24',
            "reservations": [
                {
                    'client-classes': ['DROP'],
                    'hw-address': 'ff:01:02:03:ff:05'
                }
            ]
        }
    ]
    subnets_v6 = [
        {
            'id': 1,
            'interface': world.f_cfg.server_iface,
            'pools': [
                {
                    'pool': '2001:db8:1::1-2001:db8:1::50'
                }
            ],
            'subnet': '2001:db8:1::/64',
            "reservations": [
                {
                    'client-classes': ['DROP'],
                    'duid': '00:03:00:01:f6:f5:f4:f3:f2:05'
                }
            ]
        }
    ]

    # Apply definitions to server configuration.
    if dhcp_version == 'v4':
        world.dhcp_cfg.update({'subnet4': copy.deepcopy(subnets_v4)})
    else:
        world.dhcp_cfg.update({'subnet6': copy.deepcopy(subnets_v6)})

    srv_control.build_and_send_config_files()
    srv_control.start_srv('DHCP', 'started')

    # Check if classless MAC gets IP and reserved host is dropped.
    if dhcp_version == 'v4':
        _get_address_v4('192.168.50.1', 'ff:01:02:03:ff:04')
        _get_address_v4(None, 'ff:01:02:03:ff:05', drop=True)
    else:
        _get_address_v6('2001:db8:1::1', '00:03:00:01:f6:f5:f4:f3:f2:04')
        _get_address_v6(None, '00:03:00:01:f6:f5:f4:f3:f2:05', drop=True)


@pytest.mark.v4
@pytest.mark.v6
@pytest.mark.host_reservation
def test_drop_class(dhcp_version):
    """
    Test to check if Kea assigns DROP class and drops packets.
    """
    misc.test_setup()
    # Define subnet.
    if dhcp_version == 'v4':
        srv_control.config_srv_subnet('192.168.50.0/24', '192.168.50.1-192.168.50.50')
    else:
        srv_control.config_srv_subnet('2001:db8:1::/64', '2001:db8:1::1-2001:db8:1::50')

    # Define client class to drop.
    client_classes_v4 = [
        {
            'name': 'DROP',
            'test': "hexstring(pkt4.mac, ':') == 'ff:01:02:03:ff:05'"
        }
    ]
    client_classes_v6 = [
        {
            'name': 'DROP',
            'test': "hexstring(option[1].hex, ':') == '00:03:00:01:f6:f5:f4:f3:f2:05'"
        }
    ]

    # Apply definitions to server configuration.
    if dhcp_version == 'v4':
        world.dhcp_cfg.update({'client-classes': copy.deepcopy(client_classes_v4)})
    else:
        world.dhcp_cfg.update({'client-classes': copy.deepcopy(client_classes_v6)})

    srv_control.build_and_send_config_files()
    srv_control.start_srv('DHCP', 'started')

    # Check if classless MAC gets IP and class allocated host is dropped.
    if dhcp_version == 'v4':
        _get_address_v4('192.168.50.1', 'ff:01:02:03:ff:04')
        _get_address_v4(None, 'ff:01:02:03:ff:05', drop=True)
    else:
        _get_address_v6('2001:db8:1::1', '00:03:00:01:f6:f5:f4:f3:f2:04')
        _get_address_v6(None, '00:03:00:01:f6:f5:f4:f3:f2:05', drop=True)
