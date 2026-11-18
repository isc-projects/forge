#!/usr/bin/env python3

# Copyright (C) 2024-2026 Internet Systems Consortium, Inc. ("ISC")
#
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

"""This module will load incus.json file and use data to modify the init_all.py file."""

import json
import sys


def print_json(data):
    """Print JSON.

    :param data: JSON representation
    :type data: dict
    """
    print(json.dumps(data, indent=4))


def load_json():
    """Load JSON from file into dict.

    :return: dict
    :rtype: dict
    """
    with open('incus.json', encoding='utf-8') as json_file:
        data = json.load(json_file)
    return data


def save_to_init_all(key, value):
    """Append key=value to init_all.py.

    :param key: key
    :type key: str
    :param value: value
    :type value: str
    """
    with open('init_all.py', 'a', encoding='utf-8') as file:
        file.write(f'\n{key} = "{value}"')


def _is_ula_ipv6(address):
    """Return True for unique local (ULA) addresses (fc00::/7)."""
    first_hextet = int(address.split(':')[0], 16)
    return (first_hextet & 0xfe00) == 0xfc00


def _pick_ipv6_global(addresses_lst):
    """Pick the configured static global IPv6 from multiple global addresses.

    Incus may report several global-scope IPv6 addresses on an interface: the
    static 2001:db8 test addresses, ULA from the bridge, and SLAAC temporaries.
    Prefer the test-network prefix, then the first non-ULA global address.
    """
    global_addresses = [
        addr['address']
        for addr in addresses_lst
        if addr['family'] == 'inet6' and addr['scope'] == 'global'
    ]
    if not global_addresses:
        return None

    for address in global_addresses:
        if address.lower().startswith('2001:db8:'):
            return address

    for address in global_addresses:
        if not _is_ula_ipv6(address):
            return address

    return global_addresses[0]


def get_addresses(addresses_lst):
    """Get relevant addresses from the addresses section of a network from incus.json.

    :param addresses_lst: addresses from a network from incus.json
    :type addresses_lst: dict
    :return: v4, v6 global, v6 link local
    :rtype: tuple[str, str, str]
    """
    ipv4_addr = None
    ipv6_global = None
    ipv6_link_local = None
    for addr in addresses_lst:
        if addr['family'] == 'inet':
            ipv4_addr = addr['address']
        if addr['family'] == 'inet6' and addr['scope'] == 'link':
            ipv6_link_local = addr['address']
    ipv6_global = _pick_ipv6_global(addresses_lst)
    # check if all are not None
    if ipv4_addr is None or ipv6_global is None or ipv6_link_local is None:
        print(f'ERROR: Some addresses are None: {ipv4_addr=}, {ipv6_global=}, {ipv6_link_local=}')
        sys.exit(1)
    return ipv4_addr, ipv6_global, ipv6_link_local


def main():
    """Entry point."""
    data = load_json()
    # this is temporary solution, we need to redesign address management if we want to have proper hub-and-spoke tests.
    for device in data:
        if device['name'] == 'kea-forge':
            for key, value in device['state']["network"].items():
                if key in ['lo', 'eth0']:
                    continue
                ipv4, ipv6_global, ipv6_link_local = get_addresses(value['addresses'])
                if key == 'eth1':
                    save_to_init_all("CLIENT_IPV6_ADDR_GLOBAL", ipv6_global)
                    save_to_init_all("CLNT4_ADDR", ipv4)
                    save_to_init_all("GIADDR4", ipv4)
                    save_to_init_all("CIADDR", ipv4)
                else:
                    save_to_init_all(f"CLNT4_ADDR_{key[-1]}", ipv4)
                continue
        else:
            for key, value in device['state']["network"].items():
                # so far we ignore eth2
                if key in ['lo', 'eth2']:
                    continue
                ipv4, ipv6_global, ipv6_link_local = get_addresses(value['addresses'])
                if key == 'eth0':
                    if device['name'] == 'kea-1':
                        save_to_init_all("MGMT_ADDRESS", ipv4)
                    else:
                        save_to_init_all(f"MGMT_ADDRESS_{device['name'][-1]}", ipv4)
                    continue
                if device['name'] == 'kea-1':
                    save_to_init_all("SRV4_ADDR", ipv4)
                    save_to_init_all("DNS4_ADDR", ipv4)
                    save_to_init_all("DNS6_ADDR", ipv6_global)
                    save_to_init_all("SRV_IPV6_ADDR_GLOBAL", ipv6_global)
                    save_to_init_all("SRV_IPV6_ADDR_LINK_LOCAL", ipv6_link_local)
                # this can be used in the future with different names
                else:
                    save_to_init_all(f"SRV4_ADDR_{device['name'][-1]}", ipv4)
                    save_to_init_all(f"SRV_IPV6_ADDR_GLOBAL_{device['name'][-1]}", ipv6_global)
                    save_to_init_all(f"SRV_IPV6_ADDR_LINK_LOCAL_{device['name'][-1]}", ipv6_link_local)


if __name__ == '__main__':
    main()
