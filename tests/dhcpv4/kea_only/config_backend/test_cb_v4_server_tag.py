"""Kea config backend testing server-tag."""

import pytest
import srv_control

from dhcp4_scen import get_address, get_rejected
from cb_model import setup_server_for_config_backend_cmds
from forge_cfg import world

pytestmark = [pytest.mark.kea_only,
              pytest.mark.hook,
              pytest.mark.v4,
              pytest.mark.config_backend]


@pytest.fixture(autouse=True)
def run_around_each_test(request):
    world.check_on_reload = False

    def unset():
        world.check_on_reload = True

    request.addfinalizer(unset)


def test_server_tag_subnet():
    # create first configuration
    cfg_xys = setup_server_for_config_backend_cmds(server_tag="xys")
    get_rejected()
    # add configuration for abc, don't check reconfigure result
    cfg_xys.add_subnet(server_tags=["abc"], subnet="192.168.50.0/24", id=1,
                       pools=[{'pool': "192.168.50.1-192.168.50.1"}])

    get_rejected()

    cfg_xys.add_subnet(server_tags=["unassigned"], subnet="192.168.50.0/24", id=3,
                       pools=[{'pool': "192.168.50.10-192.168.50.10"}])

    get_rejected()

    # add configuration for xys, check result
    cfg_xys.add_subnet(server_tags=["xys"], subnet="192.168.50.0/24", id=2,
                       pools=[{'pool': "192.168.50.50-192.168.50.50"}])

    get_address(mac_addr='00:00:00:00:00:01', exp_addr='192.168.50.50')

    srv_control.start_srv('DHCP', 'stopped')

    # create second configuration
    setup_server_for_config_backend_cmds(server_tag="abc")

    get_address(mac_addr='00:00:00:00:00:02', exp_addr='192.168.50.1')

    srv_control.start_srv('DHCP', 'stopped')

    # create third subnet that will use "all" tag
    cfg_qwe = setup_server_for_config_backend_cmds(server_tag=["qwe"])

    get_rejected()

    cfg_qwe.add_subnet(server_tags=["all"], subnet="192.168.50.0/24", id=2,
                       pools=[{'pool': "192.168.50.20-192.168.50.20"}])

    get_address(mac_addr='00:00:00:00:00:03', exp_addr='192.168.50.20')


def test_server_tag_global_option():
    cfg = setup_server_for_config_backend_cmds(server_tag="abc")
    cfg.add_subnet(server_tags=["abc"])

    cfg.add_option(server_tags=["all"], code=10, csv_format=True, data="1.1.1.1", name="impress-servers", space="dhcp4")
    get_address(req_opts=[10], exp_option={"code": 10, "data": "1.1.1.1"})

    cfg.add_option(server_tags=["abc"], code=10, csv_format=True, data="2.2.2.2", name="impress-servers", space="dhcp4")
    get_address(req_opts=[10], exp_option={"code": 10, "data": "2.2.2.2"})

    cfg.add_option(server_tags=["xyz"], code=10, csv_format=True, data="3.3.3.3", name="impress-servers", space="dhcp4")
    get_address(req_opts=[10], exp_option={"code": 10, "data": "2.2.2.2"})

    srv_control.start_srv('DHCP', 'stopped')

    cfg_xyz = setup_server_for_config_backend_cmds(server_tag="xyz")
    cfg_xyz.add_subnet()
    get_address(req_opts=[10], exp_option={"code": 10, "data": "3.3.3.3"})

    cfg_xyz.del_option(server_tags=["xyz"], code=10)
    get_address(req_opts=[10], exp_option={"code": 10, "data": "1.1.1.1"})


def test_server_tag_network_different_tags_in_subnet_and_sharednetwork():
    cfg = setup_server_for_config_backend_cmds(server_tag="abc")
    cfg.add_network(server_tags=["xyz"], name="flor1")

    cfg.add_subnet(shared_network_name="flor1", server_tags=["abc"],
                   subnet="192.168.50.0/24", id=1, pools=[{'pool': "192.168.50.1-192.168.50.1"}])

    get_rejected()


def test_server_tag_network():
    cfg = setup_server_for_config_backend_cmds(server_tag="abc")
    cfg.add_network(server_tags=["abc"], name="flor1")

    cfg.add_subnet(shared_network_name="flor1", server_tags=["abc"],
                   subnet="192.168.50.0/24", id=1, pools=[{'pool': "192.168.50.1-192.168.50.1"}])

    get_address(mac_addr='00:00:00:00:00:03', exp_addr='192.168.50.1')

    cfg.add_network(server_tags=["xyz"], name="flor2")

    cfg.add_subnet(shared_network_name="flor2", server_tags=["xyz"],
                   subnet="192.168.50.0/24", id=1, pools=[{'pool': "192.168.50.5-192.168.50.5"}])

    get_rejected()
    srv_control.start_srv('DHCP', 'stopped')

    setup_server_for_config_backend_cmds(server_tag="xyz")
    get_address(mac_addr='00:00:00:00:00:03', exp_addr='192.168.50.5')


def test_server_tag_global_parameter():
    cfg = setup_server_for_config_backend_cmds(server_tag="aaa")

    cfg.add_subnet(server_tags=["abc"], subnet="192.168.50.0/24", id=1,
                   pools=[{'pool': "192.168.50.1-192.168.50.100"}])

    cfg.set_global_parameter(server_tags=["unassigned"], boot_file_name="/dev/null_un")
    get_address(no_exp_boot_file_name="/dev/null_un")
    cfg.set_global_parameter(server_tags=["xyz"], boot_file_name="/dev/null_xyz")
    cfg.set_global_parameter(server_tags=["all"], boot_file_name="/dev/null_all")

    get_address(exp_boot_file_name="/dev/null_all")
    get_address(no_exp_boot_file_name="/dev/null_xyz")
    get_address(no_exp_boot_file_name="/dev/null_un")

    srv_control.start_srv('DHCP', 'stopped')
    cfg = setup_server_for_config_backend_cmds(server_tag="xyz")

    cfg.add_subnet(server_tags=["abc"], subnet="192.168.50.0/24", id=1,
                   pools=[{'pool': "192.168.50.1-192.168.50.100"}])

    get_address(exp_boot_file_name="/dev/null_xyz")
