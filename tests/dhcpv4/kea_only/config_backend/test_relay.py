"""Kea config backend testing relay."""

import pytest

from dhcp4_scen import get_address, get_rejected
from cb_model import setup_server_for_config_backend_cmds


pytestmark = [pytest.mark.v4,
              pytest.mark.v6,
              pytest.mark.kea_only,
              pytest.mark.controlchannel,
              pytest.mark.hook,
              pytest.mark.config_backend]


def test_relay_in_subnet(dhcp_version):
    relay_addr_1 = "10.0.0.1" if dhcp_version == 'v4' else '10:0:0::1'
    relay_addr_2 = "10.0.0.2" if dhcp_version == 'v4' else '10:0:0::2'
    exp_addr_1 = '192.168.50.1' if dhcp_version == 'v4' else '2001:db8:1::1'
    exp_addr_2 = '192.168.50.2' if dhcp_version == 'v4' else '2001:db8:1::2'
    exp_addr_3 = '192.168.50.3' if dhcp_version == 'v4' else '2001:db8:1::3'

    cfg = setup_server_for_config_backend_cmds()

    # create a subnet with specific IP address for relay agent
    subnet_cfg, _ = cfg.add_subnet(relay={"ip-addresses": [relay_addr_1]})

    # client 1 behind relay agent 1 should get a lease
    get_address(mac_addr='00:00:00:00:00:01', relay_addr=relay_addr_1, exp_addr=exp_addr_1)

    # client 2 behing unknown relay agent 2 should NOT get any lease
    get_rejected(mac_addr='00:00:00:00:00:02', relay_addr=relay_addr_2)

    # add another relay agent 2
    subnet_cfg.update(relay={"ip-addresses": [relay_addr_1, relay_addr_2]})

    # client 2 now should get a lease
    get_address(mac_addr='00:00:00:00:00:02', relay_addr=relay_addr_2, exp_addr=exp_addr_2)

    # another client 3 behind relay agent 1 still should be able to get a lease
    get_address(mac_addr='00:00:00:00:00:03', relay_addr=relay_addr_1, exp_addr=exp_addr_3)


def test_relay_in_network(dhcp_version):
    relay_addr_1 = "10.0.0.1" if dhcp_version == 'v4' else '10:0:0::1'
    relay_addr_2 = "10.0.0.2" if dhcp_version == 'v4' else '10:0:0::2'
    relay_addr_3 = "10.0.0.3" if dhcp_version == 'v4' else '10:0:0::3'
    exp_addr_1 = '192.168.50.1' if dhcp_version == 'v4' else '2001:db8:1::1'
    exp_addr_2 = '192.168.50.2' if dhcp_version == 'v4' else '2001:db8:1::2'
    exp_addr_3 = '192.168.50.3' if dhcp_version == 'v4' else '2001:db8:1::3'
    exp_addr_4 = '192.168.50.4' if dhcp_version == 'v4' else '2001:db8:1::4'

    cfg = setup_server_for_config_backend_cmds()

    # create a network with specific IP address for relay agent
    network_cfg, _ = cfg.add_network(relay={"ip-addresses": [relay_addr_1]})
    subnet_cfg, _ = cfg.add_subnet(network=network_cfg)

    # client 1 behind relay agent 1 should get a lease
    get_address(mac_addr='00:00:00:00:00:01', relay_addr=relay_addr_1, exp_addr=exp_addr_1)

    # client 2 behing unknown relay agent 2 should NOT get any lease
    get_rejected(mac_addr='00:00:00:00:00:02', relay_addr=relay_addr_2)

    # add another relay agent 2
    network_cfg.update(relay={"ip-addresses": [relay_addr_1, relay_addr_2]})

    # client 2 now should get a lease
    get_address(mac_addr='00:00:00:00:00:02', relay_addr=relay_addr_2, exp_addr=exp_addr_2)

    # another client 3 behind relay agent 1 still should be able to get a lease
    get_address(mac_addr='00:00:00:00:00:03', relay_addr=relay_addr_1, exp_addr=exp_addr_3)

    # and now override relay on subnet level to relay agent 3
    subnet_cfg.update(relay={"ip-addresses": [relay_addr_3]})

    # client 4 now should get a lease
    get_address(mac_addr='00:00:00:00:00:04', relay_addr=relay_addr_3, exp_addr=exp_addr_4)

    # another client 5 behind relay agent 1 now should NOT be able to get any lease
    get_rejected(mac_addr='00:00:00:00:00:03', relay_addr=relay_addr_1)
