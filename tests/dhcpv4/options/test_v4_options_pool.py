# """ DHCPv4 options defined on pool level """

# pylint: disable=invalid-name,line-too-long

import pytest

import srv_msg
import references
import srv_control
import misc


from forge_cfg import world


def _get_lease(mac, routers, address):
    misc.test_procedure()
    srv_msg.client_sets_value('Client', 'chaddr', mac)
    srv_msg.client_send_msg('DISCOVER')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', 'OFFER')
    srv_msg.response_check_content('yiaddr', address)

    misc.test_procedure()
    srv_msg.client_sets_value('Client', 'chaddr', mac)
    srv_msg.client_copy_option('server_id')
    srv_msg.client_does_include_with_value('requested_addr', address)
    srv_msg.client_requests_option(3)
    srv_msg.client_send_msg('REQUEST')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', 'ACK')
    srv_msg.response_check_content('yiaddr', address)
    srv_msg.response_check_include_option(3)
    srv_msg.response_check_option_content(3, 'value', routers)


@pytest.mark.v4
@pytest.mark.options
@pytest.mark.preference
def test_v4_options_pool_level():
    misc.test_setup()
    srv_control.config_srv_subnet("172.16.0.0/16", "172.16.0.20-172.16.0.20")
    srv_control.new_pool("172.16.0.50-172.16.0.50", 0)
    srv_control.config_srv_opt('routers', '100.100.100.10')

    option = {"data": "172.17.0.1", "name": "routers"}
    world.dhcp_cfg["subnet4"][0]["pools"][0].update({"option-data": [option]})
    option2 = {"data": "172.170.10.111", "name": "routers"}
    world.dhcp_cfg["subnet4"][0]["pools"][1].update({"option-data": [option2]})

    srv_control.build_and_send_config_files('SSH', 'config-file')
    srv_control.start_srv('DHCP', 'started')

    _get_lease("01:01:01:01:01:01", "172.17.0.1", "172.16.0.20")
    _get_lease("01:01:01:02:02:02", "172.170.10.111", "172.16.0.50")