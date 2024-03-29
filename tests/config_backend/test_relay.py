# Copyright (C) 2022 Internet Systems Consortium, Inc. ("ISC")
#
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

"""Kea config backend testing relay."""

import pytest

from src.protosupport.dhcp4_scen import get_address, get_rejected
from src.softwaresupport.cb_model import setup_server_for_config_backend_cmds


pytestmark = [pytest.mark.v4,
              pytest.mark.v6,
              pytest.mark.controlchannel,
              pytest.mark.hook,
              pytest.mark.cb]


@pytest.mark.parametrize('backend', ['mysql', 'postgresql'])
def test_relay_in_subnet(dhcp_version, backend):
    relay_addr_1 = "10.0.0.1" if dhcp_version == 'v4' else '10:0:0::1'
    relay_addr_2 = "10.0.0.2" if dhcp_version == 'v4' else '10:0:0::2'
    exp_addr_1 = '192.168.50.1' if dhcp_version == 'v4' else '2001:db8:1::1'
    exp_addr_2 = '192.168.50.2' if dhcp_version == 'v4' else '2001:db8:1::2'
    exp_addr_3 = '192.168.50.3' if dhcp_version == 'v4' else '2001:db8:1::3'

    cfg = setup_server_for_config_backend_cmds(backend_type=backend)

    # create a subnet with specific IP address for relay agent
    subnet_cfg, _ = cfg.add_subnet(backend=backend, relay={"ip-addresses": [relay_addr_1]})

    # client 1 behind relay agent 1 should get a lease
    get_address(mac_addr='00:00:00:00:00:01', relay_addr=relay_addr_1, exp_addr=exp_addr_1)

    # client 2 behing unknown relay agent 2 should NOT get any lease
    get_rejected(mac_addr='00:00:00:00:00:02', relay_addr=relay_addr_2)

    # add another relay agent 2
    subnet_cfg.update(backend=backend, relay={"ip-addresses": [relay_addr_1, relay_addr_2]})

    # client 2 now should get a lease
    get_address(mac_addr='00:00:00:00:00:02', relay_addr=relay_addr_2, exp_addr=exp_addr_2)

    # another client 3 behind relay agent 1 still should be able to get a lease
    get_address(mac_addr='00:00:00:00:00:03', relay_addr=relay_addr_1, exp_addr=exp_addr_3)


@pytest.mark.parametrize('backend', ['mysql', 'postgresql'])
def test_relay_in_network(dhcp_version, backend):
    relay_addr_1 = "10.0.0.1" if dhcp_version == 'v4' else '10:0:0::1'
    relay_addr_2 = "10.0.0.2" if dhcp_version == 'v4' else '10:0:0::2'
    relay_addr_3 = "10.0.0.3" if dhcp_version == 'v4' else '10:0:0::3'
    exp_addr_1 = '192.168.50.1' if dhcp_version == 'v4' else '2001:db8:1::1'
    exp_addr_2 = '192.168.50.2' if dhcp_version == 'v4' else '2001:db8:1::2'
    exp_addr_3 = '192.168.50.3' if dhcp_version == 'v4' else '2001:db8:1::3'
    exp_addr_4 = '192.168.50.4' if dhcp_version == 'v4' else '2001:db8:1::4'

    cfg = setup_server_for_config_backend_cmds(backend_type=backend)

    # create a network with specific IP address for relay agent
    network_cfg, _ = cfg.add_network(backend=backend, relay={"ip-addresses": [relay_addr_1]})
    subnet_cfg, _ = cfg.add_subnet(backend=backend, network=network_cfg)

    # client 1 behind relay agent 1 should get a lease
    get_address(mac_addr='00:00:00:00:00:01', relay_addr=relay_addr_1, exp_addr=exp_addr_1)

    # client 2 behing unknown relay agent 2 should NOT get any lease
    get_rejected(mac_addr='00:00:00:00:00:02', relay_addr=relay_addr_2)

    # add another relay agent 2
    network_cfg.update(backend=backend, relay={"ip-addresses": [relay_addr_1, relay_addr_2]})

    # client 2 now should get a lease
    get_address(mac_addr='00:00:00:00:00:02', relay_addr=relay_addr_2, exp_addr=exp_addr_2)

    # another client 3 behind relay agent 1 still should be able to get a lease
    get_address(mac_addr='00:00:00:00:00:03', relay_addr=relay_addr_1, exp_addr=exp_addr_3)

    # and now override relay on subnet level to relay agent 3
    subnet_cfg.update(backend=backend, relay={"ip-addresses": [relay_addr_3]})

    # client 4 now should get a lease
    get_address(mac_addr='00:00:00:00:00:04', relay_addr=relay_addr_3, exp_addr=exp_addr_4)

    # another client 5 behind relay agent 1 now should NOT be able to get any lease
    get_rejected(mac_addr='00:00:00:00:00:03', relay_addr=relay_addr_1)
