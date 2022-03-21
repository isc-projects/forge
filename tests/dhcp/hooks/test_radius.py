# Copyright (C) 2022 Internet Systems Consortium, Inc. ("ISC")
#
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

# For dhcp_version:
# pylint: disable=unused-argument,line-too-long

import pytest

import misc
import srv_control
import srv_msg

from cb_model import setup_server_with_radius
from forge_cfg import world
from softwaresupport import radius


@pytest.mark.v4
@pytest.mark.v4_bootp
@pytest.mark.v6
@pytest.mark.radius
@pytest.mark.parametrize('backend', ['memfile', 'mysql', 'postgresql'])
@pytest.mark.parametrize('config_type', ['subnet', 'network', 'multiple-subnets'])
@pytest.mark.parametrize('has_reservation', ['client-has-reservation-in-radius', 'client-has-no-reservation-in-radius'])
def test_radius(dhcp_version: str,
                backend: str,
                config_type: str,
                has_reservation: str):
    """
    Check RADIUS functionality on various Kea configurations.
    See radius.send_and_receive() for explanations on what the parametrizations mean.

    :param dhcp_version: the DHCP version being tested
    :param backend: the lease database backend type
    :param config_type: different configurations used in testing
    :param has_reservation: whether the first client coming in with a request has its lease or pool reserved in RADIUS
    """

    misc.test_setup()

    # Provide RADIUS configuration and start RADIUS server.
    radius.add_usual_reservations()
    radius.init_and_start_radius()

    # Configure and start Kea.
    configs = radius.configurations()
    setup_server_with_radius(**configs[config_type])
    srv_control.define_temporary_lease_db_backend(backend)
    if dhcp_version == 'v4_bootp':
        srv_control.add_hooks('libdhcp_bootp.so')
    srv_control.build_and_send_config_files()
    srv_control.start_srv('DHCP', 'started')

    # Check the leases.
    leases = radius.send_and_receive(config_type, has_reservation)

    # Check that leases are in the backend.
    srv_msg.check_leases(leases, backend=backend)


@pytest.mark.v4
@pytest.mark.v4_bootp
@pytest.mark.v6
@pytest.mark.radius
@pytest.mark.parametrize('attribute_cardinality', ['single-attribute', 'double-attributes'])
def test_radius_framed_pool(dhcp_version: str, attribute_cardinality: str):
    """
    Check that Kea can classify a packet using a single type of RADIUS
    attribute, either v4 or v6, as opposed to having both assigned, as in
    test_radius.

    :param dhcp_version: the DHCP version being tested
    :param attribute_cardinality: whether support for multiple attributes is tested
    """

    misc.test_setup()

    # RFC 2869 says that zero or one instance of the framed pool attribute MAY
    # be present.
    attributes = []
    if world.proto == 'v4':
        if attribute_cardinality == 'double-attributes':
            attributes.append('Framed-Pool = "bogus"')
        attributes.append('Framed-Pool = "gold"')
    elif world.proto == 'v6':
        if attribute_cardinality == 'double-attributes':
            attributes.append('Framed-IPv6-Pool = "bogus"')
        attributes.append('Framed-IPv6-Pool = "gold"')

    # Provide RADIUS configuration and start RADIUS server.
    radius.add_reservation('08:00:27:b0:c1:41', attributes)
    radius.init_and_start_radius()

    # Configure and start Kea.
    configs = radius.configurations()
    setup_server_with_radius(**configs['network'])
    if dhcp_version == 'v4_bootp':
        srv_control.add_hooks('libdhcp_bootp.so')
    srv_control.build_and_send_config_files()
    srv_control.start_srv('DHCP', 'started')

    if attribute_cardinality == 'double-attributes':
        # Wether Kea takes only the first pool into consideration, as it happens at
        # the time of writing, or if the allocation explicitly fails, expect the
        # client to not get the gold lease.
        radius.send_message_and_expect_no_more_leases(mac='08:00:27:b0:c1:41')
    else:
        # For a single attribute, expect the gold lease.
        lease = radius.get_address(mac='08:00:27:b0:c1:41',
                                   expected_lease='192.168.50.5' if world.proto == 'v4' else '2001:db8:50::5')

        # Check that leases are in the backend.
        srv_msg.check_leases([lease])


@pytest.mark.v4
@pytest.mark.v4_bootp
@pytest.mark.v6
@pytest.mark.radius
def test_radius_no_attributes(dhcp_version: str):
    """
    Check RADIUS functionality with an authorize file that has an authentication
    entry for the client with no attributes.

    :param dhcp_version: the DHCP version being tested
    """

    misc.test_setup()

    # Provide RADIUS configuration and start RADIUS server.
    radius.add_reservation('08:00:27:b0:c1:41')
    radius.init_and_start_radius()

    # Configure with an unguarded pool and start Kea.
    setup_server_with_radius(**{
        f'subnet{world.proto[1]}': [
            {
                'interface': world.f_cfg.server_iface,
                'pools': [
                    {
                        'pool': '192.168.50.5 - 192.168.50.5' if world.proto == 'v4' else '2001:db8:50::5 - 2001:db8:50::5'
                    }
                ],
                'subnet': '192.168.50.5/24'if world.proto == 'v4' else '2001:db8:50::/64'
            }
        ]
    })
    if dhcp_version == 'v4_bootp':
        srv_control.add_hooks('libdhcp_bootp.so')
    srv_control.build_and_send_config_files()
    srv_control.start_srv('DHCP', 'started')

    # The client should get a lease from the configured pool.
    lease = radius.get_address(mac='08:00:27:b0:c1:41',
                               expected_lease='192.168.50.5' if world.proto == 'v4' else '2001:db8:50::5')

    # Check that leases are in the backend.
    srv_msg.check_leases([lease])


@pytest.mark.v4
@pytest.mark.radius
@pytest.mark.parametrize('config_type', ['subnet', 'network'])
@pytest.mark.parametrize('giaddr', ['in-subnet', 'in-other-subnet', 'out-of-subnet'])
@pytest.mark.parametrize('leading_subnet', ['leading_subnet', '_'])
@pytest.mark.parametrize('reselect', ['reselect', '_'])
def test_radius_giaddr(dhcp_version: str,
                       config_type: str,
                       giaddr: str,
                       leading_subnet: str,
                       reselect: str):
    """
    Check RADIUS functionality with a client that has a giaddr either belonging
    to a configured subnet inisde Kea, or not.

    :param dhcp_version: the DHCP version being tested
    :param config_type: whether usual subnets are used or shared network
    :param giaddr: how the used giaddr is positioned relative to configured subnets
    :param leading_subnet: whether a random subnet is introduced in order to test subnet reselection
    :param reselect: whether to enable reselect-subnet-address in the RADIUS hook library
    """

    misc.test_setup()

    # Provide RADIUS configuration and start RADIUS server.
    radius.add_usual_reservations()
    radius.add_reservation('08:00:27:b0:aa:aa', [
        'Framed-IP-Address = "192.168.50.5"',
        'Framed-IPv6-Address = "2001:db8:50::5"',
    ])
    radius.init_and_start_radius()

    # Configure and start Kea.
    configs = radius.configurations()
    setup_server_with_radius(**configs[config_type])
    # Delete any client class in all pools.
    elements = [world.dhcp_cfg]
    if 'shared-networks' in world.dhcp_cfg:
        elements.append(world.dhcp_cfg['shared-networks'][0])
    for i in elements:
        if 'subnet4' in i:
            for j in i['subnet4']:
                if 'client-class' in j:
                    del j['client-class']
                for k in j['pools']:
                    if 'client-class' in k:
                        del k['client-class']
    if reselect == 'reselect':
        srv_control.add_parameter_to_hook('libdhcp_radius.so', 'reselect-subnet-address', True)

    if dhcp_version == 'v4_bootp':
        srv_control.add_hooks('libdhcp_bootp.so')
    # Add an additional subnet at the beginning to test subnet reselection.
    radius.add_leading_subnet()
    # Add another one random one if the test requests it.
    if leading_subnet == 'leading_subnet':
        radius.add_leading_subnet('192.168.22.0/24', '192.168.22.0 - 192.168.22.255')
    srv_control.build_and_send_config_files()
    srv_control.start_srv('DHCP', 'started')

    # Set giaddr.
    if giaddr == 'in-subnet':
        giaddr_value = '192.168.50.5'
    elif giaddr == 'in-other-subnet':
        giaddr_value = '192.168.99.99'
    elif giaddr == 'out-of-subnet':
        giaddr_value = '192.168.77.77'

    if giaddr == 'out-of-subnet':
        # If a subnet is not selected initially, there will be no RADIUS request
        # sent, and there is no chance of the client getting the address reserved in RADIUS.
        radius.send_message_and_expect_no_more_leases(mac='08:00:27:b0:aa:aa',
                                                      giaddr=giaddr_value)
        srv_msg.wait_for_message_in_log('DHCP4_SUBNET_SELECTION_FAILED.*failed to select subnet for the client')
    else:
        # The client should get the lease configured in RADIUS.
        lease = radius.get_address(mac='08:00:27:b0:aa:aa',
                                   giaddr=giaddr_value,
                                   expected_lease='192.168.50.5')

        # Check that leases are in the backend.
        srv_msg.check_leases([lease])
