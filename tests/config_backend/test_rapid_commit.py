"""Kea config backend testing rapid commit."""

import pytest

from src.protosupport.dhcp4_scen import get_address
from src.softwaresupport.cb_model import setup_server_for_config_backend_cmds


pytestmark = [pytest.mark.v6,
              pytest.mark.controlchannel,
              pytest.mark.hook,
              pytest.mark.cb]


@pytest.mark.parametrize('backend', ['mysql', 'postgresql'])
def test_rapid_commit_in_subnet(backend):
    cfg = setup_server_for_config_backend_cmds(backend_type=backend)

    # create a subnet and check getting address regular way
    subnet_cfg, _ = cfg.add_subnet(backend=backend)
    get_address(mac_addr='00:00:00:00:00:01', exp_addr='2001:db8:1::1')

    # disable rapid commit on subnet level and get address regular way
    subnet_cfg.update(backend=backend, rapid_commit=True)
    get_address(mac_addr='00:00:00:00:00:02', rapid_commit=True, exp_addr='2001:db8:1::2')

    # enable rapid commit on subnet level and get get address using rapid method
    subnet_cfg.update(backend=backend, rapid_commit=False)
    get_address(mac_addr='00:00:00:00:00:03', exp_addr='2001:db8:1::3')


@pytest.mark.parametrize('backend', ['mysql', 'postgresql'])
def test_rapid_commit_in_network(backend):
    cfg = setup_server_for_config_backend_cmds(backend_type=backend)

    # create a subnet with rapid commit enabled
    network_cfg, _ = cfg.add_network(backend=backend)
    subnet_cfg, _ = cfg.add_subnet(backend=backend, network=network_cfg)
    get_address(mac_addr='00:00:00:00:00:01', exp_addr='2001:db8:1::1')

    # disable rapid commit
    network_cfg.update(backend=backend, rapid_commit=True)
    get_address(mac_addr='00:00:00:00:00:02', rapid_commit=True, exp_addr='2001:db8:1::2')

    # get address using regular method
    subnet_cfg.update(backend=backend, rapid_commit=False)
    get_address(mac_addr='00:00:00:00:00:03', exp_addr='2001:db8:1::3')

    # get address using regular method
    subnet_cfg.update(backend=backend, rapid_commit=True)
    get_address(mac_addr='00:00:00:00:00:04', rapid_commit=True, exp_addr='2001:db8:1::4')
