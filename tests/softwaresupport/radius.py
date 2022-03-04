import os

import srv_msg

from .multi_server_functions import fabric_sudo_command, fabric_send_file, TemporaryFile
from dhcp4_scen import DHCPv6_STATUS_CODES, get_address4, get_address6, send_discover_with_no_answer
from forge_cfg import world


def _init_radius():
    # User-Name prefix
    if world.proto in ['v4', 'v4_bootp']:
        p = '11'
    elif world.proto == 'v6':
        p = '00:03:00:01'

    # authorize config file
    authorize_content = f'''\
{p}:08:00:27:b0:c1:41    Cleartext-password := "08:00:27:b0:c1:41"
    \tFramed-IP-Address = "192.168.51.51",
    \tFramed-IPv6-Address = "2001:db8:51::51",
    \tFramed-Pool = "blues"

{p}:08:00:27:b0:c1:42    Cleartext-password := "08:00:27:b0:c1:42"
    \tFramed-IP-Address = "192.168.52.52",
    \tFramed-IPv6-Address = "2001:db8:52::52",
    \tFramed-Pool = "gold"

{p}:08:00:27:b0:c5:01    Cleartext-password := "08:00:27:b0:c5:01"
    \tFramed-Pool = "gold"

{p}:08:00:27:b0:c5:02    Cleartext-password := "08:00:27:b0:c5:02"
    \tFramed-Pool = "gold"

{p}:08:00:27:b0:c5:03    Cleartext-password := "08:00:27:b0:c5:03"
    \tFramed-Pool = "gold"

{p}:08:00:27:b0:c5:10    Cleartext-password := "08:00:27:b0:c5:10"
    \tFramed-IP-Address = "192.168.50.5",
    \tFramed-IPv6-Address = "2001:db8:50::5",
    \tFramed-Pool = "gold"

{p}:08:00:27:b0:c6:01    Cleartext-password := "08:00:27:b0:c6:01"
    \tFramed-Pool = "silver"

{p}:08:00:27:b0:c6:02    Cleartext-password := "08:00:27:b0:c6:02"
    \tFramed-Pool = "silver"

{p}:08:00:27:b0:c6:03    Cleartext-password := "08:00:27:b0:c6:03"
    \tFramed-Pool = "silver"

{p}:08:00:27:b0:c7:01    Cleartext-password := "08:00:27:b0:c7:01"
    \tFramed-Pool = "bronze"

{p}:08:00:27:b0:c7:02    Cleartext-password := "08:00:27:b0:c7:02"
    \tFramed-Pool = "bronze"

{p}:08:00:27:b0:c7:03    Cleartext-password := "08:00:27:b0:c7:03"
    \tFramed-Pool = "bronze"

{p}:08:00:27:b0:c8:01    Cleartext-password := "08:00:27:b0:c8:01"
    \tFramed-Pool = "platinum"
'''
    authorize_file = 'authorize.txt'
    with TemporaryFile(authorize_file, authorize_content):
        if world.server_system == 'redhat':
            # freeradius 3.x
            fabric_send_file(authorize_file, "/etc/raddb/mods-config/files/authorize")
        else:
            # freeradius 3.x
            fabric_send_file(authorize_file,
                             '/etc/freeradius/3.0/mods-config/files/authorize')
            # freeradius 2.x
            fabric_send_file(authorize_file, "/etc/freeradius/users")

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
    clients_conf_content = clients_conf_content.format(mgmt_address=world.f_cfg.mgmt_address)
    clients_conf_file = 'clients.conf'
    with TemporaryFile(clients_conf_file, clients_conf_content):
        if world.server_system == 'redhat':
            # freeradius 3.x
            fabric_send_file(clients_conf_file, "/etc/raddb/clients.conf")
        else:
            # freeradius 3.x
            fabric_send_file(clients_conf_file, "/etc/freeradius/3.0/clients.conf")
            # freeradius 2.x
            fabric_send_file(clients_conf_file, "/etc/freeradius/clients.conf")


def _start_radius():
    if world.server_system == 'redhat':
        cmd = 'sudo systemctl restart radiusd'
    else:
        cmd = 'sudo systemctl restart freeradius'
    fabric_sudo_command(cmd)


def init_and_start_radius():
    _init_radius()
    _start_radius()


def get_address(mac: str, expected_lease: str = None) -> str:
    '''
    Make a full exchange, check that the expected lease is received and,
    finally, return the received leases.

    :param mac: the client's MAC address
    :param expected_lease: a lease that's expected to be given by the DHCP server
    '''
    if world.proto in ['v4', 'v4_bootp']:
        client_id = '11:' + mac.replace(':', '')
        return get_address4(chaddr=mac,
                            client_id=client_id,
                            exp_yiaddr=expected_lease)
    if world.proto == 'v6':
        duid = '00:03:00:01:' + mac
        addresses = get_address6(duid=duid, exp_ia_na_iaaddr_addr=expected_lease)
        # Tests check only one address, so return the first.
        return addresses[0] if len(addresses) > 0 else None
    assert False, f'unknown proto {world.proto}'


def send_message_and_expect_no_more_leases(mac):
    '''
    Send a discover or a solicit and expect the exhausted leases case which is
    no answer for v4 or NoAddrsAvail status code for v6.

    :param mac: the client's MAC address
    '''
    if world.proto in ['v4', 'v4_bootp']:
        client_id = '11:' + mac.replace(':', '')
        send_discover_with_no_answer(chaddr=mac, client_id=client_id)
    elif world.proto == 'v6':
        duid = '00:03:00:01:' + mac
        srv_msg.SA(duid=duid, status_code=DHCPv6_STATUS_CODES['NoAddrsAvail'])
    else:
        assert False, f'unknown proto {world.proto}'


def get_test_case_variables():
    '''
    Populate variables used in RADIUS tests: various addresses, subnets and configurations.

    :return: tuple(addresses, subnets, configurations)
    '''

    if world.proto in ['v4', 'v4_bootp']:
        addresses = {
          '50-5': '192.168.50.5',
          '50-6': '192.168.50.6',
          '50-7': '192.168.50.7',
          '52-52': '192.168.52.52',
          '60-5': '192.168.60.5',
          '60-6': '192.168.60.6',
          '70-5': '192.168.70.5',
        }
        subnets = {
          '50': '192.168.50.0/24',
          '60': '192.168.60.0/24',
          '70': '192.168.70.0/24',
        }
    elif world.proto == 'v6':
        addresses = {
          '50-5': '2001:db8:50::5',
          '50-6': '2001:db8:50::6',
          '50-7': '2001:db8:50::7',
          '52-52': '2001:db8:52::52',
          '60-5': '2001:db8:60::5',
          '60-6': '2001:db8:60::6',
          '70-5': '2001:db8:70::5',
        }
        subnets = {
          '50': '2001:db8:50::/64',
          '60': '2001:db8:60::/64',
          '70': '2001:db8:70::/64',
        }

    v = world.proto[1]
    configs = {}

    configs['subnet'] = {
        f'subnet{v}': [
            {
                'interface': '$(SERVER_IFACE)',
                'pools': [
                    {
                        'client-class': 'gold',
                        'pool': f"{addresses['50-5']} - {addresses['50-5']}"
                    }
                ],
                'subnet': subnets['50']
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
                        'interface': '$(SERVER_IFACE)',
                        'pools': [
                            {
                                'client-class': 'gold',
                                'pool': f"{addresses['50-5']} - {addresses['50-5']}"
                            }
                        ],
                        'subnet': subnets['50']
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
                        'subnet': subnets['50'],
                        'interface': '$(SERVER_IFACE)',
                        'pools': [
                            {
                                'client-class': 'gold',
                                'pool': f"{addresses['50-5']} - {addresses['50-5']}"
                            }, {
                                'client-class': 'silver',
                                'pool': f"{addresses['50-6']} - {addresses['50-6']}"
                            }, {
                                'client-class': 'bronze',
                                'pool': f"{addresses['50-7']} - {addresses['50-7']}"
                            }
                        ]
                    },
                    {
                        'subnet': subnets['60'],
                        'interface': '$(SERVER_IFACE)',
                        'pools': [
                            {
                                'client-class': 'gold',
                                'pool': f"{addresses['60-5']} - {addresses['60-5']}"
                            }, {
                                'client-class': 'silver',
                                'pool': f"{addresses['60-6']} - {addresses['60-6']}"
                            }
                        ]
                    },
                    {
                        'subnet': subnets['70'],
                        'client-class': 'platinum',
                        'interface': '$(SERVER_IFACE)',
                        'pools': [
                            {
                                'pool': f"{addresses['70-5']} - {addresses['70-5']}"
                            }
                        ]
                    }
                ]
            }
        ]
    }

    return addresses, subnets, configs


def check_leases(config_type : str, has_reservation : str, addresses : dict[str], subnets : dict[str]):
    '''
    Exchange messages and check that the proper leases were returned according
    to Kea's configuration.

    :param config_type: different configurations used in testing
        * 'subnet': a classified pool with a single address configured inside a traditional subnet
        * 'network': a classified pool with a single address configured inside a shared network
        * 'multiple-subnets': multiple classified pools in multiple subnets inside a shared network
    :param has_reservation: whether the first client coming in with a request has its lease or pool reserved in RADIUS
        * 'client-has-reservation-in-radius': yes
        * 'client-has-no-reservation-in-radius': no
    :param addresses: dictionary of addresses used in testing indexed by recognizable patterns
    :param subnets: dictionary of subnets used in testing indexed by recognizable patterns
    '''

    if has_reservation == 'client-has-reservation-in-radius':
        # Get a lease that is explicitly configured in RADIUS as
        # Framed-IP-Address that is part of a configured pool in Kea.
        get_address(mac='08:00:27:b0:c5:10',
                    expected_lease=addresses['50-5'])

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
        get_address(mac='08:00:27:b0:c1:42',
                    expected_lease=addresses['52-52'])

        # A client with a gold Framed-Pool should get the lease because the
        # pool has a free lease.
        get_address(mac='08:00:27:b0:c5:01',
                    expected_lease=addresses['50-5'])

    # 'multiple-subnets' is more complex so treat it first.
    if config_type == 'multiple-subnets':
        gold_ips = {addresses['60-5']}  # Skip '50-5' because it was leased previously.
        silver_ips = {addresses['50-6'], addresses['60-6']}

        # Get the lease that is configured explicitly in RADIUS with
        # Framed-IP-Address.
        get_address(mac='08:00:27:b0:c1:42',
                    expected_lease=addresses['52-52'])

        # ### Take all addresses from gold pools. ###
        # Skip '50-5' because it was leased previously.

        # Lease the second and last gold address.
        yiaddr = get_address(mac='08:00:27:b0:c5:02')
        assert yiaddr in gold_ips
        gold_ips.remove(yiaddr)

        # No more leases.
        send_message_and_expect_no_more_leases(mac='08:00:27:b0:c5:03')

        # ### Take all addresses from silver pools. ###
        # Lease the first silver address.
        yiaddr = get_address(mac='08:00:27:b0:c6:01')
        assert yiaddr in silver_ips
        silver_ips.remove(yiaddr)

        # Lease the second and last silver address.
        yiaddr = get_address(mac='08:00:27:b0:c6:02')
        assert yiaddr in silver_ips
        silver_ips.remove(yiaddr)

        # No more leases.
        send_message_and_expect_no_more_leases(mac='08:00:27:b0:c6:03')

        # ### Take all addresses from bronze pools. ###
        # Lease the first and only bronze address.
        get_address(mac='08:00:27:b0:c7:01',
                    expected_lease=addresses['50-7'])

        # No more leases.
        send_message_and_expect_no_more_leases(mac='08:00:27:b0:c7:02')

        # Platinum client gets platinum lease.
        get_address(mac='08:00:27:b0:c8:01',
                    expected_lease=addresses['70-5'])
