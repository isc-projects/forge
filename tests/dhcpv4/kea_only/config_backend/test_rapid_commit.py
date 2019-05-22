"""Kea config backend testing rapid commit."""

import pytest

from dhcp4_scen import get_address
from cb_model import setup_server_for_config_backend_cmds


pytestmark = [pytest.mark.v6,
              pytest.mark.kea_only,
              pytest.mark.controlchannel,
              pytest.mark.hook,
              pytest.mark.config_backend]


def test_rapid_commit_in_subnet():
    cfg = setup_server_for_config_backend_cmds()

    # create a subnet and check getting address regular way
    subnet_cfg, _ = cfg.add_subnet()
    get_address(mac_addr='00:00:00:00:00:01', exp_addr='2001:db8:1::1')

    # disable rapid commit on subnet level and get address regular way
    subnet_cfg.update(rapid_commit=True)
    get_address(mac_addr='00:00:00:00:00:02', rapid_commit=True, exp_addr='2001:db8:1::2')

    # enable rapid commit on subnet level and get get address using rapid method
    subnet_cfg.update(rapid_commit=False)
    get_address(mac_addr='00:00:00:00:00:03', exp_addr='2001:db8:1::3')


def test_rapid_commit_in_network():
    cfg = setup_server_for_config_backend_cmds()

    # create a subnet with rapid commit enabled
    network_cfg, _ = cfg.add_network()
    subnet_cfg, _ = cfg.add_subnet(network=network_cfg)
    get_address(mac_addr='00:00:00:00:00:01', exp_addr='2001:db8:1::1')

    # disable rapid commit
    network_cfg.update(rapid_commit=True)
    get_address(mac_addr='00:00:00:00:00:02', rapid_commit=True, exp_addr='2001:db8:1::2')

    # get address using regular method
    subnet_cfg.update(rapid_commit=False)
    get_address(mac_addr='00:00:00:00:00:03', exp_addr='2001:db8:1::3')

    # get address using regular method
    subnet_cfg.update(rapid_commit=True)
    get_address(mac_addr='00:00:00:00:00:04', rapid_commit=True, exp_addr='2001:db8:1::4')
