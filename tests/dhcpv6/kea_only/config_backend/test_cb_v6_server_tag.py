"""Kea config backend testing server-tag."""

import pytest
import srv_control
import srv_msg

from dhcp4_scen import get_address, get_rejected
from cb_model import setup_server_for_config_backend_cmds
from forge_cfg import world

pytestmark = [pytest.mark.kea_only,
              pytest.mark.hook,
              pytest.mark.v6,
              pytest.mark.config_backend]


@pytest.fixture(autouse=True)
def run_around_each_test(request):
    world.check_on_reload = False

    def unset():
        world.check_on_reload = True

    request.addfinalizer(unset)


def _set_server_tag(tag="abc"):
    cmd = dict(command="remote-server6-set", arguments={"remote": {"type": "mysql"},
                                                        "servers": [{"server-tag": tag}]})
    return srv_msg.send_ctrl_cmd(cmd, exp_result=0)


def _get_server_config(reload_kea=False):
    if reload_kea:
        cmd = dict(command="config-reload", arguments={})
        srv_msg.send_ctrl_cmd(cmd, exp_result=0)
    cmd = dict(command="config-get", arguments={})
    return srv_msg.send_ctrl_cmd(cmd, exp_result=0)


def test_server_tag_subnet():
    # create first configuration
    cfg_xyz = setup_server_for_config_backend_cmds(server_tag="xyz")
    _set_server_tag("xyz")
    _set_server_tag("abc")
    get_rejected()
    # add configuration for abc, don't check reconfigure result
    cfg_xyz.add_subnet(server_tags=["abc"], subnet="2001:db8:1::/64", id=1,
                       pools=[{'pool': "2001:db8:1::1/128"}])

    get_rejected()

    # unassigned is not supported yet
    # cfg_xyz.add_subnet(server_tags=["unassigned"], subnet="2001:db8:1::/64", id=3,
    #                    pools=[{'pool': "2001:db8:1::10-2001:db8:1::10"}])
    #
    # get_rejected()

    # add configuration for xyz
    cfg_xyz.add_subnet(server_tags=["xyz"], subnet="2001:db8:2::/64", id=2,
                       pools=[{'pool': "2001:db8:2::50/128"}])

    get_address(mac_addr='00:00:00:00:00:01', exp_addr='2001:db8:2::50')

    xyz = _get_server_config()
    # check if it's configured with just one subnet
    assert len(xyz["arguments"]["Dhcp6"]["subnet6"]) == 1
    # and this subnet is as expected
    assert xyz["arguments"]["Dhcp6"]["subnet6"][0]["id"] == 2
    assert xyz["arguments"]["Dhcp6"]["subnet6"][0]["subnet"] == "2001:db8:2::/64"

    srv_control.start_srv('DHCP', 'stopped')

    # create second configuration
    setup_server_for_config_backend_cmds(server_tag="abc")

    get_address(mac_addr='00:00:00:00:00:02', exp_addr='2001:db8:1::1')
    abc = _get_server_config()
    # check if it's configured with just one subnet
    assert len(abc["arguments"]["Dhcp6"]["subnet6"]) == 1
    # and this subnet is as expected
    assert abc["arguments"]["Dhcp6"]["subnet6"][0]["id"] == 1
    assert abc["arguments"]["Dhcp6"]["subnet6"][0]["subnet"] == "2001:db8:1::/64"

    srv_control.start_srv('DHCP', 'stopped')

    # create third subnet that will use "all" tag
    cfg_qwe = setup_server_for_config_backend_cmds(server_tag="qwe")

    get_rejected()

    cfg_qwe.add_subnet(server_tags=["all"], subnet="2001:db8:3::/64", id=3,
                       pools=[{'pool': "2001:db8:3::20-2001:db8:3::21"}])

    abc = _get_server_config()
    # check if it's configured with just one subnet
    assert len(abc["arguments"]["Dhcp6"]["subnet6"]) == 1
    # and this subnet is as expected
    assert abc["arguments"]["Dhcp6"]["subnet6"][0]["id"] == 3
    assert abc["arguments"]["Dhcp6"]["subnet6"][0]["subnet"] == "2001:db8:3::/64"

    get_address(mac_addr='00:00:00:00:00:03', exp_addr='2001:db8:3::20')

    srv_control.start_srv('DHCP', 'stopped')
    setup_server_for_config_backend_cmds(server_tag="abc")
    abc = _get_server_config()

    # two subnets without classification on the same interface doesn't make sense so we will just check config
    # check if it's configured with just two subnets, all and abc configured at the beginning of a test
    assert len(abc["arguments"]["Dhcp6"]["subnet6"]) == 2
    # and this subnet is as expected
    assert abc["arguments"]["Dhcp6"]["subnet6"][0]["id"] == 1
    assert abc["arguments"]["Dhcp6"]["subnet6"][1]["id"] == 3
    assert abc["arguments"]["Dhcp6"]["subnet6"][0]["subnet"] == "2001:db8:1::/64"
    assert abc["arguments"]["Dhcp6"]["subnet6"][1]["subnet"] == "2001:db8:3::/64"


def test_server_tag_global_option():
    cfg = setup_server_for_config_backend_cmds(server_tag="abc")
    _set_server_tag("xyz")
    _set_server_tag("abc")
    cfg.add_subnet(server_tags="abc")
    cfg.add_option(server_tags=["all"], code=22, csv_format=True, data="2001::1", name="sip-server-addr", space="dhcp6")

    abc = _get_server_config()
    # server should have just one option now, from "all"
    assert len(abc["arguments"]["Dhcp6"]["option-data"]) == 1
    assert abc["arguments"]["Dhcp6"]["option-data"][0]["data"] == "2001::1"

    get_address(req_opts=[22], exp_option={"code": 22, "data": "2001::1"})

    cfg.add_option(server_tags=["abc"], code=22, csv_format=True, data="2001::2", name="sip-server-addr", space="dhcp6")
    abc = _get_server_config()
    # now, despite the fact that two tags are for server "abc" ("abc" and "all") option "all" should be overwritten
    assert len(abc["arguments"]["Dhcp6"]["option-data"]) == 1
    assert abc["arguments"]["Dhcp6"]["option-data"][0]["data"] == "2001::2"
    get_address(req_opts=[22], exp_option={"code": 22, "data": "2001::2"})

    cfg.add_option(server_tags=["xyz"], code=22, csv_format=True, data="2001::3", name="sip-server-addr", space="dhcp6")
    abc = _get_server_config()
    # after adding "xyz" option, there should not be any change in running kea
    assert len(abc["arguments"]["Dhcp6"]["option-data"]) == 1
    assert abc["arguments"]["Dhcp6"]["option-data"][0]["data"] == "2001::2"
    get_address(req_opts=[22], exp_option={"code": 22, "data": "2001::2"})

    srv_control.start_srv('DHCP', 'stopped')

    cfg_xyz = setup_server_for_config_backend_cmds(server_tag="xyz")
    cfg_xyz.add_subnet(server_tags="xyz")
    abc = _get_server_config()
    # new kea is started with tag "xyz"
    assert len(abc["arguments"]["Dhcp6"]["option-data"]) == 1
    assert abc["arguments"]["Dhcp6"]["option-data"][0]["data"] == "2001::3"

    get_address(req_opts=[22], exp_option={"code": 22, "data": "2001::3"})

    # delete option with tag "xyz", kea should download tag "all"
    cfg_xyz.del_option(server_tags=["xyz"], code=22)
    xyz = _get_server_config()
    assert len(xyz["arguments"]["Dhcp6"]["option-data"]) == 1
    assert xyz["arguments"]["Dhcp6"]["option-data"][0]["data"] == "2001::1"
    get_address(req_opts=[22], exp_option={"code": 22, "data": "2001::1"})


def test_server_tag_network():
    cfg = setup_server_for_config_backend_cmds(server_tag="abc")
    _set_server_tag("xyz")
    _set_server_tag("abc")
    cfg.add_network(server_tags=["abc"], name="flor1")

    cfg.add_subnet(shared_network_name="flor1", server_tags=["abc"],
                   subnet="2001:db8:1::/64", id=1, pools=[{'pool': "2001:db8:1::1-2001:db8:1::1"}])

    xyz = _get_server_config()
    assert len(xyz["arguments"]["Dhcp6"]["shared-networks"][0]["subnet6"]) == 1
    assert xyz["arguments"]["Dhcp6"]["shared-networks"][0]["subnet6"][0]["subnet"] == "2001:db8:1::/64"

    get_address(mac_addr='00:00:00:00:00:03', exp_addr='2001:db8:1::1')

    cfg.add_network(server_tags=["xyz"], name="flor2")

    cfg.add_subnet(shared_network_name="flor2", server_tags=["xyz"],
                   subnet="2001:db8:2::/64", id=2, pools=[{'pool': "2001:db8:2::5-2001:db8:2::5"}])

    # we still want just one network with one subnet
    xyz = _get_server_config()
    assert len(xyz["arguments"]["Dhcp6"]["shared-networks"]) == 1
    assert len(xyz["arguments"]["Dhcp6"]["shared-networks"][0]["subnet6"]) == 1
    assert xyz["arguments"]["Dhcp6"]["shared-networks"][0]["subnet6"][0]["subnet"] == "2001:db8:1::/64"

    get_rejected(mac_addr='00:00:00:00:00:10')
    srv_control.start_srv('DHCP', 'stopped')

    setup_server_for_config_backend_cmds(server_tag="xyz")
    get_address(mac_addr='00:00:00:00:00:04', exp_addr='2001:db8:2::5')

    # we still want just one network with one subnet but different subnet, from xyz
    xyz = _get_server_config()
    assert len(xyz["arguments"]["Dhcp6"]["shared-networks"]) == 1
    assert len(xyz["arguments"]["Dhcp6"]["shared-networks"][0]["subnet6"]) == 1
    assert xyz["arguments"]["Dhcp6"]["shared-networks"][0]["subnet6"][0]["subnet"] == "2001:db8:2::/64"

    cfg.add_subnet(shared_network_name="flor2", server_tags=["all"],
                   subnet="2001:db8:3::/64", id=3, pools=[{'pool': "2001:db8:3::5-2001:db8:3::5"}])

    # model was incomplete on previous step so I can't use del_subnet method because it's again
    # forcing checking
    cmd = dict(command="remote-subnet6-del-by-prefix",
               arguments={"remote": {"type": "mysql"},
                          "subnets": [{"subnet": "2001:db8:2::/64"}]})
    srv_msg.send_ctrl_cmd(cmd, exp_result=0)

    xyz = _get_server_config(reload_kea=True)
    assert len(xyz["arguments"]["Dhcp6"]["shared-networks"][0]["subnet6"]) == 1
    assert xyz["arguments"]["Dhcp6"]["shared-networks"][0]["subnet6"][0]["subnet"] == "2001:db8:3::/64"

    # this time we expect address from "all"
    get_address(mac_addr='00:00:00:00:00:05', exp_addr='2001:db8:3::5')


def test_server_tag_global_parameter():
    cfg = setup_server_for_config_backend_cmds(server_tag="abc")
    _set_server_tag("xyz")
    _set_server_tag("abc")

    cfg.add_subnet(server_tags=["abc"], subnet="2001:db8:1::/64", id=1,
                   pools=[{'pool': "2001:db8:1::1-2001:db8:1::100"}])
    cfg.set_global_parameter(server_tags=["all"], valid_lifetime=7700)
    get_address(mac_addr='00:00:00:00:00:03', exp_ia_na_iaaddr_validlft=7700)

    # this update should not change anything
    cfg.set_global_parameter(server_tags=["xyz"], valid_lifetime=5001)
    xyz = _get_server_config()
    assert xyz["arguments"]["Dhcp6"]["valid-lifetime"] == 7700
    get_address(mac_addr='00:00:00:00:00:04', exp_ia_na_iaaddr_validlft=7700)

    # this should overwrite "all"
    cfg.set_global_parameter(server_tags=["abc"], valid_lifetime=5002)
    xyz = _get_server_config()
    assert xyz["arguments"]["Dhcp6"]["valid-lifetime"] == 5002

    get_address(mac_addr='00:00:00:00:00:05', exp_ia_na_iaaddr_validlft=5002)
    srv_control.start_srv('DHCP', 'stopped')
    cfg = setup_server_for_config_backend_cmds(server_tag="xyz")

    cfg.add_subnet(server_tags=["xyz"], subnet="2001:db8:1::/64", id=1,
                   pools=[{'pool': "2001:db8:1::1-2001:db8:1::100"}])

    # now server "xyz" has two parameters configured, should use "xyz"
    xyz = _get_server_config()
    assert xyz["arguments"]["Dhcp6"]["valid-lifetime"] == 5001
    get_address(mac_addr='00:00:00:00:00:06', exp_ia_na_iaaddr_validlft=5001)


def test_server_tag_kea_without_tag():
    # create first configuration, kea has no assigned tag, so it should get config just from "all"
    cfg = setup_server_for_config_backend_cmds(server_tag="")
    _set_server_tag("abc")

    cfg.add_subnet(server_tags=["abc"], subnet="2001:db8:1::/64", id=1,
                   pools=[{'pool': "2001:db8:1::1-2001:db8:1::100"}])
    get_rejected()
    xyz = _get_server_config()
    # check that we don't have anything configured except default value
    assert len(xyz["arguments"]["Dhcp6"]["subnet6"]) == 0
    assert len(xyz["arguments"]["Dhcp6"]["shared-networks"]) == 0
    assert xyz["arguments"]["Dhcp6"]["valid-lifetime"] == 7200
    assert len(xyz["arguments"]["Dhcp6"]["option-data"]) == 0

    # set network, subnet, option and parameter for "all"
    cfg.add_network(server_tags=["all"], name="flor1")
    cfg.add_subnet(server_tags=["all"], shared_network_name="flor1",
                   subnet="2001:db8:2::/64", id=2,
                   pools=[{'pool': "2001:db8:2::1-2001:db8:2::100"}])
    cfg.set_global_parameter(server_tags=["all"], valid_lifetime=7700)
    cfg.add_option(server_tags=["all"], code=22, csv_format=True, data="2001::1", name="sip-server-addr", space="dhcp6")

    xyz = _get_server_config()
    assert len(xyz["arguments"]["Dhcp6"]["subnet6"]) == 0
    assert len(xyz["arguments"]["Dhcp6"]["shared-networks"]) == 1
    assert len(xyz["arguments"]["Dhcp6"]["shared-networks"][0]["subnet6"]) == 1
    assert xyz["arguments"]["Dhcp6"]["valid-lifetime"] == 7700
    assert len(xyz["arguments"]["Dhcp6"]["option-data"]) == 1

    get_address(mac_addr='00:00:00:00:00:06', exp_ia_na_iaaddr_validlft=7700,
                req_opts=[22], exp_option={"code": 22, "data": "2001::1"})
