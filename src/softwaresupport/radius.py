# Copyright (C) 2013-2026 Internet Systems Consortium, Inc. ("ISC")
#
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

# pylint: disable=global-statement
# pylint: disable=global-variable-not-assigned
# pylint: disable=invalid-name  # for AUTHORIZE_CONTENT
# pylint: disable=line-too-long

"""Functions that help with testing RADIUS functionality in Kea."""

import re

from src import srv_msg
from src.misc import merge_containers
from src.protosupport.dhcp4_scen import DHCPv6_STATUS_CODES, get_address4, get_address6, send_discover_with_no_answer
from src.protosupport.multi_protocol_functions import sort_dict_with_scalars_first
from src.forge_cfg import world
from .multi_server_functions import fabric_is_dir, fabric_is_file, fabric_sudo_command, get_content, send_content

AUTHORIZE_CONTENT = ''


def add_leading_subnet(subnet: str = None,
                       pool: str = None):
    """Add to the first position: a subnet or a shared network with a single subnet, in both cases with a single pool.

    The subnet ID is the third octet from the v4 address.

    :param subnet: the subnet value
    :type subnet: str
    :param pool: the pool value
    :type pool: str
    """
    # Defaults
    if subnet is None:
        if world.proto == 'v4':
            subnet = '192.168.99.0/24'
        elif world.proto == 'v6':
            subnet = '2001:db8:99::/64'
    if pool is None:
        if world.proto == 'v4':
            pool = '192.168.99.0 - 192.168.99.255'
        elif world.proto == 'v6':
            pool = '2001:db8:99:: - 2001:db8:99::ffff'

    v = world.proto[1]
    if f'subnet{v}' in world.dhcp_cfg:
        delimiter = '.' if world.proto == 'v4' else ':'
        world.dhcp_cfg[f'subnet{v}'].insert(0, {
            'id': int(subnet.split(delimiter)[2]),
            'interface': world.f_cfg.server_iface,
            'pools': [
                {
                    'pool': pool
                }
            ],
            'subnet': subnet
        })
    if 'shared-networks' in world.dhcp_cfg:
        delimiter = '.' if world.proto == 'v4' else ':'
        world.dhcp_cfg['shared-networks'].insert(0, {
            'name': subnet,
            f'subnet{v}': [
                {
                    'id': int(subnet.split(delimiter)[2]),
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


def add_reservation(mac: str, attributes=None):
    """Add RADIUS reservation.

    :param mac:
    :type mac: str
    :param attributes: (Default value = None)
    :type attributes:
    """
    if attributes is None:
        attributes = []

    # User-Name prefix
    # Arbitrary number prepended to the MAC
    prefix = '11'  # for v4
    if world.proto == 'v6':
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
    """add_usual_reservations."""
    add_reservation('08:00:27:b0:c1:41', [
        'Framed-IP-Address = "192.168.51.51"',
        'Framed-IPv6-Address = "2001:db8:51::51"',
        'Framed-Pool = "blues"',
        'Framed-IPv6-Pool = "blues"',
    ])

    add_reservation('08:00:27:b0:c1:50', [
        'Framed-IP-Address = "192.168.50.50"',
        'Framed-IPv6-Address = "2001:db8:50::50"',
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

    # Prefix only
    add_reservation('08:ff:ee:dd:cc:01', [
        'Delegated-IPv6-Prefix = "2001:db8:0:0:01::/96"',
    ])

    # Framed prefix and delegated prefix. Equal.
    add_reservation('08:ff:ee:dd:cc:02', [
        'Framed-IPv6-Prefix = "2001:db8:0:0:2::/96"',
        'Delegated-IPv6-Prefix = "2001:db8:0:0:2::/96"',
    ])

    # Framed prefix and delegated prefix. Different.
    add_reservation('08:ff:ee:dd:cc:03', [
        'Framed-IPv6-Prefix = "2001:db8:0:0:3:3::/96"',
        'Delegated-IPv6-Prefix = "2001:db8:0:0:3::/96"',
    ])

    # Address and prefix
    add_reservation('08:ff:ee:dd:cc:04', [
        'Framed-IP-Address = "192.192.0.4"',
        'Framed-IPv6-Address = "2001:db8:0:0:4:4::"',
        'Delegated-IPv6-Prefix = "2001:db8:0:0:4::/96"',
    ])

    # Address same as prefix
    add_reservation('08:ff:ee:dd:cc:05', [
        'Framed-IP-Address = "192.192.0.5"',
        'Framed-IPv6-Address = "2001:db8:0:0:5::"',
        'Delegated-IPv6-Prefix = "2001:db8:0:0:5::/96"',
    ])

    # Address same as prefix and /128
    add_reservation('08:ff:ee:dd:cc:065', [
        'Framed-IP-Address = "192.192.0.6"',
        'Framed-IPv6-Address = "2001:db8:0:0:6::"',
        'Delegated-IPv6-Prefix = "2001:db8:0:0:6::/96"',
    ])

    # Pool and prefix
    add_reservation('08:ff:ee:dd:cc:07', [
        'Framed-Pool = "silver"',
        'Framed-IPv6-Pool = "silver"',
        'Delegated-IPv6-Prefix = "2001:db8:0:0:7::/96"',
    ])

    # All attributes
    add_reservation('08:ff:ee:dd:cc:08', [
        'Framed-Pool = "silver"',
        'Framed-IPv6-Pool = "silver"',
        'Framed-IP-Address = "192.192.0.8"',
        'Framed-IPv6-Address = "2001:db8:0:0:8:8::"',
        'Framed-IPv6-Prefix = "2001:db8:0:0:8:8::/112"',
        'Delegated-IPv6-Prefix = "2001:db8:0:0:8::/96"',
    ])


def configurations(interface: str = world.f_cfg.server_iface):
    """Return configurations used in RADIUS tests.

    :param interface: the name of the client-facing interface on the server side
    :type interface: str
    :return: configurations
    :rtype:
    """
    v = world.proto[1]
    configs = {}

    configs['subnet'] = {
        f'subnet{v}': [
            {
                'interface': interface,
                'id': 1,
                'pools': [
                    {
                        'client-classes': ['gold'],
                        'pool': '192.168.50.5 - 192.168.50.5'
                        if world.proto == 'v4'
                        else '2001:db8:50::5 - 2001:db8:50::5',
                    }
                ],
                'subnet': '192.168.50.0/24' if world.proto == 'v4' else '2001:db8:50::/64',
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
                        'id': 2,
                        'pools': [
                            {
                                'client-classes': ['gold'],
                                'pool': '192.168.50.5 - 192.168.50.5'
                                if world.proto == 'v4'
                                else '2001:db8:50::5 - 2001:db8:50::5',
                            }
                        ],
                        'subnet': '192.168.50.0/24' if world.proto == 'v4' else '2001:db8:50::/64',
                    }
                ],
            }
        ],
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
                        'id': 3,
                        'pools': [
                            {
                                'client-classes': ['gold'],
                                'pool': '192.168.50.5 - 192.168.50.5'
                                if world.proto == 'v4'
                                else '2001:db8:50::5 - 2001:db8:50::5',
                            },
                            {
                                'client-classes': ['silver'],
                                'pool': '192.168.50.6 - 192.168.50.6'
                                if world.proto == 'v4'
                                else '2001:db8:50::6 - 2001:db8:50::6',
                            },
                            {
                                'client-classes': ['bronze'],
                                'pool': '192.168.50.7 - 192.168.50.7'
                                if world.proto == 'v4'
                                else '2001:db8:50::7 - 2001:db8:50::7',
                            },
                        ],
                        'subnet': '192.168.50.0/24' if world.proto == 'v4' else '2001:db8:50::/64',
                    },
                    {
                        'interface': interface,
                        'id': 4,
                        'pools': [
                            {
                                'client-classes': ['gold'],
                                'pool': '192.168.60.5 - 192.168.60.5'
                                if world.proto == 'v4'
                                else '2001:db8:60::5 - 2001:db8:60::5',
                            },
                            {
                                'client-classes': ['silver'],
                                'pool': '192.168.60.6 - 192.168.60.6'
                                if world.proto == 'v4'
                                else '2001:db8:60::6 - 2001:db8:60::6',
                            },
                        ],
                        'subnet': '192.168.60.0/24' if world.proto == 'v4' else '2001:db8:60::/64',
                    },
                    {
                        'client-classes': ['platinum'],
                        'interface': interface,
                        'id': 5,
                        'pools': [
                            {
                                'pool': '192.168.70.5 - 192.168.70.5'
                                if world.proto == 'v4'
                                else '2001:db8:70::5 - 2001:db8:70::5'
                            },
                            {
                                'pool': '192.168.70.20 - 192.168.70.30'
                                if world.proto == 'v4'
                                else '2001:db8:70::20 - 2001:db8:70::30'
                            },
                        ],
                        'subnet': '192.168.70.0/24' if world.proto == 'v4' else '2001:db8:70::/64',
                    },
                ],
            }
        ],
    }

    return configs


def get_address(mac: str, giaddr: str = None, expected_lease: str = None, server_id: str = world.f_cfg.srv4_addr):
    """Make a full exchange, check that the expected lease is received and, finally, return the received leases.

    :param mac: the client's MAC address
    :type mac: str
    :param giaddr: the v4 client's giaddr value (Default value = None)
    :type giaddr: str
    :param expected_lease: a lease that's expected to be given by the DHCP server
    :type expected_lease: str
    :param server_id: (Default value = world.f_cfg.srv4_addr)
    :type server_id: str
    :return: the leased v4 address or the first lease in the v6 case, in both cases with the client ID and MAC address
    :rtype:
    """
    if world.proto == 'v4':
        client_id = '11' + mac.replace(':', '')
        address = get_address4(
            chaddr=mac,
            client_id=client_id,
            giaddr=giaddr,
            exp_yiaddr=expected_lease,
            server_id=server_id,
        )
        return {
            'address': address,
            'client_id': client_id,
            'hwaddr': mac,
        }
    if world.proto == 'v6':
        duid = '00:03:00:01:' + mac
        addresses = get_address6(duid=duid, exp_ia_na_iaaddr_addr=expected_lease)
        # Tests check only one address, so return the first.
        return {
            'address': addresses[0] if len(addresses) > 0 else None,
            'duid': duid,
        }
    assert False, f'unknown proto {world.proto}'


def init_and_start_radius(destination: str = world.f_cfg.mgmt_address):
    """Configure and restart RADIUS on remote hosts.

    :param destination: address of the server that hosts the RADIUS service
    :type destination:
    """
    _init_radius(destination=destination)
    _start_radius(destination=destination)

    # Reset for next use.
    global AUTHORIZE_CONTENT
    AUTHORIZE_CONTENT = ''


def send_and_receive(config_type: str, radius_reservation_in_pool: str, ha_mode: str = None):
    """Exchange messages and check that the proper leases were returned according to Kea's configuration.

    :param config_type: different configurations used in testing
        * 'subnet': a classified pool with a single address configured inside a traditional subnet
        * 'network': a classified pool with a single address configured inside a shared network
        * 'multiple-subnets': multiple classified pools in multiple subnets inside a shared network
    :type config_type: str
    :param radius_reservation_in_pool: whether there is an existing pool in Kea that contains the
        lease reserved by RADIUS for the first client in this test
        * 'radius-reservation-in-pool': yes
        * 'radius-reservation-outside-pool': no
    :type radius_reservation_in_pool: str
    :param ha_mode: HA mode, not strictly-related to RADIUS. Default is None meaning no HA
        * 'hot-standby'
        * 'load-balancing'
        * 'passive-backup'
    :type ha_mode: str
    :return: list of dictionaries of leases containing address, client_id, mac
    :rtype:
    """
    leases = []

    if radius_reservation_in_pool == 'radius-reservation-in-pool':
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

    elif radius_reservation_in_pool == 'radius-reservation-outside-pool':
        # Get a lease that is explicitly configured in RADIUS as
        # Framed-IP-Address that is outside of any configured pool in Kea.
        leases.append(get_address(mac='08:00:27:b0:c1:50',
                                  expected_lease='192.168.50.50' if world.proto == 'v4' else '2001:db8:50::50'))

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

        # ---- Take all addresses from gold pools. ----
        # Skip 192.168.50.5 / 2001:db8:50::5 because it was leased previously.

        # Lease the second and last gold address.
        lease = get_address(mac='08:00:27:b0:c5:02')
        assert lease['address'] in gold_ips, lease['address'] + ' not in ' + str(gold_ips)
        gold_ips.remove(lease['address'])
        leases.append(lease)

        # No more leases.
        send_message_and_expect_no_more_leases(mac='08:00:27:b0:c5:03')

        # ---- Take all addresses from silver pools. ----
        # Lease the first silver address.
        if ha_mode is not None and ha_mode == 'load-balancing':
            lease = get_address(mac='08:00:27:b0:c6:01', server_id=world.f_cfg.srv4_addr_2)
        else:
            lease = get_address(mac='08:00:27:b0:c6:01')
        assert lease['address'] in silver_ips, lease['address'] + ' not in ' + str(silver_ips)
        silver_ips.remove(lease['address'])
        leases.append(lease)

        # Lease the second and last silver address.
        lease = get_address(mac='08:00:27:b0:c6:02')
        assert lease['address'] in silver_ips, lease['address'] + ' not in ' + str(silver_ips)
        silver_ips.remove(lease['address'])
        leases.append(lease)

        # No more leases.
        send_message_and_expect_no_more_leases(mac='08:00:27:b0:c6:03')

        # ---- Take all addresses from bronze pools. ----
        # Lease the first and only bronze address.
        expected_lease = ('192.168.50.7' if world.proto == 'v4' else '2001:db8:50::7')
        if ha_mode is not None and ha_mode == 'load-balancing':
            lease = get_address(mac='08:00:27:b0:c7:01', expected_lease=expected_lease,
                                server_id=world.f_cfg.srv4_addr_2)
        else:
            lease = get_address(mac='08:00:27:b0:c7:01', expected_lease=expected_lease)
        leases.append(lease)

        # No more leases.
        send_message_and_expect_no_more_leases(mac='08:00:27:b0:c7:02')

        # Platinum client gets platinum lease.
        leases.append(get_address(mac='08:00:27:b0:c8:01',
                                  expected_lease='192.168.70.5' if world.proto == 'v4' else '2001:db8:70::5'))

    # Remove None from leases because it doesn't play nice with srv_msg.check_leases().
    filter(lambda single_lease: single_lease is not None, leases)

    return leases


def send_message_and_expect_no_more_leases(mac: str, giaddr: str = None):
    """Send a discover or a solicit and expect the exhausted leases case which is no answer for v4 or NoAddrsAvail status code for v6.

    :param mac: the client's MAC address
    :type mac:
    :param giaddr: the v4 client's giaddr value
    :type giaddr:
    """
    if world.proto == 'v4':
        client_id = '11' + mac.replace(':', '')
        send_discover_with_no_answer(chaddr=mac, client_id=client_id, giaddr=giaddr)
    elif world.proto == 'v6':
        duid = '00:03:00:01:' + mac
        srv_msg.SA(duid=duid, address=None, delegated_prefix=None,
                   status_code_IA_NA=DHCPv6_STATUS_CODES['NoAddrsAvail'],
                   status_code_IA_PD=DHCPv6_STATUS_CODES['NoPrefixAvail'])
    else:
        assert False, f'unknown proto {world.proto}'


def _init_radius(destination: str = world.f_cfg.mgmt_address):
    """Create authorize file and clients.conf needed by RADIUS and send them to {destination}.

    :param destination: address where RADIUS is set up
    :type destination:
    """
    global AUTHORIZE_CONTENT

    if world.radius_dir is None:
        for d in [
            '/etc/raddb',
            '/etc/freeradius/3.0',
        ]:
            if fabric_is_dir(d, destination):
                world.radius_dir = d
                if fabric_is_file(f'{d}/radiusd.conf', destination):
                    world.radius_config = f'{d}/radiusd.conf'
                    break
        assert world.radius_dir is not None, f'RADIUS dir not found: {world.radius_dir}'

    # If config file was not found, let us create one.
    if world.radius_config is None:
        if fabric_is_file('/etc/raddb.default/radiusd.conf', destination):
            fabric_sudo_command('sudo cp /etc/raddb.default/radiusd.conf /etc/raddb/radiusd.conf', destination)
            fabric_sudo_command('sudo mkdir -p /etc/raddb/mods-config', destination)
            fabric_sudo_command('sudo mkdir -p /etc/raddb/mods-enabled', destination)
            fabric_sudo_command('sudo mkdir -p /etc/raddb/policy.d', destination)
            fabric_sudo_command('sudo mkdir -p /etc/raddb/sites-enabled', destination)
            fabric_sudo_command('sudo touch /etc/raddb/clients.conf', destination)
            fabric_sudo_command('sudo touch /etc/raddb/proxy.conf', destination)
            world.radius_config = '/etc/raddb/radiusd.conf'

    assert world.radius_config is not None, f'RADIUS config file not found: {world.radius_config}'

    world.radius_authorize_file = f'{world.radius_dir}/mods-config/files/authorize'
    assert fabric_is_file(world.radius_authorize_file, destination), f'RADIUS authorize file not found: {world.radius_authorize_file}'

    send_content(AUTHORIZE_CONTENT, world.radius_authorize_file, 'radius', destination)

    # clients.conf file
    clients_conf_content = """
client {mgmt_address} {{
    ipaddr = {mgmt_address}
    secret = testing123
    proto = *
    nas_type = other
    limit {{
        max_connections = 16
        lifetime = 0
        idle_timeout = 30
    }}
}}
"""
    clients_conf_content = clients_conf_content.strip()
    clients_conf_content = clients_conf_content.format(mgmt_address=destination)
    for file in [
        '/etc/raddb/clients.conf',  # freeradius 3.x usualy on RPM distros
        '/etc/freeradius/3.0/clients.conf',  # freeradius 3.x usually on deb distros
        '/etc/freeradius/clients.conf',  # freeradius 2.x
    ]:
        if fabric_is_file(file, destination):
            world.radius_clients_file = file
            send_content(clients_conf_content, world.radius_clients_file, 'radius', destination)
            break


def _parse_radius_config(host=world.f_cfg.mgmt_address, lines=None):
    """Read the RADIUS config from a file and parse it into a dict.

    :param host: the host where the RADIUS config file exists
    :type host: str
    :param lines: the list of lines that need to be processed further; only used to help with the recursive calls
    :type lines: list[str]
    :return: the RADIUS config
    :rtype: dict
    """
    if lines is None:
        content = get_content(world.radius_config, host)

        # Remove comments and empty lines.
        lines = [
            line
            for line in content.splitlines()
            if not re.search(r'^\s*#.*', line) and line.strip() != ''
        ]

    config = {}
    i = 0
    while i < len(lines):
        line = lines[i].strip()
        i += 1

        if not line:
            continue

        if '$INCLUDE' in line:
            config[line] = True

        if line.endswith('{'):
            name = line[:-1].strip()

            body_lines = []
            depth = 1
            while i < len(lines) and depth > 0:
                inner = lines[i]
                i += 1
                stripped = inner.strip()
                if stripped.endswith('{'):
                    depth += 1
                elif stripped == '}':
                    depth -= 1
                    if depth == 0:
                        break
                body_lines.append(inner)

            section = _parse_radius_config(host, body_lines)

            if name not in config:
                config[name] = {}
            if isinstance(config[name], dict) and isinstance(section, dict):
                config[name].update(section)
            else:
                config[name] = section
            continue

        # Ignore stray closing braces at top level
        if line == '}':
            continue

        # key = value
        if '=' in line:
            key, _, val = line.partition('=')
            key = key.strip()
            val = val.strip()
            config[key] = val

    for k in list(config.keys()):
        v = config[k]
        if isinstance(v, (dict, list)) and len(v) == 0:
            del config[k]

    return config


def _write_radius_config(config: str, host: str = world.f_cfg.mgmt_address, indent: int = 0):
    """Serialize the RADIUS config from a dict and write it in a file.

    :param config: the RADIUS config
    :type config: dict
    :param host: the host where the RADIUS config should be written
    :type host: str
    :param indent: level of indent; used to determine how many spaces to indent the current line,
        and if this is the first call or a recursive call
    :type indent: int
    :return: the list of lines that were processed so far; only used to help with the recursive calls
    :rtype: list[str]
    """
    pad = indent * ' '
    lines = []

    for key, value in config.items():
        if '$INCLUDE' in key:
            lines.append(f'{pad}{key}')
        elif isinstance(value, dict):
            lines.append(f'{pad}{key} {{')
            lines.extend(_write_radius_config(value, host, indent + 4))
            lines.append(f'{pad}}}')
        else:
            lines.append(f'{pad}{key} = {str(value)}')

    if indent > 0:
        return lines

    serialized_config = '\n'.join(lines) + '\n'
    send_content(serialized_config, world.radius_config, 'radius', host)
    return lines


def _tweak_radius_config(destination: str = world.f_cfg.mgmt_address):
    """Remove comments and empty lines, and enable auth logs.

    :param destination: (Default value = world.f_cfg.mgmt_address)
    :type destination: str
    """
    config = _parse_radius_config(destination)

    # Make sure logging is verbose.
    merge_containers(
        config,
        {
            'log': {
                'level': 'debug',
                'auth': 'yes',
                'auth_badpass': 'yes',
                'auth_goodpass': 'yes',
            }
        },
    )

    # Zero delay makes tests potentially faster.
    merge_containers(
        config,
        {
            'security': {
                'reject_delay': '0',
            }
        },
    )

    # Temporary disabling of security. Revert when TLS is implemented.
    merge_containers(
        config,
        {
            'security': {
                'limit_proxy_state': 'no',
                'require_message_authenticator': 'no',
            }
        },
    )

    # Leave scalars first. They are used in the dicts that follow.
    config = sort_dict_with_scalars_first(config)

    _write_radius_config(config, destination)


def _start_radius(destination: str = world.f_cfg.mgmt_address):
    """Restart the RADIUS systemd service.

    :param destination: address of the server that hosts the RADIUS service
    :type destination:
    """
    fabric_sudo_command(f'truncate -s 0 {world.radius_log}', destination_host=destination, ignore_errors=True)
    _tweak_radius_config(destination)
    if world.server_system in ['redhat', 'fedora']:
        cmd = 'sudo systemctl restart radiusd'
    elif world.server_system == 'alpine':
        fabric_sudo_command('killall radiusd', destination_host=destination, ignore_errors=True)
        cmd = '/usr/sbin/radiusd'
    else:
        cmd = 'sudo systemctl restart freeradius'
    fabric_sudo_command(cmd, destination_host=destination)

    if world.radius_log is None:
        for file in [
            '/var/log/radius/radius.log',
            '/var/log/freeradius/radius.log',
        ]:
            if fabric_is_file(file, destination):
                world.radius_log = file
                break

    assert world.radius_log is not None, f'RADIUS log file not found: {world.radius_log}'
