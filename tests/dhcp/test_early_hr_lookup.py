# Copyright (C) 2022 Internet Systems Consortium, Inc. ("ISC")
#
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

# Author: Marcin Godzina

"""Early Global Host Reservation Lookup Tests"""

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
@pytest.mark.parametrize('backend', ['memfile', 'MySQL', 'PostgreSQL'])
def test_early_hr_lookup_class(backend, dhcp_version):
    """
    Test to check if Kea looks up Global Host Reservations and assigns client class before subnet allocation.
    After assigning client class, the subnet should be allocated according to class.
    """
    misc.test_setup()
    srv_control.enable_db_backend_reservation(backend)

    # Define 2 subnets, with one guarded by class.
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
            'client-class': 'first'
        },
        {
            'id': 2,
            'interface': world.f_cfg.server_iface,
            'pools': [
                {
                    'pool': '192.168.51.1-192.168.51.50'
                }
            ],
            'subnet': '192.168.51.0/24'
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
            'client-class': 'first'
        },
        {
            'id': 2,
            'interface': world.f_cfg.server_iface,
            'pools': [
                {
                    'pool': '2001:db8:2::1-2001:db8:2::50'
                }
            ],
            'subnet': '2001:db8:2::/64'
        }
    ]

    # Define client class to guard subnet.
    srv_control.create_new_class('first')

    # Define host reservation that can access "first" subnet, for memfile
    reservations_v4 = [
        {
            'client-classes': ['first'],
            'hw-address': 'ff:01:02:03:ff:04'
        }
    ]
    reservations_v6 = [
        {
            'client-classes': ['first'],
            'duid': '00:03:00:01:f6:f5:f4:f3:f2:04'
        },
    ]

    # Enable Early Global Host Reservation Lookup.
    world.dhcp_cfg['early-global-reservations-lookup'] = True

    # apply definitions to server configuration.
    if backend != 'memfile':
        if dhcp_version == 'v4':
            world.dhcp_cfg.update({'subnet4': subnets_v4})
            # Define host reservation for database, that should be assigned first class.
            srv_control.new_db_backend_reservation(backend, 'hw-address', 'ff:01:02:03:ff:04')
            srv_control.update_db_backend_reservation('dhcp4_subnet_id', 0, backend, 1)
            srv_control.update_db_backend_reservation('dhcp4_client_classes', 'first', backend, 1)
            srv_control.upload_db_reservation(backend)
        else:
            world.dhcp_cfg.update({'subnet6': subnets_v6})
            # Define host reservation for database, that should be assigned first class.
            srv_control.new_db_backend_reservation(backend, 'duid', '00:03:00:01:f6:f5:f4:f3:f2:04')
            srv_control.update_db_backend_reservation('dhcp6_subnet_id', 0, backend, 1)
            srv_control.update_db_backend_reservation('dhcp6_client_classes', 'first', backend, 1)
            srv_control.upload_db_reservation(backend)
    else:
        if dhcp_version == 'v4':
            world.dhcp_cfg.update({'subnet4': subnets_v4})
            world.dhcp_cfg.update({'reservations': reservations_v4})
        else:
            world.dhcp_cfg.update({'subnet6': subnets_v6})
            world.dhcp_cfg.update({'reservations': reservations_v6})

    srv_control.build_and_send_config_files()
    srv_control.start_srv('DHCP', 'started')

    # Check if proper IP is assigned to MAC address.
    if dhcp_version == 'v4':
        _get_address_v4('192.168.50.1', 'ff:01:02:03:ff:04')
        _get_address_v4('192.168.51.1', 'ff:01:02:03:ff:06')
    else:
        _get_address_v6('2001:db8:1::1', '00:03:00:01:f6:f5:f4:f3:f2:04')
        _get_address_v6('2001:db8:2::1', '00:03:00:01:f6:f5:f4:f3:f2:06')


@pytest.mark.v4
@pytest.mark.v6
@pytest.mark.host_reservation
@pytest.mark.parametrize('backend', ['memfile', 'MySQL', 'PostgreSQL'])
def test_early_hr_lookup_class_in_class(backend, dhcp_version):
    """
    Test to check if Kea looks up Global Host Reservations and assigns client class dependent on other classes.
    After assigning client class dependent on first one, the subnet should be allocated according to second class.
    """
    misc.test_setup()
    srv_control.enable_db_backend_reservation(backend)

    # Define 2 subnets, with one guarded by class.
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
            'client-class': 'second'
        },
        {
            'id': 2,
            'interface': world.f_cfg.server_iface,
            'pools': [
                {
                    'pool': '192.168.51.1-192.168.51.50'
                }
            ],
            'subnet': '192.168.51.0/24'
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
            'client-class': 'second'
        },
        {
            'id': 2,
            'interface': world.f_cfg.server_iface,
            'pools': [
                {
                    'pool': '2001:db8:2::1-2001:db8:2::50'
                }
            ],
            'subnet': '2001:db8:2::/64'
        }
    ]

    # Define client class to be assigned by reservation.
    srv_control.create_new_class('first')

    # Define client class to guard subnet and include other class.
    srv_control.create_new_class('second')
    srv_control.add_test_to_class(2, 'test', "member('first')")

    # Define host reservation that can access "first" subnet, for memfile
    reservations_v4 = [
        {
            'client-classes': ['first'],
            'hw-address': 'ff:01:02:03:ff:04'
        }
    ]
    reservations_v6 = [
        {
            'client-classes': ['first'],
            'duid': '00:03:00:01:f6:f5:f4:f3:f2:04'
        },
    ]

    # Enable Early Global Host Reservation Lookup.
    world.dhcp_cfg['early-global-reservations-lookup'] = True

    # apply definitions to server configuration.
    if backend != 'memfile':
        if dhcp_version == 'v4':
            world.dhcp_cfg.update({'subnet4': subnets_v4})
            # Define host reservation for database, that should be assigned first class.
            srv_control.new_db_backend_reservation(backend, 'hw-address', 'ff:01:02:03:ff:04')
            srv_control.update_db_backend_reservation('dhcp4_subnet_id', 0, backend, 1)
            srv_control.update_db_backend_reservation('dhcp4_client_classes', 'first', backend, 1)
            srv_control.upload_db_reservation(backend)
        else:
            world.dhcp_cfg.update({'subnet6': subnets_v6})
            # Define host reservation for database, that should be assigned first class.
            srv_control.new_db_backend_reservation(backend, 'duid', '00:03:00:01:f6:f5:f4:f3:f2:04')
            srv_control.update_db_backend_reservation('dhcp6_subnet_id', 0, backend, 1)
            srv_control.update_db_backend_reservation('dhcp6_client_classes', 'first', backend, 1)
            srv_control.upload_db_reservation(backend)
    else:
        if dhcp_version == 'v4':
            world.dhcp_cfg.update({'subnet4': subnets_v4})
            world.dhcp_cfg.update({'reservations': reservations_v4})
        else:
            world.dhcp_cfg.update({'subnet6': subnets_v6})
            world.dhcp_cfg.update({'reservations': reservations_v6})

    srv_control.build_and_send_config_files()
    srv_control.start_srv('DHCP', 'started')

    # Check if proper IP is assigned to MAC address.
    if dhcp_version == 'v4':
        _get_address_v4('192.168.50.1', 'ff:01:02:03:ff:04')
        _get_address_v4('192.168.51.1', 'ff:01:02:03:ff:06')
    else:
        _get_address_v6('2001:db8:1::1', '00:03:00:01:f6:f5:f4:f3:f2:04')
        _get_address_v6('2001:db8:2::1', '00:03:00:01:f6:f5:f4:f3:f2:06')


@pytest.mark.v4
@pytest.mark.v6
@pytest.mark.host_reservation
@pytest.mark.parametrize('backend', ['memfile', 'MySQL', 'PostgreSQL'])
def test_early_hr_lookup_drop(backend, dhcp_version):
    """
    Test to check if Kea looks up Global Host Reservations and assigns DROP class.
    """
    misc.test_setup()
    srv_control.enable_db_backend_reservation(backend)
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
        }
    ]

    # Define host reservation for memfile, that should be dropped.

    reservations_v4 = [
        {
            'client-classes': ['DROP'],
            'hw-address': 'ff:01:02:03:ff:05'
        }
    ]
    reservations_v6 = [
        {
            'client-classes': ['DROP'],
            'duid': '00:03:00:01:f6:f5:f4:f3:f2:05'
        }
    ]

    # Enable Early Global Host Reservation Lookup.
    world.dhcp_cfg['early-global-reservations-lookup'] = True

    # Apply definitions to server configuration.
    if backend != 'memfile':
        if dhcp_version == 'v4':
            world.dhcp_cfg.update({'subnet4': subnets_v4})
            # Define host reservation for database, that should be dropped.
            srv_control.new_db_backend_reservation(backend, 'hw-address', 'ff:01:02:03:ff:05')
            srv_control.update_db_backend_reservation('dhcp4_subnet_id', 0, backend, 1)
            srv_control.update_db_backend_reservation('dhcp4_client_classes', 'DROP', backend, 1)
            srv_control.upload_db_reservation(backend)
        else:
            world.dhcp_cfg.update({'subnet6': subnets_v6})
            # Define host reservation for database, that should be dropped.
            srv_control.new_db_backend_reservation(backend, 'duid', '00:03:00:01:f6:f5:f4:f3:f2:05')
            srv_control.update_db_backend_reservation('dhcp6_subnet_id', 0, backend, 1)
            srv_control.update_db_backend_reservation('dhcp6_client_classes', 'DROP', backend, 1)
            srv_control.upload_db_reservation(backend)
    else:
        if dhcp_version == 'v4':
            world.dhcp_cfg.update({'subnet4': subnets_v4})
            world.dhcp_cfg.update({'reservations': reservations_v4})
        else:
            world.dhcp_cfg.update({'subnet6': subnets_v6})
            world.dhcp_cfg.update({'reservations': reservations_v6})

    srv_control.build_and_send_config_files()
    srv_control.start_srv('DHCP', 'started')

    # Check if classless MAC gets IP and reserved host is dropped.
    if dhcp_version == 'v4':
        _get_address_v4('192.168.50.1', 'ff:01:02:03:ff:04')
        _get_address_v4(None, 'ff:01:02:03:ff:05', drop=True)
    else:
        _get_address_v6('2001:db8:1::1', '00:03:00:01:f6:f5:f4:f3:f2:04')
        _get_address_v6(None, '00:03:00:01:f6:f5:f4:f3:f2:05', drop=True)
