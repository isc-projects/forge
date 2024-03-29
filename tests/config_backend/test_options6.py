# Copyright (C) 2022 Internet Systems Consortium, Inc. ("ISC")
#
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

"""Kea config backend testing options."""

import pytest

from src.protosupport.dhcp4_scen import get_address
from src.softwaresupport.cb_model import setup_server_for_config_backend_cmds

pytestmark = [pytest.mark.hook,
              pytest.mark.v6,
              pytest.mark.cb]


@pytest.mark.parametrize('backend', ['mysql', 'postgresql'])
def test_options_pool(backend):
    cfg = setup_server_for_config_backend_cmds(backend_type=backend)

    cfg.add_subnet(backend=backend,
                   pool_option_data={"code": 22, "csv-format": True, "data": "2001::3",
                                     "name": "sip-server-addr", "space": "dhcp6"})
    get_address(req_opts=22, exp_option={"code": 22, "data": "2001::3"})


@pytest.mark.parametrize('backend', ['mysql', 'postgresql'])
def test_options_subnet(backend):
    cfg = setup_server_for_config_backend_cmds(backend_type=backend)

    cfg.add_subnet(backend=backend,
                   option_data={"code": 22, "csv-format": True, "data": "2001::4",
                                "name": "sip-server-addr", "space": "dhcp6"})

    get_address(req_opts=22, exp_option={"code": 22, "data": "2001::4"})


@pytest.mark.parametrize('backend', ['mysql', 'postgresql'])
def test_options_network(backend):
    cfg = setup_server_for_config_backend_cmds(backend_type=backend)
    network_cfg, _ = cfg.add_network(backend=backend,
                                     option_data={"code": 23, "csv-format": True, "data": "2001::3",
                                                  "name": "dns-servers", "space": "dhcp6"})
    cfg.add_subnet(backend=backend, network=network_cfg)

    get_address(req_opts=[23, 27], exp_option={"code": 23, "data": "2001::3"})


@pytest.mark.parametrize('backend', ['mysql', 'postgresql'])
def test_options_global(backend):
    cfg = setup_server_for_config_backend_cmds(backend_type=backend)
    cfg.add_subnet(backend=backend)
    cfg.add_option(backend=backend, code=23, csv_format=True, data="2001::3", name="dns-servers", space="dhcp6")

    get_address(req_opts=[23, 27], exp_option={"code": 23, "data": "2001::3"})

    cfg.del_option(backend=backend, code=23)

    get_address(req_opts=[23, 27], no_exp_option={"code": 23})


@pytest.mark.parametrize('backend', ['mysql', 'postgresql'])
def test_options_all_levels(backend):
    cfg = setup_server_for_config_backend_cmds(backend_type=backend)
    cfg.add_option(backend=backend, code=31, csv_format=True, data="2001::31", name="sntp-servers", space="dhcp6")
    network_cfg, _ = cfg.add_network(backend=backend,
                                     option_data={"code": 28, "csv-format": True, "data": "2001::32",
                                                  "name": "nisp-servers", "space": "dhcp6"})
    cfg.add_subnet(backend=backend,
                   network=network_cfg,
                   option_data={"code": 27, "csv-format": True, "data": "2001::33",
                                "name": "nis-servers", "space": "dhcp6"},
                   pool_option_data={"code": 22, "csv-format": True, "data": "2001::34",
                                     "name": "sip-server-addr", "space": "dhcp6"})

    get_address(req_opts=[31, 27, 22, 28], exp_option=[{"code": 31, "data": "2001::31"},
                                                       {"code": 27, "data": "2001::33"},
                                                       {"code": 22, "data": "2001::34"},
                                                       {"code": 28, "data": "2001::32"}])


@pytest.mark.parametrize('backend', ['mysql', 'postgresql'])
def test_options_inherit(backend):
    cfg = setup_server_for_config_backend_cmds(backend_type=backend)

    # just with global option and empty subnet
    cfg.add_subnet(backend=backend)
    cfg.add_option(backend=backend, code=23, csv_format=True, data="2001::31", name="dns-servers", space="dhcp6")

    get_address(req_opts=23, exp_option={"code": 23, "data": "2001::31"})

    # del subnet, set network with option and with subnet without option
    cfg.del_subnet(backend=backend)
    network_cfg, _ = cfg.add_network(backend=backend,
                                     option_data={"code": 23, "csv-format": True, "data": "2001::32",
                                                  "name": "dns-servers", "space": "dhcp6"})
    cfg.add_subnet(backend=backend, network=network_cfg)

    get_address(req_opts=23, exp_option={"code": 23, "data": "2001::32"})

    # delete subnet without option, set with new subnet with option - options on higher level are
    # still configured
    cfg.del_subnet(backend=backend)
    cfg.add_subnet(backend=backend,
                   network=network_cfg,
                   option_data={"code": 23, "csv-format": True, "data": "2001::33",
                                "name": "dns-servers", "space": "dhcp6"})

    get_address(req_opts=23, exp_option={"code": 23, "data": "2001::33"})

    # delete subnet, and set new one, with option on subnet level and option at pool level
    cfg.del_subnet(backend=backend)
    cfg.add_subnet(backend=backend,
                   network=network_cfg,
                   option_data={"code": 23, "csv-format": True, "data": "2001::33",
                                "name": "dns-servers", "space": "dhcp6"},
                   pool_option_data={"code": 23, "csv-format": True, "data": "2001::34",
                                     "name": "dns-servers", "space": "dhcp6"})

    get_address(req_opts=23, exp_option={"code": 23, "data": "2001::34"})
