import os

import srv_msg

from .multi_server_functions import fabric_sudo_command, fabric_send_file, TemporaryFile
from dhcp4_scen import DHCPv6_STATUS_CODES, get_address4, get_address6
from forge_cfg import world


def _init_radius():
    # User-Name prefix
    if world.proto == 'v4':
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
    mac: the client's MAC address
    expected_lease: a lease that's expected to be given by the DHCP server
    '''
    if world.proto == 'v4':
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
    mac: the client's MAC address
    '''
    if world.proto == 'v4':
        client_id = '11:' + mac.replace(':', '')
        send_discover_with_no_answer(chaddr=mac, client_id=client_id)
    elif world.proto == 'v6':
        duid = '00:03:00:01:' + mac
        srv_msg.SA(duid=duid, status_code=DHCPv6_STATUS_CODES['NoAddrsAvail'])
    else:
        assert False, f'unknown proto {world.proto}'
