"""Kea config backend testing server-tag."""

import pytest
import srv_control

from dhcp4_scen import get_address, get_rejected
from cb_model import setup_server_for_config_backend_cmds

pytestmark = [pytest.mark.kea_only,
              pytest.mark.hook,
              pytest.mark.v6,
              pytest.mark.config_backend]


def test_server_tag_subnet():
    # create first configuration
    cfg_xys = setup_server_for_config_backend_cmds(server_tag="xys")

    get_rejected()
    # add configuration for abc, don't check reconfigure result
    cfg_xys.add_subnet(check_on_reload=False,
                       server_tags=["abc"], subnet="2001:db8:1::/64", id=1,
                       pools=[{'pool': "2001:db8:1::1-2001:db8:1::1"}])

    get_rejected()

    cfg_xys.add_subnet(check_on_reload=False,
                       server_tags=["unassigned"], subnet="2001:db8:1::/64", id=3,
                       pools=[{'pool': "2001:db8:1::10-2001:db8:1::10"}])

    get_rejected()

    # add configuration for xys, check result
    cfg_xys.add_subnet(check_on_reload=False,
                       server_tags=["xys"], subnet="2001:db8:1::/64", id=2,
                       pools=[{'pool': "2001:db8:1::50-2001:db8:1::50"}])

    get_address(mac_addr='00:00:00:00:00:01', exp_addr='2001:db8:1::50')

    srv_control.start_srv('DHCP', 'stopped')

    # create second configuration
    setup_server_for_config_backend_cmds(server_tag="abc")

    get_address(mac_addr='00:00:00:00:00:02', exp_addr='2001:db8:1::1')

    srv_control.start_srv('DHCP', 'stopped')

    # create third subnet that will use "all" tag
    cfg_qwe = setup_server_for_config_backend_cmds(server_tag=["qwe"])

    get_rejected()

    cfg_qwe.add_subnet(check_on_reload=False,
                       server_tags=["all"], subnet="2001:db8:1::/64", id=2,
                       pools=[{'pool': "2001:db8:1::20-2001:db8:1::20"}])

    get_address(mac_addr='00:00:00:00:00:03', exp_addr='2001:db8:1::20')


def test_server_tag_global_option():
    cfg = setup_server_for_config_backend_cmds(server_tag="abc")
    cfg.add_subnet(check_on_reload=False)

    cfg.add_option(check_on_reload=False,
                   server_tags=["all"], code=22, csv_format=True, data="2001::1", name="sip-server-addr", space="dhcp6")
    get_address(req_opts=[10], exp_option={"code": 22, "data": "2001::1"})

    cfg.add_option(check_on_reload=False,
                   server_tags=["abc"], code=22, csv_format=True, data="2001::2", name="sip-server-addr", space="dhcp6")
    get_address(req_opts=[10], exp_option={"code": 22, "data": "2001::2"})

    cfg.add_option(check_on_reload=False,
                   server_tags=["xyz"], code=22, csv_format=True, data="2001::3", name="sip-server-addr", space="dhcp6")
    get_address(req_opts=[10], exp_option={"code": 22, "data": "2001::2"})

    srv_control.start_srv('DHCP', 'stopped')

    cfg_xyz = setup_server_for_config_backend_cmds(server_tag="xyz")
    cfg_xyz.add_subnet(check_on_reload=False)
    get_address(req_opts=[10], exp_option={"code": 22, "data": "2001::3"})

    cfg_xyz.del_option(check_on_reload=False, server_tags=["xyz"], code=22)
    get_address(req_opts=[10], exp_option={"code": 22, "data": "2001::1"})


def test_server_tag_network_different_tags_in_subnet_and_sharednetwork():
    cfg = setup_server_for_config_backend_cmds(server_tag="abc")

    cfg.add_network(check_on_reload=False, server_tags=["xyz"], name="flor1")

    cfg.add_subnet(check_on_reload=False,
                   shared_network_name="flor1", server_tags=["abc"],
                   subnet="2001:db8:1::/64", id=1, pools=[{'pool': "2001:db8:1::1-2001:db8:1::1"}])

    get_rejected()


def test_server_tag_network():
    cfg = setup_server_for_config_backend_cmds(server_tag="abc")

    cfg.add_network(check_on_reload=False, server_tags=["abc"], name="flor1")

    cfg.add_subnet(check_on_reload=False,
                   shared_network_name="flor1", server_tags=["abc"],
                   subnet="2001:db8:1::/64", id=1, pools=[{'pool': "2001:db8:1::1-2001:db8:1::1"}])

    get_address(mac_addr='00:00:00:00:00:03', exp_addr='2001:db8:1::1')

    cfg.add_network(check_on_reload=False, server_tags=["xyz"], name="flor2")

    cfg.add_subnet(check_on_reload=False,
                   shared_network_name="flor2", server_tags=["xyz"],
                   subnet="2001:db8:1::/64", id=1, pools=[{'pool': "2001:db8:1::5-2001:db8:1::5"}])

    get_rejected()
    srv_control.start_srv('DHCP', 'stopped')

    setup_server_for_config_backend_cmds(server_tag="xyz")
    get_address(mac_addr='00:00:00:00:00:03', exp_addr='2001:db8:1::5')


def test_server_tag_global_parameter():
    cfg = setup_server_for_config_backend_cmds(server_tag="aaa")

    cfg.add_subnet(check_on_reload=False,
                   server_tags=["abc"], subnet="2001:db8:1::/64", id=1,
                   pools=[{'pool': "2001:db8:1::1-2001:db8:1::100"}])

    cfg.set_global_parameter(check_on_reload=False, server_tags=["unassigned"], valid_lifetime=5000)
    get_address(exp_ia_na_iaaddr_validlft=7200)
    cfg.set_global_parameter(check_on_reload=False, server_tags=["xyz"], valid_lifetime=5001)
    cfg.set_global_parameter(check_on_reload=False, server_tags=["all"], valid_lifetime=5002)
    get_address(exp_ia_na_iaaddr_validlft=5002)

    srv_control.start_srv('DHCP', 'stopped')
    cfg = setup_server_for_config_backend_cmds(server_tag="xyz")

    cfg.add_subnet(check_on_reload=False,
                   server_tags=["abc"], subnet="2001:db8:1::/64", id=1,
                   pools=[{'pool': "2001:db8:1::1-2001:db8:1::100"}])

    get_address(exp_ia_na_iaaddr_validlft=5001)
