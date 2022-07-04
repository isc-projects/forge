# Copyright (C) 2022 Internet Systems Consortium, Inc. ("ISC")
#
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

# Author: Marcin Godzina

"""Kea Limits Hook tests"""

# pylint: disable=invalid-name,line-too-long,unused-argument
import time
import pytest

from src import misc
from src import srv_control
from src import srv_msg

from src.forge_cfg import world


def _get_address_v4(chaddr, vendor=None):
    """
    Local function used to send Discover and check if Offer is send back.
    Can add vendor option to trigger client class in Kea.
    :param chaddr: MAC address
    :param vendor: Vendor name
    :return: 1 if Offer is received.
    """
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


def _get_address_v6(duid, vendor=None):
    """
    Local function used to send Solicit and check if Advertise is send back.
    Can add vendor option to trigger client class in Kea.
    :param duid:  DUID address
    :param vendor: Vendor name
    :return: 1 if Advertise is received.
    """
    misc.test_procedure()
    srv_msg.client_sets_value('Client', 'DUID', duid)
    srv_msg.client_does_include('Client', 'client-id')
    srv_msg.client_does_include('Client', 'IA-NA')
    if vendor is not None:
        srv_msg.client_sets_value('Client', 'vendor_class_data', vendor)
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


def _get_lease_v4(address, chaddr, vendor=None):
    """
    Local function used to send Discover and check if Offer is send back.
    If Offer is recieved, function continues with Request and Acknowledge
    Can add vendor option to trigger client class in Kea.
    :param address: expected ip
    :param chaddr: MAC address
    :param vendor: Vendor name
    :return: 1 if Offer is received.
    """
    misc.test_procedure()

    srv_msg.client_sets_value('Client', 'chaddr', chaddr)
    if vendor is not None:
        srv_msg.client_does_include_with_value('vendor_class_id', vendor)
    srv_msg.client_send_msg('DISCOVER')

    try:
        srv_msg.send_wait_for_message('MUST', 'OFFER')
    except AssertionError as e:
        if e.args[0] == 'No response received.':
            return 0
        raise AssertionError(e) from e

    srv_msg.client_save_option_count(1, 'server_id')
    srv_msg.client_add_saved_option_count(1)
    srv_msg.client_does_include_with_value('requested_addr', address)

    srv_msg.client_send_msg('REQUEST')
    srv_msg.send_wait_for_message('MUST', 'ACK')
    srv_msg.response_check_content('yiaddr', address)

    return 1

@pytest.mark.v4
@pytest.mark.v6
@pytest.mark.hook
@pytest.mark.parametrize('unit', ['second', 'minute'])
@pytest.mark.parametrize('backend', ['memfile'])
def test_rate_limits_subnet(dhcp_version, backend, unit):
    """
    Test of subnets limit of Rate Limiting Hook.
    The test makes DO or SA exchange in the fastest way possible in a unit of time (second or minute)
    and counts how many packets were sent, and how many packets were received from Kea.
    If the received packets is the same as limit, the test passes. Some error in number of packets is accounted for.
    :param unit:  Defines testing of limit per second or minute
    """
    misc.test_setup()
    srv_control.define_temporary_lease_db_backend(backend)

    # define test duration in seconds
    duration = 1 if unit == 'second' else 60

    if dhcp_version == 'v4':
        srv_control.config_srv_subnet('192.168.0.0/16', '192.168.1.1-192.168.255.255')
        srv_control.config_srv_opt('subnet-mask', '255.255.0.0')
        # define limit for hook and test
        limit = 3 if unit == 'second' else 200

    else:
        srv_control.config_srv_subnet('2001:db8:1::/64', '2001:db8:1::1-2001:db8:1::255:255')
        # define limit for hook and test
        limit = 3 if unit == 'second' else 200

    # hook configuration in user context for subnet with limit defined above
    srv_control.add_line_to_subnet(0, {"user-context": {
        "limits": {
            "rate-limit": f"{limit} packets per {unit}"
        }}})

    srv_control.open_control_channel()
    srv_control.agent_control_channel()
    srv_control.add_hooks('libdhcp_limits.so')

    srv_control.build_and_send_config_files()
    srv_control.start_srv('DHCP', 'started')

    success = 0
    packets = 0

    # Wait time for response for v4 and v6
    if dhcp_version == 'v4':
        world.cfg['wait_interval'] = 0.1
    else:
        world.cfg['wait_interval'] = 0.1

    start = time.time()
    elapsed = 0
    if dhcp_version == 'v4':
        while elapsed < duration:  # Send packets for the duration of the test, and count them.
            # Send Discover and add 1 to success counter if Forge got Offer.
            success += _get_address_v4(chaddr='ff:01:02:03:04:05')
            # Add 1 to send packets counter
            packets += 1
            # set timer to actual duration of test.
            elapsed = time.time() - start
    else:
        while elapsed < duration:  # Send packets for the duration of the test, and count them.
            # Send Solicit and add 1 to success counter if Forge got Advertise.
            success += _get_address_v6(duid='00:03:00:01:ff:ff:ff:ff:ff:ff')
            # Add 1 to send packets counter
            packets += 1
            # set timer to actual duration of test.
            elapsed = time.time() - start

    print(f"Runtime of the program is {elapsed} seconds")
    print(f"Packets received {success} from {packets} sent")
    if unit == 'second':
        print(f"Average Packets per second {success / elapsed}")
    else:
        print(f"Average Packets per minute {success / elapsed * 60}")

    # Set threshold to account for small errors in receiving packets.
    threshold = 1 if unit == 'second' else 5

    # Check if difference between limit and received packets is within threshold.
    assert abs(limit - success) <= threshold


@pytest.mark.v4
@pytest.mark.v6
@pytest.mark.hook
@pytest.mark.parametrize('unit', ['second', 'minute'])
@pytest.mark.parametrize('backend', ['memfile'])
def test_rate_limits_class(dhcp_version, backend, unit):
    """
    Test of class limit of Rate Limiting Hook.
    The test makes DO or SA exchange in the fastest way possible in a unit of time (second or minute)
    and counts how many packets were sent, and how many packets were received from Kea.
    If the received packets is the same as limit, the test passes. Some error in number of packets is accounted for.
    :param unit:  Defines testing of limit per second or minute
    """
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

    # define test duration in seconds
    duration = 1 if unit == 'second' else 60

    # hook configuration in user context for classes with limit
    if dhcp_version == 'v4':
        # define limit for hook and test
        limit = 3 if unit == 'second' else 200
        classes = [
            {
                "name": "gold",
                "test": "option[60].text == 'PXE'",
                "user-context": {
                    "limits": {
                        "rate-limit": f"{limit} packets per {unit}"
                    }
                }
            }
        ]
    else:
        # define limit for hook and test
        limit = 3 if unit == 'second' else 200
        classes = [
            {
                "name": "VENDOR_CLASS_eRouter2.0",
                "user-context": {
                    "limits": {
                        "rate-limit": f"{limit} packets per {unit}"
                    }
                }
            }
        ]
    world.dhcp_cfg["client-classes"] = classes

    srv_control.build_and_send_config_files()
    srv_control.start_srv('DHCP', 'started')

    success = 0
    packets = 0

    # Wait time for response for v4 and v6
    if dhcp_version == 'v4':
        world.cfg['wait_interval'] = 0.1
    else:
        world.cfg['wait_interval'] = 0.1

    start = time.time()
    elapsed = 0
    if dhcp_version == 'v4':
        while elapsed < duration:  # Send packets for the duration of the test, and count them.
            # Send Discover and add 1 to success counter if Forge got Offer.
            success += _get_address_v4(chaddr='ff:01:02:03:04:05', vendor='PXE')
            # Add 1 to send packets counter
            packets += 1
            # set timer to actual duration of test.
            elapsed = time.time() - start
    else:
        while elapsed < duration:  # Send packets for the duration of the test, and count them.
            # Send Solicit and add 1 to success counter if Forge got Advertise.
            success += _get_address_v6(duid='00:03:00:01:ff:ff:ff:ff:ff:ff', vendor='eRouter2.0')
            # Add 1 to send packets counter
            packets += 1
            # set timer to actual duration of test.
            elapsed = time.time() - start

    print(f"Runtime of the program is {elapsed} seconds")
    print(f"Packets received {success} from {packets} sent")
    if unit == 'second':
        print(f"Average Packets per second {success / elapsed}")
    else:
        print(f"Average Packets per minute {success / elapsed * 60}")

    # Set threshold to account for small errors in receiving packets.
    threshold = 1 if unit == 'second' else 5

    # Check if difference between limit and received packets is within threshold.
    assert abs(limit - success) <= threshold


@pytest.mark.v4
@pytest.mark.v6
@pytest.mark.hook
@pytest.mark.parametrize('backend', ['memfile'])
def test_rate_limits_mix(dhcp_version, backend):
    """
    Test of subnet and class mixed limit of Rate Limiting Hook.
    The test makes DO or SA exchange in the fastest way possible in a unit of time (second or minute)
    and counts how many packets were sent, and how many packets were received from Kea in different classes.
    If the received packets is the same as limit, the test passes. Some error in number of packets is accounted for.
    """
    misc.test_setup()
    srv_control.define_temporary_lease_db_backend(backend)
    if dhcp_version == 'v4':
        srv_control.config_srv_subnet('192.168.0.0/16', '192.168.1.1-192.168.255.255')
        srv_control.config_srv_opt('subnet-mask', '255.255.0.0')
        # define limit for hook and test
        limit = 200
    else:
        srv_control.config_srv_subnet('2001:db8:1::/64', '2001:db8:1::1-2001:db8:1::255:255')
        # define limit for hook and test
        limit = 200
    srv_control.add_line_to_subnet(0, {"user-context": {
        "limits": {
            "rate-limit": f"{limit} packets per minute"
        }}})
    srv_control.open_control_channel()
    srv_control.agent_control_channel()
    srv_control.add_hooks('libdhcp_limits.so')
    srv_control.add_hooks('libdhcp_class_cmds.so')

    # hook configuration in user context for classes with limit
    if dhcp_version == 'v4':
        gold = 3
        silver = 50
        classes = [
            {
                "name": "gold",
                "test": "option[60].text == 'PXE'",
                "user-context": {
                    "limits": {
                        "rate-limit": f"{gold} packets per second"
                    }
                }
            },
            {
                "name": "silver",
                "test": "option[60].text == 'PXA'",
                "user-context": {
                    "limits": {
                        "rate-limit": f"{silver} packets per minute"
                    }
                }
            }

        ]
    else:
        gold = 3
        silver = 50
        classes = [
            {
                "name": "VENDOR_CLASS_eRouter2.0",
                "user-context": {
                    "limits": {
                        "rate-limit": f"{gold} packets per second"
                    }
                }
            },
            {
                "name": "VENDOR_CLASS_eRouter1.0",
                "user-context": {
                    "limits": {
                        "rate-limit": f"{silver} packets per minute"
                    }
                }
            }
        ]
    world.dhcp_cfg["client-classes"] = classes

    srv_control.build_and_send_config_files()
    srv_control.start_srv('DHCP', 'started')

    success_gold = 0
    packets_gold = 0
    success_silver = 0
    packets_silver = 0
    success_noclass = 0
    packets_noclass = 0

    if dhcp_version == 'v4':
        world.cfg['wait_interval'] = 0.1
    else:
        world.cfg['wait_interval'] = 0.1
    start = time.time()
    elapsed = 0
    if dhcp_version == 'v4':
        while elapsed < 1:  # Send packets for 1 second for gold limit.
            # Send Discover and add 1 to success counter if Forge got Offer.
            success_gold += _get_address_v4(chaddr='ff:01:02:03:04:05', vendor='PXE')
            # Add 1 to send packets counter
            packets_gold += 1
            elapsed = time.time() - start
        while elapsed < 60:  # Send packets for 59 seconds for silver limit.
            # Send Discover and add 1 to success counter if Forge got Offer.
            success_silver += _get_address_v4(chaddr='ff:01:02:03:04:05', vendor='PXA')
            success_noclass += _get_address_v4(chaddr='ff:01:02:03:04:05')
            # Add 1 to send packets counter
            packets_silver += 1
            packets_noclass += 1
            # set timer to actual duration of test.
            elapsed = time.time() - start
    else:
        while elapsed < 1:  # Send packets for 1 second for gold limit.
            # Send Solicit and add 1 to success counter if Forge got Advertise.
            success_gold += _get_address_v6(duid='00:03:00:01:ff:ff:ff:ff:ff:ff', vendor='eRouter2.0')
            # Add 1 to send packets counter
            packets_gold += 1
            elapsed = time.time() - start
        while elapsed < 60:  # Send packets for 59 seconds for silver limit.
            # Send Solicit and add 1 to success counter if Forge got Advertise.
            success_silver += _get_address_v6(duid='00:03:00:01:ff:ff:ff:ff:ff:ff', vendor='eRouter1.0')
            success_noclass += _get_address_v6(duid='00:03:00:01:ff:ff:ff:ff:ff:ff')
            # Add 1 to send packets counter
            packets_silver += 1
            packets_noclass += 1
            # set timer to actual duration of test.
            elapsed = time.time() - start

    # Sum up all successes and sent packets for subnet test.
    all_success = success_gold + success_silver + success_noclass
    all_packets = packets_gold + packets_silver + packets_noclass

    print(f"Runtime of the program is {elapsed} seconds")
    print(f"All packets received {all_success} from {all_packets} sent")
    print(f"Gold Packets received {success_gold} from {packets_gold} sent")
    print(f"Average Gold Packets per second {success_gold / elapsed * 60}")
    print(f"Silver Packets received {success_silver} from {packets_silver} sent")
    print(f"Average Silver Packets per minute {success_silver / elapsed * 60}")

    # Set threshold to account for small errors in receiving packets.
    threshold_subnet = 5
    threshold_gold = 1
    threshold_silver = 1

    # Check if difference between limit and received packets is within threshold.
    assert abs(limit - all_success) <= threshold_subnet
    assert abs(gold - success_gold) <= threshold_gold
    assert abs(silver - success_silver) <= threshold_silver


@pytest.mark.v4
# @pytest.mark.v6
@pytest.mark.hook
@pytest.mark.parametrize('backend', ['memfile'])
def test_lease_limits_subnet(dhcp_version, backend):
    misc.test_setup()
    srv_control.define_temporary_lease_db_backend(backend)

    if dhcp_version == 'v4':
        srv_control.config_srv_subnet('192.168.0.0/16', '192.168.1.1-192.168.255.255')
        srv_control.config_srv_opt('subnet-mask', '255.255.0.0')
        # define limit for hook and test
        limit = 3

    # hook configuration in user context for subnet with limit defined above
    # srv_control.add_line_to_subnet(0, {"user-context": {
    #     "limits": {
    #         "address-limit": limit
    #     }}})

    srv_control.open_control_channel()
    srv_control.agent_control_channel()
    # srv_control.add_hooks('libdhcp_limits.so')

    srv_control.build_and_send_config_files()
    srv_control.start_srv('DHCP', 'started')

    success = 0
    exchanges = 0

    # Wait time for response for v4 and v6
#    if dhcp_version == 'v4':
#        world.cfg['wait_interval'] = 0.1
#    else:
#        world.cfg['wait_interval'] = 0.1

#    start = time.time()
    elapsed = 0
    to_send = 20

    if dhcp_version == 'v4':
        for i in range(1, 5):
            #success += _get_lease_v4(f'192.168.1.{i}', f'ff:01:02:03:04:{i:02}', vendor=None)
            srv_msg.DORA(address=f'192.168.1.{i}', chaddr=f'ff:01:02:03:04:{i:02}', subnet_mask='255.255.0.0')
            exchanges += 1

    # Set threshold to account for small errors in receiving packets.
    threshold = 1

    # Check if difference between limit and received packets is within threshold.
    print(f"exchanges made: {exchanges}")
    print(f"successes made: {success}")
