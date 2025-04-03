# Copyright (C) 2013-2025 Internet Systems Consortium, Inc. ("ISC")
#
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

# Author: Wlodzimierz Wencel


from src.forge_cfg import world


def add_ddns_server(address, port):
    world.ddns_enable = True  # flag for ddns
    world.ddns_add = {}  # part of the config which is added to dhcp config section

    if address == "default":
        address = "127.0.0.1"
    if port == "default":
        port = 53001

    if world.f_cfg.install_method == 'make' or world.server_system == 'alpine':
        logging_file = 'kea-dhcp-ddns.log'
        logging_file_path = world.f_cfg.log_join(logging_file)
    else:
        logging_file_path = 'stdout'

    world.ddns_cfg = {"ip-address": address,
                      "port": int(port),  # this value is passed as string
                      "dns-server-timeout": 2000,
                      "reverse-ddns": {'ddns-domains': []},
                      "forward-ddns": {'ddns-domains': []},
                      "hooks-libraries": [],
                      "tsig-keys": [],
                      "ncr-format": "JSON",  # default value
                      "ncr-protocol": "UDP",
                      "loggers": [
                          {"debuglevel": 99, "name": "kea-dhcp-ddns",
                           "output-options": [{
                               "output": logging_file_path}],
                           "severity": "DEBUG"}]
                      }  # default value

    add_ddns_server_connectivity_options("server-ip", address)
    add_ddns_server_connectivity_options("server-port", int(port))
    add_ddns_server_connectivity_options("enable-updates", False)


def change_to_boolean(value):
    if not isinstance(value, str):
        return value
    if value.lower() == "true":
        return True
    if value.lower() == "false":
        return False
    return value


# Kea now has two types of configuration parameters, Behavioral Parameters and Connectivity Parameters.
# Connectivity Parameters are kept in {"DhcpX":{"dhcp-ddns": {} }}
# Behavioral Parameters are kept globally {"DhcpX": {}} or per subnet
def add_ddns_server_behavioral_options(option, value=None, subnet: int = None, sharednetwork: str = None):
    """add_ddns_server_behavioral_options Put behavioral options for DDNS server into configuration
    If subnet is not none - put it in subnet section
    If sharednetwork is not none - put it in sharednetwork section
    If both are none - put it in global section

    :param option: option name
    :type option: str
    :param subnet: subnet id to which ddns parameter should be applied, defaults to None
    :type subnet: int, optional
    :param sharednetwork: network name to which parameter should be applied, defaults to None
    :type sharednetwork: str, optional
    :param value: value of an option, can be string, int, dict, defaults to None
    :type value: any, optional
    """
    dhcp_version = int(world.proto[1])
    if not subnet and not sharednetwork:
        if isinstance(option, dict) and value is None:
            world.dhcp_cfg.update(option)
        else:
            world.dhcp_cfg[option] = change_to_boolean(value)
    elif subnet:
        for sub in world.dhcp_cfg[f"subnet{dhcp_version}"]:
            if sub["id"] == sub:
                if isinstance(option, dict) and value is None:
                    sub.update(option)
                else:
                    sub[option] = change_to_boolean(value)
    elif sharednetwork:
        for network in world.dhcp_cfg["shared-networks"]:
            if network["name"] == network:
                if isinstance(option, dict) and value is None:
                    network.update(option)
                else:
                    network[option] = change_to_boolean(value)


def add_ddns_server_connectivity_options(option, value=None):
    if "dhcp-ddns" not in world.dhcp_cfg:
        world.dhcp_cfg["dhcp-ddns"] = {}
    if isinstance(option, dict) and value is None:
        world.dhcp_cfg["dhcp-ddns"].update(option)

    world.dhcp_cfg["dhcp-ddns"][option] = change_to_boolean(value)


def add_forward_ddns(name, key_name, ip_address, port, hostname=""):
    tmp_record = {
        "name": name,
        "key-name": key_name,
        "dns-servers": [{
            "hostname": hostname,
            "ip-address": ip_address,
            "port": port
        }]
    }

    if key_name == "EMPTY_KEY":
        del tmp_record["key-name"]
    world.ddns_cfg["forward-ddns"]["ddns-domains"].append(tmp_record)


def add_reverse_ddns(name, key_name, ip_address, port, hostname=""):
    tmp_record = {
        "name": name,
        "key-name": key_name,
        "dns-servers": [{
            "hostname": hostname,
            "ip-address": ip_address,
            "port": port
        }]
    }

    if key_name == "EMPTY_KEY":
        del tmp_record["key-name"]
    world.ddns_cfg["reverse-ddns"]["ddns-domains"].append(tmp_record)


def add_keys(secret, name, algorithm):
    world.ddns_cfg["tsig-keys"].append({
        "secret": secret,
        "name": name,
        "algorithm": algorithm,
        "digest-bits": 0  # default value
    })


def ddns_open_control_channel_socket(socket_name=None):
    if socket_name is not None:
        socket_path = world.f_cfg.run_join(socket_name)
    else:
        socket_path = world.f_cfg.run_join('ddns_control_socket')

    world.ddns_cfg["control-sockets"] = [{"socket-type": "unix", "socket-name": socket_path}]


def ddns_add_gss_tsig(addr, dns_system,
                      client_principal="DHCP/admin.example.com@EXAMPLE.COM",
                      client_tab="FILE:/tmp/dhcp.keytab",
                      fallback=False,
                      retry_interval=None,
                      rekey_interval=None,
                      server_id="server1",
                      server_principal="DNS/server.example.com@EXAMPLE.COM",
                      tkey_lifetime=3600):
    gss_tsig_cfg = {
        "library": "libddns_gss_tsig.so",
        "parameters": {
            "server-principal": server_principal,
            "tkey-protocol": "TCP",
            "rekey-interval": rekey_interval if rekey_interval is not None else tkey_lifetime-int(tkey_lifetime*0.1),
            "retry-interval": retry_interval if retry_interval is not None else tkey_lifetime-int(tkey_lifetime*0.2),
            "tkey-lifetime": tkey_lifetime,
            "fallback": fallback,
            "servers": [{
                "id": server_id,
                "ip-address": addr,
            }]
        }
    }
    if dns_system == 'linux':
        gss_tsig_cfg["parameters"].update({
            "client-principal": client_principal,
            "client-keytab": client_tab})

    world.ddns_cfg["hooks-libraries"] = [gss_tsig_cfg]
