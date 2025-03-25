# Copyright (C) 2022-2023 Internet Systems Consortium, Inc. ("ISC")
#
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

# pylint: disable=invalid-name
# pylint: disable=too-many-branches

# Author: Marcin Godzina

"""Kea Limits Hook tests"""
import time
import secrets
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
    If Offer is received, function continues with Request and Acknowledge
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

    misc.pass_criteria()
    try:
        srv_msg.send_wait_for_message('MUST', 'OFFER')
    except AssertionError as e:
        if e.args[0] == 'No response received.':
            return 0
        raise AssertionError(e) from e
    srv_msg.response_check_content('yiaddr', address)

    misc.test_procedure()
    srv_msg.client_sets_value('Client', 'chaddr', chaddr)
    srv_msg.client_copy_option('server_id')
    srv_msg.client_does_include_with_value('requested_addr', address)
    if vendor is not None:
        srv_msg.client_does_include_with_value('vendor_class_id', vendor)

    srv_msg.client_send_msg('REQUEST')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', 'ACK')
    srv_msg.response_check_content('yiaddr', address)
    return 1


def _get_lease_v6(address, duid, vendor=None, ia_na=None, ia_pd=None):
    """
    Local function used to send Solicit and check if Advertise is send back.
    If Advertise is received with address, function continues with Request and Reply
    Can add vendor option to trigger client class in Kea.
    :param address: expected ip
    :param vendor: Vendor name
    :return: 1 if Offer is received.
    """
    successes = 0
    misc.test_procedure()
    srv_msg.client_sets_value('Client', 'DUID', duid)
    srv_msg.client_does_include('Client', 'client-id')
    if ia_na is not None:
        srv_msg.client_does_include('Client', 'IA_Address')
        srv_msg.client_does_include('Client', 'IA-NA')
    if ia_pd is not None:
        srv_msg.client_does_include('Client', 'IA-PD')

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

    if ia_na is not None:
        try:
            srv_msg.check_IA_NA(address)
            successes += 1
        except AssertionError as e:
            if e.args[0] == 'Expected sub-option DHCP6OptIAAddress[5], ' \
                            'but it is not present in the option DHCP6OptIA_NA[3]':
                ia_na = None
            else:
                raise AssertionError(e) from e
    if ia_pd is not None:
        srv_msg.response_check_include_option(25)
        try:
            srv_msg.response_check_option_content(25, 'sub-option', 26)
            successes += 1
        except AssertionError as e:
            if e.args[0] == 'Expected sub-option DHCP6OptIAPrefix[26], ' \
                            'but it is not present in the option DHCP6OptIA_PD[25]':
                ia_pd = None
            else:
                raise AssertionError(e) from e
    if successes == 0:
        return 0
    # Build and send a request.
    if ia_na is not None:
        srv_msg.client_copy_option('IA_NA')
    if ia_pd is not None:
        srv_msg.client_copy_option('IA_PD')
    srv_msg.client_copy_option('server-id')
    srv_msg.client_sets_value('Client', 'DUID', duid)
    srv_msg.client_does_include('Client', 'client-id')
    if vendor is not None:
        srv_msg.client_sets_value('Client', 'vendor_class_data', vendor)
        srv_msg.client_does_include('Client', 'vendor-class')
    srv_msg.client_send_msg('REQUEST')

    # Expect a reply.
    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', 'REPLY')
    if ia_na is not None:
        srv_msg.check_IA_NA(address)
    if ia_pd is not None:
        srv_msg.response_check_include_option(25)
        srv_msg.response_check_option_content(25, 'sub-option', 26)

    return successes


@pytest.mark.v4
@pytest.mark.v6
@pytest.mark.hook
@pytest.mark.limits_hook
@pytest.mark.parametrize('unit', ['second', 'minute'])
@pytest.mark.parametrize('backend', ['memfile'])
def test_rate_limits_subnet(dhcp_version, backend, unit):
    """
    Test of subnets limit of rate limiting in Limits Hook.
    The test makes DO or SA exchange in the fastest way possible in a unit of time (second or minute)
    and counts how many packets were sent, and how many packets were received from Kea.
    If the received packets is the same as limit, the test passes. Some error in number of packets is accounted for.
    :type dhcp_version: str
    :param dhcp_version: The DHCP version being tested ('v4' or 'v6').
    :type backend: str
    :param backend: The backend being used for the test ('memfile', 'mysql', or 'postgresql').
    :type unit: str
    :param unit:  Defines testing of limit per second or minute
    """
    misc.test_setup()
    srv_control.define_lease_db_backend(backend)

    # define test duration in seconds
    duration = 1 if unit == 'second' else 60
    limit = 3 if unit == 'second' else 200

    if dhcp_version == 'v4':
        srv_control.config_srv_subnet('192.168.1.0/24', '192.168.1.1-192.168.1.255')
        srv_control.config_srv_opt('subnet-mask', '255.255.255.0')
        # define limit for hook and test

    else:
        srv_control.config_srv_subnet('2001:db8:1::/64', '2001:db8:1::1-2001:db8:1::255:255')
        # define limit for hook and test

    # hook configuration in user context for subnet with limit defined above
    srv_control.add_line_to_subnet(0, {"user-context": {
        "limits": {
            "rate-limit": f"{limit} packets per {unit}"
        }}})

    srv_control.add_unix_socket()
    srv_control.add_http_control_channel()
    srv_control.add_hooks('libdhcp_limits.so')

    srv_control.build_and_send_config_files()
    srv_control.start_srv('DHCP', 'started')

    success = 0
    packets = 0

    # Wait time for response for v4 and v6
    world.cfg['wait_interval'] = 0.1
    if dhcp_version == 'v6':
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
    assert abs(limit - success) <= threshold, f'Difference between responses and limit ({abs(limit - success)})' \
                                              f' exceeds threshold ({threshold})'


@pytest.mark.v4
@pytest.mark.v6
@pytest.mark.hook
@pytest.mark.limits_hook
@pytest.mark.parametrize('unit', ['second', 'minute'])
@pytest.mark.parametrize('backend', ['memfile'])
def test_rate_limits_class(dhcp_version, backend, unit):
    """
    Test of class limit of rate limiting in Limits Hook..
    The test makes DO or SA exchange in the fastest way possible in a unit of time (second or minute)
    and counts how many packets were sent, and how many packets were received from Kea.
    If the received packets is the same as limit, the test passes. Some error in number of packets is accounted for.
    :type dhcp_version: str
    :param dhcp_version: The DHCP version being tested ('v4' or 'v6').
    :type backend: str
    :param backend: The backend being used for the test ('memfile', 'mysql', or 'postgresql').
    :type unit: str
    :param unit:  Defines testing of limit per second or minute
    """
    misc.test_setup()
    srv_control.define_lease_db_backend(backend)
    if dhcp_version == 'v4':
        srv_control.config_srv_subnet('192.168.1.0/24', '192.168.1.1-192.168.1.255')
        srv_control.config_srv_opt('subnet-mask', '255.255.255.0')
    else:
        srv_control.config_srv_subnet('2001:db8:1::/64', '2001:db8:1::1-2001:db8:1::255:255')
    srv_control.add_unix_socket()
    srv_control.add_http_control_channel()
    srv_control.add_hooks('libdhcp_limits.so')

    # define test duration in seconds
    duration = 1 if unit == 'second' else 60

    # hook configuration in user context for classes with limit
    limit = 3 if unit == 'second' else 200
    if dhcp_version == 'v4':
        # define limit for hook and test
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
    world.cfg['wait_interval'] = 0.1
    if dhcp_version == 'v6':
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
    assert abs(limit - success) <= threshold, f'Difference between responses and limit ({abs(limit - success)})' \
                                              f' exceeds threshold ({threshold})'


@pytest.mark.v4
@pytest.mark.v6
@pytest.mark.hook
@pytest.mark.limits_hook
@pytest.mark.parametrize('unit', ['second', 'minute'])
@pytest.mark.parametrize('backend', ['memfile'])
def test_rate_limits_builtin_class(dhcp_version, backend, unit):
    """
    Test of rate limits for built-in classes in Limits Hook.
    The test makes DO or SA exchange in the fastest way possible in a unit of time (second or minute)
    and counts how many packets were sent, and how many packets were received from Kea.
    If the received packets is the same as limit, the test passes. Some error in number of packets is accounted for.
    :type dhcp_version: str
    :param dhcp_version: The DHCP version being tested ('v4' or 'v6').
    :type backend: str
    :param backend: The backend being used for the test ('memfile', 'mysql', or 'postgresql').
    :type unit: str
    :param unit:  Defines testing of limit per second or minute
    """
    misc.test_setup()
    srv_control.define_lease_db_backend(backend)
    if dhcp_version == 'v4':
        srv_control.config_srv_subnet('192.168.1.0/24', '192.168.1.1-192.168.1.255')
        srv_control.config_srv_opt('subnet-mask', '255.255.255.0')
    else:
        srv_control.config_srv_subnet('2001:db8:1::/64', '2001:db8:1::1-2001:db8:1::255:255')
    srv_control.add_unix_socket()
    srv_control.add_http_control_channel()
    srv_control.add_hooks('libdhcp_limits.so')

    # define test duration in seconds
    duration = 1 if unit == 'second' else 60

    # hook configuration in user context for classes with limit
    limit = 3 if unit == 'second' else 200
    if dhcp_version == 'v4':
        # define limit for hook and test
        classes = [
            {
                "name": "ALL",
                "user-context": {
                    "limits": {
                        "rate-limit": f"{limit} packets per {unit}"
                    }
                }
            }
        ]
    else:
        # define limit for hook and test
        classes = [
            {
                "name": "ALL",
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
    world.cfg['wait_interval'] = 0.1
    if dhcp_version == 'v6':
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
    assert abs(limit - success) <= threshold, f'Difference between responses and limit ({abs(limit - success)})' \
                                              f' exceeds threshold ({threshold})'


@pytest.mark.v4
@pytest.mark.v6
@pytest.mark.hook
@pytest.mark.limits_hook
@pytest.mark.parametrize('backend', ['memfile'])
def test_rate_limits_mix(dhcp_version, backend):
    """
    Test of subnet and class mixed limit of rate limiting in Limits Hook.
    The test makes DO or SA exchange in the fastest way possible in a unit of time (second or minute)
    and counts how many packets were sent, and how many packets were received from Kea in different classes.
    If the received packets is the same as limit, the test passes. Some error in number of packets is accounted for.
    :type dhcp_version: str
    :param dhcp_version: The DHCP version being tested ('v4' or 'v6').
    :type backend: str
    :param backend: The backend being used for the test ('memfile', 'mysql', or 'postgresql').
    """
    misc.test_setup()
    srv_control.define_lease_db_backend(backend)
    limit = 200
    if dhcp_version == 'v4':
        srv_control.config_srv_subnet('192.168.1.0/24', '192.168.1.1-192.168.1.255')
        srv_control.config_srv_opt('subnet-mask', '255.255.255.0')
        # define limit for hook and test
    else:
        srv_control.config_srv_subnet('2001:db8:1::/64', '2001:db8:1::1-2001:db8:1::255:255')
        # define limit for hook and test
    srv_control.add_line_to_subnet(0, {"user-context": {
        "limits": {
            "rate-limit": f"{limit} packets per minute"
        }}})
    srv_control.add_unix_socket()
    srv_control.add_http_control_channel()
    srv_control.add_hooks('libdhcp_limits.so')

    # hook configuration in user context for classes with limit
    gold = 3
    silver = 50
    if dhcp_version == 'v4':
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

    world.cfg['wait_interval'] = 0.1
    if dhcp_version == 'v6':
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
    assert abs(limit - all_success) <= threshold_subnet, \
        f'Difference between responses and limit ({abs(limit - all_success)})' \
        f' exceeds Subnet threshold ({threshold_subnet})'
    assert abs(gold - success_gold) <= threshold_gold, \
        f'Difference between responses and limit ({abs(gold - success_gold)})' \
        f' exceeds Gold Class threshold ({threshold_gold})'
    assert abs(silver - success_silver) <= threshold_silver, \
        f'Difference between responses and limit ({abs(silver - success_silver)})' \
        f' exceeds Silver Class threshold ({threshold_silver})'


@pytest.mark.v4
@pytest.mark.v6
@pytest.mark.hook
@pytest.mark.limits_hook
@pytest.mark.parametrize('backend', ['memfile', 'mysql', 'postgresql'])
def test_lease_limits_subnet(dhcp_version, backend):
    """
    Test of subnets lease limit in Limits Hook.
    The test makes DORA or SARR exchange to acquire leases and counts if dropped or returned
    "no leases available".
    Test removes leases and tries again to check if the limit is restored.
    If the received leases is the same as limit, the test passes.
    Some error in number of packets is accounted for.
    :type dhcp_version: str
    :param dhcp_version: The DHCP version being tested ('v4' or 'v6').
    :type backend: str
    :param backend: The backend being used for the test ('memfile', 'mysql', or 'postgresql').
    """
    misc.test_setup()
    srv_control.define_lease_db_backend(backend)
    # define limit for hook and test
    limit = 5
    if dhcp_version == 'v4':
        srv_control.config_srv_subnet('192.168.1.0/24', '192.168.1.1-192.168.1.255')
        srv_control.config_srv_opt('subnet-mask', '255.255.255.0')
    else:
        srv_control.config_srv_subnet('2001:db8:1::/64', '2001:db8:1::1-2001:db8:1::255:255')
        srv_control.config_srv_prefix('2002:db8:1::', 0, 90, 96)

    # hook configuration in user context for subnet with limit defined above
    srv_control.add_line_to_subnet(0, {"user-context": {
        "limits": {
            "address-limit": limit,
            "prefix-limit": limit
        }}})

    srv_control.add_unix_socket()
    srv_control.add_http_control_channel()
    srv_control.add_hooks('libdhcp_limits.so')
    srv_control.add_hooks('libdhcp_lease_cmds.so')
    srv_control.build_and_send_config_files()
    srv_control.start_srv('DHCP', 'started')

    success = 0
    if dhcp_version == 'v6':
        success_na = 0
        success_pd = 0
    exchanges = 0
    to_send = 9

    if dhcp_version == 'v4':
        for i in range(1, to_send + 1):  # Try to acquire more leases than the limit.
            # Try exchanging DORA and add 1 to success counter if Forge got ACK.
            success += _get_lease_v4(f'192.168.1.{i}', f'ff:01:02:03:04:{i:02}', vendor=None)
            # Add 1 to exchanges counter
            exchanges += 1

        for i in range(1, success + 1):  # Delete all acquired leases to reset limit.
            cmd = {"command": "lease4-del", "arguments": {"ip-address": f'192.168.1.{i}'}}
            srv_msg.send_ctrl_cmd(cmd)

        for i in range(to_send + 1, 2 * to_send + 1):  # Try to acquire more leases than the limit.
            success += _get_lease_v4(f'192.168.1.{i}', f'ff:01:02:03:04:{i:02}', vendor=None)
            exchanges += 1

    else:
        # IA_NA
        for i in range(1, to_send + 1):  # Try to acquire more IA_NA leases than the limit.
            # Try exchanging SARR and add 1 to success counter if Forge got Reply with lease.
            success_na += _get_lease_v6(f'2001:db8:1::{hex(i)[2:]}', f'00:03:00:01:ff:ff:ff:ff:ff:{i:02}', ia_na=True)
            # Add 1 to exchanges counter
            exchanges += 1

        batch1 = success_na

        for i in range(1, success_na + 1):  # Delete all acquired leases to reset limit.
            cmd = {"command": "lease6-del", "arguments": {"ip-address": f'2001:db8:1::{hex(i)[2:]}'}}
            srv_msg.send_ctrl_cmd(cmd)

        for i in range(to_send + 1, 2 * to_send + 1):  # Try to acquire more leases than the limit.
            success_na += _get_lease_v6(f'2001:db8:1::{hex(i)[2:]}', f'00:03:00:01:ff:ff:ff:ff:ff:{i:02}', ia_na=True)
            exchanges += 1

        for i in range(to_send + 1, to_send + success_na - batch1 + 1):  # Delete all acquired leases to reset limit.
            cmd = {"command": "lease6-del", "arguments": {"ip-address": f'2001:db8:1::{hex(i)[2:]}'}}
            srv_msg.send_ctrl_cmd(cmd)

        # IA_PD
        for i in range(2 * to_send + 1, 3 * to_send + 1):  # Try to acquire more IA_PD leases than the limit
            # Try exchanging SARR and add 1 to success counter if Forge got Reply with lease.
            success_pd += _get_lease_v6(f'2001:db8:1::{hex(i)[2:]}', f'00:03:00:01:ff:ff:ff:ff:ff:{i:02}', ia_pd=1)
            # Add 1 to exchanges counter
            exchanges += 1

        for i in range(2 * to_send + 1, 2 * to_send + 1 + success_pd):  # Delete all acquired leases to reset limit.
            cmd = {"command": "lease6-get-by-duid", "arguments": {"duid": f'00:03:00:01:ff:ff:ff:ff:ff:{i:02}'}}
            response = srv_msg.send_ctrl_cmd(cmd)
            iaid = response['arguments']['leases'][0]['iaid']
            cmd = {"command": "lease6-del",
                   "arguments": {"subnet-id": 1,
                                 "identifier": f'00:03:00:01:ff:ff:ff:ff:ff:{i:02}',
                                 "identifier-type": "duid",
                                 "iaid": iaid,
                                 "type": "IA_PD"}}
            srv_msg.send_ctrl_cmd(cmd)

        for i in range(3 * to_send + 1, 4 * to_send + 1):  # Try to acquire more leases than the limit.
            success_pd += _get_lease_v6(f'2001:db8:1::{hex(i)[2:]}', f'00:03:00:01:ff:ff:ff:ff:ff:{i:02}', ia_pd=1)
            exchanges += 1

        success = success_na + success_pd

    # Set threshold to account for small errors in receiving packets.
    threshold = 1

    print(f"exchanges made: {exchanges}")
    print(f"successes made: {success}")

    # Check if difference between limit and received packets is within threshold.
    if dhcp_version == 'v4':
        assert abs(2 * limit - success) <= threshold, \
            f'Difference between responses and limit ({abs(2 * limit - success)}) exceeds threshold ({threshold})'
    else:
        assert abs(4 * limit - success) <= threshold, \
            f'Difference between responses and limit ({abs(4 * limit - success)}) exceeds threshold ({threshold})'


@pytest.mark.v4
@pytest.mark.v6
@pytest.mark.hook
@pytest.mark.limits_hook
@pytest.mark.parametrize('backend', ['memfile', 'mysql', 'postgresql'])
def test_lease_limits_class(dhcp_version, backend):
    """
    Test of class lease limit in Limits Hook.
    The test makes DORA or SARR exchange to acquire leases and counts if dropped or returned
    "no leases available".
    Test removes leases and tries again to check if the limit is restored.
    If the received leases is the same as limit, the test passes.
    Some error in number of packets is accounted for.
    :type dhcp_version: str
    :param dhcp_version: The DHCP version being tested ('v4' or 'v6').
    :type backend: str
    :param backend: The backend being used for the test ('memfile', 'mysql', or 'postgresql').
    """
    misc.test_setup()
    srv_control.define_lease_db_backend(backend)
    # define limit for hook and test
    limit = 5
    if dhcp_version == 'v4':
        srv_control.config_srv_subnet('192.168.1.0/24', '192.168.1.1-192.168.1.255')
        srv_control.config_srv_opt('subnet-mask', '255.255.255.0')
    else:
        srv_control.config_srv_subnet('2001:db8:1::/64', '2001:db8:1::1-2001:db8:1::255:255')
        srv_control.config_srv_prefix('2002:db8:1::', 0, 90, 96)

    # hook configuration in user context for classes with limit
    if dhcp_version == 'v4':
        classes = [
            {
                "name": "gold",
                "test": "option[60].text == 'PXE'",
                "user-context": {
                    "limits": {
                        "address-limit": limit
                    }
                }
            },
            {
                "name": "silver",
                "test": "option[60].text == 'PXA'",
                "user-context": {
                    "limits": {
                        "address-limit": limit
                    }
                }
            }

        ]
    else:
        classes = [
            {
                "name": "VENDOR_CLASS_eRouter2.0",
                "user-context": {
                    "limits": {
                        "address-limit": limit,
                        "prefix-limit": limit
                    }
                }
            },
            {
                "name": "VENDOR_CLASS_eRouter1.0",
                "user-context": {
                    "limits": {
                        "address-limit": limit,
                        "prefix-limit": limit
                    }
                }
            }
        ]
    world.dhcp_cfg["client-classes"] = classes

    srv_control.add_unix_socket()
    srv_control.add_http_control_channel()
    srv_control.add_hooks('libdhcp_limits.so')
    srv_control.add_hooks('libdhcp_lease_cmds.so')
    srv_control.build_and_send_config_files()
    srv_control.start_srv('DHCP', 'started')

    success = 0
    if dhcp_version == 'v6':
        success_na = 0
        success_pd = 0
    exchanges = 0
    to_send = 9

    if dhcp_version == 'v4':
        for i in range(1, to_send + 1):  # Try to acquire more leases than the limit.
            # Try exchanging DORA and add 1 to success counter if Forge got ACK.
            success += _get_lease_v4(f'192.168.1.{i}', f'ff:01:02:03:04:{i:02}', vendor='PXE')
            # Add 1 to exchanges counter
            exchanges += 1

        for i in range(1, success + 1):  # Delete all acquired leases to reset limit.
            cmd = {"command": "lease4-del", "arguments": {"ip-address": f'192.168.1.{i}'}}
            srv_msg.send_ctrl_cmd(cmd)

        for i in range(to_send + 1, 2 * to_send + 1):  # Try to acquire more leases than the limit.
            success += _get_lease_v4(f'192.168.1.{i}', f'ff:01:02:03:04:{i:02}', vendor='PXE')
            exchanges += 1

        # Try to acquire more leases than the limit with second class.
        for i in range(2 * to_send + 1, 3 * to_send + 1):
            success += _get_lease_v4(f'192.168.1.{i}', f'ff:01:02:03:04:{i:02}', vendor='PXA')
            exchanges += 1

    else:
        # IA_NA
        for i in range(1, to_send + 1):  # Try to acquire more IA_NA leases than the limit.
            # Try exchanging SARR and add 1 to success counter if Forge got Reply with lease.
            success_na += _get_lease_v6(f'2001:db8:1::{hex(i)[2:]}', f'00:03:00:01:ff:ff:ff:ff:ff:{i:02}',
                                        vendor='eRouter2.0', ia_na=True)
            # Add 1 to exchanges counter
            exchanges += 1

        for i in range(1, success_na + 1):  # Delete all acquired leases to reset limit.
            cmd = {"command": "lease6-del", "arguments": {"ip-address": f'2001:db8:1::{hex(i)[2:]}'}}
            srv_msg.send_ctrl_cmd(cmd)

        for i in range(to_send + 1, 2 * to_send + 1):  # Try to acquire more IA_NA leases than the limit.
            success_na += _get_lease_v6(f'2001:db8:1::{hex(i)[2:]}', f'00:03:00:01:ff:ff:ff:ff:ff:{i:02}',
                                        vendor='eRouter2.0', ia_na=True)
            exchanges += 1

        # Try to acquire more IA_NA leases than the limit of second class.
        for i in range(2 * to_send + 1, 3 * to_send + 1):
            success_na += _get_lease_v6(f'2001:db8:1::{hex(i)[2:]}', f'00:03:00:01:ff:ff:ff:ff:ff:{i:02}',
                                        vendor='eRouter1.0', ia_na=True)
            exchanges += 1

        # IA_PD
        for i in range(3 * to_send + 1, 4 * to_send + 1):  # Try to acquire more IA_PD leases than the limit
            # Try exchanging SARR and add 1 to success counter if Forge got Reply with lease.
            success_pd += _get_lease_v6(f'2001:db8:1::{hex(i)[2:]}', f'00:03:00:01:ff:ff:ff:ff:ff:{i:02}',
                                        ia_pd=1, vendor='eRouter2.0')
            exchanges += 1

        for i in range(3 * to_send + 1, 3 * to_send + 1 + success_pd):  # Delete all acquired leases to reset limit.
            cmd = {"command": "lease6-get-by-duid", "arguments": {"duid": f'00:03:00:01:ff:ff:ff:ff:ff:{i:02}'}}
            response = srv_msg.send_ctrl_cmd(cmd)
            iaid = response['arguments']['leases'][0]['iaid']

            cmd = {"command": "lease6-del",
                   "arguments": {"subnet-id": 1,
                                 "identifier": f'00:03:00:01:ff:ff:ff:ff:ff:{i:02}',
                                 "identifier-type": "duid",
                                 "iaid": iaid,
                                 "type": "IA_PD"}}
            srv_msg.send_ctrl_cmd(cmd)

        for i in range(4 * to_send + 1, 5 * to_send + 1):
            success_pd += _get_lease_v6(f'2001:db8:1::{hex(i)[2:]}', f'00:03:00:01:ff:ff:ff:ff:ff:{i:02}',
                                        ia_pd=1, vendor='eRouter2.0')
            exchanges += 1

        # Try to acquire more IA_PD leases than the limit of second class.
        for i in range(5 * to_send + 1, 6 * to_send + 1):
            success_pd += _get_lease_v6(f'2001:db8:1::{hex(i)[2:]}', f'00:03:00:01:ff:ff:ff:ff:ff:{i:02}',
                                        ia_pd=1, vendor='eRouter1.0')
            exchanges += 1

        success = success_na + success_pd

    # Set threshold to account for small errors in receiving packets.
    threshold = 1

    print(f"exchanges made: {exchanges}")
    print(f"successes made: {success}")

    # Check if difference between limit and received packets is within threshold.
    if dhcp_version == 'v4':
        assert abs(3 * limit - success) <= threshold, \
            f'Difference between responses and limit ({abs(3 * limit - success)}) exceeds threshold ({threshold})'
    else:
        assert abs(6 * limit - success) <= threshold, \
            f'Difference between responses and limit ({abs(6 * limit - success)}) exceeds threshold ({threshold})'


@pytest.mark.v4
@pytest.mark.v6
@pytest.mark.hook
@pytest.mark.limits_hook
@pytest.mark.parametrize('backend', ['memfile', 'mysql', 'postgresql'])
def test_lease_limits_builtin_class(dhcp_version, backend):
    """
    Test of class limit for built-in classes in Limits Hook.
    The test makes DORA or SARR exchange to acquire leases and counts if dropped or returned
    "no leases available".
    Test removes leases and tries again to check if the limit is restored.
    If the received leases is the same as limit, the test passes.
    Some error in number of packets is accounted for.
    :type dhcp_version: str
    :param dhcp_version: The DHCP version being tested ('v4' or 'v6').
    :type backend: str
    :param backend: The backend being used for the test ('memfile', 'mysql', or 'postgresql').
    """
    misc.test_setup()
    srv_control.define_lease_db_backend(backend)
    # define limit for hook and test
    limit = 5
    if dhcp_version == 'v4':
        srv_control.config_srv_subnet('192.168.1.0/24', '192.168.1.1-192.168.1.255')
        srv_control.config_srv_opt('subnet-mask', '255.255.255.0')
    else:
        srv_control.config_srv_subnet('2001:db8:1::/64', '2001:db8:1::1-2001:db8:1::255:255')
        srv_control.config_srv_prefix('2002:db8:1::', 0, 90, 96)

    # hook configuration in user context for classes with limit
    if dhcp_version == 'v4':
        classes = [
            {
                "name": "ALL",
                "user-context": {
                    "limits": {
                        "address-limit": limit
                    }
                }
            }
        ]
    else:
        classes = [
            {
                "name": "ALL",
                "user-context": {
                    "limits": {
                        "address-limit": limit,
                        "prefix-limit": limit
                    }
                }
            }
        ]
    world.dhcp_cfg["client-classes"] = classes

    srv_control.add_unix_socket()
    srv_control.add_http_control_channel()
    srv_control.add_hooks('libdhcp_limits.so')
    srv_control.add_hooks('libdhcp_lease_cmds.so')
    srv_control.build_and_send_config_files()
    srv_control.start_srv('DHCP', 'started')

    success = 0
    if dhcp_version == 'v6':
        success_na = 0
        success_pd = 0
    exchanges = 0
    to_send = 9

    if dhcp_version == 'v4':
        for i in range(1, to_send + 1):  # Try to acquire more leases than the limit.
            # Try exchanging DORA and add 1 to success counter if Forge got ACK.
            success += _get_lease_v4(f'192.168.1.{i}', f'ff:01:02:03:04:{i:02}')
            # Add 1 to exchanges counter
            exchanges += 1

        for i in range(1, success + 1):  # Delete all acquired leases to reset limit.
            cmd = {"command": "lease4-del", "arguments": {"ip-address": f'192.168.1.{i}'}}
            srv_msg.send_ctrl_cmd(cmd)

        for i in range(to_send + 1, 2 * to_send + 1):  # Try to acquire more leases than the limit.
            success += _get_lease_v4(f'192.168.1.{i}', f'ff:01:02:03:04:{i:02}')
            exchanges += 1

    else:
        # IA_NA
        for i in range(1, to_send + 1):  # Try to acquire more IA_NA leases than the limit.
            # Try exchanging SARR and add 1 to success counter if Forge got Reply with lease.
            success_na += _get_lease_v6(f'2001:db8:1::{hex(i)[2:]}', f'00:03:00:01:ff:ff:ff:ff:ff:{i:02}',
                                        ia_na=True)
            # Add 1 to exchanges counter
            exchanges += 1

        for i in range(1, success_na + 1):  # Delete all acquired leases to reset limit.
            cmd = {"command": "lease6-del", "arguments": {"ip-address": f'2001:db8:1::{hex(i)[2:]}'}}
            srv_msg.send_ctrl_cmd(cmd)

        for i in range(to_send + 1, 2 * to_send + 1):  # Try to acquire more IA_NA leases than the limit.
            success_na += _get_lease_v6(f'2001:db8:1::{hex(i)[2:]}', f'00:03:00:01:ff:ff:ff:ff:ff:{i:02}',
                                        ia_na=True)
            exchanges += 1

        # IA_PD
        for i in range(3 * to_send + 1, 4 * to_send + 1):  # Try to acquire more IA_PD leases than the limit
            # Try exchanging SARR and add 1 to success counter if Forge got Reply with lease.
            success_pd += _get_lease_v6(f'2001:db8:1::{hex(i)[2:]}', f'00:03:00:01:ff:ff:ff:ff:ff:{i:02}',
                                        ia_pd=1)
            exchanges += 1

        for i in range(3 * to_send + 1, 3 * to_send + 1 + success_pd):  # Delete all acquired leases to reset limit.
            cmd = {"command": "lease6-get-by-duid", "arguments": {"duid": f'00:03:00:01:ff:ff:ff:ff:ff:{i:02}'}}
            response = srv_msg.send_ctrl_cmd(cmd)
            iaid = response['arguments']['leases'][0]['iaid']

            cmd = {"command": "lease6-del",
                   "arguments": {"subnet-id": 1,
                                 "identifier": f'00:03:00:01:ff:ff:ff:ff:ff:{i:02}',
                                 "identifier-type": "duid",
                                 "iaid": iaid,
                                 "type": "IA_PD"}}
            srv_msg.send_ctrl_cmd(cmd)

        for i in range(4 * to_send + 1, 5 * to_send + 1):
            success_pd += _get_lease_v6(f'2001:db8:1::{hex(i)[2:]}', f'00:03:00:01:ff:ff:ff:ff:ff:{i:02}',
                                        ia_pd=1)
            exchanges += 1

        success = success_na + success_pd

    # Set threshold to account for small errors in receiving packets.
    threshold = 1

    print(f"exchanges made: {exchanges}")
    print(f"successes made: {success}")

    # Check if difference between limit and received packets is within threshold.
    if dhcp_version == 'v4':
        assert abs(2 * limit - success) <= threshold, \
            f'Difference between responses and limit ({abs(2 * limit - success)}) exceeds threshold ({threshold})'
    else:
        assert abs(4 * limit - success) <= threshold, \
            f'Difference between responses and limit ({abs(4 * limit - success)}) exceeds threshold ({threshold})'


@pytest.mark.v4
@pytest.mark.v6
@pytest.mark.hook
@pytest.mark.limits_hook
@pytest.mark.parametrize('backend', ['memfile', 'mysql', 'postgresql'])
def test_lease_limits_mix(dhcp_version, backend):
    """
    Test of subnet and class lease limit in Limits Hook.
    The test makes DORA or SARR exchange to acquire leases and counts if dropped or returned
    "no leases available".
    Test removes leases and tries again to check if the limit is restored.
    If the received leases is the same as limit, the test passes.
    Some error in number of packets is accounted for.
    :type dhcp_version: str
    :param dhcp_version: The DHCP version being tested ('v4' or 'v6').
    :type backend: str
    :param backend: The backend being used for the test ('memfile', 'mysql', or 'postgresql').
    """
    misc.test_setup()
    srv_control.define_lease_db_backend(backend)
    # define limit for hook and test
    limit_subnet = 15
    limit_class = 5
    if dhcp_version == 'v4':
        srv_control.config_srv_subnet('192.168.1.0/24', '192.168.1.1-192.168.1.255')
        srv_control.config_srv_opt('subnet-mask', '255.255.255.0')
    else:
        srv_control.config_srv_subnet('2001:db8:1::/64', '2001:db8:1::1-2001:db8:1::255:255')
        srv_control.config_srv_prefix('2002:db8:1::', 0, 90, 96)

    # hook configuration in user context for subnet with limit defined above
    srv_control.add_line_to_subnet(0, {"user-context": {
        "limits": {
            "address-limit": limit_subnet,
            "prefix-limit": limit_subnet
        }}})

    # hook configuration in user context for classes with limit
    if dhcp_version == 'v4':
        classes = [
            {
                "name": "gold",
                "test": "option[60].text == 'PXE'",
                "user-context": {
                    "limits": {
                        "address-limit": limit_class
                    }
                }
            },
            {
                "name": "silver",
                "test": "option[60].text == 'PXA'",
                "user-context": {
                    "limits": {
                        "address-limit": limit_class
                    }
                }
            }

        ]
    else:
        classes = [
            {
                "name": "VENDOR_CLASS_eRouter2.0",
                "user-context": {
                    "limits": {
                        "address-limit": limit_class,
                        "prefix-limit": limit_class
                    }
                }
            },
            {
                "name": "VENDOR_CLASS_eRouter1.0",
                "user-context": {
                    "limits": {
                        "address-limit": limit_class,
                        "prefix-limit": limit_class
                    }
                }
            }
        ]
    world.dhcp_cfg["client-classes"] = classes

    srv_control.add_unix_socket()
    srv_control.add_http_control_channel()
    srv_control.add_hooks('libdhcp_limits.so')
    srv_control.add_hooks('libdhcp_lease_cmds.so')
    srv_control.build_and_send_config_files()
    srv_control.start_srv('DHCP', 'started')

    success = 0
    if dhcp_version == 'v4':
        success_class = 0
        success_noclass = 0
    else:
        success_na = 0
        success_pd = 0
        success_noclass = 0
    exchanges = 0
    to_send = 9

    if dhcp_version == 'v4':
        for i in range(1, to_send + 1):  # Try to acquire more leases than the limit.
            # Try exchanging DORA and add 1 to success counter if Forge got ACK.
            success_class += _get_lease_v4(f'192.168.1.{i}', f'ff:01:02:03:04:{i:02}', vendor='PXE')
            # Add 1 to exchanges counter
            exchanges += 1

        for i in range(1, success_class + 1):  # Delete all acquired leases to reset limit.
            cmd = {"command": "lease4-del", "arguments": {"ip-address": f'192.168.1.{i}'}}
            srv_msg.send_ctrl_cmd(cmd)

        for i in range(to_send + 1, 2 * to_send + 1):  # Try to acquire more leases than the limit.
            success_class += _get_lease_v4(f'192.168.1.{i}', f'ff:01:02:03:04:{i:02}', vendor='PXE')
            exchanges += 1

        for i in range(2 * to_send + 1, 3 * to_send + 1):  # Try to acquire more leases than the limit of second class
            success_class += _get_lease_v4(f'192.168.1.{i}', f'ff:01:02:03:04:{i:02}', vendor='PXA')
            exchanges += 1

        for i in range(3 * to_send + 1, 4 * to_send + 1):  # Try to acquire more leases than the limit of subnet.
            success_noclass += _get_lease_v4(f'192.168.1.{i}', f'ff:01:02:03:04:{i:02}')
            exchanges += 1

    else:
        # IA_NA
        for i in range(1, to_send + 1):
            success_na += _get_lease_v6(f'2001:db8:1::{hex(i)[2:]}', f'00:03:00:01:ff:ff:ff:ff:ff:{i:02}',
                                        vendor='eRouter2.0', ia_na=True)
            exchanges += 1

        for i in range(1, success_na + 1):
            cmd = {"command": "lease6-del", "arguments": {"ip-address": f'2001:db8:1::{hex(i)[2:]}'}}
            srv_msg.send_ctrl_cmd(cmd)

        for i in range(to_send + 1, 2 * to_send + 1):
            success_na += _get_lease_v6(f'2001:db8:1::{hex(i)[2:]}', f'00:03:00:01:ff:ff:ff:ff:ff:{i:02}',
                                        vendor='eRouter2.0', ia_na=True)
            exchanges += 1

        for i in range(2 * to_send + 1, 3 * to_send + 1):  # Try to acquire more leases than the limit second class.
            success_na += _get_lease_v6(f'2001:db8:1::{hex(i)[2:]}', f'00:03:00:01:ff:ff:ff:ff:ff:{i:02}',
                                        vendor='eRouter1.0', ia_na=True)
            exchanges += 1

        for i in range(3 * to_send + 1, 4 * to_send + 1):  # Try to acquire more leases than the limit of IA_NA.
            success_noclass += _get_lease_v6(f'2001:db8:1::{hex(i)[2:]}', f'00:03:00:01:ff:ff:ff:ff:ff:{i:02}',
                                             ia_na=True)
            exchanges += 1

        # IA_PD
        for i in range(4 * to_send + 1, 5 * to_send + 1):
            success_pd += _get_lease_v6(f'2001:db8:1::{hex(i)[2:]}', f'00:03:00:01:ff:ff:ff:ff:ff:{i:02}', ia_pd=1,
                                        vendor='eRouter2.0')
            exchanges += 1

        for i in range(4 * to_send + 1, 4 * to_send + 1 + success_pd):
            cmd = {"command": "lease6-get-by-duid", "arguments": {"duid": f'00:03:00:01:ff:ff:ff:ff:ff:{i:02}'}}
            response = srv_msg.send_ctrl_cmd(cmd)
            iaid = response['arguments']['leases'][0]['iaid']

            cmd = {"command": "lease6-del",
                   "arguments": {"subnet-id": 1,
                                 "identifier": f'00:03:00:01:ff:ff:ff:ff:ff:{i:02}',
                                 "identifier-type": "duid",
                                 "iaid": iaid,
                                 "type": "IA_PD"}}
            srv_msg.send_ctrl_cmd(cmd)

        for i in range(5 * to_send + 1, 6 * to_send + 1):
            success_pd += _get_lease_v6(f'2001:db8:1::{hex(i)[2:]}', f'00:03:00:01:ff:ff:ff:ff:ff:{i:02}', ia_pd=1,
                                        vendor='eRouter2.0')
            exchanges += 1

        for i in range(6 * to_send + 1, 7 * to_send + 1):  # Try to acquire more leases than the limit second class.
            success_pd += _get_lease_v6(f'2001:db8:1::{hex(i)[2:]}', f'00:03:00:01:ff:ff:ff:ff:ff:{i:02}', ia_pd=1,
                                        vendor='eRouter1.0')

        for i in range(7 * to_send + 1, 8 * to_send + 1):  # Try to acquire more leases than the limit of IA_PD.
            success_noclass += _get_lease_v6(f'2001:db8:1::{hex(i)[2:]}', f'00:03:00:01:ff:ff:ff:ff:ff:{i:02}', ia_pd=1)
            exchanges += 1

        success = success_na + success_pd
    # Set threshold to account for small errors in receiving packets.
    threshold = 1

    # Check if difference between limit and received packets is within threshold.
    if dhcp_version == 'v4':
        print(f"exchanges made: {exchanges}")
        print(f"class successes made: {success_class}")
        print(f"noclass successes made: {success_noclass}")
        assert abs(3 * limit_class - success_class) <= threshold, \
            f'Difference between Class responses and limit ({abs(3 * limit_class - success_class)})' \
            f' exceeds threshold ({threshold})'
        assert abs((limit_subnet + limit_class) - (success_class + success_noclass)) <= threshold, \
            f'Difference between All responses and limit' \
            f' ({abs((limit_subnet + limit_class) - (success_class + success_noclass))})' \
            f' exceeds threshold ({threshold})'
    else:
        print(f"exchanges made: {exchanges}")
        print(f"class successes made: {success}")
        print(f"noclass successes made: {success_noclass}")
        assert abs(6 * limit_class - success) <= threshold, \
            f'Difference between Class responses and limit ({abs(6 * limit_class - success)})' \
            f' exceeds threshold ({threshold})'
        assert abs(2 * (limit_subnet + limit_class) - (success + success_noclass)) <= threshold, \
            f'Difference between All responses and limit' \
            f' ({abs(2 * (limit_subnet + limit_class) - (success + success_noclass))})' \
            f' exceeds threshold ({threshold})'


@pytest.mark.v6
@pytest.mark.hook
@pytest.mark.limits_hook
@pytest.mark.parametrize('backend', ['memfile', 'mysql', 'postgresql'])
def test_lease_limits_v6_multipleIA(backend):
    """
    Test to check correct behaviour when multiple IA-NA and IA-PD address request is made that exceeds limit.
    :type backend: str
    :param backend: The backend being used for the test ('memfile', 'mysql', or 'postgresql').
    """
    misc.test_setup()
    srv_control.define_lease_db_backend(backend)
    # define limit for hook and test
    limit = 2
    # define addresses number to try to get
    iaid = iapd = 3
    srv_control.config_srv_subnet('2001:db8:1::/64', '2001:db8:1::1-2001:db8:1::255:255')
    srv_control.config_srv_prefix('2002:db8:1::', 0, 90, 96)

    # hook configuration in user context for subnet with limit defined above
    srv_control.add_line_to_subnet(0, {"user-context": {
        "limits": {
            "address-limit": limit,
            "prefix-limit": limit
        }}})

    srv_control.add_unix_socket()
    srv_control.add_http_control_channel()
    srv_control.add_hooks('libdhcp_limits.so')
    srv_control.add_hooks('libdhcp_lease_cmds.so')
    srv_control.build_and_send_config_files()
    srv_control.start_srv('DHCP', 'started')

    ia_1 = secrets.randbelow(5000) + 2000
    pd_1 = secrets.randbelow(2000) + 5000

    misc.test_procedure()
    srv_msg.client_sets_value('Client', 'DUID', '00:03:00:01:ff:ff:ff:ff:ff:00')
    srv_msg.client_does_include('Client', 'client-id')

    # Generate ia-na and ia-pd requests
    for ia in range(iaid):
        srv_msg.client_sets_value('Client', 'ia_id', ia_1 + ia)
        srv_msg.client_does_include('Client', 'IA-NA')
    for pd in range(iapd):
        srv_msg.client_sets_value('Client', 'ia_pd', pd_1 + pd)
        srv_msg.client_does_include('Client', 'IA-PD')
    srv_msg.client_send_msg('SOLICIT')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', 'ADVERTISE')
    srv_msg.response_check_include_option(1)
    srv_msg.response_check_include_option(2)
    srv_msg.response_check_include_option(3)
    srv_msg.response_check_include_option(25)

    misc.test_procedure()
    srv_msg.client_sets_value('Client', 'DUID', '00:03:00:01:ff:ff:ff:ff:ff:00')
    srv_msg.client_does_include('Client', 'client-id')

    # Include expected addresses in Request
    for ia in range(iaid):
        srv_msg.client_sets_value('Client', 'ia_id', ia_1 + ia)
        srv_msg.client_sets_value('Client', 'IA_Address', f'2001:db8:1::{ia+1}')
        srv_msg.client_does_include('Client', 'IA_Address')
        srv_msg.client_does_include('Client', 'IA-NA')

    prefixes = ['2002:db8:1::', '2002:db8:1::1:0:0', '2002:db8:1::2:0:0']
    for pd in range(iapd):
        srv_msg.client_sets_value('Client', 'ia_pd', pd_1 + pd)
        srv_msg.client_sets_value('Client', 'plen', 96)
        srv_msg.client_sets_value('Client', 'prefix', prefixes[pd])
        srv_msg.client_does_include('Client', 'IA_Prefix')
        srv_msg.client_does_include('Client', 'IA-PD')

    srv_msg.client_copy_option('server-id')
    srv_msg.client_send_msg('REQUEST')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', 'REPLY')
    srv_msg.response_check_include_option(3)
    srv_msg.response_check_option_content(3, 'sub-option', 5)
    # Check for acquired and refused addresses
    srv_msg.response_check_suboption_content(5, 3, 'addr', '2001:db8:1::1')
    srv_msg.response_check_suboption_content(5, 3, 'addr', '2001:db8:1::2')
    srv_msg.response_check_suboption_content(13, 3, 'statuscode', 2)  # NoAddrAvail
    srv_msg.response_check_suboption_content(26, 25, 'prefix', '2002:db8:1::')
    srv_msg.response_check_suboption_content(26, 25, 'prefix', '2002:db8:1::1:0:0')
    srv_msg.response_check_suboption_content(13, 25, 'statuscode', 6)  # NoPrefixAvail


@pytest.mark.v4
@pytest.mark.v6
@pytest.mark.hook
@pytest.mark.limits_hook
@pytest.mark.parametrize('unit', ['minute'])
@pytest.mark.parametrize('backend', ['memfile'])
def test_rate_limits_in_template_class(dhcp_version, backend, unit):
    """
    Test limit of rate limiting in Limits Hook when configured in template class
    (each SPAWN class should get it's own limit).
    The test makes DO or SA exchange in the fastest way possible in a unit of time (second or minute)
    and counts how many packets were sent, and how many packets were received from Kea.
    If the received packets is the same as limit, the test passes. Some error in number of packets is accounted for.
    :type unit: str
    :param unit:  Defines testing of limit per second or minute
    :type dhcp_version: str
    :param dhcp_version: The DHCP version being tested ('v4' or 'v6').
    :type backend: str
    :param backend: The backend being used for the test ('memfile', 'mysql', or 'postgresql').
    """
    misc.test_setup()
    srv_control.define_lease_db_backend(backend)

    # define test duration in seconds
    duration = 1 if unit == 'second' else 60
    limit = 3 if unit == 'second' else 40

    if dhcp_version == 'v4':
        srv_control.config_srv_subnet('192.168.1.0/24', '192.168.1.1-192.168.1.255')
        srv_control.config_srv_opt('subnet-mask', '255.255.255.0')
    else:
        srv_control.config_srv_subnet('2001:db8:1::/64', '2001:db8:1::1-2001:db8:1::1255')

    template = "hexstring(substring(pkt4.mac, 0, 3), ':')"
    if dhcp_version == 'v6':
        template = "hexstring(substring(option[1].hex, 4, 3), ':')"

    classes = [
        {
            # SPAWN_mac_vendor_<first 3 octets of mac address>
            "name": "mac_vendor",
            "template-test": template,
            "user-context": {
                "limits": {
                    "rate-limit": f"{limit} packets per {unit}"
                }
            }
        }
    ]

    world.dhcp_cfg["client-classes"] = classes

    srv_control.add_unix_socket()
    srv_control.add_http_control_channel()
    srv_control.add_hooks('libdhcp_limits.so')

    srv_control.build_and_send_config_files()
    srv_control.start_srv('DHCP', 'started')

    packets_no1 = 0  # packets sent SPAWN_mac_vendor_ff:01:02
    success_no1 = 0  # responses to packets SPAWN_mac_vendor_ff:01:02

    packets_no2 = 0  # packets send SPAWN_mac_vendor_11:22:33
    success_no2 = 0  # responses to packets SPAWN_mac_vendor_11:22:33

    # Wait time for response for v4 and v6
    world.cfg['wait_interval'] = 0.1
    if dhcp_version == 'v6':
        world.cfg['wait_interval'] = 0.1

    start = time.time()
    if dhcp_version == 'v4':
        while time.time() - start < duration:  # Send packets for the duration of the test, and count them.
            # fist SPAWN class
            # Send Discover and add 1 to success counter if Forge got Offer.
            success_no1 += _get_address_v4(chaddr='ff:01:02:03:04:05')
            # Add 1 to send packets counter
            packets_no1 += 1
            # second SPAWN class
            success_no2 += _get_address_v4(chaddr='11:22:33:03:04:05')
            packets_no2 += 1
    else:
        while time.time() - start < duration:  # Send packets for the duration of the test, and count them.
            # Send Solicit and add 1 to success counter if Forge got Advertise.
            success_no1 += _get_address_v6(duid='00:03:00:01:ff:01:02:ff:ff:ff')
            # Add 1 to send packets counter
            packets_no1 += 1

            success_no2 += _get_address_v6(duid='00:03:00:01:11:22:33:ff:ff:ff')
            # Add 1 to send packets counter
            packets_no2 += 1
    elapsed = time.time() - start

    print(f"Runtime of the program is {elapsed} seconds")
    print(f"Packets received {success_no1} from {packets_no1} sent in SPAWN class ff:01:02")
    print(f"Packets received {success_no2} from {packets_no2} sent in SPAWN class 11:22:33")
    if unit == 'second':
        print(f"Average Packets per second {success_no1 / elapsed} in SPAWN class ff:01:02")
        print(f"Average Packets per second {success_no2 / elapsed} in SPAWN class 11:22:33")
    else:
        print(f"Average Packets per minute {success_no1 / elapsed * 60} in SPAWN class ff:01:02")
        print(f"Average Packets per minute {success_no2 / elapsed * 60} in SPAWN class 11:22:33")

    # Set threshold to account for small errors in receiving packets.
    threshold = 1 if unit == 'second' else 10

    print(f'Difference between responses and limit ({abs(limit - success_no1)}) in SPAWN class ff:01:02')
    print(f'Difference between responses and limit ({abs(limit - success_no2)}) in SPAWN class 11:22:33')

    # Check if difference between limit and received packets is within threshold.
    assert abs(limit - success_no1) <= threshold, f'Difference between responses and limit' \
                                                  f' ({abs(limit - success_no1)}) exceeds threshold ({threshold})' \
                                                  f' in SPAWN class ff:01:02'

    assert abs(limit - success_no2) <= threshold, f'Difference between responses and limit' \
                                                  f' ({abs(limit - success_no2)}) exceeds threshold ({threshold})' \
                                                  f' in SPAWN class 11:22:33'


@pytest.mark.v4
@pytest.mark.v6
@pytest.mark.hook
@pytest.mark.limits_hook
@pytest.mark.parametrize('backend', ['memfile', 'mysql', 'postgresql'])
def test_lease_limits_template_class(dhcp_version, backend):
    """
    Test lease limit configured in template class
    The test makes DORA or SARR exchange to acquire leases and counts if dropped or returned
    "no leases available".
    Test removes leases and tries again to check if the limit is restored.
    If the received leases is the same as limit, the test passes.
    Some error in number of packets is accounted for.

    Due to the fact that original test on which this is based relay on exact returned addresses
    additional subnets with class guards were added

    :type dhcp_version: str
    :param dhcp_version: The DHCP version being tested ('v4' or 'v6').
    :type backend: str
    :param backend: The backend being used for the test ('memfile', 'mysql', or 'postgresql').
    """
    misc.test_setup()
    srv_control.define_lease_db_backend(backend)
    # define limit for hook and test
    limit = 5
    if dhcp_version == 'v4':
        srv_control.config_srv_subnet('192.168.1.0/24', '192.168.1.1-192.168.1.255')
        srv_control.config_srv_another_subnet_no_interface('192.168.2.0/24', '192.168.2.1-192.168.2.255')
        srv_control.config_srv_opt('subnet-mask', '255.255.255.0')
    else:
        srv_control.config_srv_subnet('2001:db8:1::/64', '2001:db8:1::1-2001:db8:1::255:255')
        srv_control.config_srv_prefix('2002:db8:2::', 0, 64, 96)
        srv_control.config_srv_another_subnet_no_interface('2001:db8:3::/64', '2001:db8:3::1-2001:db8:3::255:255')
        srv_control.add_prefix_to_subnet('2002:db8:4::', 64, 96, 1)

    template = "hexstring(substring(pkt4.mac, 0, 3), ':')"
    if dhcp_version == 'v6':
        template = "hexstring(substring(option[1].hex, 4, 3), ':')"

    classes = [
        {
            # SPAWN_mac_vendor_<first 3 octets of mac address>
            "name": "mac_vendor",
            "template-test": template,
            "user-context": {
                "limits": {
                    "address-limit": limit,
                    "prefix-limit": limit
                }
            }
        }
    ]

    world.dhcp_cfg["client-classes"] = classes

    srv_control.config_client_classification(0, 'SPAWN_mac_vendor_aa:bb:cc')
    srv_control.config_client_classification(1, 'SPAWN_mac_vendor_11:22:33')

    srv_control.add_unix_socket()
    srv_control.add_http_control_channel()
    srv_control.add_hooks('libdhcp_limits.so')
    srv_control.add_hooks('libdhcp_lease_cmds.so')
    srv_control.build_and_send_config_files()
    srv_control.start_srv('DHCP', 'started')

    # stats for SPAWN_mac_vendor_aa:bb:cc
    success_no1 = 0  # successful v4 address assignments
    success_na_no1 = 0  # successful v6 address assignments
    success_pd_no1 = 0  # successful v6 prefix assignments

    # stats for SPAWN_mac_vendor_11:22:33
    success_no2 = 0  # successful v4 address assignments
    success_na_no2 = 0  # successful v6 address assignments
    success_pd_no2 = 0  # successful v6 prefix assignments

    exchanges = 0
    to_send = 15
    threshold = 1  # threshold for errors
    leases = []

    if dhcp_version == 'v4':
        for i in range(1, to_send + 1):  # Try to acquire more leases than the limit.
            # Try exchanging DORA and add 1 to success counter if Forge got ACK.
            res = _get_lease_v4(f'192.168.1.{i}', f'aa:bb:cc:03:04:{i:02}', vendor=None)
            if res > 0:
                # we need a bit magic here, lease is needed to easily remove leases
                # but calling srv_msg.get_all_leases() when there is no response will trigger an error
                # rather than rewrite all existing tests, I will add ifs in this one
                success_no1 += res
                leases.append(srv_msg.get_all_leases())
            res = _get_lease_v4(f'192.168.2.{i}', f'11:22:33:03:05:{i:02}', vendor=None)
            if res > 0:
                success_no2 += res
                leases.append(srv_msg.get_all_leases())
            # Add 1 to exchanges counter
            exchanges += 1

        # compare collected stats with limits
        assert limit - success_no1 <= threshold, "In SPAWN_mac_vendor_aa:bb:cc we assigned more addresses than limit!"
        assert limit - success_no2 <= threshold, "In SPAWN_mac_vendor_11:22:33 we assigned more addresses than limit!"

        for lease in leases:
            cmd = {"command": "lease4-del", "arguments": {"ip-address": lease['address']}}
            srv_msg.send_ctrl_cmd(cmd)

        for i in range(to_send + 1, 2 * to_send + 1):  # Try to acquire more leases than the limit.
            success_no1 += _get_lease_v4(f'192.168.1.{i}', f'aa:bb:cc:03:06:{i:02}', vendor=None)
            success_no2 += _get_lease_v4(f'192.168.2.{i}', f'11:22:33:03:07:{i:02}', vendor=None)
            exchanges += 1

    else:
        # IA_NA
        for i in range(1, to_send + 1):  # Try to acquire more IA_NA leases than the limit.
            # Try exchanging SARR and add 1 to success counter if Forge got Reply with lease.
            res = _get_lease_v6(f'2001:db8:1::{hex(i)[2:]}', f'00:03:00:01:aa:bb:cc:11:ff:{i:02}', ia_na=True)
            if res > 0:
                success_na_no1 += res
                leases += srv_msg.get_all_leases()
            res = _get_lease_v6(f'2001:db8:3::{hex(i)[2:]}', f'00:03:00:01:11:22:33:22:ff:{i:02}', ia_na=True)
            if res > 0:
                success_na_no2 += res
                leases += srv_msg.get_all_leases()
            # Add 1 to exchanges counter
            exchanges += 1

        for lease in leases:
            cmd = {"command": "lease6-del", "arguments": {"ip-address": lease['address']}}
            srv_msg.send_ctrl_cmd(cmd)

        leases = []

        for i in range(to_send + 1, 2 * to_send + 1):  # Try to acquire more leases than the limit.
            res = _get_lease_v6(f'2001:db8:1::{hex(i)[2:]}', f'00:03:00:01:aa:bb:cc:33:ff:{i:02}', ia_na=True)
            if res > 0:
                success_na_no1 += res
                leases += srv_msg.get_all_leases()
            res = _get_lease_v6(f'2001:db8:3::{hex(i)[2:]}', f'00:03:00:01:11:22:33:44:ff:{i:02}', ia_na=True)
            if res > 0:
                success_na_no2 += res
                leases += srv_msg.get_all_leases()
            exchanges += 1

        assert limit - success_na_no1 <= threshold, \
            "In SPAWN_mac_vendor_aa:bb:cc we assigned more addresses than limit!"
        assert limit - success_na_no2 <= threshold, \
            "In SPAWN_mac_vendor_11:22:33 we assigned more addresses than limit!"

        for lease in leases:
            cmd = {"command": "lease6-del", "arguments": {"ip-address": lease['address']}}
            srv_msg.send_ctrl_cmd(cmd)

        leases = []
        # IA_PD
        for i in range(2 * to_send + 1, 3 * to_send + 1):  # Try to acquire more IA_PD leases than the limit
            # Try exchanging SARR and add 1 to success counter if Forge got Reply with lease.
            res = _get_lease_v6(f'2001:db8:1::{hex(i)[2:]}', f'00:03:00:01:aa:bb:cc::55:ff:{i:02}', ia_pd=1)
            if res > 0:
                success_pd_no1 += res
                leases += srv_msg.get_all_leases()

            res = _get_lease_v6(f'2001:db8:3::{hex(i)[2:]}', f'00:03:00:01:11:22:33:66:ff:{i:02}', ia_pd=1)
            if res > 0:
                success_pd_no2 += res
                leases += srv_msg.get_all_leases()

            # Add 1 to exchanges counter
            exchanges += 1

        for lease in leases:
            # TODO command based on address should be used
            # cmd = {"command": "lease6-del", "arguments": {"ip-address": lease['address']}}
            cmd = {"command": "lease6-del",
                   "arguments": {"subnet-id": 1 if '2002:db8:2' in lease['address'] else 2,
                                 "identifier": lease['duid'],
                                 "identifier-type": "duid",
                                 "iaid": lease['iaid'],
                                 "type": "IA_PD"}}
            srv_msg.send_ctrl_cmd(cmd)

        for i in range(3 * to_send + 1, 4 * to_send + 1):  # Try to acquire more leases than the limit.
            res = _get_lease_v6(f'2001:db8:1::{hex(i)[2:]}', f'00:03:00:01:aa:bb:cc:88:ff:{i:02}', ia_pd=1)
            if res > 0:
                success_pd_no1 += res
                leases += srv_msg.get_all_leases()

            res = _get_lease_v6(f'2001:db8:3::{hex(i)[2:]}', f'00:03:00:01:11:22:33:99:ff:{i:02}', ia_pd=1)
            if res > 0:
                success_pd_no2 += res
                leases += srv_msg.get_all_leases()
            exchanges += 1

        # limit both for address and prefix was 5 each, we assigned all 2 times, success should be 20
        success_no1 = success_na_no1 + success_pd_no1
        success_no2 = success_na_no2 + success_pd_no2

    # Set threshold to account for small errors in receiving packets.

    print(f"exchanges made: {exchanges}")
    print(f"successes made: {success_no1}")
    print(f"successes made: {success_no2}")

    # Check if difference between limit and received packets is within threshold.
    if dhcp_version == 'v4':
        assert abs(2 * limit - success_no1) <= threshold, \
            f'Difference between responses and limit ({abs(2 * limit - success_no1)}) exceeds threshold ({threshold})'
    else:
        assert abs(4 * limit - success_no2) <= threshold, \
            f'Difference between responses and limit ({abs(4 * limit - success_no2)}) exceeds threshold ({threshold})'


def _get_lease_v4_82_2(address, chaddr, vendor=None):
    """
    Local function used to send Discover and check if Offer is sent back.
    Includes relay agent information option with value 020672656C617931
    If Offer is received, function continues with Request and Acknowledge
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
    srv_msg.client_does_include_with_value("relay_agent_information", "020672656C617931")
    srv_msg.client_send_msg('DISCOVER')

    misc.pass_criteria()
    try:
        srv_msg.send_wait_for_message('MUST', 'OFFER')
    except AssertionError as e:
        if e.args[0] == 'No response received.':
            return 0
        raise AssertionError(e) from e
    srv_msg.response_check_content('yiaddr', address)

    misc.test_procedure()
    srv_msg.client_sets_value('Client', 'chaddr', chaddr)
    srv_msg.client_copy_option('server_id')
    srv_msg.client_does_include_with_value('requested_addr', address)

    if vendor is not None:
        srv_msg.client_does_include_with_value('vendor_class_id', vendor)
    srv_msg.client_does_include_with_value("relay_agent_information", "020672656C617931")
    srv_msg.client_send_msg('REQUEST')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', 'ACK')
    srv_msg.response_check_content('yiaddr', address)
    return 1


@pytest.mark.v4
@pytest.mark.v6
@pytest.mark.hook
@pytest.mark.parametrize('backend', ['memfile', 'mysql', 'postgresql'])
@pytest.mark.parametrize('extended_info', [True, False])
def test_lease_limits_extended_info(dhcp_version, backend, extended_info):
    """
    Test of lease limit in Limits Hook with extended info .
    Tests Kea#3702 Issue
    v4 includes relay agent information option with value 020672656C617931
    The test makes DORA or SARR exchange to acquire leases and counts if dropped or returned
    "no leases available".

    :type dhcp_version: str
    :param dhcp_version: The DHCP version being tested ('v4' or 'v6').
    :type backend: str
    :param backend: The backend database used for storing leases ('memfile', 'mysql', 'postgresql').
    :type extended_info: bool
    :param extended_info: True or False
    """
    misc.test_setup()
    srv_control.define_lease_db_backend(backend)
    # define limit for hook and test
    limit = 5

    if dhcp_version == 'v4':
        srv_control.config_srv_subnet('192.168.1.0/24', '192.168.1.1-192.168.1.255')
        srv_control.config_srv_opt('subnet-mask', '255.255.255.0')
    else:
        srv_control.config_srv_subnet('2001:db8:1::/64', '2001:db8:1::1-2001:db8:1::255:255')

    if dhcp_version == 'v4':
        # hook configuration in user context for classes with limit
        # Option 82 does not have to be in class test to trigger bug.
        classes = [
            {
                "name": "gold",
                # "test": "option[82].option[2].hex == 0x72656C617931",
                "test": "option[60].text == 'PXE'",
                "user-context": {
                    "limits": {
                        "address-limit": limit
                    }
                }
            }
        ]
    else:
        classes = [
            {
                "name": "VENDOR_CLASS_eRouter2.0",
                "user-context": {
                    "limits": {
                        "address-limit": limit,
                        "prefix-limit": limit
                    }
                }
            }
        ]
    world.dhcp_cfg["client-classes"] = classes

    # Verify that test works with or without extended info before testing bug.
    if extended_info:
        world.dhcp_cfg['store-extended-info'] = True

    srv_control.add_unix_socket()
    srv_control.add_http_control_channel()
    srv_control.add_hooks('libdhcp_limits.so')
    srv_control.add_hooks('libdhcp_lease_cmds.so')
    srv_control.build_and_send_config_files()
    srv_control.start_srv('DHCP', 'started')

    success = 0
    to_send = 9

    if dhcp_version == 'v4':
        for i in range(1, to_send + 1):  # Try to acquire more leases than the limit.
            # Try exchanging DORA and add 1 to success counter if Forge got ACK.
            # Send Discover with option 82 to trigger bug.
            try:
                srv_msg.DORA(f'192.168.1.{i}', chaddr=f'ff:01:02:03:04:{i:02}', options={
                    'vendor_class_id': 'PXE',
                    'relay_agent_information': '020672656C617931',
                })
                success += 1
            except AssertionError:
                pass

        for i in range(1, success + 1):  # Delete all acquired leases to reset limit.
            cmd = {"command": "lease4-del", "arguments": {"ip-address": f'192.168.1.{i}'}}
            srv_msg.send_ctrl_cmd(cmd)

    else:

        for i in range(1, to_send + 1):  # Try to acquire more leases than the limit.
            # Try exchanging SARR and add 1 to success counter if Forge got Reply with lease.
            try:
                srv_msg.SARR(f'2001:db8:1::{hex(i)[2:]}', duid=f'00:03:00:01:f6:f5:f4:f3:f2:{hex(i)[2:]}',
                             vendor='eRouter2.0', relay_information=True)
                success += 1
            except AssertionError:
                pass

        for i in range(1, success + 1):  # Delete all acquired leases to reset limit.
            cmd = {"command": "lease6-del", "arguments": {"ip-address": f'2001:db8:1::{hex(i)[2:]}'}}
            srv_msg.send_ctrl_cmd(cmd)

    # Set threshold to account for small errors in receiving packets.
    threshold = 1

    print(f"exchanges made: {to_send}")
    print(f"successes made: {success}")

    # Check if difference between limit and received packets is within threshold.

    assert abs(limit - success) <= threshold, \
        f'Difference between responses and limit ({abs(limit - success)}) exceeds threshold ({threshold})'
