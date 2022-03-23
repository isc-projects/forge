# Copyright (C) 2019-2022 Internet Systems Consortium, Inc. ("ISC")
#
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.


from src import srv_msg

from .multi_server_functions import fabric_sudo_command, fabric_send_file, TemporaryFile
from src.protosupport.dhcp4_scen import DHCPv6_STATUS_CODES, get_address4, get_address6, send_discover_with_no_answer
from src.forge_cfg import world

AUTHORIZE_CONTENT = ''


def add_leading_subnet(subnet: str = '192.168.99.0/24',
                       pool: str = '192.168.99.0 - 192.168.99.255'):
    """
    Add to the first position: a subnet or a shared network with a single subnet,
    in both cases with a single pool. The subnet ID is the third octet from the
    v4 address.
    :param subnet: the subnet value
    :param pool: the pool value
    """
    # TODO: make it work with v6?
    v = world.proto[1]
    if f'subnet{v}' in world.dhcp_cfg:
        world.dhcp_cfg[f'subnet{v}'].insert(0, {
            'id': int(subnet.split('.')[2]),
            'interface': world.f_cfg.server_iface,
            'pools': [
                {
                    'pool': pool
                }
            ],
            'subnet': subnet
        })
    if 'shared-networks' in world.dhcp_cfg:
        world.dhcp_cfg['shared-networks'].insert(0,
            {
                'name': subnet,
                f'subnet{v}': [
                    {
                        'id': int(subnet.split('.')[2]),
                        'interface': world.f_cfg.server_iface,
                        'pools': [
                            {
                                'pool': pool
                            }
                        ],
                        'subnet': subnet
                    }
                ]
            }
        )


def add_reservation(mac: str, attributes = None):
    if attributes is None:
        attributes = []

    # User-Name prefix
    if world.proto == 'v4':
        # Arbitrary number prepended to the MAC
        prefix = '11'
    elif world.proto == 'v6':
        # DUID_LL
        prefix = '00:03:00:01'

    global AUTHORIZE_CONTENT
    AUTHORIZE_CONTENT += f'{prefix}:{mac}    Cleartext-password := "{mac}"\n'
    for i, attribute in enumerate(attributes):
        AUTHORIZE_CONTENT += f'    \t{attribute}'
        if i + 1 != len(attributes):
            AUTHORIZE_CONTENT += ','
        AUTHORIZE_CONTENT += '\n'
    AUTHORIZE_CONTENT += '\n'


def add_usual_reservations():
    add_reservation('08:00:27:b0:c1:41', [
        'Framed-IP-Address = "192.168.51.51"',
        'Framed-IPv6-Address = "2001:db8:51::51"',
        'Framed-Pool = "blues"',
        'Framed-IPv6-Pool = "blues"',
    ])

    add_reservation('08:00:27:b0:c1:42', [
        'Framed-IP-Address = "192.168.52.52"',
        'Framed-IPv6-Address = "2001:db8:52::52"',
        'Framed-Pool = "gold"',
        'Framed-IPv6-Pool = "gold"',
    ])

    add_reservation('08:00:27:b0:c5:01', [
        'Framed-Pool = "gold"',
        'Framed-IPv6-Pool = "gold"',
    ])

    add_reservation('08:00:27:b0:c5:02', [
        'Framed-Pool = "gold"',
        'Framed-IPv6-Pool = "gold"',
    ])

    add_reservation('08:00:27:b0:c5:03', [
        'Framed-Pool = "gold"',
        'Framed-IPv6-Pool = "gold"',
    ])

    add_reservation('08:00:27:b0:c5:10', [
        'Framed-IP-Address = "192.168.50.5"',
        'Framed-IPv6-Address = "2001:db8:50::5"',
        'Framed-Pool = "gold"',
        'Framed-IPv6-Pool = "gold"',
    ])

    add_reservation('08:00:27:b0:c6:01', [
        'Framed-Pool = "silver"',
        'Framed-IPv6-Pool = "silver"',
    ])

    add_reservation('08:00:27:b0:c6:02', [
        'Framed-Pool = "silver"',
        'Framed-IPv6-Pool = "silver"',
    ])

    add_reservation('08:00:27:b0:c6:03', [
        'Framed-Pool = "silver"',
        'Framed-IPv6-Pool = "silver"',
    ])

    add_reservation('08:00:27:b0:c7:01', [
        'Framed-Pool = "bronze"',
        'Framed-IPv6-Pool = "bronze"',
    ])

    add_reservation('08:00:27:b0:c7:02', [
        'Framed-Pool = "bronze"',
        'Framed-IPv6-Pool = "bronze"',
    ])

    add_reservation('08:00:27:b0:c7:03', [
        'Framed-Pool = "bronze"',
        'Framed-IPv6-Pool = "bronze"',
    ])

    add_reservation('08:00:27:b0:c8:01', [
        'Framed-Pool = "platinum"',
        'Framed-IPv6-Pool = "platinum"',
    ])


def configurations(interface: str = world.f_cfg.server_iface):
    """
    Return configurations used in RADIUS tests.

    :param interface: the name of the client-facing interface on the server side
    :return: configurations
    """

    v = world.proto[1]
    configs = {}

    configs['subnet'] = {
        f'subnet{v}': [
            {
                'interface': interface,
                'pools': [
                    {
                        'client-class': 'gold',
                        'pool': '192.168.50.5 - 192.168.50.5' if world.proto == 'v4' else '2001:db8:50::5 - 2001:db8:50::5'
                    }
                ],
                'subnet': '192.168.50.0/24' if world.proto == 'v4' else '2001:db8:50::/64'
            }
        ]
    }

    configs['network'] = {
        # Global reservation mode.
        'reservations-global': True,
        'reservations-in-subnet': False,
        'shared-networks': [
            {
                'name': 'net-1',
                f'subnet{v}': [
                    {
                        'interface': interface,
                        'pools': [
                            {
                                'client-class': 'gold',
                                'pool': '192.168.50.5 - 192.168.50.5' if world.proto == 'v4' else '2001:db8:50::5 - 2001:db8:50::5'
                            }
                        ],
                        'subnet': '192.168.50.0/24' if world.proto == 'v4' else '2001:db8:50::/64'
                    }
                ]
            }
        ]
    }

    configs['multiple-subnets'] = {
        # Global reservation mode.
        'reservations-global': True,
        'reservations-in-subnet': False,
        'shared-networks': [
            {
                'name': 'net-1',
                f'subnet{v}': [
                    {
                        'interface': interface,
                        'pools': [
                            {
                                'client-class': 'gold',
                                'pool': '192.168.50.5 - 192.168.50.5' if world.proto == 'v4' else '2001:db8:50::5 - 2001:db8:50::5'
                            }, {
                                'client-class': 'silver',
                                'pool': '192.168.50.6 - 192.168.50.6' if world.proto == 'v4' else '2001:db8:50::6 - 2001:db8:50::6'
                            }, {
                                'client-class': 'bronze',
                                'pool': '192.168.50.7 - 192.168.50.7' if world.proto == 'v4' else '2001:db8:50::7 - 2001:db8:50::7'
                            }
                        ],
                        'subnet': '192.168.50.0/24' if world.proto == 'v4' else '2001:db8:50::/64'
                    },
                    {
                        'interface': interface,
                        'pools': [
                            {
                                'client-class': 'gold',
                                'pool': '192.168.60.5 - 192.168.60.5' if world.proto == 'v4' else '2001:db8:60::5 - 2001:db8:60::5'
                            }, {
                                'client-class': 'silver',
                                'pool': '192.168.60.6 - 192.168.60.6' if world.proto == 'v4' else '2001:db8:60::6 - 2001:db8:60::6'
                            }
                        ],
                        'subnet': '192.168.60.0/24' if world.proto == 'v4' else '2001:db8:60::/64'
                    },
                    {
                        'client-class': 'platinum',
                        'interface': interface,
                        'pools': [
                            {
                                'pool': '192.168.70.5 - 192.168.70.5' if world.proto == 'v4' else '2001:db8:70::5 - 2001:db8:70::5'
                            }
                        ],
                        'subnet': '192.168.70.0/24' if world.proto == 'v4' else '2001:db8:70::/64'
                    }
                ]
            }
        ]
    }

    return configs


def get_address(mac: str, giaddr: str = None, expected_lease: str = None):
    """
    Make a full exchange, check that the expected lease is received and,
    finally, return the received leases.

    :param mac: the client's MAC address
    :param giaddr: the v4 client's giaddr value
    :param expected_lease: a lease that's expected to be given by the DHCP server
    :return: the leased v4 address or the first lease in the v6 case, in both cases along with the client ID and MAC address
    """

    if world.proto == 'v4':
        client_id = '11' + mac.replace(':', '')
        address = get_address4(chaddr=mac,
                               client_id=client_id,
                               giaddr=giaddr,
                               exp_yiaddr=expected_lease)
        return {
            'address': address,
            'client_id': client_id,
            'hwaddr': mac
        }
    if world.proto == 'v6':
        duid = '00:03:00:01:' + mac
        addresses = get_address6(duid=duid, exp_ia_na_iaaddr_addr=expected_lease)
        # Tests check only one address, so return the first.
        return {
            'address': addresses[0] if len(addresses) > 0 else None,
            'duid': duid
        }
    assert False, f'unknown proto {world.proto}'


def init_and_start_radius(destination: str = world.f_cfg.mgmt_address):
    """
    Configure and restart RADIUS on remote hosts.
    :param destination: address of the server that hosts the RADIUS service
    """
    _init_radius(destination=destination)
    _start_radius(destination=destination)

    # Reset for next use.
    global AUTHORIZE_CONTENT
    AUTHORIZE_CONTENT = ''


def send_and_receive(config_type: str, has_reservation: str):
    """
    Exchange messages and check that the proper leases were returned according
    to Kea's configuration.

    :param config_type: different configurations used in testing
        * 'subnet': a classified pool with a single address configured inside a traditional subnet
        * 'network': a classified pool with a single address configured inside a shared network
        * 'multiple-subnets': multiple classified pools in multiple subnets inside a shared network
    :param has_reservation: whether the first client coming in with a request has its lease or pool reserved in RADIUS
        * 'client-has-reservation-in-radius': yes
        * 'client-has-no-reservation-in-radius': no
    :return list of dictionaries of leases containing address, client_id, mac
    """

    leases = []

    if has_reservation == 'client-has-reservation-in-radius':
        # Get a lease that is explicitly configured in RADIUS as
        # Framed-IP-Address that is part of a configured pool in Kea.
        leases.append(get_address(mac='08:00:27:b0:c5:10',
                                  expected_lease='192.168.50.5' if world.proto == 'v4' else '2001:db8:50::5'))

        # If the config has only one address in the pool...
        if config_type in ['subnet', 'network']:
            # Even if the client has the right gold Framed-Pool, it should get
            # no lease because the pool is full.
            send_message_and_expect_no_more_leases(mac='08:00:27:b0:c5:01')
        else:
            # It should get the '60-5' lease, but don't lease that address here
            # so that the rest of the test is the same.
            pass

    elif has_reservation == 'client-has-no-reservation-in-radius':
        # Get a lease that is explicitly configured in RADIUS as
        # Framed-IP-Address that is outside of any configured pool in Kea.
        leases.append(get_address(mac='08:00:27:b0:c1:42',
                                  expected_lease='192.168.52.52' if world.proto == 'v4' else '2001:db8:52::52'))

        # A client with a gold Framed-Pool should get the lease because the
        # pool has a free lease.
        leases.append(get_address(mac='08:00:27:b0:c5:01',
                                  expected_lease='192.168.50.5' if world.proto == 'v4' else '2001:db8:50::5'))

    # 'multiple-subnets' is more complex so treat it first.
    if config_type == 'multiple-subnets':
        # Skip 192.168.50.5 / 2001:db8:50::5 because it was leased previously.
        gold_ips = {'192.168.60.5' if world.proto == 'v4' else '2001:db8:60::5'}
        silver_ips = {'192.168.50.6' if world.proto == 'v4' else '2001:db8:50::6',
                      '192.168.60.6' if world.proto == 'v4' else '2001:db8:60::6'}

        # Get the lease that is configured explicitly in RADIUS with
        # Framed-IP-Address.
        leases.append(get_address(mac='08:00:27:b0:c1:42',
                                  expected_lease='192.168.52.52' if world.proto == 'v4' else '2001:db8:52::52'))

        # ---- Take all addresses from gold pools. ----
        # Skip 192.168.50.5 / 2001:db8:50::5 because it was leased previously.

        # Lease the second and last gold address.
        lease = get_address(mac='08:00:27:b0:c5:02')
        assert lease['address'] in gold_ips
        gold_ips.remove(lease['address'])
        leases.append(lease)

        # No more leases.
        send_message_and_expect_no_more_leases(mac='08:00:27:b0:c5:03')

        # ---- Take all addresses from silver pools. ----
        # Lease the first silver address.
        lease = get_address(mac='08:00:27:b0:c6:01')
        assert lease['address'] in silver_ips
        silver_ips.remove(lease['address'])
        leases.append(lease)

        # Lease the second and last silver address.
        lease = get_address(mac='08:00:27:b0:c6:02')
        assert lease['address'] in silver_ips
        silver_ips.remove(lease['address'])
        leases.append(lease)

        # No more leases.
        send_message_and_expect_no_more_leases(mac='08:00:27:b0:c6:03')

        # ---- Take all addresses from bronze pools. ----
        # Lease the first and only bronze address.
        leases.append(get_address(mac='08:00:27:b0:c7:01',
                                  expected_lease='192.168.50.7' if world.proto == 'v4' else '2001:db8:50::7'))

        # No more leases.
        send_message_and_expect_no_more_leases(mac='08:00:27:b0:c7:02')

        # Platinum client gets platinum lease.
        leases.append(get_address(mac='08:00:27:b0:c8:01',
                                  expected_lease='192.168.70.5' if world.proto == 'v4' else '2001:db8:70::5'))

    # Remove None from leases because it doesn't play nice with srv_msg.check_leases().
    leases = [l for l in leases if l is not None]

    return leases


def send_message_and_expect_no_more_leases(mac: str, giaddr: str = None):
    """
    Send a discover or a solicit and expect the exhausted leases case which is
    no answer for v4 or NoAddrsAvail status code for v6.

    :param mac: the client's MAC address
    :param giaddr: the v4 client's giaddr value
    """
    if world.proto == 'v4':
        client_id = '11' + mac.replace(':', '')
        send_discover_with_no_answer(chaddr=mac, client_id=client_id, giaddr=giaddr)
    elif world.proto == 'v6':
        duid = '00:03:00:01:' + mac
        srv_msg.SA(duid=duid, status_code=DHCPv6_STATUS_CODES['NoAddrsAvail'])
    else:
        assert False, f'unknown proto {world.proto}'


def _init_radius(destination: str = world.f_cfg.mgmt_address):
    """
    Create authorize file and clients.conf needed by RADIUS and send them to {destination}.
    :param destination: address where RADIUS is set up
    """

    global AUTHORIZE_CONTENT
    authorize_file = 'authorize.txt'
    with TemporaryFile(authorize_file, AUTHORIZE_CONTENT):
        if world.server_system == 'redhat':
            # freeradius 3.x
            fabric_send_file(authorize_file, '/etc/raddb/mods-config/files/authorize',
                             destination_host=destination)
        else:
            # freeradius 3.x
            fabric_send_file(authorize_file,
                             '/etc/freeradius/3.0/mods-config/files/authorize',
                             destination_host=destination)
            # freeradius 2.x
            fabric_send_file(authorize_file, '/etc/freeradius/users',
                             destination_host=destination)

    # clients.conf file
    clients_conf_content = '''
client {mgmt_address} {{
   ipaddr = {mgmt_address}
   require_message_authenticator = no
   secret = testing123
   proto = *
   nas_type = other
   limit {{
      max_connections = 16
      lifetime = 0
      idle_timeout = 30
   }}
}}'''
    clients_conf_content = clients_conf_content.format(mgmt_address=destination)
    clients_conf_file = 'clients.conf'
    with TemporaryFile(clients_conf_file, clients_conf_content):
        if world.server_system == 'redhat':
            # freeradius 3.x
            fabric_send_file(clients_conf_file, '/etc/raddb/clients.conf',
                             destination_host=destination)
        else:
            # freeradius 3.x
            fabric_send_file(clients_conf_file, '/etc/freeradius/3.0/clients.conf',
                             destination_host=destination)
            # freeradius 2.x
            fabric_send_file(clients_conf_file, '/etc/freeradius/clients.conf',
                             destination_host=destination)


def _start_radius(destination: str = world.f_cfg.mgmt_address):
    """
    Restart the RADIUS systemd service.

    :param destination: address of the server that hosts the RADIUS service
    """
    if world.server_system == 'redhat':
        cmd = 'sudo systemctl restart radiusd'
    else:
        cmd = 'sudo systemctl restart freeradius'
    fabric_sudo_command(cmd, destination_host=destination)
