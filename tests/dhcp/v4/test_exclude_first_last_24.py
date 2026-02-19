# Copyright (C) 2023-2026 Internet Systems Consortium, Inc. ("ISC")
#
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

"""
Tests for the exclude-first-last-24 configuration knob of kea-dhcp4.
"""

import pytest

from src import srv_control
from src import srv_msg
from src import misc

from src.forge_cfg import world


@pytest.mark.v4
def test_v4_exclude_first_last_24_subnet_24():
    """
    Check exclude-first-last-24 on a single /24 pool.
    """

    # Enable exclude-first-last-24.
    misc.test_setup()
    world.dhcp_cfg['compatibility'] = {'exclude-first-last-24': True}
    srv_control.config_srv_subnet('192.0.2.0/24', '192.0.2.0 - 192.0.2.255')
    srv_control.build_and_send_config_files()
    srv_control.start_srv('DHCP', 'started')

    # Addresses 1-254 should be leasable.
    for i in range(1, 255):
        srv_msg.DORA(f'192.0.2.{i}', chaddr=f'ff:ff:01:02:03:{i:02x}')

    # There should be no more leases.
    srv_msg.DORA(None, chaddr='ff:ff:ff:ff:ff:01', response_type='NAK')

    # Disable exclude-first-last-24.
    misc.test_setup()
    srv_control.config_srv_subnet('192.0.2.0/24', '192.0.2.0 - 192.0.2.255')
    srv_control.build_and_send_config_files()
    srv_control.start_srv('DHCP', 'reconfigured')

    # Addresses 0 and 255 should be leased.
    srv_msg.DORA('192.0.2.0', chaddr='ff:ff:ff:ff:ff:01')
    srv_msg.DORA('192.0.2.255', chaddr='ff:ff:ff:ff:ff:02')

    # But not more than that.
    srv_msg.DORA(None, chaddr='ff:ff:ff:ff:ff:03', response_type='NAK')


@pytest.mark.v4
def test_v4_exclude_first_last_24_subnet_23():
    """
    Check exclude-first-last-24 on a single pool bigger than /24.
    Let's use /23 in the interest of run time.
    """

    # Enable exclude-first-last-24.
    misc.test_setup()
    world.dhcp_cfg['compatibility'] = {'exclude-first-last-24': True}
    srv_control.config_srv_subnet('192.0.2.0/23', '192.0.2.0 - 192.0.3.255')
    srv_control.build_and_send_config_files()
    srv_control.start_srv('DHCP', 'started')

    # Addresses 1-254 should be leasable.
    for i in range(1, 255):
        srv_msg.DORA(f'192.0.2.{i}', chaddr=f'ff:ff:01:02:03:{i:02x}', subnet_mask='255.255.254.0')
    for i in range(1, 255):
        srv_msg.DORA(f'192.0.3.{i}', chaddr=f'ff:ff:01:02:04:{i:02x}', subnet_mask='255.255.254.0')

    # There should be no more leases.
    srv_msg.DORA(None, chaddr='ff:ff:ff:ff:ff:01', response_type='NAK')

    # Disable exclude-first-last-24.
    misc.test_setup()
    srv_control.config_srv_subnet('192.0.2.0/23', '192.0.2.0 - 192.0.3.255')
    srv_control.build_and_send_config_files()
    srv_control.start_srv('DHCP', 'reconfigured')

    # Addresses 0 and 255 should be leased.
    srv_msg.DORA('192.0.2.0', chaddr='ff:ff:ff:ff:ff:01', subnet_mask='255.255.254.0')
    srv_msg.DORA('192.0.2.255', chaddr='ff:ff:ff:ff:ff:02', subnet_mask='255.255.254.0')
    srv_msg.DORA('192.0.3.0', chaddr='ff:ff:ff:ff:ff:03', subnet_mask='255.255.254.0')
    srv_msg.DORA('192.0.3.255', chaddr='ff:ff:ff:ff:ff:04', subnet_mask='255.255.254.0')

    # But not more than that.
    srv_msg.DORA(None, chaddr='ff:ff:ff:ff:ff:05', response_type='NAK')


@pytest.mark.v4
def test_v4_exclude_first_last_24_subnet_25_first_half():
    """
    Check that exclude-first-last-24 does not have any effect, as documented, on subnets smaller than /24.
    Let's use a /25 range that contains address 0.
    Harden the test such that the subnet range does not match the pool range.
    """

    # Enable exclude-first-last-24.
    misc.test_setup()
    world.dhcp_cfg['compatibility'] = {'exclude-first-last-24': True}
    srv_control.config_srv_subnet('192.0.2.0/25', '192.0.2.0 - 192.0.2.127')
    srv_control.build_and_send_config_files()
    srv_control.start_srv('DHCP', 'started')

    # Addresses 0-127 should be leasable.
    for i in range(0, 128):
        srv_msg.DORA(f'192.0.2.{i}', chaddr=f'ff:ff:01:02:03:{i:02x}', subnet_mask='255.255.255.128')

    # There should be no more leases.
    srv_msg.DORA(None, chaddr='ff:ff:ff:ff:ff:ff', response_type='NAK')

    # Disable exclude-first-last-24.
    misc.test_setup()
    srv_control.config_srv_subnet('192.0.2.0/25', '192.0.2.0 - 192.0.2.127')
    srv_control.build_and_send_config_files()
    srv_control.start_srv('DHCP', 'reconfigured')

    # There should still be no more leases.
    srv_msg.DORA(None, chaddr='ff:ff:ff:ff:ff:ff', response_type='NAK')

    # Switch to subnet /23 with same pool range. It does take effect this time.
    srv_control.clear_some_data('leases')
    misc.test_setup()
    world.dhcp_cfg['compatibility'] = {'exclude-first-last-24': True}
    srv_control.config_srv_subnet('192.0.2.0/23', '192.0.2.0 - 192.0.2.127')
    srv_control.build_and_send_config_files()
    srv_control.start_srv('DHCP', 'reconfigured')

    # Address 0 not leased.
    for i in range(1, 128):
        srv_msg.DORA(f'192.0.2.{i}', chaddr=f'ff:ff:01:01:01:{i:02x}', subnet_mask='255.255.254.0')

    # There should be no more leases.
    srv_msg.DORA(None, chaddr='ff:ff:ff:ff:ff:ff', response_type='NAK')


@pytest.mark.v4
def test_v4_exclude_first_last_24_subnet_25_second_half():
    """
    Check that exclude-first-last-24 does not have any effect, as documented, on subnets smaller than /24.
    Let's use a /25 range that contains address 255.
    Harden the test such that the subnet range does not match the pool range.
    """

    # Enable exclude-first-last-24.
    misc.test_setup()
    world.dhcp_cfg['compatibility'] = {'exclude-first-last-24': True}
    srv_control.config_srv_subnet('192.0.2.128/25', '192.0.2.128 - 192.0.2.255')
    srv_control.build_and_send_config_files()
    srv_control.start_srv('DHCP', 'started')

    # Addresses 128-255 should be leasable.
    for i in range(128, 256):
        srv_msg.DORA(f'192.0.2.{i}', chaddr=f'ff:ff:01:02:03:{i:02x}', subnet_mask='255.255.255.128')

    # There should be no more leases.
    srv_msg.DORA(None, chaddr='ff:ff:ff:ff:ff:ff', response_type='NAK')

    # Disable exclude-first-last-24.
    misc.test_setup()
    srv_control.config_srv_subnet('192.0.2.128/25', '192.0.2.128 - 192.0.2.255')
    srv_control.build_and_send_config_files()
    srv_control.start_srv('DHCP', 'reconfigured')

    # There should still be no more leases.
    srv_msg.DORA(None, chaddr='ff:ff:ff:ff:ff:ff', response_type='NAK')

    # Switch to subnet /23 with same pool range. It does take effect this time.
    srv_control.clear_some_data('leases')
    misc.test_setup()
    world.dhcp_cfg['compatibility'] = {'exclude-first-last-24': True}
    srv_control.config_srv_subnet('192.0.2.0/23', '192.0.2.128 - 192.0.2.255')
    srv_control.build_and_send_config_files()
    srv_control.start_srv('DHCP', 'reconfigured')

    # Address 255 not leased.
    for i in range(128, 255):
        srv_msg.DORA(f'192.0.2.{i}', chaddr=f'ff:ff:01:01:01:{i:02x}', subnet_mask='255.255.254.0')

    # There should be no more leases.
    srv_msg.DORA(None, chaddr='ff:ff:ff:ff:ff:ff', response_type='NAK')
