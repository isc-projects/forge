"""Kea config backend testing interface-id."""

import pytest

from dhcp4_scen import get_address, get_rejected
from cb_model import setup_server_for_config_backend_cmds


pytestmark = [pytest.mark.v6,
              pytest.mark.kea_only,
              pytest.mark.controlchannel,
              pytest.mark.hook,
              pytest.mark.cb]


@pytest.mark.parametrize('backend', ['mysql', 'postgresql'])
def test_interface_id_in_subnet(backend):
    cfg = setup_server_for_config_backend_cmds(backend_type=backend)

    # relay_addr='7::1' always set to avoid matching thie relay agent
    # to defined subnet

    # create a subnet with specific relay agent interface-id
    subnet_cfg, _ = cfg.add_subnet(backend=backend, interface_id='vlan-a')

    # client 1 behind interface-id 'vlan-a' should get a lease
    get_address(mac_addr='00:00:00:00:00:01', interface_id='vlan-a', relay_addr='7::1')

    # client 2 behind interface-id 'vlan-b' should NOT get any lease
    get_rejected(mac_addr='00:00:00:00:00:02', interface_id='vlan-b', relay_addr='7::1')

    # change interface-id in subnet from 'vlan-a' to 'vlan-b'
    subnet_cfg.update(backend=backend, interface_id='vlan-b')

    # client 3 now should get a lease over interface-id 'vlan-b'
    get_address(mac_addr='00:00:00:00:00:03', interface_id='vlan-b', relay_addr='7::1')

    # but client 4 now behind interface-id 'vlan-a' should NOT get any lease
    get_rejected(mac_addr='00:00:00:00:00:04', interface_id='vlan-a', relay_addr='7::1')


@pytest.mark.parametrize('backend', ['mysql', 'postgresql'])
def test_interface_id_in_network(backend):
    cfg = setup_server_for_config_backend_cmds(backend_type=backend)

    # relay_addr='7::1' always set to avoid matching thie relay agent
    # to defined subnet

    # create a network with specific relay agent interface-id
    network_cfg, _ = cfg.add_network(backend=backend, interface_id='vlan-a')
    # bug #1058, FIXED
    subnet_cfg, _ = cfg.add_subnet(backend=backend, network=network_cfg, interface='')

    # client 1 behind interface-id 'vlan-a' should get a lease
    get_address(mac_addr='00:00:00:00:00:01', interface_id='vlan-a', relay_addr='7::1')

    # client 2 behind interface-id 'vlan-b' should NOT get any lease
    get_rejected(mac_addr='00:00:00:00:00:02', interface_id='vlan-b', relay_addr='7::1')

    # change interface-id in network from 'vlan-a' to 'vlan-b'
    network_cfg.update(backend=backend, interface_id='vlan-b')

    # client 3 now should get a lease over interface-id 'vlan-b'
    get_address(mac_addr='00:00:00:00:00:03', interface_id='vlan-b', relay_addr='7::1')

    # but client 4 now behind interface-id 'vlan-a' should NOT get any lease
    get_rejected(mac_addr='00:00:00:00:00:04', interface_id='vlan-a', relay_addr='7::1')

    # set interface-id in subnet from 'vlan-c' ie. override the one in network
    subnet_cfg.update(backend=backend, interface_id='vlan-c')

    # client 5 now should get a lease over interface-id 'vlan-c'
    get_address(mac_addr='00:00:00:00:00:05', interface_id='vlan-b', relay_addr='7::1')

    # but client 6 now behind interface-id 'vlan-b' (that is set in network)
    # should NOT get any lease
    get_rejected(mac_addr='00:00:00:00:00:06', interface_id='vlan-b', relay_addr='7::1')
