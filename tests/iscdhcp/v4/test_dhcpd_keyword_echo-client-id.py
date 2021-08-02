"""ISC_DHCP DHCPv4 Keywords"""


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
@pytest.mark.echo_client_id
def test_v4_dhcpd_keyword_echo_client_id_off_offer_ack_nak(step):
    """new-v4.dhcpd.keyword.echo-client-id-off-offer-ack-nak"""
    # # Checks that the default behavior is echo-client-id off and that the
    # # does not echo back a received client-id.
    # #
    # # Message details 		Client		Server
    # # 						DISCOVER -->
    # # 		   						<--	OFFER
    # # 						REQUEST -->
    # # 		   						<--	ACK
    # # 						REQUEST -->
    # # 		   						<--	NAK
    # # Pass Criteria:
    # #
    # # OFFER received without client-id option
    # #
    misc.test_setup(step)
    srv_control.run_command(step, ' ping-check off;')
    srv_control.run_command(step, ' subnet 178.16.1.0 netmask 255.255.255.0 {')
    srv_control.run_command(step, ' authoritative;')
    srv_control.run_command(step, '    range 178.16.1.100 178.16.1.101; }')
    srv_control.build_and_send_config_files(step, 'SSH', 'config-file')
    srv_control.start_srv(step, 'DHCP', 'started')

    misc.test_procedure(step)
    # set client-id to 'rec1234'
    srv_msg.client_does_include_with_value(step, 'client_id', '72656331323334')
    srv_msg.client_send_msg(step, 'DISCOVER')

    misc.pass_criteria(step)
    srv_msg.send_wait_for_message(step, 'MUST', None, 'OFFER')
    srv_msg.response_check_include_option(step, 'Response', None, '1')
    srv_msg.response_check_content(step, 'Response', None, 'yiaddr', '178.16.1.100')
    srv_msg.response_check_option_content(step, 'Response', '1', None, 'value', '255.255.255.0')
    srv_msg.response_check_include_option(step, 'Response', 'NOT ', '61')

    misc.test_procedure(step)
    srv_msg.client_copy_option(step, 'server_id')
    srv_msg.client_does_include_with_value(step, 'requested_addr', '178.16.1.100')
    srv_msg.client_does_include_with_value(step, 'client_id', '72656331323334')
    srv_msg.client_send_msg(step, 'REQUEST')

    misc.pass_criteria(step)
    srv_msg.send_wait_for_message(step, 'MUST', None, 'ACK')
    srv_msg.response_check_content(step, 'Response', None, 'yiaddr', '178.16.1.100')
    srv_msg.response_check_include_option(step, 'Response', 'NOT ', '61')

    misc.test_procedure(step)
    srv_msg.client_copy_option(step, 'server_id')
    srv_msg.client_does_include_with_value(step, 'client_id', '72656331323334')
    # Use an out-of-subnet address to force NAK
    srv_msg.client_does_include_with_value(step, 'requested_addr', '172.16.1.100')
    srv_msg.client_send_msg(step, 'REQUEST')

    misc.pass_criteria(step)
    srv_msg.send_wait_for_message(step, 'MUST', None, 'NAK')
    srv_msg.response_check_include_option(step, 'Response', 'NOT ', '61')



@pytest.mark.py_test
@pytest.mark.v4
@pytest.mark.dhcpd
@pytest.mark.keyword
@pytest.mark.echo_client_id
def test_v4_dhcpd_keyword_echo_client_id_on_offer_ack_nak(step):
    """new-v4.dhcpd.keyword.echo-client-id-on-offer-ack-nak"""
    # # Checks that the when echo-client-id is  enabled the server echoes
    # # back a client-id IF received.
    # #
    # # The following sequence is performed twice, once with the client
    # # sending a client_id and once without:
    # # Message details 		Client		Server
    # # 						DISCOVER -->
    # # 		   						<--	OFFER
    # # 						REQUEST -->
    # # 		   						<--	ACK
    # # 						REQUEST -->
    # # 		   						<--	NAK
    # # Pass Criteria:
    # #
    # # OFFER,ACK and NAK received with client-id option
    # #
    misc.test_setup(step)
    srv_control.run_command(step, ' ping-check off;')
    srv_control.run_command(step, ' echo-client-id on;')
    srv_control.run_command(step, ' subnet 178.16.1.0 netmask 255.255.255.0 {')
    srv_control.run_command(step, ' authoritative;')
    srv_control.run_command(step, '    range 178.16.1.100 178.16.1.101; }')
    srv_control.build_and_send_config_files(step, 'SSH', 'config-file')
    srv_control.start_srv(step, 'DHCP', 'started')

    misc.test_procedure(step)
    # set client-id to 'rec1234'
    srv_msg.client_does_include_with_value(step, 'client_id', '72656331323334')
    srv_msg.client_send_msg(step, 'DISCOVER')

    misc.pass_criteria(step)
    srv_msg.send_wait_for_message(step, 'MUST', None, 'OFFER')
    srv_msg.response_check_include_option(step, 'Response', None, '1')
    srv_msg.response_check_content(step, 'Response', None, 'yiaddr', '178.16.1.100')
    srv_msg.response_check_option_content(step, 'Response', '1', None, 'value', '255.255.255.0')
    srv_msg.response_check_option_content(step, 'Response', '61', None, 'value', '72656331323334')

    misc.test_procedure(step)
    srv_msg.client_copy_option(step, 'server_id')
    srv_msg.client_does_include_with_value(step, 'client_id', '72656331323334')
    srv_msg.client_does_include_with_value(step, 'requested_addr', '178.16.1.100')
    srv_msg.client_send_msg(step, 'REQUEST')

    misc.pass_criteria(step)
    srv_msg.send_wait_for_message(step, 'MUST', None, 'ACK')
    srv_msg.response_check_option_content(step, 'Response', '61', None, 'value', '72656331323334')
    srv_msg.response_check_content(step, 'Response', None, 'yiaddr', '178.16.1.100')

    misc.test_procedure(step)
    srv_msg.client_copy_option(step, 'server_id')
    srv_msg.client_does_include_with_value(step, 'client_id', '72656331323334')
    # Use an out-of-subnet address to force NAK
    srv_msg.client_does_include_with_value(step, 'requested_addr', '172.16.1.100')
    srv_msg.client_send_msg(step, 'REQUEST')

    misc.pass_criteria(step)
    srv_msg.send_wait_for_message(step, 'MUST', None, 'NAK')
    srv_msg.response_check_option_content(step, 'Response', '61', None, 'value', '72656331323334')

    # ##############################################################
    # Repeat the sequence without a client sending an id
    # ##############################################################
    misc.test_procedure(step)
    srv_msg.client_send_msg(step, 'DISCOVER')

    misc.pass_criteria(step)
    srv_msg.send_wait_for_message(step, 'MUST', None, 'OFFER')
    srv_msg.response_check_include_option(step, 'Response', None, '1')
    srv_msg.response_check_content(step, 'Response', None, 'yiaddr', '178.16.1.101')
    srv_msg.response_check_include_option(step, 'Response', 'NOT ', '61')

    misc.test_procedure(step)
    srv_msg.client_copy_option(step, 'server_id')
    srv_msg.client_does_include_with_value(step, 'requested_addr', '178.16.1.101')
    srv_msg.client_send_msg(step, 'REQUEST')

    misc.pass_criteria(step)
    srv_msg.send_wait_for_message(step, 'MUST', None, 'ACK')
    srv_msg.response_check_include_option(step, 'Response', 'NOT ', '61')

    misc.test_procedure(step)
    srv_msg.client_copy_option(step, 'server_id')
    # Use an out-of-subnet address to force NAK
    srv_msg.client_does_include_with_value(step, 'requested_addr', '172.16.1.101')
    srv_msg.client_send_msg(step, 'REQUEST')

    misc.pass_criteria(step)
    srv_msg.send_wait_for_message(step, 'MUST', None, 'NAK')
    srv_msg.response_check_include_option(step, 'Response', 'NOT ', '61')





@pytest.mark.py_test
@pytest.mark.v4
@pytest.mark.dhcpd
@pytest.mark.keyword
@pytest.mark.echo_client_id
def test_v4_dhcpd_keyword_echo_client_id_per_class(step):
    """new-v4.dhcpd.keyword.echo-client-id-per-class"""
    # # Tests the echo-client-id can be specified on class basis.
    # # The following message sequence is performed once for a client
    # # which belongs to class "echo" and once for a client which does not.
    # # In the former, echo-client-id enabled, in the latter it is not:
    # #
    # # Message details 		Client		Server
    # # 						DISCOVER -->
    # # 		   						<--	OFFER
    # # 						REQUEST -->
    # # 		   						<--	ACK
    # # 						REQUEST -->
    # # 		   						<--	NAK
    # # Pass Criteria:
    # #
    # # OFFER,ACK and NAK received with client-id option for first subnet,
    # # not received for the second.
    # #
    misc.test_setup(step)
    srv_control.run_command(step, 'ping-check off;')
    srv_control.run_command(step, 'class "echo" {')
    srv_control.run_command(step, '    match if (substring(option host-name, 0, 4) = "echo");')
    srv_control.run_command(step, '    echo-client-id on;')
    srv_control.run_command(step, '}')
    srv_control.run_command(step, 'class "noecho" {')
    srv_control.run_command(step, '    match if (substring(option host-name, 0, 6) = "noecho");')
    srv_control.run_command(step, '}')
    srv_control.run_command(step, 'subnet 178.16.1.0 netmask 255.255.255.0 {')
    srv_control.run_command(step, '    authoritative;')
    srv_control.run_command(step, '    pool {')
    srv_control.run_command(step, '        range 178.16.1.100 178.16.1.101;')
    srv_control.run_command(step, '    }')
    srv_control.run_command(step, '}')

    # set client-id to 'rec1234'
    srv_msg.client_does_include_with_value(step, 'client_id', '72656331323334')
    srv_msg.client_does_include_with_value(step, 'hostname', 'echo')
    srv_control.build_and_send_config_files(step, 'SSH', 'config-file')
    srv_control.start_srv(step, 'DHCP', 'started')

    misc.test_procedure(step)
    srv_msg.client_send_msg(step, 'DISCOVER')

    misc.pass_criteria(step)
    srv_msg.send_wait_for_message(step, 'MUST', None, 'OFFER')
    srv_msg.response_check_include_option(step, 'Response', None, '1')
    srv_msg.response_check_content(step, 'Response', None, 'yiaddr', '178.16.1.100')
    srv_msg.response_check_option_content(step, 'Response', '1', None, 'value', '255.255.255.0')
    srv_msg.response_check_option_content(step, 'Response', '61', None, 'value', '72656331323334')

    misc.test_procedure(step)
    srv_msg.client_copy_option(step, 'server_id')
    srv_msg.client_does_include_with_value(step, 'hostname', 'echo')
    srv_msg.client_does_include_with_value(step, 'client_id', '72656331323334')
    srv_msg.client_does_include_with_value(step, 'requested_addr', '178.16.1.100')
    srv_msg.client_send_msg(step, 'REQUEST')

    misc.pass_criteria(step)
    srv_msg.send_wait_for_message(step, 'MUST', None, 'ACK')
    srv_msg.response_check_content(step, 'Response', None, 'yiaddr', '178.16.1.100')
    srv_msg.response_check_option_content(step, 'Response', '61', None, 'value', '72656331323334')

    misc.test_procedure(step)
    srv_msg.client_copy_option(step, 'server_id')
    srv_msg.client_does_include_with_value(step, 'hostname', 'echo')
    srv_msg.client_does_include_with_value(step, 'client_id', '72656331323334')
    # Use an out-of-subnet address to force NAK
    srv_msg.client_does_include_with_value(step, 'requested_addr', '172.16.1.100')
    srv_msg.client_send_msg(step, 'REQUEST')

    misc.pass_criteria(step)
    srv_msg.send_wait_for_message(step, 'MUST', None, 'NAK')
    srv_msg.response_check_option_content(step, 'Response', '61', None, 'value', '72656331323334')

    # #########################################################
    # Now test with a client that is NOT in class "echo"
    # #########################################################
    misc.test_procedure(step)
    srv_msg.client_does_include_with_value(step, 'client_id', '72656331323334')
    srv_msg.client_does_include_with_value(step, 'hostname', 'noecho')
    srv_msg.client_send_msg(step, 'DISCOVER')

    misc.pass_criteria(step)
    srv_msg.send_wait_for_message(step, 'MUST', None, 'OFFER')
    srv_msg.response_check_include_option(step, 'Response', None, '1')
    srv_msg.response_check_content(step, 'Response', None, 'yiaddr', '178.16.1.100')
    srv_msg.response_check_option_content(step, 'Response', '1', None, 'value', '255.255.255.0')
    srv_msg.response_check_include_option(step, 'Response', 'NOT ', '61')

    misc.test_procedure(step)
    srv_msg.client_copy_option(step, 'server_id')
    srv_msg.client_does_include_with_value(step, 'hostname', 'noecho')
    srv_msg.client_does_include_with_value(step, 'client_id', '72656331323334')
    srv_msg.client_does_include_with_value(step, 'requested_addr', '178.16.1.100')
    srv_msg.client_send_msg(step, 'REQUEST')

    misc.pass_criteria(step)
    srv_msg.send_wait_for_message(step, 'MUST', None, 'ACK')
    srv_msg.response_check_content(step, 'Response', None, 'yiaddr', '178.16.1.100')
    srv_msg.response_check_include_option(step, 'Response', 'NOT ', '61')

    misc.test_procedure(step)
    srv_msg.client_copy_option(step, 'server_id')
    srv_msg.client_does_include_with_value(step, 'hostname', 'noecho')
    srv_msg.client_does_include_with_value(step, 'client_id', '72656331323334')
    # Use an out-of-subnet address to force NAK
    srv_msg.client_does_include_with_value(step, 'requested_addr', '172.16.1.100')
    srv_msg.client_send_msg(step, 'REQUEST')

    misc.pass_criteria(step)
    srv_msg.send_wait_for_message(step, 'MUST', None, 'NAK')
    srv_msg.response_check_include_option(step, 'Response', 'NOT ', '61')



@pytest.mark.py_test
@pytest.mark.v4
@pytest.mark.dhcpd
@pytest.mark.keyword
@pytest.mark.echo_client_id
def test_v4_dhcpd_keyword_echo_client_id_vs_config_id(step):
    """new-v4.dhcpd.keyword.echo-client-id-vs-config-id"""
    # #
    # # Message details 		Client		Server
    # # 						DISCOVER -->
    # # 		   						<--	OFFER
    # # 						REQUEST -->
    # # 		   						<--	ACK
    # # 						REQUEST -->
    # # 		   						<--	NAK
    # # Pass Criteria:
    # #
    # # OFFER,ACK and NAK received with client-id option
    # #
    misc.test_setup(step)
    srv_control.run_command(step, ' ping-check off;')
    srv_control.run_command(step, ' subnet 178.16.1.0 netmask 255.255.255.0 {')
    srv_control.run_command(step, ' authoritative;')
    srv_control.run_command(step, ' echo-client-id on;')
    srv_control.run_command(step, ' option dhcp-client-identifier "cfg1234";')
    srv_control.run_command(step, '    range 178.16.1.100 178.16.1.101; }')
    srv_control.build_and_send_config_files(step, 'SSH', 'config-file')
    srv_control.start_srv(step, 'DHCP', 'started')

    misc.test_procedure(step)
    # set client-id to 'rec1234'
    srv_msg.client_does_include_with_value(step, 'client_id', '72656331323334')
    srv_msg.client_send_msg(step, 'DISCOVER')

    misc.pass_criteria(step)
    srv_msg.send_wait_for_message(step, 'MUST', None, 'OFFER')
    srv_msg.response_check_include_option(step, 'Response', None, '1')
    srv_msg.response_check_content(step, 'Response', None, 'yiaddr', '178.16.1.100')
    srv_msg.response_check_option_content(step, 'Response', '1', None, 'value', '255.255.255.0')
    srv_msg.response_check_option_content(step, 'Response', '61', None, 'value', '72656331323334')

    misc.test_procedure(step)
    srv_msg.client_copy_option(step, 'server_id')
    srv_msg.client_does_include_with_value(step, 'client_id', '72656331323334')
    srv_msg.client_does_include_with_value(step, 'requested_addr', '178.16.1.100')
    srv_msg.client_send_msg(step, 'REQUEST')

    misc.pass_criteria(step)
    srv_msg.send_wait_for_message(step, 'MUST', None, 'ACK')
    srv_msg.response_check_option_content(step, 'Response', '61', None, 'value', '72656331323334')
    srv_msg.response_check_content(step, 'Response', None, 'yiaddr', '178.16.1.100')

    misc.test_procedure(step)
    srv_msg.client_copy_option(step, 'server_id')
    srv_msg.client_does_include_with_value(step, 'client_id', '72656331323334')
    # Use an out-of-subnet address to force NAK
    srv_msg.client_does_include_with_value(step, 'requested_addr', '172.16.1.100')
    srv_msg.client_send_msg(step, 'REQUEST')

    misc.pass_criteria(step)
    srv_msg.send_wait_for_message(step, 'MUST', None, 'NAK')
    # Received id is available even on NAKs
    srv_msg.response_check_option_content(step, 'Response', '61', None, 'value', '72656331323334')

    # ##############################################################
    # Repeat the sequence without a client sending an id, should
    # get configured id
    # ##############################################################
    misc.test_procedure(step)
    srv_msg.client_send_msg(step, 'DISCOVER')

    misc.pass_criteria(step)
    srv_msg.send_wait_for_message(step, 'MUST', None, 'OFFER')
    srv_msg.response_check_include_option(step, 'Response', None, '1')
    srv_msg.response_check_content(step, 'Response', None, 'yiaddr', '178.16.1.101')
    srv_msg.response_check_option_content(step, 'Response', '61', None, 'value', '63666731323334')

    misc.test_procedure(step)
    srv_msg.client_copy_option(step, 'server_id')
    srv_msg.client_does_include_with_value(step, 'requested_addr', '178.16.1.101')
    srv_msg.client_send_msg(step, 'REQUEST')

    misc.pass_criteria(step)
    srv_msg.send_wait_for_message(step, 'MUST', None, 'ACK')
    srv_msg.response_check_option_content(step, 'Response', '61', None, 'value', '63666731323334')

    misc.test_procedure(step)
    srv_msg.client_copy_option(step, 'server_id')
    # Use an out-of-subnet address to force NAK
    srv_msg.client_does_include_with_value(step, 'requested_addr', '172.16.1.101')
    srv_msg.client_send_msg(step, 'REQUEST')

    misc.pass_criteria(step)
    srv_msg.send_wait_for_message(step, 'MUST', None, 'NAK')
    # Configured id is set at selected subnet level, in this case it
    # is not there to send.
    srv_msg.response_check_include_option(step, 'Response', 'NOT ', '61')



@pytest.mark.py_test
@pytest.mark.v4
@pytest.mark.dhcpd
@pytest.mark.keyword
@pytest.mark.echo_client_id
def test_v4_dhcpd_keyword_echo_client_id_off_and_PRL(step):
    """new-v4.dhcpd.keyword.echo-client-id-off-and-PRL"""
    # Verifies the following scenarios with ehco-client-id disabled:
    # DISCOVER with client-id but no PRL
    # DISCOVER with client-id and a PRL which does NOT ask for client-id
    # DISCOVER with client-id and a PRL which does asks for client-id
    # DISCOVER without client-id but no PRL
    # DISCOVER without client-id and a PRL which does NOT ask for client-id
    # DISCOVER without client-id and a PRL which does asks for client-id
    # 
    misc.test_setup(step)
    srv_control.run_command(step, ' ping-check off;')
    srv_control.run_command(step, ' subnet 178.16.1.0 netmask 255.255.255.0 {')
    srv_control.run_command(step, ' authoritative;')
    srv_control.run_command(step, ' option root-path "/opt/var/stuff";')
    srv_control.run_command(step, ' option dhcp-client-identifier "cfg1234";')
    srv_control.run_command(step, '    range 178.16.1.100 178.16.1.120; }')
    srv_control.build_and_send_config_files(step, 'SSH', 'config-file')
    srv_control.start_srv(step, 'DHCP', 'started')

    # Send DISCOVER with client-id but without PRL
    # Should get configured id in OFFER
    misc.test_procedure(step)
    srv_msg.client_does_include_with_value(step, 'client_id', '72656331323334')
    srv_msg.client_send_msg(step, 'DISCOVER')

    misc.pass_criteria(step)
    srv_msg.send_wait_for_message(step, 'MUST', None, 'OFFER')
    srv_msg.response_check_option_content(step, 'Response', '61', None, 'value', '63666731323334')

    # Send DISCOVER with client-id and a PRL which does NOT ask for client-id
    # Should NOT client-id in OFFER
    misc.test_procedure(step)
    srv_msg.client_requests_option(step, '17')
    srv_msg.client_does_include_with_value(step, 'client_id', '72656331323334')
    srv_msg.client_send_msg(step, 'DISCOVER')

    misc.pass_criteria(step)
    srv_msg.send_wait_for_message(step, 'MUST', None, 'OFFER')
    srv_msg.response_check_option_content(step, 'Response', '17', None, 'value', '/opt/var/stuff')
    srv_msg.response_check_include_option(step, 'Response', 'NOT ', '61')

    # Send DISCOVER with client-id and a PRL which does asks for client-id
    # Should get configured-id in OFFER
    misc.test_procedure(step)
    srv_msg.client_requests_option(step, '17')
    srv_msg.client_requests_option(step, '61')
    srv_msg.client_does_include_with_value(step, 'client_id', '72656331323334')
    srv_msg.client_send_msg(step, 'DISCOVER')

    misc.pass_criteria(step)
    srv_msg.send_wait_for_message(step, 'MUST', None, 'OFFER')
    srv_msg.response_check_option_content(step, 'Response', '17', None, 'value', '/opt/var/stuff')
    srv_msg.response_check_option_content(step, 'Response', '61', None, 'value', '63666731323334')

    # Send DISCOVER WIHTOUT client-id or PRL
    # Should get configured-id in OFFER
    misc.test_procedure(step)
    srv_msg.client_send_msg(step, 'DISCOVER')

    misc.pass_criteria(step)
    srv_msg.send_wait_for_message(step, 'MUST', None, 'OFFER')
    srv_msg.response_check_option_content(step, 'Response', '61', None, 'value', '63666731323334')

    # Send DISCOVER WITHOUT client-id but a PRL which does NOT ask for
    # client-id.
    # Should NOT get configured client-id in OFFER
    misc.test_procedure(step)
    srv_msg.client_requests_option(step, '17')
    srv_msg.client_send_msg(step, 'DISCOVER')

    misc.pass_criteria(step)
    srv_msg.send_wait_for_message(step, 'MUST', None, 'OFFER')
    srv_msg.response_check_option_content(step, 'Response', '17', None, 'value', '/opt/var/stuff')
    srv_msg.response_check_include_option(step, 'Response', 'NOT ', '61')

    # Send DISCOVER WITHOUT client-id but a PRL which does asks for client-id
    # Should get configured client-id in OFFER
    misc.test_procedure(step)
    srv_msg.client_requests_option(step, '17')
    srv_msg.client_requests_option(step, '61')
    srv_msg.client_send_msg(step, 'DISCOVER')

    misc.pass_criteria(step)
    srv_msg.send_wait_for_message(step, 'MUST', None, 'OFFER')
    srv_msg.response_check_option_content(step, 'Response', '17', None, 'value', '/opt/var/stuff')
    srv_msg.response_check_option_content(step, 'Response', '61', None, 'value', '63666731323334')




@pytest.mark.py_test
@pytest.mark.v4
@pytest.mark.dhcpd
@pytest.mark.keyword
@pytest.mark.echo_client_id
def test_v4_dhcpd_keyword_echo_client_id_on_and_PRL(step):
    """new-v4.dhcpd.keyword.echo-client-id-on-and-PRL"""
    # Verifies the following scenarios with ehco-client-id enabled:
    # DISCOVER with client-id but no PRL
    # DISCOVER with client-id and a PRL which does NOT ask for client-id
    # DISCOVER with client-id and a PRL which does asks for client-id
    # DISCOVER without client-id but no PRL
    # DISCOVER without client-id and a PRL which does NOT ask for client-id
    # DISCOVER without client-id and a PRL which does asks for client-id
    # 
    misc.test_setup(step)
    srv_control.run_command(step, ' ping-check off;')
    srv_control.run_command(step, ' subnet 178.16.1.0 netmask 255.255.255.0 {')
    srv_control.run_command(step, ' authoritative;')
    srv_control.run_command(step, ' echo-client-id on;')
    srv_control.run_command(step, ' option root-path "/opt/var/stuff";')
    srv_control.run_command(step, ' option dhcp-client-identifier "cfg1234";')
    srv_control.run_command(step, '    range 178.16.1.100 178.16.1.120; }')
    srv_control.build_and_send_config_files(step, 'SSH', 'config-file')
    srv_control.start_srv(step, 'DHCP', 'started')

    # Send DISCOVER with client-id but without PRL
    # Should get client-id we sent back in OFFER
    misc.test_procedure(step)
    srv_msg.client_does_include_with_value(step, 'client_id', '72656331323334')
    srv_msg.client_send_msg(step, 'DISCOVER')

    misc.pass_criteria(step)
    srv_msg.send_wait_for_message(step, 'MUST', None, 'OFFER')
    srv_msg.response_check_option_content(step, 'Response', '61', None, 'value', '72656331323334')

    # Send DISCOVER with client-id and a PRL which does NOT ask for client-id
    # Should get client-id we sent back in OFFER
    misc.test_procedure(step)
    srv_msg.client_requests_option(step, '17')
    srv_msg.client_does_include_with_value(step, 'client_id', '72656331323334')
    srv_msg.client_send_msg(step, 'DISCOVER')

    misc.pass_criteria(step)
    srv_msg.send_wait_for_message(step, 'MUST', None, 'OFFER')
    srv_msg.response_check_option_content(step, 'Response', '17', None, 'value', '/opt/var/stuff')
    srv_msg.response_check_option_content(step, 'Response', '61', None, 'value', '72656331323334')

    # Send DISCOVER with client-id and a PRL which does asks for client-id
    # Should get client-id we sent back in OFFER
    misc.test_procedure(step)
    srv_msg.client_requests_option(step, '17')
    srv_msg.client_requests_option(step, '61')
    srv_msg.client_does_include_with_value(step, 'client_id', '72656331323334')
    srv_msg.client_send_msg(step, 'DISCOVER')

    misc.pass_criteria(step)
    srv_msg.send_wait_for_message(step, 'MUST', None, 'OFFER')
    srv_msg.response_check_option_content(step, 'Response', '17', None, 'value', '/opt/var/stuff')
    srv_msg.response_check_option_content(step, 'Response', '61', None, 'value', '72656331323334')

    # Send DISCOVER WIHTOUT client-id or PRL
    # Should get configured-id in OFFER
    misc.test_procedure(step)
    srv_msg.client_send_msg(step, 'DISCOVER')

    misc.pass_criteria(step)
    srv_msg.send_wait_for_message(step, 'MUST', None, 'OFFER')
    srv_msg.response_check_option_content(step, 'Response', '61', None, 'value', '63666731323334')

    # Send DISCOVER WITHOUT client-id but a PRL which does NOT ask for
    # client-id.
    # Should get configured client-id in OFFER
    misc.test_procedure(step)
    srv_msg.client_requests_option(step, '17')
    srv_msg.client_send_msg(step, 'DISCOVER')

    misc.pass_criteria(step)
    srv_msg.send_wait_for_message(step, 'MUST', None, 'OFFER')
    srv_msg.response_check_option_content(step, 'Response', '17', None, 'value', '/opt/var/stuff')
    srv_msg.response_check_option_content(step, 'Response', '61', None, 'value', '63666731323334')

    # Send DISCOVER WITHOUT client-id but a PRL which does asks for client-id
    # Should get configured client-id in OFFER
    misc.test_procedure(step)
    srv_msg.client_requests_option(step, '17')
    srv_msg.client_requests_option(step, '61')
    srv_msg.client_send_msg(step, 'DISCOVER')

    misc.pass_criteria(step)
    srv_msg.send_wait_for_message(step, 'MUST', None, 'OFFER')
    srv_msg.response_check_option_content(step, 'Response', '17', None, 'value', '/opt/var/stuff')
    srv_msg.response_check_option_content(step, 'Response', '61', None, 'value', '63666731323334')


