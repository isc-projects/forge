"""billing class"""


import sys
if 'features' not in sys.path:
    sys.path.append('features')

if 'pytest' in sys.argv[0]:
    import pytest
else:
    import lettuce as pytest

import misc
import srv_control
import srv_msg


@pytest.mark.py_test
@pytest.mark.v4
@pytest.mark.dhcpd
@pytest.mark.keyword
def test_v4_dhcpd_billing_class_limit(step):
    """new-v4.dhcpd.billing_class_limit"""

    misc.test_setup(step)
    srv_control.run_command(step, ' ping-check off;')
    srv_control.run_command(step, ' ddns-updates off;')
    srv_control.run_command(step, ' max-lease-time 50;')
    srv_control.run_command(step, ' default-lease-time 50;')
    srv_control.run_command(step, ' subnet 192.168.50.0 netmask 255.255.255.0 {')
    srv_control.run_command(step, '     authoritative;')
    srv_control.run_command(step, '     pool {')
    srv_control.run_command(step, '         range 192.168.50.100 192.168.50.101;')
    srv_control.run_command(step, '     }')
    srv_control.run_command(step, ' }')
    srv_control.run_command(step, ' class "vnd1001" {')
    srv_control.run_command(step, '     match if (option vendor-class-identifier = "vnd1001");')
    srv_control.run_command(step, '     lease limit 1;')
    srv_control.run_command(step, ' }')

    srv_control.run_command(step, ' class "vendor-classes"')
    srv_control.run_command(step, ' {')
    srv_control.run_command(step, '     match option vendor-class-identifier;')
    srv_control.run_command(step, ' }')

    srv_control.run_command(step, ' subclass "vendor-classes" "4491" {')
    srv_control.run_command(step, '     vendor-option-space vendor-4491;')
    srv_control.run_command(step, '     lease limit 1;')
    srv_control.run_command(step, ' }')

    srv_control.build_and_send_config_files(step, 'SSH', 'config-file')
    srv_control.start_srv(step, 'DHCP', 'started')


    misc.test_procedure(step)
    srv_msg.forge_sleep(step, '1', 'seconds')
    # Client sets chaddr value to 00:00:00:00:00:11.
    srv_msg.client_does_include_with_value(step, 'client_id', '72656331323334')
    srv_msg.client_does_include_with_value(step, 'vendor_class_id', 'vnd1001')
    srv_msg.client_send_msg(step, 'DISCOVER')

    misc.pass_criteria(step)
    srv_msg.send_wait_for_message(step, 'MUST', None, 'OFFER')
    srv_msg.response_check_content(step, 'Response', None, 'yiaddr', '192.168.50.100')

    misc.test_procedure(step)
    srv_msg.client_does_include_with_value(step, 'client_id', '72656331323334')
    srv_msg.client_does_include_with_value(step, 'vendor_class_id', 'vnd1001')
    srv_msg.client_copy_option(step, 'server_id')
    srv_msg.client_does_include_with_value(step, 'requested_addr', '192.168.50.100')
    srv_msg.client_send_msg(step, 'REQUEST')

    misc.pass_criteria(step)
    srv_msg.send_wait_for_message(step, 'MUST', None, 'ACK')
    srv_msg.response_check_content(step, 'Response', None, 'yiaddr', '192.168.50.100')



    misc.test_procedure(step)
    srv_msg.forge_sleep(step, '1', 'seconds')
    # Client sets chaddr value to 00:00:00:00:00:22.
    srv_msg.client_does_include_with_value(step, 'client_id', '72656331323335')
    srv_msg.client_does_include_with_value(step, 'vendor_class_id', 'vnd1001')
    srv_msg.client_send_msg(step, 'DISCOVER')

    misc.pass_criteria(step)
    srv_msg.send_dont_wait_for_message(step)
    srv_msg.log_includes_count(step,
                               'DHCP',
                               '1',
                               'no available billing: lease limit reached in all matching classes (last: \'vnd1001\')')


