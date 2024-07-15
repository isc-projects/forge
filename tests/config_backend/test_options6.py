# Copyright (C) 2022 Internet Systems Consortium, Inc. ("ISC")
#
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

"""Kea config backend testing options."""

import pytest

from src import misc
from src import srv_control
from src import srv_msg
from src.forge_cfg import world

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


@pytest.mark.parametrize('parameter', ['shared-networks', 'subnet', 'client-classes'])
def test_suboptions_configfile(parameter):
    """Control tests using config file.
    Kea is configured with option 160 and suboption 1 in shared-networks, subnet and client-classes.
    Forge tests if client gets suboption value.
    Test for Kea#3481

    """
    misc.test_setup()
    # prepare base config
    config = {
        'shared-networks': [
            {
                "interface": "enp0s9",
                "name": "floor13",
                "option-data": [],
                "relay": {
                        "ip-addresses": []
                },
                "subnet6": [
                    {
                        "id": 1,
                        "interface": "enp0s9",
                        "option-data": [],
                        "pools": [
                            {
                                "option-data": [],
                                "pool": "2001:db8:1::1-2001:db8:1::100"
                            }
                        ],
                        "relay": {
                            "ip-addresses": []
                        },
                        "reservations": [],
                        "subnet": "2001:db8:1::/64"
                    }
                ]
            }
        ],
    }

    # add option definitions
    config["option-def"] = [
        {
            "name": "container",
            "code": 160,
            "space": "dhcp6",
            "type": "empty",
            "array": False,
            "record-types": "",
            "encapsulate": "isc"
        },
        {
            "name": "subopt1",
            "code": 1,
            "space": "isc",
            "type": "binary",
            "record-types": "",
            "array": False,
            "encapsulate": ""
        }
    ]

    # Add option 160 to shared-networks, subnet or client-classes
    if parameter == "shared-networks":
        config["shared-networks"][0]["option-data"] = [
            {
                "name": "container",
                "code": 160,
                "space": "dhcp6"
            },
            {
                "name": "subopt1",
                "code": 1,
                "space": "isc",
                "data": "012345"
            }]
    elif parameter == "subnet":
        config["shared-networks"][0]["subnet6"][0]["option-data"] = [
            {
                "name": "container",
                "code": 160,
                "space": "dhcp6"
            },
            {
                "name": "subopt1",
                "code": 1,
                "space": "isc",
                "data": "012345"
            }]
    else:
        config["client-classes"] = [
            {
                "name": "option-class",
                "test": "member('ALL')",
                "option-data": [
                    {
                        "name": "container",
                        "code": 160,
                        "space": "dhcp6"
                    },
                    {
                        "name": "subopt1",
                        "code": 1,
                        "space": "isc",
                        "data": "012345"
                    }]
            }
        ]

    # Upload config and start server
    world.dhcp_cfg.update(config)
    srv_control.build_and_send_config_files()
    srv_control.start_srv('DHCP', 'started')

    # Check if Forge makes SARR exchange with included suboption
    get_address(req_opts=[160], exp_option={"code": 160, "data": "00010003012345"})


@pytest.mark.parametrize('backend', ['mysql', 'postgresql'])
@pytest.mark.parametrize('parameter', ['shared-networks', 'subnet', 'client-classes'])
def test_suboptions(parameter, backend):
    """
    Kea is configured with empty option 160.
    Suboption 1 is added to config backend in shared-networks, subnet or client-classes
    Forge tests if client gets suboption value.
    Test for Kea#3481
    """
    # Prepare and start Kea
    cfg = setup_server_for_config_backend_cmds(backend_type=backend)

    # Add option 160 and suboption data to shared-networks, subnet or client-classes
    if parameter == "shared-networks":
        network_cfg, _ = cfg.add_network(backend=backend,
                                         option_data=[
                                             {
                                                 "always-send": True,
                                                 "csv-format": False,
                                                 "code": 160,
                                                 "space": "dhcp6",
                                                 "data": "",
                                                 "never-send": False
                                             },
                                             {
                                                 "always-send": True,
                                                 "csv-format": False,
                                                 "code": 1,
                                                 "space": "isc",
                                                 "data": "012345"
                                             }])
        cfg.add_subnet(backend=backend, network=network_cfg)
    elif parameter == "subnet":
        network_cfg, _ = cfg.add_network(backend=backend)
        cfg.add_subnet(backend=backend, network=network_cfg,
                       option_data=[
                           {
                               "always-send": True,
                               "csv-format": False,
                               "code": 160,
                               "space": "dhcp6",
                               "data": "",
                               "never-send": False
                           },
                           {
                               "always-send": True,
                               "csv-format": False,
                               "code": 1,
                               "space": "isc",
                               "data": "012345"
                           }])
    else:
        network_cfg, _ = cfg.add_network(backend=backend)
        cfg.add_subnet(backend=backend, network=network_cfg)
        cfg.add_class(backend=backend, name="option-class", test="member('ALL')",
                      option_data=[
                          {
                              "always-send": True,
                              "csv-format": False,
                              "code": 160,
                              "space": "dhcp6",
                              "data": "",
                              "never-send": False
                          },
                          {
                              "always-send": True,
                              "csv-format": False,
                              "code": 1,
                              "space": "isc",
                              "data": "012345"
                          }])

    # Add option 160 definition to config backend
    option_defs1 = [
        {
            "name": "container",
            "code": 160,
            "space": "dhcp6",
            "type": "empty",
            "array": False,
            "record-types": "",
            "encapsulate": "isc"
        }
    ]
    cmd = {"command": "remote-option-def6-set",
           "arguments": {"remote": {"type": backend},
                         'server-tags': ['ALL'],
                         "option-defs": option_defs1}
           }
    srv_msg.send_ctrl_cmd(cmd)

    # Add suboption definition to config backend
    option_defs2 = [
        {
            "name": "subopt1",
            "code": 1,
            "space": "isc",
            "type": "binary",
            "record-types": "",
            "array": False,
            "encapsulate": ""
        }
    ]
    cmd = {"command": "remote-option-def6-set",
           "arguments": {"remote": {"type": backend},
                         'server-tags': ['ALL'],
                         "option-defs": option_defs2}
           }
    srv_msg.send_ctrl_cmd(cmd)

    # Refresh config from config backend
    cmd = {"command": "config-backend-pull",
           "arguments": {}
           }
    srv_msg.send_ctrl_cmd(cmd)

    # Check if Forge makes SARR exchange with included suboption
    get_address(req_opts=[160], exp_option={"code": 160, "data": "00010003012345"})
