import pytest

import srv_msg
import srv_control
import misc

from forge_cfg import world


@pytest.mark.v4
@pytest.mark.bootp
def test_bootp():
    misc.test_setup()
    srv_control.config_srv_subnet('192.168.50.0/24', '192.168.50.1-192.168.50.1')
    srv_control.new_pool('192.168.50.10-192.168.50.10', 0)
    srv_control.add_hooks('libdhcp_bootp.so')

    world.dhcp_cfg["subnet4"][0]["pools"][0]["client-class"] = "BOOTP"
    world.dhcp_cfg["subnet4"][0]["pools"][1]["client-class"] = "DHCP"
    srv_control.create_new_class('DHCP')
    srv_control.add_test_to_class(1, 'test', "not member('BOOTP')")
    srv_control.build_and_send_config_files()
    srv_control.start_srv('DHCP', 'started')

    misc.test_procedure()
    srv_msg.client_send_msg('DISCOVER')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', 'OFFER')
    srv_msg.response_check_content('yiaddr', '192.168.50.10')

    misc.test_procedure()
    srv_msg.client_send_msg('BOOTP_REQUEST')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', 'BOOTP_REPLY')
    srv_msg.response_check_include_option(53, expect_include=False)
    srv_msg.response_check_include_option(58, expect_include=False)
    srv_msg.response_check_include_option(59, expect_include=False)
    srv_msg.response_check_content('yiaddr', '192.168.50.1')
