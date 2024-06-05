# Copyright (C) 2022 Internet Systems Consortium, Inc. ("ISC")
#
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

"""Kea config backend testing server-tag."""

import pytest

from src import srv_control
from src import srv_msg

from src.protosupport.dhcp4_scen import get_address, get_rejected
from src.softwaresupport.cb_model import setup_server_for_config_backend_cmds
from src.forge_cfg import world

pytestmark = [pytest.mark.hook,
              pytest.mark.v4,
              pytest.mark.cb]


@pytest.fixture(autouse=True)
def run_around_each_test(request):
    world.check_on_reload = False

    def unset():
        world.check_on_reload = True

    request.addfinalizer(unset)


def _set_server_tag(backend, tag="abc"):
    cmd = dict(command="remote-server4-set", arguments={"remote": {"type": backend},
                                                        "servers": [{"server-tag": tag}]})
    return srv_msg.send_ctrl_cmd(cmd, exp_result=0)


def _get_server_config(reload_kea=False):
    if reload_kea:
        cmd = dict(command="config-backend-pull", arguments={})
        srv_msg.send_ctrl_cmd(cmd, exp_result=0)
    cmd = dict(command="config-get", arguments={})
    return srv_msg.send_ctrl_cmd(cmd, exp_result=0)


@pytest.mark.parametrize('backend', ['mysql', 'postgresql'])
def test_server_tag_subnet4(backend):
    # create first configuration
    cfg_xyz = setup_server_for_config_backend_cmds(backend_type=backend, server_tag="xyz")
    _set_server_tag(backend, "xyz")
    _set_server_tag(backend, "abc")
    get_rejected()
    # add configuration for abc, don't check reconfigure result
    cfg_xyz.add_subnet(backend=backend, server_tags=["abc"], subnet="192.168.50.0/24", id=1,
                       pools=[{'pool': "192.168.50.1-192.168.50.1"}])

    get_rejected()

    # unassigned is not supported yet
    # cfg_xyz.add_subnet(backend=backend, server_tags=["unassigned"], subnet="192.168.50.0/24", id=3,
    #                    pools=[{'pool': "192.168.50.10-192.168.50.10"}])
    #
    # get_rejected()

    # add configuration for xyz
    cfg_xyz.add_subnet(backend=backend, server_tags=["xyz"], subnet="192.168.51.0/24", id=2,
                       pools=[{'pool': "192.168.51.50-192.168.51.50"}])

    get_address(mac_addr='00:00:00:00:00:01', exp_addr='192.168.51.50')

    xyz = _get_server_config()
    # check if it's configured with just one subnet
    assert len(xyz["arguments"]["Dhcp4"]["subnet4"]) == 1
    # and this subnet is as expected
    assert xyz["arguments"]["Dhcp4"]["subnet4"][0]["id"] == 2
    assert xyz["arguments"]["Dhcp4"]["subnet4"][0]["subnet"] == "192.168.51.0/24"

    srv_control.start_srv('DHCP', 'stopped')

    # create second configuration
    setup_server_for_config_backend_cmds(backend_type=backend, server_tag="abc")

    get_address(mac_addr='00:00:00:00:00:02', exp_addr='192.168.50.1')
    abc = _get_server_config()
    # check if it's configured with just one subnet
    assert len(abc["arguments"]["Dhcp4"]["subnet4"]) == 1
    # and this subnet is as expected
    assert abc["arguments"]["Dhcp4"]["subnet4"][0]["id"] == 1
    assert abc["arguments"]["Dhcp4"]["subnet4"][0]["subnet"] == "192.168.50.0/24"

    srv_control.start_srv('DHCP', 'stopped')

    # create third subnet that will use "all" tag
    cfg_qwe = setup_server_for_config_backend_cmds(backend_type=backend, server_tag="qwe")

    get_rejected()

    cfg_qwe.add_subnet(backend=backend, server_tags=["all"], subnet="192.168.52.0/24", id=3,
                       pools=[{'pool': "192.168.52.20-192.168.52.21"}])

    abc = _get_server_config()
    # check if it's configured with just one subnet
    assert len(abc["arguments"]["Dhcp4"]["subnet4"]) == 1
    # and this subnet is as expected
    assert abc["arguments"]["Dhcp4"]["subnet4"][0]["id"] == 3
    assert abc["arguments"]["Dhcp4"]["subnet4"][0]["subnet"] == "192.168.52.0/24"

    get_address(mac_addr='00:00:00:00:00:03', exp_addr='192.168.52.20')

    srv_control.start_srv('DHCP', 'stopped')
    setup_server_for_config_backend_cmds(backend_type=backend, server_tag="abc")
    abc = _get_server_config()

    # two subnets without classification on the same interface doesn't make sense so we will just check config
    # check if it's configured with just two subnets, all and abc configured at the beginning of a test
    assert len(abc["arguments"]["Dhcp4"]["subnet4"]) == 2
    # and this subnet is as expected
    assert abc["arguments"]["Dhcp4"]["subnet4"][0]["id"] == 1
    assert abc["arguments"]["Dhcp4"]["subnet4"][1]["id"] == 3
    assert abc["arguments"]["Dhcp4"]["subnet4"][0]["subnet"] == "192.168.50.0/24"
    assert abc["arguments"]["Dhcp4"]["subnet4"][1]["subnet"] == "192.168.52.0/24"


@pytest.mark.parametrize('backend', ['mysql', 'postgresql'])
def test_server_tag_global_option4_trimmed(backend):
    cfg = setup_server_for_config_backend_cmds(backend_type=backend, server_tag="abc")
    _set_server_tag(backend, "xyz")
    _set_server_tag(backend, "abc")
    cfg.add_subnet(backend=backend, server_tags="abc")
    cfg.add_option(backend=backend, server_tags=["all"], code=3, csv_format=True, data="10.0.0.1", name="routers",
                   space="dhcp4")

    abc = _get_server_config()
    # server should have just one option now, from "all"
    assert len(abc["arguments"]["Dhcp4"]["option-data"]) == 1
    assert abc["arguments"]["Dhcp4"]["option-data"][0]["data"] == "10.0.0.1"

    get_address(req_opts=[3], exp_option={"code": 3, "data": "10.0.0.1"})

    cfg.add_option(backend=backend, server_tags=["abc"], code=3, csv_format=True, data="10.0.0.2", name="routers",
                   space="dhcp4")
    abc = _get_server_config()
    # now, despite the fact that two tags are for server "abc" ("abc" and "all") option "all" should be overwritten
    assert len(abc["arguments"]["Dhcp4"]["option-data"]) == 1
    assert abc["arguments"]["Dhcp4"]["option-data"][0]["data"] == "10.0.0.2"
    get_address(req_opts=[3], exp_option={"code": 3, "data": "10.0.0.2"})

    cfg.add_option(backend=backend, server_tags=["xyz"], code=3, csv_format=True, data="10.0.0.3", name="routers",
                   space="dhcp4")
    abc = _get_server_config()
    # after adding "xyz" option, there should not be any change in running kea
    assert len(abc["arguments"]["Dhcp4"]["option-data"]) == 1
    assert abc["arguments"]["Dhcp4"]["option-data"][0]["data"] == "10.0.0.2"
    get_address(req_opts=[3], exp_option={"code": 3, "data": "10.0.0.2"})

    srv_control.start_srv('DHCP', 'stopped')

    cfg_xyz = setup_server_for_config_backend_cmds(backend_type=backend, server_tag="xyz")
    cfg_xyz.add_subnet(backend=backend, server_tags="xyz")
    abc = _get_server_config()
    # new kea is started with tag "xyz"
    assert len(abc["arguments"]["Dhcp4"]["option-data"]) == 1
    assert abc["arguments"]["Dhcp4"]["option-data"][0]["data"] == "10.0.0.3"

    get_address(req_opts=[3], exp_option={"code": 3, "data": "10.0.0.3"})


@pytest.mark.awaiting_fix
@pytest.mark.disabled
@pytest.mark.parametrize('backend', ['mysql', 'postgresql'])
def test_server_tag_global_option4(backend):
    # kea1600 disabled because we will be waiting for a long time to fix,
    # if this test will be enabled please remove test_server_tag_global_option4_trimmed
    cfg = setup_server_for_config_backend_cmds(backend_type=backend, server_tag="abc")
    _set_server_tag(backend, "xyz")
    _set_server_tag(backend, "abc")
    cfg.add_subnet(backend=backend, server_tags="abc")
    cfg.add_option(backend=backend, server_tags=["all"], code=3, csv_format=True, data="10.0.0.1", name="routers",
                   space="dhcp4")

    abc = _get_server_config()
    # server should have just one option now, from "all"
    assert len(abc["arguments"]["Dhcp4"]["option-data"]) == 1
    assert abc["arguments"]["Dhcp4"]["option-data"][0]["data"] == "10.0.0.1"

    get_address(req_opts=[3], exp_option={"code": 3, "data": "10.0.0.1"})

    cfg.add_option(backend=backend, server_tags=["abc"], code=3, csv_format=True, data="10.0.0.2", name="routers",
                   space="dhcp4")
    abc = _get_server_config()
    # now, despite the fact that two tags are for server "abc" ("abc" and "all") option "all" should be overwritten
    assert len(abc["arguments"]["Dhcp4"]["option-data"]) == 1
    assert abc["arguments"]["Dhcp4"]["option-data"][0]["data"] == "10.0.0.2"
    get_address(req_opts=[3], exp_option={"code": 3, "data": "10.0.0.2"})

    cfg.add_option(backend=backend, server_tags=["xyz"], code=3, csv_format=True, data="10.0.0.3", name="routers",
                   space="dhcp4")
    abc = _get_server_config()
    # after adding "xyz" option, there should not be any change in running kea
    assert len(abc["arguments"]["Dhcp4"]["option-data"]) == 1
    assert abc["arguments"]["Dhcp4"]["option-data"][0]["data"] == "10.0.0.2"
    get_address(req_opts=[3], exp_option={"code": 3, "data": "10.0.0.2"})

    srv_control.start_srv('DHCP', 'stopped')

    cfg_xyz = setup_server_for_config_backend_cmds(backend_type=backend, server_tag="xyz")
    cfg_xyz.add_subnet(backend=backend, server_tags="xyz")
    abc = _get_server_config()
    # new kea is started with tag "xyz"
    assert len(abc["arguments"]["Dhcp4"]["option-data"]) == 1
    assert abc["arguments"]["Dhcp4"]["option-data"][0]["data"] == "10.0.0.3"

    get_address(req_opts=[3], exp_option={"code": 3, "data": "10.0.0.3"})

    # delete option with tag "xyz", kea should download tag "all"
    cfg_xyz.del_option(backend=backend, server_tags=["xyz"], code=3)
    xyz = _get_server_config(reload_kea=True)
    assert len(xyz["arguments"]["Dhcp4"]["option-data"]) == 1
    assert xyz["arguments"]["Dhcp4"]["option-data"][0]["data"] == "10.0.0.1"
    get_address(req_opts=[3], exp_option={"code": 3, "data": "10.0.0.1"})


@pytest.mark.parametrize('backend', ['mysql', 'postgresql'])
def test_server_tag_network4(backend):
    cfg = setup_server_for_config_backend_cmds(backend_type=backend, server_tag="abc")
    _set_server_tag(backend, "xyz")
    _set_server_tag(backend, "abc")
    cfg.add_network(backend=backend, server_tags=["abc"], name="flor1")

    cfg.add_subnet(backend=backend, shared_network_name="flor1", server_tags=["abc"],
                   subnet="192.168.50.0/24", id=1, pools=[{'pool': "192.168.50.1-192.168.50.1"}])

    xyz = _get_server_config()
    assert len(xyz["arguments"]["Dhcp4"]["shared-networks"][0]["subnet4"]) == 1
    assert xyz["arguments"]["Dhcp4"]["shared-networks"][0]["subnet4"][0]["subnet"] == "192.168.50.0/24"

    get_address(mac_addr='00:00:00:00:00:03', exp_addr='192.168.50.1')

    cfg.add_network(backend=backend, server_tags=["xyz"], name="flor2")

    cfg.add_subnet(backend=backend, shared_network_name="flor2", server_tags=["xyz"],
                   subnet="192.168.51.0/24", id=2, pools=[{'pool': "192.168.51.5-192.168.51.5"}])

    # we still want just one network with one subnet
    xyz = _get_server_config()
    assert len(xyz["arguments"]["Dhcp4"]["shared-networks"]) == 1
    assert len(xyz["arguments"]["Dhcp4"]["shared-networks"][0]["subnet4"]) == 1
    assert xyz["arguments"]["Dhcp4"]["shared-networks"][0]["subnet4"][0]["subnet"] == "192.168.50.0/24"

    get_rejected(mac_addr='00:00:00:00:00:10')
    srv_control.start_srv('DHCP', 'stopped')

    setup_server_for_config_backend_cmds(backend_type=backend, server_tag="xyz")
    get_address(mac_addr='00:00:00:00:00:04', exp_addr='192.168.51.5')

    # we still want just one network with one subnet but different subnet, from xyz
    xyz = _get_server_config()
    assert len(xyz["arguments"]["Dhcp4"]["shared-networks"]) == 1
    assert len(xyz["arguments"]["Dhcp4"]["shared-networks"][0]["subnet4"]) == 1
    assert xyz["arguments"]["Dhcp4"]["shared-networks"][0]["subnet4"][0]["subnet"] == "192.168.51.0/24"

    cfg.add_subnet(backend=backend, shared_network_name="flor2", server_tags=["all"],
                   subnet="192.168.52.0/24", id=3, pools=[{'pool': "192.168.52.5-192.168.52.5"}])

    # model was incomplete on previous step so I can't use del_subnet method because it's again
    # forcing checking
    cmd = dict(command="remote-subnet4-del-by-prefix",
               arguments={"remote": {"type": backend},
                          "subnets": [{"subnet": "192.168.51.0/24"}]})
    srv_msg.send_ctrl_cmd(cmd, exp_result=0)

    xyz = _get_server_config(reload_kea=True)
    assert len(xyz["arguments"]["Dhcp4"]["shared-networks"][0]["subnet4"]) == 1
    assert xyz["arguments"]["Dhcp4"]["shared-networks"][0]["subnet4"][0]["subnet"] == "192.168.52.0/24"

    # this time we expect address from "all"
    get_address(mac_addr='00:00:00:00:00:05', exp_addr='192.168.52.5')


@pytest.mark.parametrize('backend', ['mysql', 'postgresql'])
def test_server_tag_global_parameter4(backend):
    cfg = setup_server_for_config_backend_cmds(backend_type=backend, server_tag="abc")
    _set_server_tag(backend, "xyz")
    _set_server_tag(backend, "abc")

    cfg.add_subnet(backend=backend, server_tags=["abc"], subnet="192.168.50.0/24", id=1,
                   pools=[{'pool': "192.168.50.1-192.168.50.100"}])

    cfg.set_global_parameter(backend=backend, server_tags=["all"], boot_file_name="/dev/null_all")
    get_address(exp_boot_file_name="/dev/null_all")
    xyz = _get_server_config()
    assert xyz["arguments"]["Dhcp4"]["boot-file-name"] == "/dev/null_all"

    cfg.set_global_parameter(backend=backend, server_tags=["xyz"], boot_file_name="/dev/null_xyz")
    get_address(exp_boot_file_name="/dev/null_all")

    xyz = _get_server_config()
    assert xyz["arguments"]["Dhcp4"]["boot-file-name"] == "/dev/null_all"

    # now despite the fact that there still is "all" tag in db, we should have "abc"
    cfg.set_global_parameter(backend=backend, server_tags=["abc"], boot_file_name="/dev/null_abc")
    get_address(exp_boot_file_name="/dev/null_abc")

    xyz = _get_server_config()
    assert xyz["arguments"]["Dhcp4"]["boot-file-name"] == "/dev/null_abc"

    srv_control.start_srv('DHCP', 'stopped')
    cfg = setup_server_for_config_backend_cmds(backend_type=backend, server_tag="xyz")

    cfg.add_subnet(backend=backend, server_tags=["xyz"], subnet="192.168.52.0/24", id=3,
                   pools=[{'pool': "192.168.52.1-192.168.52.100"}])

    # new servers should start with "xyz"
    xyz = _get_server_config(reload_kea=True)
    assert xyz["arguments"]["Dhcp4"]["boot-file-name"] == "/dev/null_xyz"
    get_address(exp_boot_file_name="/dev/null_xyz")


def _set_global_map_parameter(backend, tag, parameter, value):
    cmd = dict(command="remote-global-parameter4-set",
               arguments={"remote": {"type": backend},
                          "server-tags": [tag],
                          "parameters": {
                              parameter: value,
               }})
    response = srv_msg.send_ctrl_cmd(cmd)
    # request config reloading
    cmd = {"command": "config-backend-pull", "arguments": {}}
    reload = srv_msg.send_ctrl_cmd(cmd)
    assert reload == {'result': 0, 'text': 'On demand configuration update successful.'}
    return response


@pytest.mark.parametrize('backend', ['mysql', 'postgresql'])
def test_server_tag_global_map4(backend):
    cfg = setup_server_for_config_backend_cmds(server_tag="abc", backend_type=backend)
    _set_server_tag(backend, "xyz")
    _set_server_tag(backend, "abc")

    cfg.add_subnet(backend=backend, server_tags=["abc"], subnet="192.168.50.0/24", id=1,
                   pools=[{'pool': "192.168.50.1-192.168.50.100"}])
    _set_global_map_parameter(backend, "abc", "expired-leases-processing.reclaim-timer-wait-time", 345)

    # this update should not change anything
    _set_global_map_parameter(backend, "xyz", "expired-leases-processing.reclaim-timer-wait-time", 999)
    xyz = _get_server_config()
    assert xyz["arguments"]["Dhcp4"]["expired-leases-processing"]["reclaim-timer-wait-time"] == 345

    # this should overwrite "all"
    _set_global_map_parameter(backend, "abc", "expired-leases-processing.reclaim-timer-wait-time", 655)
    xyz = _get_server_config()
    assert xyz["arguments"]["Dhcp4"]["expired-leases-processing"]["reclaim-timer-wait-time"] == 655

    srv_control.start_srv('DHCP', 'stopped')
    cfg = setup_server_for_config_backend_cmds(server_tag="xyz", backend_type=backend)

    cfg.add_subnet(backend=backend, server_tags=["xyz"], subnet="192.168.52.0/24", id=3,
                   pools=[{'pool': "192.168.52.1-192.168.52.100"}])

    # now server "xyz" has two parameters configured, should use "xyz"
    xyz = _get_server_config()
    assert xyz["arguments"]["Dhcp4"]["expired-leases-processing"]["reclaim-timer-wait-time"] == 999


@pytest.mark.parametrize('backend', ['mysql', 'postgresql'])
def test_server_tag_kea_without_tag(backend):
    # create first configuration, kea has no assigned tag, so it should get config just from "all"
    cfg = setup_server_for_config_backend_cmds(backend_type=backend, server_tag="")
    _set_server_tag(backend, "abc")

    cfg.add_subnet(backend=backend, server_tags=["abc"], subnet="192.168.52.0/24", id=1,
                   pools=[{'pool': "192.168.52.1-192.168.52.100"}])
    get_rejected()
    xyz = _get_server_config()
    # check that we don't have anything configured except default value
    assert len(xyz["arguments"]["Dhcp4"]["subnet4"]) == 0
    assert len(xyz["arguments"]["Dhcp4"]["shared-networks"]) == 0
    assert xyz["arguments"]["Dhcp4"]["boot-file-name"] == ""
    assert len(xyz["arguments"]["Dhcp4"]["option-data"]) == 0

    # set network, subnet, option and parameter for "all"
    cfg.add_network(backend=backend, server_tags=["all"], name="flor1")
    cfg.add_subnet(backend=backend, server_tags=["all"], shared_network_name="flor1",
                   subnet="192.168.50.0/24", id=2,
                   pools=[{'pool': "192.168.50.1-192.168.50.100"}])
    cfg.set_global_parameter(backend=backend, server_tags=["all"], valid_lifetime=7700)
    cfg.set_global_parameter(backend=backend, server_tags=["all"], boot_file_name="/dev/null_all")
    cfg.add_option(backend=backend, server_tags=["all"], code=3, csv_format=True, data="10.0.0.1", name="routers",
                   space="dhcp4")

    xyz = _get_server_config()
    assert len(xyz["arguments"]["Dhcp4"]["subnet4"]) == 0
    assert len(xyz["arguments"]["Dhcp4"]["shared-networks"]) == 1
    assert len(xyz["arguments"]["Dhcp4"]["shared-networks"][0]["subnet4"]) == 1
    assert xyz["arguments"]["Dhcp4"]["boot-file-name"] == "/dev/null_all"
    assert len(xyz["arguments"]["Dhcp4"]["option-data"]) == 1

    get_address(mac_addr='00:00:00:00:00:06', exp_boot_file_name="/dev/null_all",
                req_opts=[3], exp_option={"code": 3, "data": "10.0.0.1"})
