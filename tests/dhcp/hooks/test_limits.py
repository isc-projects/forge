# Copyright (C) 2022 Internet Systems Consortium, Inc. ("ISC")
#
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

# Author: Marcin Godzina

"""Kea Limits Hook"""

# pylint: disable=invalid-name,line-too-long,unused-argument
import time
import pytest

from src import misc
from src import srv_control
from src import srv_msg

from src.forge_cfg import world


def _get_address_v4(address, chaddr, vendor=None):
    misc.test_procedure()
    srv_msg.client_sets_value('Client', 'chaddr', chaddr)
    if vendor is not None:
        srv_msg.client_does_include_with_value('vendor_class_id', vendor)
    srv_msg.client_send_msg('DISCOVER')

    misc.pass_criteria()
    try:
        srv_msg.send_wait_for_message('MUST', 'OFFER')
    except AssertionError as e:
        if e.args[0] == 'No response received.':
            return 0
        raise AssertionError(e) from e
    return 1


def _get_address_v6(address, duid, vendor=None):
    misc.test_procedure()
    srv_msg.client_sets_value('Client', 'DUID', duid)
    srv_msg.client_does_include('Client', 'client-id')
    srv_msg.client_does_include('Client', 'IA-NA')
    if vendor is not None:
        srv_msg.client_sets_value('Client', 'vendor_class_data', 'eRouter1.0')
        srv_msg.client_does_include('Client', 'vendor-class')
    srv_msg.client_send_msg('SOLICIT')

    misc.pass_criteria()
    try:
        srv_msg.send_wait_for_message('MUST', 'ADVERTISE')
    except AssertionError as e:
        if e.args[0] == 'No response received.':
            return 0
        raise AssertionError(e) from e
    return 1


# @pytest.mark.v4
@pytest.mark.v6
@pytest.mark.hook
@pytest.mark.parametrize('backend', ['memfile'])
def test_limits_subnet(dhcp_version, backend):
    misc.test_setup()
    srv_control.define_temporary_lease_db_backend(backend)
    if dhcp_version == 'v4':
        srv_control.config_srv_subnet('192.168.0.0/16', '192.168.1.1-192.168.255.255')
        srv_control.config_srv_opt('subnet-mask', '255.255.0.0')
        limit = 20
    else:
        srv_control.config_srv_subnet('2001:db8:1::/64', '2001:db8:1::1-2001:db8:1::255:255')
        limit = 3
    srv_control.add_line_to_subnet(0, {"user-context": {
        "limits": {
            "rate-limit": f"{limit} packets per second"
        }}})

    srv_control.open_control_channel()
    srv_control.agent_control_channel()
    srv_control.add_hooks('libdhcp_limits.so')

    srv_control.build_and_send_config_files()
    srv_control.start_srv('DHCP', 'started')

    success = 0
    packets = 0

    if dhcp_version == 'v4':
        world.cfg['wait_interval'] = 0.002
    else:
        world.cfg['wait_interval'] = 0.1
    start = time.time()
    for k in range(1, 10):
        for i in range(1, 30):
            if dhcp_version == 'v4':
                success += _get_address_v4(f'192.168.{k}.{i}', chaddr=f'ff:01:02:03:{k:0>2x}:{i:0>2x}')
            else:
                success += _get_address_v6(f'2001:db8:1::{k}:{i}', duid=f'00:03:00:01:ff:ff:ff:ff:{k:0>2x}:{i:0>2x}')
            packets += 1
    end = time.time()
    run1 = end - start

    print(f"Runtime of the program is {run1}")
    print(f"Packets received {success}/{packets}")
    print(f"Packets per second {success / run1}")


@pytest.mark.v4
@pytest.mark.v6
@pytest.mark.hook
@pytest.mark.parametrize('backend', ['memfile'])
def test_limits_class(dhcp_version, backend):
    misc.test_setup()
    srv_control.define_temporary_lease_db_backend(backend)
    if dhcp_version == 'v4':
        srv_control.config_srv_subnet('192.168.0.0/16', '192.168.1.1-192.168.255.255')
        srv_control.config_srv_opt('subnet-mask', '255.255.0.0')
    else:
        srv_control.config_srv_subnet('2001:db8:1::/64', '2001:db8:1::1-2001:db8:1::255:255')
    srv_control.open_control_channel()
    srv_control.agent_control_channel()
    srv_control.add_hooks('libdhcp_limits.so')
    srv_control.add_hooks('libdhcp_class_cmds.so')
    if dhcp_version == 'v4':
        classes = [
            {
                "name": "gold",
                "test": "option[60].text == 'PXE'",
                "user-context": {
                    "limits": {
                        "rate-limit": "20 packets per second"
                    }
                }
            }
        ]
    else:
        classes = [
            {
                "name": "VENDOR_CLASS_eRouter1.0",
                "user-context": {
                    "limits": {
                        "rate-limit": "3 packets per second"
                    }
                }
            }
        ]
    world.dhcp_cfg["client-classes"] = classes

    srv_control.build_and_send_config_files()
    srv_control.start_srv('DHCP', 'started')

    success = 0
    packets = 0

    if dhcp_version == 'v4':
        world.cfg['wait_interval'] = 0.002
    else:
        world.cfg['wait_interval'] = 0.1
    start = time.time()
    for k in range(1, 10):
        for i in range(1, 30):
            if dhcp_version == 'v4':
                success += _get_address_v4(f'192.168.{k}.{i}', chaddr=f'ff:01:02:03:{k:0>2x}:{i:0>2x}', vendor='PXE')
            else:
                success += _get_address_v6(f'2001:db8:1::{k}:{i}', duid=f'00:03:00:01:ff:ff:ff:ff:{k:0>2x}:{i:0>2x}', vendor=True)
            packets += 1
    end = time.time()
    run1 = end - start

    print(f"Runtime of the program is {run1}")
    print(f"Packets received {success}/{packets}")
    print(f"Packets per second {success / run1}")
