#!/usr/bin/env python3
# Copyright (C) 2024 Internet Systems Consortium, Inc. ("ISC")
#
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

# This module will load incus.json file and use data to modufy init_all.py file
import json
import sys
def print_json(data):
    print(json.dumps(data, indent=4))

def load_json():
    with open('incus.json') as json_file:
        data = json.load(json_file)
    return data

def save_to_init_all(key, value):
    # print(f'ADD TO init_all.py: {key}="{value}"')
    # append key=value to init_all.py
    with open('init_all.py', 'a') as file:
        file.write(f'\n{key} = "{value}"')

def get_addresses(addresses_lst):
    ipv4_addr = None
    ipv6_global = None
    ipv6_link_local = None
    for addr in addresses_lst:
        if addr['family'] == 'inet':
            ipv4_addr = addr['address']
        if addr['family'] == 'inet6' and addr['scope'] == 'global':
            ipv6_global = addr['address']
        if addr['family'] == 'inet6'  and addr['scope'] == 'link':
            ipv6_link_local = addr['address']
    # check if all are not None
    if ipv4_addr is None or ipv6_global is None or ipv6_link_local is None:
        print("ERROR: Some addresses are None")
        sys.exit(1)
    return ipv4_addr, ipv6_global, ipv6_link_local



if __name__ == '__main__':
    data = load_json()
    # this is temporary solution, we need to redesign address management if we want to have a proper hub-and-spoke tests.
    for device in data:
        if device['name'] == 'kea-forge':
            for key, value in device['state']["network"].items():
                if key in ['lo', 'eth0']:
                    continue
                ipv4, ipv6_global, ipv6_link_local = get_addresses(value['addresses'])
                if key == 'eth1':
                    save_to_init_all("CLIENT_IPV6_ADDR_GLOBAL", ipv6_global)
                    save_to_init_all("CLNT4_ADDR", ipv4)
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
                else:
                    if device['name'] == 'kea-1' :
                        save_to_init_all("SRV4_ADDR", ipv4)
                        save_to_init_all("DNS4_ADDR", ipv4)
                        save_to_init_all("SRV_IPV6_ADDR_GLOBAL", ipv6_global)
                        save_to_init_all("SRV_IPV6_ADDR_LINK_LOCAL", ipv6_link_local)
                    # this can be used in the future with different names
                    else:
                        save_to_init_all(f"SRV4_ADDR_{device['name'][-1]}", ipv4)
                        save_to_init_all(f"SRV_IPV6_ADDR_GLOBAL_{device['name'][-1]}", ipv6_global)
                        save_to_init_all(f"SRV_IPV6_ADDR_LINK_LOCAL_{device['name'][-1]}", ipv6_link_local)
