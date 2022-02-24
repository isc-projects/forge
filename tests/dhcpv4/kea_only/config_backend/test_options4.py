"""Kea config backend testing options."""

import pytest

from dhcp4_scen import get_address
from cb_model import setup_server_for_config_backend_cmds

pytestmark = [pytest.mark.kea_only,
              pytest.mark.hook,
              pytest.mark.v4,
              pytest.mark.configbackend]


@pytest.mark.parametrize('backend', ['mysql', 'postgresql'])
def test_options_pool(backend):
    cfg = setup_server_for_config_backend_cmds(backend_type=backend)

    cfg.add_subnet(backend=backend, pool_option_data={"code": 6, "csv-format": True, "data": "192.0.3.3",
                                                      "name": "domain-name-servers", "space": "dhcp4"})
    get_address(req_opts=6, exp_option={"code": 6, "data": "192.0.3.3"})


@pytest.mark.parametrize('backend', ['mysql', 'postgresql'])
def test_options_subnet(backend):
    cfg = setup_server_for_config_backend_cmds(backend_type=backend)

    cfg.add_subnet(backend=backend, option_data={"code": 6, "csv-format": True, "data": "192.0.2.2",
                                                 "name": "domain-name-servers", "space": "dhcp4"})

    get_address(req_opts=6, exp_option={"code": 6, "data": "192.0.2.2"})


@pytest.mark.parametrize('backend', ['mysql', 'postgresql'])
def test_options_network(backend):
    cfg = setup_server_for_config_backend_cmds(backend_type=backend)
    network_cfg, _ = cfg.add_network(backend=backend, option_data={"code": 10, "csv-format": True, "data": "1.1.1.1",
                                                                   "name": "impress-servers", "space": "dhcp4"})
    cfg.add_subnet(backend=backend, network=network_cfg)

    get_address(req_opts=[6, 10], exp_option={"code": 10, "data": "1.1.1.1"})


@pytest.mark.parametrize('backend', ['mysql', 'postgresql'])
def test_options_global(backend):
    cfg = setup_server_for_config_backend_cmds(backend_type=backend)
    cfg.add_subnet(backend=backend)
    cfg.add_option(backend=backend, code=10, csv_format=True, data="1.1.1.1", name="impress-servers", space="dhcp4")

    get_address(req_opts=[6, 10], exp_option={"code": 10, "data": "1.1.1.1"})

    cfg.del_option(backend=backend, code=10, server_tags=['all'])

    get_address(req_opts=[6, 10], no_exp_option={"code": 10})


@pytest.mark.parametrize('backend', ['mysql', 'postgresql'])
def test_options_all_levels(backend):
    cfg = setup_server_for_config_backend_cmds(backend_type=backend)
    cfg.add_option(backend=backend, code=10, csv_format=True, data="1.1.1.1", name="impress-servers", space="dhcp4")
    network_cfg, _ = cfg.add_network(backend=backend, option_data={"code": 4, "csv-format": True, "data": "2.2.2.2",
                                                                   "name": "time-servers", "space": "dhcp4"})
    cfg.add_subnet(backend=backend, network=network_cfg,
                   option_data={"code": 5, "csv-format": True, "data": "3.3.3.3",
                                "name": "name-servers", "space": "dhcp4"},
                   pool_option_data={"code": 6, "csv-format": True, "data": "4.4.4.4",
                                     "name": "domain-name-servers", "space": "dhcp4"})

    get_address(req_opts=[4, 5, 6, 10], exp_option=[{"code": 10, "data": "1.1.1.1"},
                                                    {"code": 5, "data": "3.3.3.3"},
                                                    {"code": 6, "data": "4.4.4.4"},
                                                    {"code": 4, "data": "2.2.2.2"}])


@pytest.mark.parametrize('backend', ['mysql', 'postgresql'])
def test_options_inherit(backend):
    cfg = setup_server_for_config_backend_cmds(backend_type=backend)

    # just with global option and empty subnet
    cfg.add_subnet(backend=backend)
    cfg.add_option(backend=backend, code=10, csv_format=True, data="1.1.1.1", name="impress-servers", space="dhcp4")

    get_address(req_opts=10, exp_option={"code": 10, "data": "1.1.1.1"})

    # del subnet, set network with option and with subnet without option
    cfg.del_subnet(backend=backend)
    network_cfg, _ = cfg.add_network(backend=backend, option_data={"code": 10, "csv-format": True, "data": "2.2.2.2",
                                                                   "name": "impress-servers", "space": "dhcp4"})
    cfg.add_subnet(backend=backend, network=network_cfg)

    get_address(req_opts=10, exp_option={"code": 10, "data": "2.2.2.2"})

    # delete subnet without option, set with new subnet with option - options on higher level are
    # still configured
    cfg.del_subnet(backend=backend)
    cfg.add_subnet(backend=backend, network=network_cfg,
                   option_data={"code": 10, "csv-format": True, "data": "3.3.3.3",
                                "name": "impress-servers", "space": "dhcp4"})

    get_address(req_opts=10, exp_option={"code": 10, "data": "3.3.3.3"})

    # delete subnet, and set new one, with option on subnet level and option at pool level
    cfg.del_subnet(backend=backend)
    cfg.add_subnet(backend=backend, network=network_cfg,
                   option_data={"code": 10, "csv-format": True, "data": "3.3.3.3",
                                "name": "impress-servers", "space": "dhcp4"},
                   pool_option_data={"code": 10, "csv-format": True, "data": "4.4.4.4",
                                     "name": "impress-servers", "space": "dhcp4"})

    get_address(req_opts=10, exp_option={"code": 10, "data": "4.4.4.4"})

#
#
# @pytest.mark.v4
# @pytest.mark.kea_only
# def test_options_inherit_custom_option(backend):
#     cfg = setup_server_for_config_backend_cmds(backend_type=backend)
# for now I don't know how to test custom option without tweaking scapy, TODO figure it out!
