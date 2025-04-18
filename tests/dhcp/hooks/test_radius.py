# Copyright (C) 2022-2024 Internet Systems Consortium, Inc. ("ISC")
#
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

# pylint: disable=invalid-name
# pylint: disable=line-too-long
# pylint: disable=too-many-branches
# pylint: disable=unused-argument

import pytest

from src import misc
from src import srv_control
from src import srv_msg

from src.forge_cfg import world
from src.protosupport.multi_protocol_functions import wait_for_message_in_log
from src.softwaresupport.cb_model import setup_server_with_radius
from src.softwaresupport import radius


@pytest.mark.v4
@pytest.mark.v4_bootp
@pytest.mark.v6
@pytest.mark.radius
@pytest.mark.parametrize('backend', ['memfile'])  # other possible values: 'mysql', 'postgresql'
@pytest.mark.parametrize('config_type', ['multiple-subnets'])  # other possible values: 'network', 'subnet'
@pytest.mark.parametrize('radius_reservation_in_pool', ['radius-reservation-in-pool', 'radius-reservation-outside-pool'])
def test_RADIUS(dhcp_version: str,
                backend: str,
                config_type: str,
                radius_reservation_in_pool: str):
    """
    Check RADIUS functionality on various Kea configurations.
    See radius.send_and_receive() for explanations on what the parametrizations mean.

    :param dhcp_version: the DHCP version being tested
    :param backend: the lease database backend type
    :param config_type: different configurations used in testing
    :param radius_reservation_in_pool: whether there is an existing pool in Kea that contains the
                                       lease reserved by RADIUS for the first client in this test.
                                       In both cases, the reserved lease is inside the initially
                                       assigned subnet.
    """

    misc.test_setup()

    # Provide RADIUS configuration and start RADIUS server.
    radius.add_usual_reservations()
    radius.init_and_start_radius()

    # Configure and start Kea.
    configs = radius.configurations()
    setup_server_with_radius(**configs[config_type])
    srv_control.define_lease_db_backend(backend)
    if dhcp_version == 'v4_bootp':
        srv_control.add_hooks('libdhcp_bootp.so')
    if radius_reservation_in_pool == 'radius-reservation-in-pool':
        # We can afford the more complex case of subnet reselection if the reservation is in pool.
        srv_control.add_parameter_to_hook('libdhcp_radius.so', 'reselect-subnet-address', True)
        srv_control.add_parameter_to_hook('libdhcp_radius.so', 'reselect-subnet-pool', True)
    else:
        # The only way a test case can pass if the reservation is out of pool is with reselect.
        srv_control.add_parameter_to_hook('libdhcp_radius.so', 'reselect-subnet-address', False)
        srv_control.add_parameter_to_hook('libdhcp_radius.so', 'reselect-subnet-pool', False)
    srv_control.build_and_send_config_files()
    srv_control.start_srv('DHCP', 'started')

    # Check the leases.
    leases = radius.send_and_receive(config_type, radius_reservation_in_pool)

    # Check that the leases are in the backend.
    srv_msg.check_leases(leases, backend=backend)


@pytest.mark.v4
@pytest.mark.v4_bootp
@pytest.mark.v6
@pytest.mark.radius
@pytest.mark.parametrize('attribute_cardinality', ['single-attribute', 'double-attributes-bogus-first', 'double-attributes-bogus-last'])
def test_RADIUS_framed_pool(dhcp_version: str, attribute_cardinality: str):
    """
    Check that Kea can classify a packet using a single type of RADIUS
    attribute, either v4 or v6, as opposed to having both assigned, as in
    test_RADIUS.

    :param dhcp_version: the DHCP version being tested
    :param attribute_cardinality: whether support for multiple attributes is tested
    """

    misc.test_setup()

    # RFC 2869 says that zero or one instance of the framed pool attribute MAY
    # be present.
    attributes = []
    if attribute_cardinality == 'double-attributes-bogus-first':
        attributes.append('Framed-Pool = "bogus"')
    attributes.append('Framed-Pool = "gold"')
    if attribute_cardinality == 'double-attributes-bogus-last':
        attributes.append('Framed-Pool = "bogus"')

    # Provid§e RADIUS configuration and start RADIUS server.
    radius.add_reservation('08:00:27:b0:c1:41', attributes)
    radius.init_and_start_radius()

    # Configure and start Kea.
    configs = radius.configurations()
    setup_server_with_radius(**configs['network'])
    if dhcp_version == 'v4_bootp':
        srv_control.add_hooks('libdhcp_bootp.so')
    srv_control.build_and_send_config_files()
    srv_control.start_srv('DHCP', 'started')

    if attribute_cardinality == 'double-attributes-bogus-last':
        # Whether Kea takes only the first pool into consideration, as it happens at
        # the time of writing, or if the allocation explicitly fails, expect the
        # client to not get the gold lease.
        radius.send_message_and_expect_no_more_leases(mac='08:00:27:b0:c1:41')
    else:
        # For a single attribute, expect the gold lease.
        lease = radius.get_address(mac='08:00:27:b0:c1:41',
                                   expected_lease='192.168.50.5' if world.proto == 'v4' else '2001:db8:50::5')

        # Check that the leases are in the backend.
        srv_msg.check_leases([lease])


@pytest.mark.v4
@pytest.mark.v4_bootp
@pytest.mark.v6
@pytest.mark.radius
def test_RADIUS_no_attributes(dhcp_version: str):
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
                'id': 50,
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

    # Check that the leases are in the backend.
    srv_msg.check_leases([lease])


@pytest.mark.v4
@pytest.mark.radius
@pytest.mark.parametrize('config_type', ['subnet', 'network'])
@pytest.mark.parametrize('giaddr', ['in-subnet', 'in-other-subnet', 'out-of-subnet'])
@pytest.mark.parametrize('leading_subnet', ['leading_subnet', '_'])
@pytest.mark.parametrize('reselect', ['reselect', '_'])
def test_RADIUS_giaddr(dhcp_version: str,
                       config_type: str,
                       giaddr: str,
                       leading_subnet: str,
                       reselect: str):
    """
    Check RADIUS functionality with a client that has a giaddr either belonging
    to a configured subnet inside Kea, or not.

    :param dhcp_version: the DHCP version being tested
    :param config_type: whether usual subnets are used or shared network
    :param giaddr: how the used giaddr is positioned relative to configured subnets
    :param leading_subnet: whether a random subnet is introduced in order to test subnet reselection
    :param reselect: whether to enable reselect-subnet-* in the RADIUS hook library
    """

    misc.test_setup()

    # Provide RADIUS configuration and start RADIUS server.
    radius.add_usual_reservations()
    radius.add_reservation('08:00:27:b0:50:50', [
        'Framed-IP-Address = "192.168.50.123"',
        'Framed-IPv6-Address = "2001:db8:50::123"',
    ])
    radius.add_reservation('08:00:27:b0:77:77', [
        'Framed-IP-Address = "192.168.77.123"',
        'Framed-IPv6-Address = "2001:db8:77::123"',
    ])
    radius.add_reservation('08:00:27:b0:99:99', [
        'Framed-IP-Address = "192.168.99.123"',
        'Framed-IPv6-Address = "2001:db8:99::123"',
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
                if 'client-classes' in j:
                    del j['client-classes']
                for k in j['pools']:
                    if 'client-classes' in k:
                        del k['client-classes']
    if reselect == 'reselect':
        srv_control.add_parameter_to_hook('libdhcp_radius.so', 'reselect-subnet-address', True)
        srv_control.add_parameter_to_hook('libdhcp_radius.so', 'reselect-subnet-pool', True)
    else:
        srv_control.add_parameter_to_hook('libdhcp_radius.so', 'reselect-subnet-address', False)
        srv_control.add_parameter_to_hook('libdhcp_radius.so', 'reselect-subnet-pool', False)

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
    else:
        giaddr_value = None
        pytest.fail(f"unrecognized giaddr == '{giaddr}'")

    leases = []

    if giaddr == 'out-of-subnet':
        # If a subnet is not selected initially, nothing makes the client able to get a lease. Not
        # even the RADIUS reselect is able to select a subnet for the packet, so zero chances for a
        # dynamic lease. On top of that, there is no RADIUS request sent, so also zero chances of
        # the client getting the address reserved in RADIUS.
        radius.send_message_and_expect_no_more_leases(mac='08:00:27:b0:50:50',
                                                      giaddr=giaddr_value)
        wait_for_message_in_log('DHCP4_SUBNET_SELECTION_FAILED.*failed to select subnet for the client')
        radius.send_message_and_expect_no_more_leases(mac='08:00:27:b0:77:77',
                                                      giaddr=giaddr_value)
        wait_for_message_in_log('DHCP4_SUBNET_SELECTION_FAILED.*failed to select subnet for the client', 2)
        radius.send_message_and_expect_no_more_leases(mac='08:00:27:b0:99:99',
                                                      giaddr=giaddr_value)
        wait_for_message_in_log('DHCP4_SUBNET_SELECTION_FAILED.*failed to select subnet for the client', 3)

    elif reselect == 'reselect':
        # There is a subnet that can hold the reserved address. Reselect is enabled, so regardless
        # of giaddr and the initially selected subnet, the reserved address is given to the client.
        leases.append(radius.get_address(mac='08:00:27:b0:50:50',
                                         giaddr=giaddr_value,
                                         expected_lease='192.168.50.123'))

        # Reserved RADIUS address out of any subnet. Reselect is enabled, so the packet gets
        # assigned to SUBNET_ID_UNUSED. Expect no response.
        radius.send_message_and_expect_no_more_leases(mac='08:00:27:b0:77:77',
                                                      giaddr=giaddr_value)

        # There is a subnet that can hold the reserved address. Reselect is enabled, so regardless
        # of giaddr and the initially selected subnet, the reserved address is given to the client.
        leases.append(radius.get_address(mac='08:00:27:b0:99:99',
                                         giaddr=giaddr_value,
                                         expected_lease='192.168.99.123'))

    elif giaddr == 'in-subnet':
        # giaddr 'in-subnet', reserved RADIUS address also in the same subnet.
        # The client should get the lease configured in RADIUS.
        leases.append(radius.get_address(mac='08:00:27:b0:50:50',
                                         giaddr=giaddr_value,
                                         expected_lease='192.168.50.123'))

        if giaddr == 'network':
            # giaddr 'in-subnet', reserved RADIUS address out of any subnet.
            # The client should get a lease from the dynamic pool.
            leases.append(radius.get_address(mac='08:00:27:b0:77:77',
                                             giaddr=giaddr_value,
                                             expected_lease='192.168.50.5'))
        elif giaddr == 'subnet':
            # giaddr 'in-subnet', reserved RADIUS address out of any subnet.
            # Not in a shared network, so it doesn't benefit from normal reselection caused by the
            # global address reservation, so it blindly gets the reserved address.
            leases.append(radius.get_address(mac='08:00:27:b0:77:77',
                                             giaddr=giaddr_value,
                                             expected_lease='192.168.77.123'))

        if giaddr == 'network':
            # giaddr 'in-subnet', reserved RADIUS in another subnet.
            # The client should get a lease from the dynamic pool.
            leases.append(radius.get_address(mac='08:00:27:b0:99:99',
                                             giaddr=giaddr_value,
                                             expected_lease='192.168.50.5'))
        elif giaddr == 'subnet':
            # giaddr 'in-subnet', reserved RADIUS in another subnet.
            # Not in a shared network, so it doesn't benefit from normal reselection caused by the
            # global address reservation, so it blindly gets the reserved address.
            leases.append(radius.get_address(mac='08:00:27:b0:99:99',
                                             giaddr=giaddr_value,
                                             expected_lease='192.168.99.123'))

    elif giaddr == 'in-other-subnet':
        if giaddr == 'network':
            # giaddr 'in-other-subnet', reserved RADIUS address in another subnet.
            # The client should get a lease from the dynamic pool.
            leases.append(radius.get_address(mac='08:00:27:b0:50:50',
                                             giaddr=giaddr_value,
                                             expected_lease='192.168.99.0'))
        elif giaddr == 'subnet':
            # giaddr 'in-other-subnet', reserved RADIUS address in another subnet.
            # Not in a shared network, so it doesn't benefit from normal reselection caused by the
            # global address reservation, so it blindly gets the reserved address.
            leases.append(radius.get_address(mac='08:00:27:b0:50:50',
                                             giaddr=giaddr_value,
                                             expected_lease='192.168.50.123'))

        if giaddr == 'network':
            # giaddr 'in-other-subnet', reserved RADIUS address out of any subnet.
            # The client should get a lease from the dynamic pool.
            leases.append(radius.get_address(mac='08:00:27:b0:77:77',
                                             giaddr=giaddr_value,
                                             expected_lease='192.168.99.1'))
        elif giaddr == 'subnet':
            # giaddr 'in-other-subnet', reserved RADIUS address out of any subnet.
            # Not in a shared network, so it doesn't benefit from normal reselection caused by the
            # global address reservation, so it blindly gets the reserved address.
            leases.append(radius.get_address(mac='08:00:27:b0:77:77',
                                             giaddr=giaddr_value,
                                             expected_lease='192.168.77.123'))

        # giaddr 'in-other-subnet', reserved RADIUS in the same subnet.
        # The client should get the lease configured in RADIUS.
        leases.append(radius.get_address(mac='08:00:27:b0:99:99',
                                         giaddr=giaddr_value,
                                         expected_lease='192.168.99.123'))

    # Check that the leases are in the backend.
    srv_msg.check_leases(leases)


@pytest.mark.v4
@pytest.mark.v4_bootp
@pytest.mark.v6
@pytest.mark.radius
def test_RADIUS_Delegated_IPv6_Prefix_simple(dhcp_version: str):
    """
    Simple test for the Delegated-IPv6-Prefix RADIUS attribute.

    :param dhcp_version: the DHCP version being tested
    """

    misc.test_setup()

    # Provide RADIUS configuration and start RADIUS server.
    radius.add_usual_reservations()
    radius.init_and_start_radius()

    # Configure a subnet with no pool and start Kea.
    setup_server_with_radius(**{
        f'subnet{world.proto[1]}': [
            {
                'id': 50,
                'interface': world.f_cfg.server_iface,
                'subnet': '192.168.50.5/24'if world.proto == 'v4' else '2001:db8:50::/64'
            }
        ]
    })
    if dhcp_version == 'v4_bootp':
        srv_control.add_hooks('libdhcp_bootp.so')
    srv_control.build_and_send_config_files()
    srv_control.start_srv('DHCP', 'started')

    # Check that Delegated-IPv6-Prefix has no effect on v4.
    if dhcp_version.startswith('v4'):
        radius.send_message_and_expect_no_more_leases(mac='08:ff:ee:dd:cc:00')
        return

    # Two consecutive SARRs should both get the delegated prefix configured in RADIUS.
    srv_msg.SARR(duid='00:03:00:01:08:ff:ee:dd:cc:01', delegated_prefix='2001:db8:0:0:1::/96')
    srv_msg.SARR(duid='00:03:00:01:08:ff:ee:dd:cc:01', delegated_prefix='2001:db8:0:0:1::/96')

    # A random client should not get the delegated prefix configured in RADIUS
    # or any other lease for that matter.
    srv_msg.SARR(duid='00:03:00:01:00:00:00:00:00:00')
    srv_msg.SARR(duid='00:03:00:01:00:00:00:00:00:00')

    # Check that the leases are in the backend.
    srv_msg.check_leases([{'address': '2001:db8:0:0:1::', 'prefix_len': 96}])


@pytest.mark.v6
@pytest.mark.radius
@pytest.mark.parametrize('pool', ['pool', 'no-pool'])
@pytest.mark.parametrize('reselect', ['reselect', '_'])
def test_RADIUS_Delegated_IPv6_Prefix(dhcp_version: str,
                                      pool: str,
                                      reselect: str):
    """
    Check the Delegated-IPv6-Prefix RADIUS attribute.

    :param dhcp_version: the DHCP version being tested
    :param pool: whether to use a pool or not
    :param reselect: whether to enable reselect-subnet-* in the RADIUS hook library
    """

    misc.test_setup()

    # Provide RADIUS configuration and start RADIUS server.
    radius.add_usual_reservations()
    radius.init_and_start_radius()

    # Configure a subnet and start Kea.
    if pool == 'pool':
        setup_server_with_radius(**{
            'subnet6': [
                {
                    'id': 2001,
                    'interface': world.f_cfg.server_iface,
                    'pools': [
                        {
                           'pool': '2001:db8::1 - 2001:db8::100'
                        }
                    ],
                    'subnet': '2001:db8::/64'
                }
            ]
        })
    elif pool == 'no-pool':
        setup_server_with_radius(**{
            'subnet6': [
                {
                    'id': 2001,
                    'interface': world.f_cfg.server_iface,
                    'subnet': '2001:db8::/64'
                }
            ]
        })
    else:
        pytest.fail(f"unrecognized pool == '{pool}'")
    if reselect == 'reselect':
        srv_control.add_parameter_to_hook('libdhcp_radius.so', 'reselect-subnet-address', True)
        srv_control.add_parameter_to_hook('libdhcp_radius.so', 'reselect-subnet-pool', True)
    else:
        srv_control.add_parameter_to_hook('libdhcp_radius.so', 'reselect-subnet-address', False)
        srv_control.add_parameter_to_hook('libdhcp_radius.so', 'reselect-subnet-pool', False)
    srv_control.build_and_send_config_files()
    srv_control.start_srv('DHCP', 'started')

    # All the following should get the delegated prefixes and framed ipv6 addresses configured in RADIUS or otherwise
    # addresses from the dynamic pool.
    srv_msg.SARR(duid='00:03:00:01:08:ff:ee:dd:cc:01',
                 address='2001:db8::1' if pool == 'pool' else None, delegated_prefix='2001:db8:0:0:1::/96')
    srv_msg.SARR(duid='00:03:00:01:08:ff:ee:dd:cc:01',
                 address='2001:db8::1' if pool == 'pool' else None, delegated_prefix='2001:db8:0:0:1::/96')

    srv_msg.SARR(duid='00:03:00:01:08:ff:ee:dd:cc:02',
                 address='2001:db8::2' if pool == 'pool' else None, delegated_prefix='2001:db8:0:0:2::/96')
    srv_msg.SARR(duid='00:03:00:01:08:ff:ee:dd:cc:02',
                 address='2001:db8::2' if pool == 'pool' else None, delegated_prefix='2001:db8:0:0:2::/96')

    srv_msg.SARR(duid='00:03:00:01:08:ff:ee:dd:cc:03',
                 address='2001:db8::3' if pool == 'pool' else None, delegated_prefix='2001:db8:0:0:3::/96')
    srv_msg.SARR(duid='00:03:00:01:08:ff:ee:dd:cc:03',
                 address='2001:db8::3' if pool == 'pool' else None, delegated_prefix='2001:db8:0:0:3::/96')

    srv_msg.SARR(duid='00:03:00:01:08:ff:ee:dd:cc:04',
                 address='2001:db8::4:4:0:0', delegated_prefix='2001:db8:0:0:4::/96')
    srv_msg.SARR(duid='00:03:00:01:08:ff:ee:dd:cc:04',
                 address='2001:db8::4:4:0:0', delegated_prefix='2001:db8:0:0:4::/96')

    # TODO: investigate what is going on. Kea with reselect enabled treats clients with Framed-Pool differently based on
    # whether a subnet has pools or not. That should not be the case.
    if reselect == 'reselect' and pool == 'no-pool':
        srv_msg.SARR(duid='00:03:00:01:08:ff:ee:dd:cc:07')
        srv_msg.SARR(duid='00:03:00:01:08:ff:ee:dd:cc:07')

        srv_msg.SARR(duid='00:03:00:01:08:ff:ee:dd:cc:08')
        srv_msg.SARR(duid='00:03:00:01:08:ff:ee:dd:cc:08')
    else:
        srv_msg.SARR(duid='00:03:00:01:08:ff:ee:dd:cc:07',
                     address='2001:db8::4' if pool == 'pool' else None, delegated_prefix='2001:db8:0:0:7::/96')
        srv_msg.SARR(duid='00:03:00:01:08:ff:ee:dd:cc:07',
                     address='2001:db8::4' if pool == 'pool' else None, delegated_prefix='2001:db8:0:0:7::/96')

        srv_msg.SARR(duid='00:03:00:01:08:ff:ee:dd:cc:08',
                     address='2001:db8::8:8:0:0', delegated_prefix='2001:db8:0:0:8::/96')
        srv_msg.SARR(duid='00:03:00:01:08:ff:ee:dd:cc:08',
                     address='2001:db8::8:8:0:0', delegated_prefix='2001:db8:0:0:8::/96')

    # A random client should not get any lease.
    srv_msg.SARR(duid='00:03:00:01:00:00:00:00:00:00')
    srv_msg.SARR(duid='00:03:00:01:00:00:00:00:00:00')

    # Check that the leases are in the backend.
    srv_msg.check_leases([
        {'address': '2001:db8:0:0:1::', 'duid': '00:03:00:01:08:ff:ee:dd:cc:01', 'prefix_len': 96},
        {'address': '2001:db8:0:0:2::', 'duid': '00:03:00:01:08:ff:ee:dd:cc:02', 'prefix_len': 96},
        {'address': '2001:db8:0:0:3::', 'duid': '00:03:00:01:08:ff:ee:dd:cc:03', 'prefix_len': 96},
        {'address': '2001:db8:0:0:4::', 'duid': '00:03:00:01:08:ff:ee:dd:cc:04', 'prefix_len': 96},
        {'address': '2001:db8::4:4:0:0', 'duid': '00:03:00:01:08:ff:ee:dd:cc:04', 'prefix_len': 128},
    ])
    if pool == 'pool':
        srv_msg.check_leases([
            {'address': '2001:db8::1', 'duid': '00:03:00:01:08:ff:ee:dd:cc:01', 'prefix_len': 128},
            {'address': '2001:db8::2', 'duid': '00:03:00:01:08:ff:ee:dd:cc:02', 'prefix_len': 128},
            {'address': '2001:db8::3', 'duid': '00:03:00:01:08:ff:ee:dd:cc:03', 'prefix_len': 128},
        ])
        if reselect != 'reselect':
            srv_msg.check_leases([
                {'address': '2001:db8::4', 'duid': '00:03:00:01:08:ff:ee:dd:cc:07', 'prefix_len': 128},
            ])

    if reselect != 'reselect' or pool == 'pool':
        srv_msg.check_leases([
            {'address': '2001:db8:0:0:7::', 'duid': '00:03:00:01:08:ff:ee:dd:cc:07', 'prefix_len': 96},
            {'address': '2001:db8:0:0:8::', 'duid': '00:03:00:01:08:ff:ee:dd:cc:08', 'prefix_len': 96},
            {'address': '2001:db8::8:8:0:0', 'duid': '00:03:00:01:08:ff:ee:dd:cc:08', 'prefix_len': 128},
        ])


@pytest.mark.v6
@pytest.mark.radius
def test_RADIUS_Delegated_IPv6_Prefix_same_prefix(dhcp_version: str):
    """
    Check that the Delegated-IPv6-Prefix RADIUS attribute alongside a Framed-IPv6-Address with the same prefix result in
    both leases being offered.

    Fails. Under investigation in kea#3423. When fixed, consider merging the SARRs into
    test_RADIUS_Delegated_IPv6_Prefix_no_pool. The only reason they were separated is because this particular test fails.

    :param dhcp_version: the DHCP version being tested
    """

    misc.test_setup()

    # Provide RADIUS configuration and start RADIUS server.
    radius.add_usual_reservations()
    radius.init_and_start_radius()

    # Configure a subnet with no pool and start Kea.
    setup_server_with_radius(**{
        'subnet6': [
            {
                'id': 2001,
                'interface': world.f_cfg.server_iface,
                'subnet': '2001:db8::/64'
            }
        ]
    })
    srv_control.build_and_send_config_files()
    srv_control.start_srv('DHCP', 'started')

    srv_msg.SARR(duid='00:03:00:01:08:ff:ee:dd:cc:05',
                 address='2001:db8:0:0:5::', delegated_prefix='2001:db8:0:0:5::/96')
    srv_msg.SARR(duid='00:03:00:01:08:ff:ee:dd:cc:05',
                 address='2001:db8:0:0:5::', delegated_prefix='2001:db8:0:0:5::/96')

    # Check that the leases are in the backend.
    srv_msg.check_leases([
        {'address': '2001:db8:0:0:5::', 'prefix_len': 128},
        {'address': '2001:db8:0:0:5::', 'prefix_len': 96},
    ])


@pytest.mark.v6
@pytest.mark.radius
def test_RADIUS_Delegated_IPv6_Prefix_same_prefix_and_prefix_length(dhcp_version: str):
    """
    Check that the Delegated-IPv6-Prefix RADIUS attribute alongside a Framed-IPv6-Address with the same prefix and the
    same prefix length result in both leases being offered.

    Fails. Under investigation in kea#3423. When fixed, consider merging the SARRs into
    test_RADIUS_Delegated_IPv6_Prefix_no_pool. The only reason they were separated is because this particular test fails.

    :param dhcp_version: the DHCP version being tested
    """

    misc.test_setup()

    # Provide RADIUS configuration and start RADIUS server.
    radius.add_usual_reservations()
    radius.init_and_start_radius()

    # Configure a subnet with no pool and start Kea.
    setup_server_with_radius(**{
        'subnet6': [
            {
                'id': 2001,
                'interface': world.f_cfg.server_iface,
                'subnet': '2001:db8::/64'
            }
        ]
    })
    srv_control.build_and_send_config_files()
    srv_control.start_srv('DHCP', 'started')

    srv_msg.SARR(duid='00:03:00:01:08:ff:ee:dd:cc:06',
                 address='2001:db8:0:0:6::', delegated_prefix='2001:db8:0:0:6::/128')
    srv_msg.SARR(duid='00:03:00:01:08:ff:ee:dd:cc:06',
                 address='2001:db8:0:0:6::', delegated_prefix='2001:db8:0:0:6::/128')

    # Check that the leases are in the backend.
    srv_msg.check_leases([
        {'address': '2001:db8:0:0:5::', 'prefix_len': 128},
    ])
