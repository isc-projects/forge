"""billing class"""

# pylint: disable=invalid-name,line-too-long

import pytest
from src import misc
from src import srv_control
from src import srv_msg

from src.softwaresupport.isc_dhcp6_server.functions import build_log_path, add_line_in_global


@pytest.mark.v4
@pytest.mark.dhcpd
def test_v4_dhcpd_billing_class_limit():
    """new-v4.dhcpd.billing_class_limit"""

    misc.test_setup()
    add_line_in_global(' ping-check off;')
    add_line_in_global(' ddns-updates off;')
    add_line_in_global(' max-lease-time 50;')
    add_line_in_global(' default-lease-time 50;')
    add_line_in_global(' subnet 192.168.50.0 netmask 255.255.255.0 {')
    add_line_in_global('     authoritative;')
    add_line_in_global('     pool {')
    add_line_in_global('         range 192.168.50.100 192.168.50.101;')
    add_line_in_global('     }')
    add_line_in_global(' }')
    add_line_in_global(' class "vnd1001" {')
    add_line_in_global('     match if (option vendor-class-identifier = "vnd1001");')
    add_line_in_global('     lease limit 1;')
    add_line_in_global(' }')

    add_line_in_global(' class "vendor-classes"')
    add_line_in_global(' {')
    add_line_in_global('     match option vendor-class-identifier;')
    add_line_in_global(' }')

    add_line_in_global(' subclass "vendor-classes" "4491" {')
    add_line_in_global('     vendor-option-space vendor-4491;')
    add_line_in_global('     lease limit 1;')
    add_line_in_global(' }')

    srv_control.build_and_send_config_files()
    srv_control.start_srv('DHCP', 'started')

    misc.test_procedure()
    srv_msg.forge_sleep(1, 'seconds')
    # Client sets chaddr value to 00:00:00:00:00:11.
    srv_msg.client_does_include_with_value('client_id', '72656331323334')
    srv_msg.client_does_include_with_value('vendor_class_id', 'vnd1001')
    srv_msg.client_send_msg('DISCOVER')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', 'OFFER')
    srv_msg.response_check_content('yiaddr', '192.168.50.100')

    misc.test_procedure()
    srv_msg.client_does_include_with_value('client_id', '72656331323334')
    srv_msg.client_does_include_with_value('vendor_class_id', 'vnd1001')
    srv_msg.client_copy_option('server_id')
    srv_msg.client_does_include_with_value('requested_addr', '192.168.50.100')
    srv_msg.client_send_msg('REQUEST')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', 'ACK')
    srv_msg.response_check_content('yiaddr', '192.168.50.100')

    misc.test_procedure()
    srv_msg.forge_sleep(1, 'seconds')
    # Client sets chaddr value to 00:00:00:00:00:22.
    srv_msg.client_does_include_with_value('client_id', '72656331323335')
    srv_msg.client_does_include_with_value('vendor_class_id', 'vnd1001')
    srv_msg.client_send_msg('DISCOVER')

    misc.pass_criteria()
    srv_msg.send_dont_wait_for_message()
    srv_msg.wait_for_message_in_log('no available billing: lease limit reached in all matching classes (last: \'vnd1001\')',
                                    count=1, log_file=build_log_path())
