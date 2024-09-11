# Copyright (C) 2024 Internet Systems Consortium, Inc. ('ISC')
#
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

import copy

import pytest

from src import srv_control
from src import srv_msg
from src import misc

from src.forge_cfg import world


@pytest.mark.v4
@pytest.mark.host_reservation
def test_v4_reservation_with_offer_lifetime():
    """ Checks that offer-lifetime does not change the behavior of address reservations. """
    misc.test_setup()

    # --------------------------------------------------------------------------
    # Baseline test case first. Settle what happens when the identifier changes
    # for a reservation.

    srv_control.config_srv_subnet('192.1.2.0/24', '192.1.2.0/24', id=1)
    srv_control.host_reservation_in_subnet('ip-address', '192.1.2.102', 0,
                                           'hw-address', '01:02:03:04:ff:02')
    srv_control.host_reservation_in_subnet('ip-address', '192.1.2.104', 0,
                                           'hw-address', '01:02:03:04:ff:04')
    srv_control.host_reservation_in_subnet('ip-address', '192.1.2.106', 0,
                                           'hw-address', '01:02:03:04:ff:06')

    srv_control.build_and_send_config_files()
    srv_control.start_srv('DHCP', 'started')
    dhcp_cfg = copy.deepcopy(world.dhcp_cfg['Dhcp4'])

    # Client gets reserved address. Nothing special.
    srv_msg.DORA('192.1.2.102', chaddr='01:02:03:04:ff:02')

    # Change reservation identifier.
    world.dhcp_cfg = copy.deepcopy(dhcp_cfg)
    world.dhcp_cfg['subnet4'][0]['reservations'][0]['hw-address'] = '01:02:03:04:ff:03'
    srv_control.build_and_send_config_files()
    srv_control.start_srv('DHCP', 'started')
    dhcp_cfg = copy.deepcopy(world.dhcp_cfg['Dhcp4'])

    # At first, if the reserved client tries to get a lease before the previous
    # lease was expired or released, it gets it the from the dynamic pool.
    srv_msg.DORA('192.1.2.0', chaddr='01:02:03:04:ff:03')
    # The old lessee gets a dynamic address.
    srv_msg.DORA('192.1.2.1', chaddr='01:02:03:04:ff:02')
    # The reserved client gets the reserved address.
    srv_msg.DORA('192.1.2.102', chaddr='01:02:03:04:ff:03')

    # --------------------------------------------------------------------------
    # The actual test case now. Add offer-lifetime. Test previous clients, and
    # new clients too.

    # Add offer-lifetime.
    world.dhcp_cfg = copy.deepcopy(dhcp_cfg)
    world.dhcp_cfg['offer-lifetime'] = 20
    srv_control.build_and_send_config_files()
    srv_control.start_srv('DHCP', 'started')
    dhcp_cfg = copy.deepcopy(world.dhcp_cfg['Dhcp4'])

    # All clients get their current leases.
    srv_msg.DORA('192.1.2.1', chaddr='01:02:03:04:ff:02')
    srv_msg.DORA('192.1.2.102', chaddr='01:02:03:04:ff:03')
    srv_msg.DORA('192.1.2.104', chaddr='01:02:03:04:ff:04')

    # Change reservation identifier.
    world.dhcp_cfg = copy.deepcopy(dhcp_cfg)
    world.dhcp_cfg['subnet4'][0]['reservations'][1]['hw-address'] = '01:02:03:04:ff:05'
    srv_control.build_and_send_config_files()
    srv_control.start_srv('DHCP', 'started')
    dhcp_cfg = copy.deepcopy(world.dhcp_cfg['Dhcp4'])

    # Clients get their current leases. Old reservation gets dynamic address.
    # New reservation gets reserved address.
    srv_msg.DORA('192.1.2.1', chaddr='01:02:03:04:ff:02')
    srv_msg.DORA('192.1.2.102', chaddr='01:02:03:04:ff:03')
    # This should have happened:
    srv_msg.DORA('192.1.2.0', chaddr='01:02:03:04:ff:04')
    srv_msg.DORA('192.1.2.104', chaddr='01:02:03:04:ff:05')
    # This is the buggy behavior:
    # srv_msg.DO('192.1.2.0', chaddr='01:02:03:04:ff:04')
    # srv_msg.RA('192.1.2.0', response_type='NAK', chaddr='01:02:03:04:ff:04')
    # srv_msg.RA('192.1.2.0', response_type='NAK', chaddr='01:02:03:04:ff:04')
    # srv_msg.DORA('192.1.2.2', chaddr='01:02:03:04:ff:05')

    # Remove offer lifetime.
    world.dhcp_cfg = copy.deepcopy(dhcp_cfg)
    del world.dhcp_cfg['offer-lifetime']
    srv_control.build_and_send_config_files()
    srv_control.start_srv('DHCP', 'started')
    dhcp_cfg = copy.deepcopy(world.dhcp_cfg['Dhcp4'])

    # All clients get their current leases.
    srv_msg.DORA('192.1.2.1', chaddr='01:02:03:04:ff:02')
    srv_msg.DORA('192.1.2.102', chaddr='01:02:03:04:ff:03')
    # This should have happened:
    srv_msg.DORA('192.1.2.0', chaddr='01:02:03:04:ff:04')
    # Buggy behavior: the NAK persists even after taking out offer-lifetime, although only for renews?
    # srv_msg.DO('192.1.2.3', chaddr='01:02:03:04:ff:04')
    # srv_msg.RA('192.1.2.3', chaddr='01:02:03:04:ff:04')
    # srv_msg.RA('192.1.2.3', response_type='NAK', chaddr='01:02:03:04:ff:04')
    # == ! ==
    srv_msg.DORA('192.1.2.104', chaddr='01:02:03:04:ff:05')
    srv_msg.DORA('192.1.2.106', chaddr='01:02:03:04:ff:06')

    # Change dhcp identifier.
    world.dhcp_cfg = copy.deepcopy(dhcp_cfg)
    world.dhcp_cfg['subnet4'][0]['reservations'][2]['hw-address'] = '01:02:03:04:ff:07'
    srv_control.build_and_send_config_files()
    srv_control.start_srv('DHCP', 'started')
    dhcp_cfg = copy.deepcopy(world.dhcp_cfg['Dhcp4'])

    # Clients get their current leases. Old reservation gets dynamic address.
    # New reservation gets reserved address.
    srv_msg.DORA('192.1.2.1', chaddr='01:02:03:04:ff:02')
    srv_msg.DORA('192.1.2.102', chaddr='01:02:03:04:ff:03')
    srv_msg.DORA('192.1.2.0', chaddr='01:02:03:04:ff:04')
    srv_msg.DORA('192.1.2.104', chaddr='01:02:03:04:ff:05')
    srv_msg.DORA('192.1.2.2', chaddr='01:02:03:04:ff:06')
    srv_msg.DORA('192.1.2.106', chaddr='01:02:03:04:ff:07')
