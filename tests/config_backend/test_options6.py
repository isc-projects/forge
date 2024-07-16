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


@pytest.mark.parametrize('parameter', ['shared-networks', 'subnet', 'pool', 'global', 'client-classes'])
def test_suboptions_configfile(parameter):
    """Control tests using config file.
    Kea is configured with option 160 and suboption 1 in shared-networks, subnet and client-classes.
    Forge tests if client gets suboption value.
    Test for Kea#3481
    """
    misc.test_setup()
    # Option definitions.
    option_def = [
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
    option_data = [
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

    # Prepare option definitions.
    srv_control.set_conf_parameter_global('option-def', option_def)

    # Prepare networks and add options-data.
    if parameter == "shared-networks":
        srv_control.config_srv_subnet("2001:db8:1::/64", "2001:db8:1::1-2001:db8:1::100", id=1)
        srv_control.shared_subnet('2001:db8:1::/64', 0)
        srv_control.set_conf_parameter_shared_subnet('name', 'floor13', 0)
        world.dhcp_cfg['shared-networks'][0]['option-data'] = option_data
    elif parameter == "subnet":
        srv_control.config_srv_subnet("2001:db8:1::/64", "2001:db8:1::1-2001:db8:1::100", id=1, option_data=option_data)
        srv_control.shared_subnet('2001:db8:1::/64', 0)
        srv_control.set_conf_parameter_shared_subnet('name', 'floor13', 0)
    elif parameter == "pool":
        srv_control.config_srv_subnet("2001:db8:1::/64", "2001:db8:1::1-2001:db8:1::100", id=1)
        srv_control.shared_subnet('2001:db8:1::/64', 0)
        srv_control.set_conf_parameter_shared_subnet('name', 'floor13', 0)
        world.dhcp_cfg['shared-networks'][0]['subnet6'][0]['pools'][0]['option-data'] = option_data
    elif parameter == "global":
        srv_control.config_srv_subnet("2001:db8:1::/64", "2001:db8:1::1-2001:db8:1::100", id=1)
        srv_control.shared_subnet('2001:db8:1::/64', 0)
        srv_control.set_conf_parameter_shared_subnet('name', 'floor13', 0)
        srv_control.set_conf_parameter_global('option-data', option_data)
    else:
        srv_control.config_srv_subnet("2001:db8:1::/64", "2001:db8:1::1-2001:db8:1::100", id=1)
        srv_control.shared_subnet('2001:db8:1::/64', 0)
        srv_control.set_conf_parameter_shared_subnet('name', 'floor13', 0)
        srv_control.create_new_class('option-class')
        srv_control.add_test_to_class(1, 'test', 'member(\'ALL\')')
        srv_control.add_test_to_class(1, 'option-data', option_data[0])
        srv_control.add_test_to_class(1, 'option-data', option_data[1])

    srv_control.open_control_channel()
    srv_control.build_and_send_config_files()
    srv_control.start_srv('DHCP', 'started')

    # Check if Forge makes SARR exchange with included suboption.
    get_address(req_opts=[160], exp_option={"code": 160, "data": "00010003012345"})


def _send_option_data(option_data, parameter, backend, cfg):
    """Helper function for test_suboptions() test
    Adds networks, subnets, classes and option data using confing backend commands.
    """
    # Add option 160 and suboption data to specific place.
    if parameter == "shared-networks":
        network_cfg, _ = cfg.add_network(backend=backend,
                                         option_data=option_data)
        cfg.add_subnet(backend=backend, network=network_cfg)
    elif parameter == "subnet":
        network_cfg, _ = cfg.add_network(backend=backend)
        cfg.add_subnet(backend=backend, network=network_cfg,
                       option_data=option_data)
    elif parameter == "pool":
        network_cfg, _ = cfg.add_network(backend=backend)
        cfg.add_subnet(backend=backend, network=network_cfg,
                       pool_option_data=option_data)
    elif parameter == "client-classes":
        network_cfg, _ = cfg.add_network(backend=backend)
        cfg.add_subnet(backend=backend, network=network_cfg)
        cfg.add_class(backend=backend, name="option-class", test="member('ALL')",
                      option_data=option_data)
    else:
        network_cfg, _ = cfg.add_network(backend=backend)
        cfg.add_subnet(backend=backend, network=network_cfg)
        # add_option() required adding backend parameter.
        for i, _ in enumerate(option_data):
            option_data[i]["backend"] = backend
        cfg.add_option(option_data[0], option_data[1])


@pytest.mark.parametrize('backend', ['mysql', 'postgresql'])
@pytest.mark.parametrize('parameter', ['shared-networks', 'subnet', 'client-classes', 'global'])
@pytest.mark.parametrize('order', ['normal'])  # 'reverse'
# "Reverse option declaration test are skipped due to lack of design of Kea behavior"
def test_suboptions(parameter, order, backend):
    """
    Kea is configured with empty data in option 160 and suboption using config backend commands.
    Suboption and option definition is added to config backend in all posible places.
    Forge tests if client gets suboption value.

    order: Set order of adding Option-def and option-data

    Test for Kea#3481
    """
    option_data = [
        {
            "always-send": True,
            "csv-format": False,
            "code": 160,
            "space": "dhcp6",
            "data": "",
            "never-send": False,
            "name": "container"
        },
        {
            "always-send": True,
            "csv-format": False,
            "code": 1,
            "space": "isc",
            "data": "012345",
            "name": "subopt1"
        }]

    option_defs = [
        {
            "backend": backend,
            "name": "container",
            "code": 160,
            "space": "dhcp6",
            "type": "empty",
            "array": False,
            "record-types": "",
            "encapsulate": "isc"
        },
        {
            "backend": backend,
            "name": "subopt1",
            "code": 1,
            "space": "isc",
            "type": "binary",
            "record-types": "",
            "array": False,
            "encapsulate": ""
        }]

    # Prepare and start Kea
    cfg = setup_server_for_config_backend_cmds(backend_type=backend)

    if order == 'normal':
        # Add option 160 and 1 definition to config backend.
        cfg.add_option_def(option_defs[0], option_defs[1])
        # Add option data 160 and suboption data to specific place.
        _send_option_data(option_data, parameter, backend, cfg)
    else:
        # When adding options in reverse, Kea does not return 'name' in option-data in config-get.
        # This interferes with response checking in Forge and is not the goal of this test.
        for option in option_data:
            option.pop('name')
        # Add option data 160 and suboption data to specific place.
        _send_option_data(option_data, parameter, backend, cfg)
        # Add option 160 and 1 definition to config backend
        cfg.add_option_def(option_defs[0], option_defs[1])

    # Check if Forge makes SARR exchange with included suboption.
    get_address(req_opts=[160], exp_option={"code": 160, "data": "00010003012345"})
