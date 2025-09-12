# Copyright (C) 2023-2025 Internet Systems Consortium, Inc. ("ISC")
#
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

"""Kea random and flq allocators"""


import ipaddress
import logging
from secrets import randbelow
import pytest

from src import misc
from src import srv_control
from src import srv_msg

log = logging.getLogger('forge')


def _get_lease_4(allocator: str, mac: str, giaddr: str, all_leases: list = None, netmask: int = 16):
    """Get v4 lease from kea. Check if address is correct by checking previously assigned address.
    :param allocator: type of allocator
    :type allocator:
    :param mac: mac address of a client
    :type mac:
    :param giaddr: relay address
    :type giaddr:
    :param all_leases: list of previously assigned leases from single subnet
    :type all_leases:
    :param netmask: subnet netmask
    :type netmask:
    :return: dictionary with single lease
    :rtype: dict
    """
    misc.test_procedure()
    srv_msg.network_variable('source_port', 67)
    srv_msg.network_variable('source_address', '$(GIADDR4)')
    srv_msg.network_variable('destination_address', '$(SRV4_ADDR)')
    srv_msg.client_sets_value('Client', 'giaddr', giaddr)
    srv_msg.client_sets_value('Client', 'chaddr', mac)  # '00:00:00:00:00:22'
    srv_msg.client_sets_value('Client', 'hops', 1)
    srv_msg.client_send_msg('DISCOVER')

    misc.pass_criteria()
    msg = srv_msg.send_wait_for_message('MUST', 'OFFER')[0]
    srv_msg.response_check_include_option(1)

    misc.test_procedure()
    srv_msg.client_sets_value('Client', 'giaddr', giaddr)
    srv_msg.client_sets_value('Client', 'hops', 1)
    srv_msg.client_sets_value('Client', 'chaddr', mac)
    srv_msg.client_copy_option('server_id')
    srv_msg.client_does_include_with_value('requested_addr', msg.yiaddr)
    srv_msg.client_send_msg('REQUEST')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', 'ACK')
    srv_msg.response_check_content('yiaddr', msg.yiaddr)

    lease = srv_msg.get_all_leases()
    srv_msg.check_if_address_belongs_to_subnet(subnet=f"{giaddr[:-1]}0/{netmask}", address=lease['address'])
    # let's check if address is actually correct for allocator

    if len(all_leases) != 0:
        if allocator == 'iterative':
            # we want to have new address to be next from the last received
            assert ipaddress.ip_address(msg.yiaddr) == ipaddress.ip_address(all_leases[-1]["address"]) + 1, \
                f"Received address {msg.yiaddr} is not +1 after previously assigned"
        else:
            # allocator will not guarantee that next address is not +1, but with pool big
            # enough we can assume it's highly unlikely
            assert ipaddress.ip_address(msg.yiaddr) != ipaddress.ip_address(all_leases[-1]["address"]) + 1, \
                f"Received address {msg.yiaddr} is simple +1 after previously assigned this is incorrect for flq/random"

        log.debug('Current %s previous was %s', msg.yiaddr, all_leases[-1]["address"])
    return lease


@pytest.mark.v4
@pytest.mark.allocators
@pytest.mark.parametrize('backend', ['memfile', 'postgresql', 'mysql'])
@pytest.mark.parametrize('scope', ['subnets', 'shared-networks'])
def test_v4_allocators(backend, scope):
    """Get 10 addresses from each subnet, check if:
    - iterative starts from first and have all others are one by one
    - random and flq wont start from first in the pool and each next is not +1 from the previous
    - check if all leases are correctly saved in the lease file/database
    - allocator configured per subnet
    :param backend: database backend
    :type backend: str
    :param scope:
    :type scope:
    """
    misc.test_setup()
    srv_control.config_srv_subnet('192.167.0.0/16', '192.167.0.0/16', allocator='iterative')
    srv_control.config_srv_another_subnet_no_interface('192.168.0.0/16', '192.168.0.0/16', allocator='flq')
    srv_control.config_srv_another_subnet_no_interface('192.169.0.0/16', '192.169.0.0/16', allocator='random')

    if scope == "shared_networks":
        srv_control.shared_subnet('192.167.0.0/16', 0)
        srv_control.shared_subnet('192.168.0.0/16', 0)
        srv_control.shared_subnet('192.169.0.0/16', 0)

        srv_control.set_conf_parameter_shared_subnet('name', '"name-abc"', 0)
        srv_control.set_conf_parameter_shared_subnet('interface', '"$(SERVER_IFACE)"', 0)

    srv_control.define_lease_db_backend(backend)

    srv_control.build_and_send_config_files()

    srv_control.start_srv('DHCP', 'started')
    leases_subnet1 = []
    leases_subnet2 = []
    leases_subnet3 = []
    for i in range(10, 20):
        leases_subnet1.append(_get_lease_4('iterative', f'22:00:00:00:00:{i}', '192.167.0.1', leases_subnet1))
        leases_subnet2.append(_get_lease_4('flq', f'33:00:00:00:00:{i}', '192.168.0.1', leases_subnet2))
        leases_subnet3.append(_get_lease_4('random', f'44:00:00:00:00:{i}', '192.169.0.1', leases_subnet3))
    srv_msg.check_leases(leases_subnet1 + leases_subnet2 + leases_subnet3, backend=backend)


@pytest.mark.v4
@pytest.mark.allocators
@pytest.mark.parametrize('backend', ['memfile'])
def test_v4_allocator_randomness(backend):
    """This will check if random and flq allocator will assign different addresses after Kea restart.
    :param backend: database backend
    :type backend: str
    """
    misc.test_setup()
    srv_control.config_srv_subnet('192.167.0.0/16', '192.167.0.0/16', allocator='random')
    srv_control.config_srv_another_subnet_no_interface('192.168.0.0/16', '192.168.0.0/16', allocator='flq')
    srv_control.define_lease_db_backend(backend)
    srv_control.build_and_send_config_files()
    srv_control.start_srv('DHCP', 'started')

    leases_subnet1 = []
    leases_subnet2 = []
    for i in range(10, 20):
        leases_subnet1.append(_get_lease_4('random', f'22:00:00:00:00:{i}', '192.167.0.1', leases_subnet1))
        leases_subnet2.append(_get_lease_4('flq', f'33:00:00:00:00:{i}', '192.168.0.1', leases_subnet2))
    srv_msg.check_leases(leases_subnet1 + leases_subnet2, backend=backend)

    srv_control.start_srv('DHCP', 'stopped')
    srv_control.clear_some_data('all')

    misc.test_setup()
    srv_control.config_srv_subnet('192.167.0.0/16', '192.167.0.0/16', allocator='random')
    srv_control.config_srv_another_subnet_no_interface('192.168.0.0/16', '192.168.0.0/16', allocator='flq')
    srv_control.define_lease_db_backend(backend)
    srv_control.build_and_send_config_files()
    srv_control.start_srv('DHCP', 'started')

    leases_subnet1_2 = []
    leases_subnet2_2 = []
    # let's generate exactly the same traffic, addresses may repeat but chances that we get at least 1 repeated address
    # from pool of /16 should be slim, and that is what we are testing here
    for i in range(10, 20):
        leases_subnet1_2.append(_get_lease_4('random', f'22:00:00:00:00:{i}', '192.167.0.1', leases_subnet1))
        leases_subnet2_2.append(_get_lease_4('flq', f'33:00:00:00:00:{i}', '192.168.0.1', leases_subnet2))
    srv_msg.check_leases(leases_subnet1_2 + leases_subnet2_2, backend=backend)

    before_restart = leases_subnet1 + leases_subnet2
    after_restart = leases_subnet1_2 + leases_subnet2_2

    for lease1, lease2 in zip(before_restart, after_restart):
        assert lease1['address'] != lease2['address'], "Looks like address was repeated!"


@pytest.mark.v4
@pytest.mark.allocators
@pytest.mark.parametrize('backend', ['memfile'])
@pytest.mark.parametrize('allocator', ['random', 'flq'])
def test_v4_allocator_exhausted_pool(backend, allocator):
    """This will check if random and flq allocator will assign different addresses after Kea restart.
    :param backend: database backend
    :type backend: str
    :param allocator:
    :type allocator:
    """
    misc.test_setup()
    srv_control.config_srv_subnet('192.167.0.0/16', '192.167.0.1-192.167.0.4', allocator=allocator)
    srv_control.new_pool('192.167.0.6-192.167.0.8', 0)
    srv_control.new_pool('192.167.0.10-192.167.0.14', 0)

    srv_control.define_lease_db_backend(backend)
    srv_control.build_and_send_config_files()
    srv_control.start_srv('DHCP', 'started')

    leases_subnet1 = []
    for i in range(10, 22):
        leases_subnet1.append(_get_lease_4('random', f'22:00:00:00:00:{i}', '192.167.0.1', []))

    srv_msg.check_leases(leases_subnet1, backend=backend)

    misc.test_procedure()
    srv_msg.client_sets_value('Client', 'chaddr', '20:20:20:20:20:22')
    srv_msg.client_send_msg('DISCOVER')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', None, expect_response=False)


@pytest.mark.v4
@pytest.mark.allocators
@pytest.mark.parametrize('backend', ['memfile', 'postgresql', 'mysql'])
@pytest.mark.parametrize('scope', ['global', 'subnets', 'shared-networks'])
def test_v4_adaptive_lease_time_threshold(backend, scope):
    """Test adaptive lease time threshold option.
    Multiple DORA messages are sent to the server.
    First part of leases should have valid lifetime of 4000, rest of leases should have valid lifetime of 1000.

    :param backend: database backend
    :type backend: str
    :param scope: scope of the test
    :type scope: str
    """
    misc.test_setup()
    # adaptive lease time threshold is set to 0.5, so 50% of leases should have valid lifetime of 4000,
    # leases are rounded and Kea will assign 1 less lease with valid lifetime of 4000
    adaptive_lease_time_threshold = 0.5
    amount_of_max = 9
    amount_of_min = 11
    pool_size = amount_of_max + amount_of_min  # Pool size can not exceed 49 in this test
    if scope == 'subnets':
        srv_control.config_srv_subnet('192.168.50.0/24',
                                      f'192.168.50.1-192.168.50.{pool_size}',
                                      allocator='flq',
                                      id=1,
                                      valid_lifetime=4000,
                                      max_valid_lifetime=4000,
                                      min_valid_lifetime=1000,
                                      adaptive_lease_time_threshold=adaptive_lease_time_threshold)
    else:
        srv_control.config_srv_subnet('192.168.50.0/24',
                                      f'192.168.50.1-192.168.50.{pool_size}', allocator='flq', id=1)
    srv_control.config_srv_another_subnet_no_interface('192.168.51.0/24',
                                                       f'192.168.51.1-192.168.51.{pool_size}', allocator='flq', id=2)

    srv_control.shared_subnet('192.168.50.0/24', 0)
    srv_control.shared_subnet('192.168.51.0/24', 0)
    srv_control.set_conf_parameter_shared_subnet('name', '"name-abc"', 0)
    srv_control.set_conf_parameter_shared_subnet('interface', '"$(SERVER_IFACE)"', 0)
    if scope == 'shared-networks':
        srv_control.set_conf_parameter_shared_subnet('valid-lifetime', 4000, 0)
        srv_control.set_conf_parameter_shared_subnet('max-valid-lifetime', 4000, 0)
        srv_control.set_conf_parameter_shared_subnet('min-valid-lifetime', 1000, 0)
        srv_control.set_conf_parameter_shared_subnet('adaptive-lease-time-threshold', adaptive_lease_time_threshold, 0)

    if scope == 'global':
        srv_control.set_conf_parameter_global('valid-lifetime', 4000)
        srv_control.set_conf_parameter_global('max-valid-lifetime', 4000)
        srv_control.set_conf_parameter_global('min-valid-lifetime', 1000)
        srv_control.set_conf_parameter_global('adaptive-lease-time-threshold', adaptive_lease_time_threshold)

    srv_control.define_lease_db_backend(backend)
    srv_control.build_and_send_config_files()
    srv_control.start_srv('DHCP', 'started')

    # send DORA messages to get 20 leases
    for i in range(1, pool_size*2+1):
        srv_msg.DORA('ANY', chaddr=f'ff:01:02:03:ff:{i:02}', exchange='dora-only')

    # check if first amount_of_max leases have valid lifetime of 4000
    for i in range(1, amount_of_max+1):
        srv_msg.check_leases({"hwaddr": f'ff:01:02:03:ff:{i:02}', "valid_lifetime": 4000},
                             backend=backend)

    # check if next amount_of_min leases have valid lifetime of 1000
    for i in range(amount_of_max+1, pool_size+1):
        srv_msg.check_leases({"hwaddr": f'ff:01:02:03:ff:{i:02}', "valid_lifetime": 1000},
                             backend=backend)

    if scope == 'subnets':
        # check if the rest of leases have valid lifetime of 4000
        for i in range(pool_size+1, pool_size*2+1):
            srv_msg.check_leases({"hwaddr": f'ff:01:02:03:ff:{i:02}', "valid_lifetime": 4000},
                                 backend=backend)
    else:
        # check if first amount_of_max leases in second subnet have valid lifetime of 4000
        for i in range(1+pool_size, amount_of_max+1+pool_size):
            srv_msg.check_leases({"hwaddr": f'ff:01:02:03:ff:{i:02}', "valid_lifetime": 4000},
                                 backend=backend)

        # check if next amount_of_min leases in second subnet have valid lifetime of 1000
        for i in range(amount_of_max+1+pool_size, amount_of_max+amount_of_min+1+pool_size):
            srv_msg.check_leases({"hwaddr": f'ff:01:02:03:ff:{i:02}', "valid_lifetime": 1000},
                                 backend=backend)


def _check_multiple_v6_addresses(all_leases: list, offset: int = 1) -> str:
    """Check if list of addresses is iterative or randomly allocated
    :param all_leases: list of ip addresses as strings
    :type all_leases:
    :param offset: offset to check between addresses, with addresses it will be 1,
    :type offset: in prefixes number should be higher than 1
    :return: True if conditional is met
    :rtype:
    """
    def _verdict(lst):
        """

        :param lst:

        """
        if any(lst):
            return 'iterative'
        return 'random'

    result = []
    for i, lease in enumerate(all_leases):
        if i + 1 == len(all_leases):  # we don't want to compare last address non existing next address
            return _verdict(result)

        if ipaddress.ip_address(lease['address']) + offset == ipaddress.ip_address(all_leases[i+1]['address']):
            result.append(True)
        else:
            result.append(False)


def _get_lease_6(allocator: str, mac: str, relay: str, iaid: int = None, iapd: int = None, netmask: int = 112,
                 all_leases: list = None):
    """Get leases with possible multiple IA-NAs and IA-PDs. Also check if all received addresses/prefixes meets
    assumptions from particular allocator, and if those fit inside proper subnet
    :param allocator: name of allocator
    :type allocator:
    :param mac: mac address of a client (used for DUID)
    :type mac:
    :param iaid: number of iaids
    :type iaid:
    :param iapd: number of iapds
    :type iapd:
    :param netmask: netmask of subnet
    :type netmask:
    :param all_leases: list of all previously assigned leases from particular subnet
    :type all_leases:
    :return: list of leases assigned
    :rtype: list
    """
    misc.test_procedure()
    srv_msg.client_sets_value('Client', 'DUID', f'00:03:00:01:{mac}')
    srv_msg.client_does_include('Client', 'client-id')
    if iaid:
        for _ in range(iaid):
            srv_msg.client_sets_value('Client', 'ia_id', randbelow(8999) + 1000)
            srv_msg.client_does_include('Client', 'IA-NA')
    if iapd:
        for _ in range(iapd):
            srv_msg.client_sets_value('Client', 'ia_pd', randbelow(8999) + 1000)
            srv_msg.client_does_include('Client', 'IA-PD')

    srv_msg.client_send_msg('SOLICIT')

    srv_msg.client_sets_value('RelayAgent', 'linkaddr', relay)
    srv_msg.create_relay_forward()

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', 'RELAYREPLY')
    srv_msg.response_check_include_option(9)
    srv_msg.response_check_option_content(9, 'Relayed', 'Message')
    if iaid:
        srv_msg.response_check_include_option(3)
        srv_msg.response_check_option_content(3, 'sub-option', 5)
    if iapd:
        srv_msg.response_check_include_option(25)
        srv_msg.response_check_option_content(25, 'sub-option', 26)

    misc.test_procedure()
    srv_msg.client_sets_value('Client', 'server_id', '00:03:00:01:ff:ff:ff:ff:ff:01')
    srv_msg.client_does_include('Client', 'server-id')
    srv_msg.client_sets_value('Client', 'DUID', f'00:03:00:01:{mac}')
    srv_msg.client_does_include('Client', 'client-id')
    if iaid:
        srv_msg.client_copy_option('IA_NA', copy_all=True)
    if iapd:
        srv_msg.client_copy_option('IA_PD', copy_all=True)
    srv_msg.client_send_msg('REQUEST')

    srv_msg.client_sets_value('RelayAgent', 'linkaddr', relay)
    srv_msg.create_relay_forward()

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', 'RELAYREPLY')
    srv_msg.response_check_include_option(9)
    srv_msg.response_check_option_content(9, 'Relayed', 'Message')
    if iaid:
        srv_msg.response_check_include_option(3)
        srv_msg.response_check_option_content(3, 'sub-option', 5)
    if iapd:
        srv_msg.response_check_include_option(25)
        srv_msg.response_check_option_content(25, 'sub-option', 26)

    if allocator == 'flq':
        allocator = 'random'
    leases = srv_msg.get_all_leases()

    # we can have more than one address or prefix so we have to check if randomness (or it's lack) is
    # kept between previously assigned address and newly assigned as well between newly assigned addresses
    new_addresses = [x for x in leases if x['prefix_len'] == 0]
    new_prefixes = [x for x in leases if x['prefix_len'] > 0]

    if allocator:
        if len(new_prefixes) > 1:
            # with 125 delegated length prefix will change by 8!
            assert _check_multiple_v6_addresses(new_prefixes, offset=8) == allocator, \
                f"Looks like assigned prefixes are not with {allocator} allocator: {new_prefixes}"

        if len(new_addresses) > 1:
            assert _check_multiple_v6_addresses(new_addresses) == allocator, \
                f"Looks like assigned prefixes are not with {allocator} allocator: {new_addresses}"

        # check if previously assigned and new meet allocator requirements
        old_addresses = [x for x in all_leases if x['prefix_len'] == 0]
        old_prefixes = [x for x in all_leases if x['prefix_len'] > 0]

        if len(old_prefixes) > 0:
            assert _check_multiple_v6_addresses(old_prefixes + new_prefixes, offset=8) == allocator, \
                f"Looks like assigned prefixes are not with {allocator} allocator: {old_prefixes + new_prefixes}"

        if len(old_addresses) > 0:
            assert _check_multiple_v6_addresses(old_addresses + new_addresses) == allocator, \
                f"Looks like assigned addresses are not with {allocator} allocator: {old_addresses + new_addresses}"

    # check if address/prefix belongs to subnets
    for address in new_addresses:
        srv_msg.check_if_address_belongs_to_subnet(subnet=f"{relay[:-1]}/{netmask}", address=address['address'])
    for prefix in new_prefixes:
        srv_msg.check_if_address_belongs_to_subnet(subnet=f"{relay[:-1].replace('db8', 'db7')}/{netmask}",
                                                   address=prefix['address'])
    return leases


@pytest.mark.v6
@pytest.mark.allocators
@pytest.mark.parametrize('backend', ['memfile', 'postgresql', 'mysql'])
@pytest.mark.parametrize('scope', ['subnets', 'shared-networks'])
def test_v6_allocators(backend, scope):
    """Test allocators in v6, addresses as well as prefixes. Checks:
    - randomness between addresses/prefixes assigned in single exchange (one client)
    - randomness between addresses/prefixes assigned in multiple exchanges (multiple clients)
    - correctness of address/prefix assigned (if it fits subnet)
    :param backend: database backend
    :type backend: str
    :param scope:
    :type scope:
    """
    misc.test_setup()
    netmask = 110
    srv_control.config_srv_subnet('2001:db8:1::/64', f'2001:db8:1::/{netmask}',
                                  allocator='iterative', pd_allocator='iterative')
    srv_control.config_srv_another_subnet_no_interface('2001:db8:2::/64', f'2001:db8:2::/{netmask}',
                                                       allocator='random', pd_allocator='random')
    srv_control.config_srv_another_subnet_no_interface('2001:db8:3::/64', f'2001:db8:3::/{netmask}',
                                                       allocator='random', pd_allocator='flq')

    srv_control.config_srv_prefix('2001:db7:1::', 0, netmask, 125)
    srv_control.config_srv_prefix('2001:db7:2::', 1, netmask, 125)
    srv_control.config_srv_prefix('2001:db7:3::', 2, netmask, 125)

    if scope == "shared_networks":
        srv_control.shared_subnet('2001:db8:1::/64', 0)
        srv_control.shared_subnet('2001:db8:2::/64', 0)
        srv_control.shared_subnet('2001:db8:3::/64', 0)

        srv_control.set_conf_parameter_shared_subnet('name', '"name-abc"', 0)
        srv_control.set_conf_parameter_shared_subnet('interface', '"$(SERVER_IFACE)"', 0)

    srv_control.config_srv_id('LL', '00:03:00:01:ff:ff:ff:ff:ff:01')
    srv_control.define_lease_db_backend(backend)

    srv_control.build_and_send_config_files()

    srv_control.start_srv('DHCP', 'started')

    leases_subnet1 = []
    leases_subnet2 = []
    leases_subnet3 = []

    for i in range(10, 15):
        leases_subnet1 += _get_lease_6('iterative', iaid=3, iapd=3, relay='2001:db8:1::1',
                                       mac=f'11:f5:f4:f3:f2:{i}', all_leases=leases_subnet1, netmask=netmask)
        leases_subnet2 += _get_lease_6('random', iaid=3, iapd=3, relay='2001:db8:2::1',
                                       mac=f'22:f5:f4:f3:f2:{i}', all_leases=leases_subnet2, netmask=netmask)
        leases_subnet3 += _get_lease_6('random', iaid=3, iapd=3, relay='2001:db8:3::1',
                                       mac=f'33:f5:f4:f3:f2:{i}', all_leases=leases_subnet3, netmask=netmask)

    for i in range(20, 25):  # without prefix
        leases_subnet1 += _get_lease_6('iterative', iaid=2, relay='2001:db8:1::1',
                                       mac=f'44:f5:f4:f3:f2:{i}', all_leases=leases_subnet1, netmask=netmask)
        leases_subnet2 += _get_lease_6('random', iaid=2, relay='2001:db8:2::1',
                                       mac=f'55:f5:f4:f3:f2:{i}', all_leases=leases_subnet2, netmask=netmask)
        leases_subnet3 += _get_lease_6('random', iaid=2, relay='2001:db8:3::1',
                                       mac=f'66:f5:f4:f3:f2:{i}', all_leases=leases_subnet3, netmask=netmask)

    for i in range(30, 35):  # with just prefix
        leases_subnet1 += _get_lease_6('iterative', iapd=2, relay='2001:db8:1::1',
                                       mac=f'77:f5:f4:f3:f2:{i}', all_leases=leases_subnet1, netmask=netmask)
        leases_subnet2 += _get_lease_6('random', iapd=2, relay='2001:db8:2::1',
                                       mac=f'88:f5:{i}:f3:f2:{i}', all_leases=leases_subnet2, netmask=netmask)
        leases_subnet3 += _get_lease_6('random', iapd=2, relay='2001:db8:3::1',
                                       mac=f'99:f5:f4:f3:{i}:{i}', all_leases=leases_subnet3, netmask=netmask)

    all_leases = leases_subnet1 + leases_subnet2 + leases_subnet3
    srv_msg.check_leases(all_leases, backend=backend)

    for i in filter(lambda d: d['prefix_len'] > 0, all_leases):
        print(f"duid: {i['duid']}; iaid: {i['iaid']}; prefix: {i['address']}; prefix: {i['prefix_len']}")

    for i in filter(lambda d: d['prefix_len'] == 0, all_leases):
        print(f"duid: {i['duid']}; iaid: {i['iaid']}; address: {i['address']}")


@pytest.mark.v6
@pytest.mark.allocators
@pytest.mark.parametrize('backend', ['memfile'])
@pytest.mark.parametrize('prefix_allocator', ['random', 'flq'])
def test_v6_allocator_randomness(backend, prefix_allocator):
    """This will check if random and flq allocator will assign different addresses after Kea restart.
    :param backend: database backend
    :type backend: str
    :param prefix_allocator:
    :type prefix_allocator:
    """
    misc.test_setup()
    netmask = 112
    srv_control.config_srv_subnet('2001:db8:1::/64', f'2001:db8:1::/{netmask}',
                                  allocator='random', pd_allocator=prefix_allocator)

    srv_control.config_srv_prefix('2001:db7:1::', 0, netmask, 125)
    srv_control.config_srv_id('LL', '00:03:00:01:ff:ff:ff:ff:ff:01')
    srv_control.define_lease_db_backend(backend)

    srv_control.build_and_send_config_files()
    srv_control.start_srv('DHCP', 'started')

    before_restart = []

    for i in range(10, 30):
        before_restart += _get_lease_6('random', iaid=3, iapd=3, relay='2001:db8:1::1',
                                       mac=f'11:f5:f4:f3:f2:{i}', all_leases=before_restart)
    srv_msg.check_leases(before_restart, backend=backend)

    srv_control.start_srv('DHCP', 'stopped')
    srv_control.clear_some_data('all')

    misc.test_setup()
    srv_control.config_srv_subnet('2001:db8:1::/64', f'2001:db8:1::/{netmask}',
                                  allocator='random', pd_allocator='random')

    srv_control.config_srv_prefix('2001:db7:1::', 0, netmask, 125)
    srv_control.config_srv_id('LL', '00:03:00:01:ff:ff:ff:ff:ff:01')
    srv_control.define_lease_db_backend(backend)

    srv_control.build_and_send_config_files()
    srv_control.start_srv('DHCP', 'started')

    # get the same number of leases with the same duids
    after_restart = []
    for i in range(10, 30):
        after_restart += _get_lease_6('random', iaid=3, iapd=3, relay='2001:db8:1::1',
                                      mac=f'11:f5:f4:f3:f2:{i}', all_leases=after_restart)
    srv_msg.check_leases(after_restart, backend=backend)

    addresses_before_restart = [x for x in before_restart if x['prefix_len'] == 0]
    addresses_after_restart = [x for x in after_restart if x['prefix_len'] == 0]

    prefixes_before_restart = [x for x in before_restart if x['prefix_len'] > 0]
    prefixes_after_restart = [x for x in after_restart if x['prefix_len'] > 0]

    for lease1, lease2 in zip(addresses_before_restart, addresses_after_restart):
        log.debug("Checking %s and %s", lease1['address'], lease2['address'])
        assert lease1['address'] != lease2['address'], "Looks like address was repeated!"

    for lease1, lease2 in zip(prefixes_before_restart, prefixes_after_restart):
        log.debug("Checking %s and %s", lease1['address'], lease2['address'])
        assert lease1['address'] != lease2['address'], "Looks like address was repeated!"


@pytest.mark.v6
@pytest.mark.allocators
@pytest.mark.parametrize('backend', ['memfile', 'postgresql', 'mysql'])
def test_v6_allocators_exhausted_pools_address(backend):
    """Check if kea can change pools with different allocators
    :param backend: database backend
    :type backend: str
    """
    misc.test_setup()
    srv_control.config_srv_subnet('2001:db8:1::/64', '2001:db8:1::1-2001:db8:1::4', allocator='random')
    srv_control.new_pool('2001:db8:1::6-2001:db8:1::9', 0)
    srv_control.new_pool('2001:db8:1::a-2001:db8:1::d', 0)

    srv_control.config_srv_id('LL', '00:03:00:01:ff:ff:ff:ff:ff:01')
    srv_control.define_lease_db_backend(backend)

    srv_control.build_and_send_config_files()

    srv_control.start_srv('DHCP', 'started')

    leases = []
    for i in range(10, 22):
        leases += _get_lease_6(None, iaid=1, iapd=0, relay='2001:db8:1::1',
                               mac=f'11:f5:f4:f3:f2:{i}', all_leases=leases, netmask=64)

    srv_msg.check_leases(leases, backend=backend)


@pytest.mark.v6
@pytest.mark.allocators
@pytest.mark.parametrize('backend', ['memfile', 'postgresql', 'mysql'])
def test_v6_allocators_exhausted_prefix(backend):
    """Check if kea can change pools with different allocators
    :param backend: database backend
    :type backend: str
    """
    misc.test_setup()

    srv_control.config_srv_subnet('2001:db8:1::/64', '$(EMPTY)', pd_allocator='flq')
    srv_control.add_prefix_to_subnet('2001:db7:1::', 124, 126, 0)
    srv_control.add_prefix_to_subnet('2001:db7:2::', 123, 126, 0)
    srv_control.add_prefix_to_subnet('2001:db7:3::', 122, 126, 0)

    srv_control.define_lease_db_backend(backend)
    srv_control.build_and_send_config_files()

    srv_control.start_srv('DHCP', 'started')

    leases = []
    for i in range(10, 23):
        misc.test_procedure()
        srv_msg.client_sets_value('Client', 'DUID', f'00:03:00:01:11:22:33:44:55:{i}')
        srv_msg.client_does_include('Client', 'IA-PD')
        srv_msg.client_does_include('Client', 'client-id')
        srv_msg.client_send_msg('SOLICIT')

        misc.pass_criteria()
        srv_msg.send_wait_for_message('MUST', 'ADVERTISE')
        srv_msg.response_check_include_option(25)

        misc.test_procedure()
        srv_msg.client_sets_value('Client', 'DUID', f'00:03:00:01:11:22:33:44:55:{i}')
        srv_msg.client_does_include('Client', 'client-id')
        srv_msg.client_copy_option('server-id')
        srv_msg.client_copy_option('IA_PD')
        srv_msg.client_send_msg('REQUEST')

        misc.pass_criteria()
        srv_msg.send_wait_for_message('MUST', 'REPLY')
        srv_msg.response_check_include_option(25)
        srv_msg.response_check_option_content(25, 'sub-option', 26)
        leases += srv_msg.get_all_leases()
    srv_msg.check_leases(leases, backend=backend)


@pytest.mark.v6
@pytest.mark.allocators
@pytest.mark.parametrize('backend', ['memfile', 'postgresql', 'mysql'])
@pytest.mark.parametrize('scope', ['global', 'subnets', 'shared-networks'])
def test_v6_adaptive_lease_time_threshold(backend, scope):
    """Test adaptive lease time threshold option.
    Multiple SARR messages are sent to the server.
    First part of leases should have valid lifetime of 4000, rest of leases should have valid lifetime of 1000.
    Adaptive-lease-time-threshold works only with iapd leases.

    :param backend: database backend
    :type backend: str
    :param scope: scope of the test
    :type scope: str
    """
    misc.test_setup()
    # adaptive lease time threshold is set to 0.5, so 50% of pd leases should have valid lifetime of 4000,
    # leases are rounded and Kea will assign 1 less lease with valid lifetime of 4000
    adaptive_lease_time_threshold = 0.5
    amount_of_max = 7
    amount_of_min = 9
    pool_size = amount_of_max + amount_of_min  # Pool size is connected to prefix length
    if scope == 'subnets':
        srv_control.config_srv_subnet('2001:db8:1::/64',
                                      f'2001:db8:1::1-2001:db8:1::{pool_size}',
                                      pd_allocator='flq',
                                      id=1,
                                      valid_lifetime=4000,
                                      max_valid_lifetime=4000,
                                      min_valid_lifetime=1000,
                                      adaptive_lease_time_threshold=adaptive_lease_time_threshold)

    else:
        srv_control.config_srv_subnet('2001:db8:1::/64',
                                      f'2001:db8:1::1-2001:db8:1::{pool_size}', pd_allocator='flq', id=1)
    srv_control.config_srv_prefix('2001:db6:1::', 0, 124, 128)
    srv_control.config_srv_another_subnet_no_interface('2001:db8:2::/64',
                                                       f'2001:db8:2::1-2001:db8:2::{pool_size}',
                                                       pd_allocator='flq',
                                                       id=2)
    srv_control.config_srv_prefix('2001:db7:1::', 1, 124, 128)

    srv_control.shared_subnet('2001:db8:1::/64', 0)
    srv_control.shared_subnet('2001:db8:2::/64', 0)
    srv_control.set_conf_parameter_shared_subnet('name', '"name-abc"', 0)
    srv_control.set_conf_parameter_shared_subnet('interface', '"$(SERVER_IFACE)"', 0)
    if scope == 'shared-networks':
        srv_control.set_conf_parameter_shared_subnet('valid-lifetime', 4000, 0)
        srv_control.set_conf_parameter_shared_subnet('max-valid-lifetime', 4000, 0)
        srv_control.set_conf_parameter_shared_subnet('min-valid-lifetime', 1000, 0)
        srv_control.set_conf_parameter_shared_subnet('adaptive-lease-time-threshold', adaptive_lease_time_threshold, 0)

    if scope == 'global':
        srv_control.set_conf_parameter_global('valid-lifetime', 4000)
        srv_control.set_conf_parameter_global('max-valid-lifetime', 4000)
        srv_control.set_conf_parameter_global('min-valid-lifetime', 1000)
        srv_control.set_conf_parameter_global('adaptive-lease-time-threshold', adaptive_lease_time_threshold)

    srv_control.define_lease_db_backend(backend)
    srv_control.build_and_send_config_files()
    srv_control.start_srv('DHCP', 'started')

    # send DORA messages to get 20 leases
    for i in range(1, pool_size*2+1):
        srv_msg.SARR(address='ANY',
                     delegated_prefix='ANY',
                     duid=f'00:03:00:01:f6:f5:f4:f3:f2:{i:02}',
                     exchange='sarr-only')

    # check if first amount_of_max leases have valid lifetime of 4000.
    # We count 2 leases per duid because of iana and iapd.
    for i in range(1, amount_of_max+1):
        srv_msg.check_leases({"duid": f'00:03:00:01:f6:f5:f4:f3:f2:{i:02}',
                             "valid_lifetime": 4000, "lease_type": 2}, backend=backend, lease_count=2)

    # check if next amount_of_min leases have valid lifetime of 1000
    # We count 1 lease per duid because of iana is not affected by adaptive lease time threshold.
    for i in range(amount_of_max+1, pool_size+1):
        srv_msg.check_leases({"duid": f'00:03:00:01:f6:f5:f4:f3:f2:{i:02}',
                             "valid_lifetime": 1000, "lease_type": 2}, backend=backend, lease_count=1)

    if scope == 'subnets':
        # check if the rest of leases have valid lifetime of 4000
        for i in range(pool_size+1, pool_size*2+1):
            srv_msg.check_leases({"duid": f'00:03:00:01:f6:f5:f4:f3:f2:{i:02}',
                                 "valid_lifetime": 4000, "lease_type": 2}, backend=backend, lease_count=2)
    else:
        # check if first amount_of_max leases in second subnet have valid lifetime of 4000
        for i in range(1+pool_size, amount_of_max+1+pool_size):
            srv_msg.check_leases({"duid": f'00:03:00:01:f6:f5:f4:f3:f2:{i:02}',
                                 "valid_lifetime": 4000, "lease_type": 2}, backend=backend, lease_count=2)

        # check if next amount_of_min leases in second subnet have valid lifetime of 1000
        for i in range(amount_of_max+1+pool_size, amount_of_max+amount_of_min+1+pool_size):
            srv_msg.check_leases({"duid": f'00:03:00:01:f6:f5:f4:f3:f2:{i:02}',
                                 "valid_lifetime": 1000, "lease_type": 2}, backend=backend, lease_count=1)
