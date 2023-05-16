# Copyright (C) 2023 Internet Systems Consortium, Inc. ("ISC")
#
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

"""Kea random and flq allocators"""


import pytest
import ipaddress
import logging

from src import misc
from src import srv_control
from src import srv_msg

log = logging.getLogger('forge')


def _get_lease_4(allocator: str, mac: str, giaddr: str, all_leases: list = None):
    """
    Get v4 lease from kea. Check if address is correct by checking previously assigned address.
    :param allocator: type of allocator
    :param mac: mac address of a client
    :param giaddr: relay address
    :param all_leases: list of previously assigned leases from single subnet
    :return: dictionary with single lease
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
    srv_msg.check_if_address_belongs_to_subnet(subnet=f"{giaddr[:-1]}0/24", address=lease['address'])
    # let's check if address is actually correct for allocator

    if len(all_leases) != 0:
        if allocator == 'iterative':
            # we want to have new address to be next from the last received
            assert ipaddress.ip_address(msg.yiaddr) == ipaddress.ip_address(all_leases[-1]["address"]) + 1,\
                f"Received address {msg.yiaddr} is not +1 after previously assigned"
        else:
            assert ipaddress.ip_address(msg.yiaddr) != ipaddress.ip_address(all_leases[-1]["address"]) + 1, \
                f"Received address {msg.yiaddr} is simple +1 after previously assigned this is incorrect for flq/random"

        log.debug(f'Current {msg.yiaddr} previous was {all_leases[-1]["address"]}')
    return lease


@pytest.mark.v4
@pytest.mark.allocators
@pytest.mark.parametrize('backend', ['memfile', 'postgresql', 'mysql'])
@pytest.mark.parametrize('scope', ['subnets', 'shared-networks'])
def test_v4_allocators(backend, scope):
    """
    Get 10 addresses from each subnet, check if:
    - iterative starts from first and have all others are one by one
    - random and flq wont start from first in the pool and each next is not +1 from the previous
    - check if all leases are correctly saved in the lease file/database
    - allocator configured per subnet
    """
    misc.test_setup()
    srv_control.config_srv_subnet('192.168.50.0/24', '192.168.50.0/24', allocator='iterative')
    srv_control.config_srv_another_subnet_no_interface('192.168.51.0/24', '192.168.51.0/24', allocator='flq')
    srv_control.config_srv_another_subnet_no_interface('192.168.52.0/24', '192.168.52.0/24', allocator='random')

    if scope is "shared_networks":
        srv_control.shared_subnet('192.168.50.0/24', 0)
        srv_control.shared_subnet('192.168.51.0/24', 0)
        srv_control.shared_subnet('192.168.52.0/24', 0)

        srv_control.set_conf_parameter_shared_subnet('name', '"name-abc"', 0)
        srv_control.set_conf_parameter_shared_subnet('interface', '"$(SERVER_IFACE)"', 0)

    srv_control.define_temporary_lease_db_backend(backend)

    srv_control.build_and_send_config_files()

    srv_control.start_srv('DHCP', 'started')
    leases_subnet1 = list()
    leases_subnet2 = list()
    leases_subnet3 = list()
    for i in range(10, 20):
        leases_subnet1.append(_get_lease_4('iterative', f'22:00:00:00:00:{i}', '192.168.50.1', leases_subnet1))
        leases_subnet2.append(_get_lease_4('flq', f'33:00:00:00:00:{i}', '192.168.51.1', leases_subnet2))
        leases_subnet3.append(_get_lease_4('random', f'44:00:00:00:00:{i}', '192.168.52.1', leases_subnet3))
    srv_msg.check_leases(leases_subnet1 + leases_subnet2 + leases_subnet3, backend=backend)
