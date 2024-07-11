# Copyright (C) 2022 Internet Systems Consortium, Inc. ("ISC")
#
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

"""Kea config backend testing options."""

import pytest

from src import misc
from src import srv_control
from src.forge_cfg import world

from src.protosupport.dhcp4_scen import get_address
from src.softwaresupport.cb_model import setup_server_for_config_backend_cmds


pytestmark = [pytest.mark.hook,
              pytest.mark.v4,
              pytest.mark.cb]


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
# def test_options_inherit_custom_option(backend):
#     cfg = setup_server_for_config_backend_cmds(backend_type=backend)
# for now I don't know how to test custom option without tweaking scapy, TODO figure it out!


@pytest.mark.parametrize('parameter', ['shared-networks', 'subnet', 'client-classes'])
def test_suboptions_configfile(parameter):
    """Control tests using config file.
    Kea is configured with option 43 and suboption 61 in shared-networks, subnet and client-classes.
    Forge tests if client gets suboption value.
    Test for Kea#3481

    """
    misc.test_setup()
    config = {
        'shared-networks': [
            {
                "interface": "enp0s9",
                "name": "floor13",
                "option-data": [],
                "relay": {
                        "ip-addresses": []
                },
                "subnet4": [
                    {
                        "4o6-interface": "",
                        "4o6-interface-id": "",
                        "4o6-subnet": "",
                        "id": 1,
                        "interface": "enp0s9",
                        "option-data": [],
                        "pools": [
                            {
                                "option-data": [],
                                "pool": "192.168.50.1-192.168.50.100"
                            }
                        ],
                        "relay": {
                            "ip-addresses": []
                        },
                        "reservations": [],
                        "subnet": "192.168.50.0/24"
                    }
                ]
            }
        ],
    }
    if parameter == "shared-networks":
        config["shared-networks"][0]["option-data"] = [{
            "always-send": True,
            "code": 43,
        },
            {
            "code": 61,
                "data": "FF3D0408080808",
                "space": "vendor-encapsulated-options-space"
        }]
    elif parameter == "subnet":
        config["shared-networks"][0]["subnet4"][0]["option-data"] = [{
            "always-send": True,
            "code": 43,
        },
            {
            "code": 61,
                "data": "FF3D0408080808",
                "space": "vendor-encapsulated-options-space"
        }]
    else:
        config["client-classes"] = [
            {
                "name": "option-class",
                "test": "member('ALL')",
                "option-data": [{
                    "always-send": True,
                    "code": 43,
                },
                    {
                    "code": 61,
                    "data": "FF3D0408080808",
                    "space": "vendor-encapsulated-options-space"
                }]
            }
        ]

    world.dhcp_cfg.update(config)
    srv_control.build_and_send_config_files()
    srv_control.start_srv('DHCP', 'started')

    # Hex data: 3D - option number "61", 07 - length , FF3D0408080808 - suboption 61 value.
    get_address(req_opts=[43], exp_option={"code": 43, "data": "HEX:3D07FF3D0408080808"})


@pytest.mark.parametrize('backend', ['mysql', 'postgresql'])
@pytest.mark.parametrize('parameter', ['shared-networks', 'subnet', 'client-classes'])
def test_suboptions(parameter, backend):
    """
    Kea is configured with empty option 43.
    Suboption 61 is added to config backend in shared-networks, subnet or client-classes
    Forge tests if client gets suboption value.
    Test for Kea#3481
    """
    cfg = setup_server_for_config_backend_cmds(backend_type=backend)
    if parameter == "shared-networks":
        network_cfg, _ = cfg.add_network(backend=backend,
                                         option_data=[{"code": 43, "always-send": True,
                                                       "name": "vendor-encapsulated-options",
                                                       "space": "dhcp4"},
                                                      {"code": 61, "data": "FF3D0408080808",
                                                       "space": "vendor-encapsulated-options-space"}])
        cfg.add_subnet(backend=backend, network=network_cfg)

    elif parameter == "subnet":
        network_cfg, _ = cfg.add_network(backend=backend)
        cfg.add_subnet(backend=backend, network=network_cfg,
                       option_data=[{"code": 43, "always-send": True,
                                     "name": "vendor-encapsulated-options",
                                     "space": "dhcp4"},
                                    {"code": 61, "data": "FF3D0408080808",
                                     "space": "vendor-encapsulated-options-space"}])

    else:
        network_cfg, _ = cfg.add_network(backend=backend)
        cfg.add_subnet(backend=backend, network=network_cfg)
        cfg.add_class(backend=backend, name="option-class", test="member('ALL')",
                      option_data=[{"code": 43, "always-send": True,
                                    "name": "vendor-encapsulated-options",
                                    "space": "dhcp4"},
                                   {"code": 61, "data": "FF3D0408080808",
                                    "space": "vendor-encapsulated-options-space"}])

    get_address(req_opts=[43], exp_option={"code": 43, "data": "HEX:3D07FF3D0408080808"})
