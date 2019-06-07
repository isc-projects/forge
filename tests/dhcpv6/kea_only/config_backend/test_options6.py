"""Kea config backend testing options."""

import pytest

from dhcp4_scen import get_address
from cb_model import setup_server_for_config_backend_cmds

pytestmark = [pytest.mark.kea_only,
              pytest.mark.hook,
              pytest.mark.v6,
              pytest.mark.config_backend]


def test_options_pool():
    cfg = setup_server_for_config_backend_cmds()

    cfg.add_subnet(pool_option_data={"code": 22, "csv-format": True, "data": "2001::3",
                                     "name": "sip-server-addr", "space": "dhcp6"})
    get_address(req_opts=22, exp_option={"code": 22, "data": "2001::3"})


def test_options_subnet():
    cfg = setup_server_for_config_backend_cmds()

    cfg.add_subnet(option_data={"code": 22, "csv-format": True, "data": "2001::4",
                                "name": "sip-server-addr", "space": "dhcp6"})

    get_address(req_opts=22, exp_option={"code": 22, "data": "2001::4"})


def test_options_network():
    cfg = setup_server_for_config_backend_cmds()
    network_cfg, _ = cfg.add_network(option_data={"code": 23, "csv-format": True, "data": "2001::3",
                                                  "name": "dns-servers", "space": "dhcp6"})
    cfg.add_subnet(network=network_cfg)

    get_address(req_opts=[23, 27], exp_option={"code": 23, "data": "2001::3"})


def test_options_global():
    cfg = setup_server_for_config_backend_cmds()
    cfg.add_subnet()
    cfg.add_option(code=23, csv_format=True, data="2001::3", name="dns-servers", space="dhcp6")

    get_address(req_opts=[23, 27], exp_option={"code": 23, "data": "2001::3"})

    cfg.del_option(code=23)

    get_address(req_opts=[23, 27], no_exp_option={"code": 23})


def test_options_all_levels():
    cfg = setup_server_for_config_backend_cmds()
    cfg.add_option(code=31, csv_format=True, data="2001::31", name="sntp-servers", space="dhcp6")
    network_cfg, _ = cfg.add_network(option_data={"code": 28, "csv-format": True, "data": "2001::32",
                                                  "name": "nisp-servers", "space": "dhcp6"})
    cfg.add_subnet(network=network_cfg,
                   option_data={"code": 27, "csv-format": True, "data": "2001::33",
                                "name": "nis-servers", "space": "dhcp6"},
                   pool_option_data={"code": 22, "csv-format": True, "data": "2001::34",
                                     "name": "sip-server-addr", "space": "dhcp6"})

    get_address(req_opts=[31, 27, 22, 28], exp_option=[{"code": 31, "data": "2001::31"},
                                                       {"code": 27, "data": "2001::33"},
                                                       {"code": 22, "data": "2001::34"},
                                                       {"code": 28, "data": "2001::32"}])


def test_options_inherit():
    cfg = setup_server_for_config_backend_cmds()

    # just with global option and empty subnet
    cfg.add_subnet()
    cfg.add_option(code=23, csv_format=True, data="2001::31", name="dns-servers", space="dhcp6")

    get_address(req_opts=23, exp_option={"code": 23, "data": "2001::31"})

    # del subnet, set network with option and with subnet without option
    cfg.del_subnet()
    network_cfg, _ = cfg.add_network(option_data={"code": 23, "csv-format": True, "data": "2001::32",
                                                  "name": "dns-servers", "space": "dhcp6"})
    cfg.add_subnet(network=network_cfg)

    get_address(req_opts=23, exp_option={"code": 23, "data": "2001::32"})

    # delete subnet without option, set with new subnet with option - options on higher level are
    # still configured
    cfg.del_subnet()
    cfg.add_subnet(network=network_cfg,
                   option_data={"code": 23, "csv-format": True, "data": "2001::33",
                                "name": "dns-servers", "space": "dhcp6"})

    get_address(req_opts=23, exp_option={"code": 23, "data": "2001::33"})

    # delete subnet, and set new one, with option on subnet level and option at pool level
    cfg.del_subnet()
    cfg.add_subnet(network=network_cfg,
                   option_data={"code": 23, "csv-format": True, "data": "2001::33",
                                "name": "dns-servers", "space": "dhcp6"},
                   pool_option_data={"code": 23, "csv-format": True, "data": "2001::34",
                                     "name": "dns-servers", "space": "dhcp6"})

    get_address(req_opts=23, exp_option={"code": 23, "data": "2001::34"})
