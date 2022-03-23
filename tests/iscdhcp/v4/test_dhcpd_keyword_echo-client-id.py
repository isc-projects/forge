"""ISC_DHCP DHCPv4 Keywords"""

# pylint: disable=invalid-name,line-too-long

import pytest
from src import misc
from src import srv_control
from src import srv_msg

from src.softwaresupport.isc_dhcp6_server.functions import add_line_in_global


@pytest.mark.v4
@pytest.mark.dhcpd
def test_v4_dhcpd_keyword_echo_client_id_off_offer_ack_nak():
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
    misc.test_setup()
    add_line_in_global(' ping-check off;')
    add_line_in_global(' subnet 192.168.50.0 netmask 255.255.255.0 {')
    add_line_in_global(' authoritative;')
    add_line_in_global('    range 192.168.50.100 192.168.50.101; }')
    srv_control.build_and_send_config_files()
    srv_control.start_srv('DHCP', 'started')

    misc.test_procedure()
    # set client-id to 'rec1234'
    srv_msg.client_does_include_with_value('client_id', '72656331323334')
    srv_msg.client_send_msg('DISCOVER')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', 'OFFER')
    srv_msg.response_check_include_option(1)
    srv_msg.response_check_content('yiaddr', '192.168.50.100')
    srv_msg.response_check_option_content(1, 'value', '255.255.255.0')
    srv_msg.response_check_include_option(61, expect_include=False)

    misc.test_procedure()
    srv_msg.client_copy_option('server_id')
    srv_msg.client_does_include_with_value('requested_addr', '192.168.50.100')
    srv_msg.client_does_include_with_value('client_id', '72656331323334')
    srv_msg.client_send_msg('REQUEST')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', 'ACK')
    srv_msg.response_check_content('yiaddr', '192.168.50.100')
    srv_msg.response_check_include_option(61, expect_include=False)

    misc.test_procedure()
    srv_msg.client_copy_option('server_id')
    srv_msg.client_does_include_with_value('client_id', '72656331323334')
    # Use an out-of-subnet address to force NAK
    srv_msg.client_does_include_with_value('requested_addr', '172.16.1.100')
    srv_msg.client_send_msg('REQUEST')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', 'NAK')
    srv_msg.response_check_include_option(61, expect_include=False)


@pytest.mark.v4
@pytest.mark.dhcpd
def test_v4_dhcpd_keyword_echo_client_id_on_offer_ack_nak():
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
    misc.test_setup()
    add_line_in_global(' ping-check off;')
    add_line_in_global(' echo-client-id on;')
    add_line_in_global(' subnet 192.168.50.0 netmask 255.255.255.0 {')
    add_line_in_global(' authoritative;')
    add_line_in_global('    range 192.168.50.100 192.168.50.101; }')
    srv_control.build_and_send_config_files()
    srv_control.start_srv('DHCP', 'started')

    misc.test_procedure()
    # set client-id to 'rec1234'
    srv_msg.client_does_include_with_value('client_id', '72656331323334')
    srv_msg.client_send_msg('DISCOVER')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', 'OFFER')
    srv_msg.response_check_include_option(1)
    srv_msg.response_check_content('yiaddr', '192.168.50.100')
    srv_msg.response_check_option_content(1, 'value', '255.255.255.0')
    srv_msg.response_check_option_content(61, 'value', '72656331323334')

    misc.test_procedure()
    srv_msg.client_copy_option('server_id')
    srv_msg.client_does_include_with_value('client_id', '72656331323334')
    srv_msg.client_does_include_with_value('requested_addr', '192.168.50.100')
    srv_msg.client_send_msg('REQUEST')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', 'ACK')
    srv_msg.response_check_option_content(61, 'value', '72656331323334')
    srv_msg.response_check_content('yiaddr', '192.168.50.100')

    misc.test_procedure()
    srv_msg.client_copy_option('server_id')
    srv_msg.client_does_include_with_value('client_id', '72656331323334')
    # Use an out-of-subnet address to force NAK
    srv_msg.client_does_include_with_value('requested_addr', '172.16.1.100')
    srv_msg.client_send_msg('REQUEST')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', 'NAK')
    srv_msg.response_check_option_content(61, 'value', '72656331323334')

    # ##############################################################
    # Repeat the sequence without a client sending an id
    # ##############################################################
    misc.test_procedure()
    srv_msg.client_send_msg('DISCOVER')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', 'OFFER')
    srv_msg.response_check_include_option(1)
    srv_msg.response_check_content('yiaddr', '192.168.50.101')
    srv_msg.response_check_include_option(61, expect_include=False)

    misc.test_procedure()
    srv_msg.client_copy_option('server_id')
    srv_msg.client_does_include_with_value('requested_addr', '192.168.50.101')
    srv_msg.client_send_msg('REQUEST')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', 'ACK')
    srv_msg.response_check_include_option(61, expect_include=False)

    misc.test_procedure()
    srv_msg.client_copy_option('server_id')
    # Use an out-of-subnet address to force NAK
    srv_msg.client_does_include_with_value('requested_addr', '172.16.1.101')
    srv_msg.client_send_msg('REQUEST')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', 'NAK')
    srv_msg.response_check_include_option(61, expect_include=False)


@pytest.mark.v4
@pytest.mark.dhcpd
def test_v4_dhcpd_keyword_echo_client_id_per_class():
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
    misc.test_setup()
    add_line_in_global('ping-check off;')
    add_line_in_global('class "echo" {')
    add_line_in_global('    match if (substring(option host-name, 0, 4) = "echo");')
    add_line_in_global('    echo-client-id on;')
    add_line_in_global('}')
    add_line_in_global('class "noecho" {')
    add_line_in_global('    match if (substring(option host-name, 0, 6) = "noecho");')
    add_line_in_global('}')
    add_line_in_global('subnet 192.168.50.0 netmask 255.255.255.0 {')
    add_line_in_global('    authoritative;')
    add_line_in_global('    pool {')
    add_line_in_global('        range 192.168.50.100 192.168.50.101;')
    add_line_in_global('    }')
    add_line_in_global('}')

    # set client-id to 'rec1234'
    srv_msg.client_does_include_with_value('client_id', '72656331323334')
    srv_msg.client_does_include_with_value('hostname', 'echo')
    srv_control.build_and_send_config_files()
    srv_control.start_srv('DHCP', 'started')

    misc.test_procedure()
    srv_msg.client_send_msg('DISCOVER')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', 'OFFER')
    srv_msg.response_check_include_option(1)
    srv_msg.response_check_content('yiaddr', '192.168.50.100')
    srv_msg.response_check_option_content(1, 'value', '255.255.255.0')
    srv_msg.response_check_option_content(61, 'value', '72656331323334')

    misc.test_procedure()
    srv_msg.client_copy_option('server_id')
    srv_msg.client_does_include_with_value('hostname', 'echo')
    srv_msg.client_does_include_with_value('client_id', '72656331323334')
    srv_msg.client_does_include_with_value('requested_addr', '192.168.50.100')
    srv_msg.client_send_msg('REQUEST')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', 'ACK')
    srv_msg.response_check_content('yiaddr', '192.168.50.100')
    srv_msg.response_check_option_content(61, 'value', '72656331323334')

    misc.test_procedure()
    srv_msg.client_copy_option('server_id')
    srv_msg.client_does_include_with_value('hostname', 'echo')
    srv_msg.client_does_include_with_value('client_id', '72656331323334')
    # Use an out-of-subnet address to force NAK
    srv_msg.client_does_include_with_value('requested_addr', '172.16.1.100')
    srv_msg.client_send_msg('REQUEST')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', 'NAK')
    srv_msg.response_check_option_content(61, 'value', '72656331323334')

    # #########################################################
    # Now test with a client that is NOT in class "echo"
    # #########################################################
    misc.test_procedure()
    srv_msg.client_does_include_with_value('client_id', '72656331323334')
    srv_msg.client_does_include_with_value('hostname', 'noecho')
    srv_msg.client_send_msg('DISCOVER')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', 'OFFER')
    srv_msg.response_check_include_option(1)
    srv_msg.response_check_content('yiaddr', '192.168.50.100')
    srv_msg.response_check_option_content(1, 'value', '255.255.255.0')
    srv_msg.response_check_include_option(61, expect_include=False)

    misc.test_procedure()
    srv_msg.client_copy_option('server_id')
    srv_msg.client_does_include_with_value('hostname', 'noecho')
    srv_msg.client_does_include_with_value('client_id', '72656331323334')
    srv_msg.client_does_include_with_value('requested_addr', '192.168.50.100')
    srv_msg.client_send_msg('REQUEST')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', 'ACK')
    srv_msg.response_check_content('yiaddr', '192.168.50.100')
    srv_msg.response_check_include_option(61, expect_include=False)

    misc.test_procedure()
    srv_msg.client_copy_option('server_id')
    srv_msg.client_does_include_with_value('hostname', 'noecho')
    srv_msg.client_does_include_with_value('client_id', '72656331323334')
    # Use an out-of-subnet address to force NAK
    srv_msg.client_does_include_with_value('requested_addr', '172.16.1.100')
    srv_msg.client_send_msg('REQUEST')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', 'NAK')
    srv_msg.response_check_include_option(61, expect_include=False)


@pytest.mark.v4
@pytest.mark.dhcpd
def test_v4_dhcpd_keyword_echo_client_id_vs_config_id():
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
    misc.test_setup()
    add_line_in_global(' ping-check off;')
    add_line_in_global(' subnet 192.168.50.0 netmask 255.255.255.0 {')
    add_line_in_global(' authoritative;')
    add_line_in_global(' echo-client-id on;')
    add_line_in_global(' option dhcp-client-identifier "cfg1234";')
    add_line_in_global('    range 192.168.50.100 192.168.50.101; }')
    srv_control.build_and_send_config_files()
    srv_control.start_srv('DHCP', 'started')

    misc.test_procedure()
    # set client-id to 'rec1234'
    srv_msg.client_does_include_with_value('client_id', '72656331323334')
    srv_msg.client_send_msg('DISCOVER')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', 'OFFER')
    srv_msg.response_check_include_option(1)
    srv_msg.response_check_content('yiaddr', '192.168.50.100')
    srv_msg.response_check_option_content(1, 'value', '255.255.255.0')
    srv_msg.response_check_option_content(61, 'value', '72656331323334')

    misc.test_procedure()
    srv_msg.client_copy_option('server_id')
    srv_msg.client_does_include_with_value('client_id', '72656331323334')
    srv_msg.client_does_include_with_value('requested_addr', '192.168.50.100')
    srv_msg.client_send_msg('REQUEST')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', 'ACK')
    srv_msg.response_check_option_content(61, 'value', '72656331323334')
    srv_msg.response_check_content('yiaddr', '192.168.50.100')

    misc.test_procedure()
    srv_msg.client_copy_option('server_id')
    srv_msg.client_does_include_with_value('client_id', '72656331323334')
    # Use an out-of-subnet address to force NAK
    srv_msg.client_does_include_with_value('requested_addr', '172.16.1.100')
    srv_msg.client_send_msg('REQUEST')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', 'NAK')
    # Received id is available even on NAKs
    srv_msg.response_check_option_content(61, 'value', '72656331323334')

    # ##############################################################
    # Repeat the sequence without a client sending an id, should
    # get configured id
    # ##############################################################
    misc.test_procedure()
    srv_msg.client_send_msg('DISCOVER')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', 'OFFER')
    srv_msg.response_check_include_option(1)
    srv_msg.response_check_content('yiaddr', '192.168.50.101')
    srv_msg.response_check_option_content(61, 'value', '63666731323334')

    misc.test_procedure()
    srv_msg.client_copy_option('server_id')
    srv_msg.client_does_include_with_value('requested_addr', '192.168.50.101')
    srv_msg.client_send_msg('REQUEST')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', 'ACK')
    srv_msg.response_check_option_content(61, 'value', '63666731323334')

    misc.test_procedure()
    srv_msg.client_copy_option('server_id')
    # Use an out-of-subnet address to force NAK
    srv_msg.client_does_include_with_value('requested_addr', '172.16.1.101')
    srv_msg.client_send_msg('REQUEST')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', 'NAK')
    # Configured id is set at selected subnet level, in this case it
    # is not there to send.
    srv_msg.response_check_include_option(61, expect_include=False)


@pytest.mark.v4
@pytest.mark.dhcpd
def test_v4_dhcpd_keyword_echo_client_id_off_and_PRL():
    """new-v4.dhcpd.keyword.echo-client-id-off-and-PRL"""
    # Verifies the following scenarios with ehco-client-id disabled:
    # DISCOVER with client-id but no PRL
    # DISCOVER with client-id and a PRL which does NOT ask for client-id
    # DISCOVER with client-id and a PRL which does asks for client-id
    # DISCOVER without client-id but no PRL
    # DISCOVER without client-id and a PRL which does NOT ask for client-id
    # DISCOVER without client-id and a PRL which does asks for client-id
    #
    misc.test_setup()
    add_line_in_global(' ping-check off;')
    add_line_in_global(' subnet 192.168.50.0 netmask 255.255.255.0 {')
    add_line_in_global(' authoritative;')
    add_line_in_global(' option root-path "/opt/var/stuff";')
    add_line_in_global(' option dhcp-client-identifier "cfg1234";')
    add_line_in_global('    range 192.168.50.100 192.168.50.120; }')
    srv_control.build_and_send_config_files()
    srv_control.start_srv('DHCP', 'started')

    # Send DISCOVER with client-id but without PRL
    # Should get configured id in OFFER
    misc.test_procedure()
    srv_msg.client_does_include_with_value('client_id', '72656331323334')
    srv_msg.client_send_msg('DISCOVER')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', 'OFFER')
    srv_msg.response_check_option_content(61, 'value', '63666731323334')

    # Send DISCOVER with client-id and a PRL which does NOT ask for client-id
    # Should NOT client-id in OFFER
    misc.test_procedure()
    srv_msg.client_requests_option(17)
    srv_msg.client_does_include_with_value('client_id', '72656331323334')
    srv_msg.client_send_msg('DISCOVER')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', 'OFFER')
    srv_msg.response_check_option_content(17, 'value', '/opt/var/stuff')
    srv_msg.response_check_include_option(61, expect_include=False)

    # Send DISCOVER with client-id and a PRL which does asks for client-id
    # Should get configured-id in OFFER
    misc.test_procedure()
    srv_msg.client_requests_option(17)
    srv_msg.client_requests_option(61)
    srv_msg.client_does_include_with_value('client_id', '72656331323334')
    srv_msg.client_send_msg('DISCOVER')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', 'OFFER')
    srv_msg.response_check_option_content(17, 'value', '/opt/var/stuff')
    srv_msg.response_check_option_content(61, 'value', '63666731323334')

    # Send DISCOVER WIHTOUT client-id or PRL
    # Should get configured-id in OFFER
    misc.test_procedure()
    srv_msg.client_send_msg('DISCOVER')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', 'OFFER')
    srv_msg.response_check_option_content(61, 'value', '63666731323334')

    # Send DISCOVER WITHOUT client-id but a PRL which does NOT ask for
    # client-id.
    # Should NOT get configured client-id in OFFER
    misc.test_procedure()
    srv_msg.client_requests_option(17)
    srv_msg.client_send_msg('DISCOVER')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', 'OFFER')
    srv_msg.response_check_option_content(17, 'value', '/opt/var/stuff')
    srv_msg.response_check_include_option(61, expect_include=False)

    # Send DISCOVER WITHOUT client-id but a PRL which does asks for client-id
    # Should get configured client-id in OFFER
    misc.test_procedure()
    srv_msg.client_requests_option(17)
    srv_msg.client_requests_option(61)
    srv_msg.client_send_msg('DISCOVER')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', 'OFFER')
    srv_msg.response_check_option_content(17, 'value', '/opt/var/stuff')
    srv_msg.response_check_option_content(61, 'value', '63666731323334')


@pytest.mark.v4
@pytest.mark.dhcpd
def test_v4_dhcpd_keyword_echo_client_id_on_and_PRL():
    """new-v4.dhcpd.keyword.echo-client-id-on-and-PRL"""
    # Verifies the following scenarios with ehco-client-id enabled:
    # DISCOVER with client-id but no PRL
    # DISCOVER with client-id and a PRL which does NOT ask for client-id
    # DISCOVER with client-id and a PRL which does asks for client-id
    # DISCOVER without client-id but no PRL
    # DISCOVER without client-id and a PRL which does NOT ask for client-id
    # DISCOVER without client-id and a PRL which does asks for client-id
    #
    misc.test_setup()
    add_line_in_global(' ping-check off;')
    add_line_in_global(' subnet 192.168.50.0 netmask 255.255.255.0 {')
    add_line_in_global(' authoritative;')
    add_line_in_global(' echo-client-id on;')
    add_line_in_global(' option root-path "/opt/var/stuff";')
    add_line_in_global(' option dhcp-client-identifier "cfg1234";')
    add_line_in_global('    range 192.168.50.100 192.168.50.120; }')
    srv_control.build_and_send_config_files()
    srv_control.start_srv('DHCP', 'started')

    # Send DISCOVER with client-id but without PRL
    # Should get client-id we sent back in OFFER
    misc.test_procedure()
    srv_msg.client_does_include_with_value('client_id', '72656331323334')
    srv_msg.client_send_msg('DISCOVER')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', 'OFFER')
    srv_msg.response_check_option_content(61, 'value', '72656331323334')

    # Send DISCOVER with client-id and a PRL which does NOT ask for client-id
    # Should get client-id we sent back in OFFER
    misc.test_procedure()
    srv_msg.client_requests_option(17)
    srv_msg.client_does_include_with_value('client_id', '72656331323334')
    srv_msg.client_send_msg('DISCOVER')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', 'OFFER')
    srv_msg.response_check_option_content(17, 'value', '/opt/var/stuff')
    srv_msg.response_check_option_content(61, 'value', '72656331323334')

    # Send DISCOVER with client-id and a PRL which does asks for client-id
    # Should get client-id we sent back in OFFER
    misc.test_procedure()
    srv_msg.client_requests_option(17)
    srv_msg.client_requests_option(61)
    srv_msg.client_does_include_with_value('client_id', '72656331323334')
    srv_msg.client_send_msg('DISCOVER')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', 'OFFER')
    srv_msg.response_check_option_content(17, 'value', '/opt/var/stuff')
    srv_msg.response_check_option_content(61, 'value', '72656331323334')

    # Send DISCOVER WIHTOUT client-id or PRL
    # Should get configured-id in OFFER
    misc.test_procedure()
    srv_msg.client_send_msg('DISCOVER')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', 'OFFER')
    srv_msg.response_check_option_content(61, 'value', '63666731323334')

    # Send DISCOVER WITHOUT client-id but a PRL which does NOT ask for
    # client-id.
    # Should get configured client-id in OFFER
    misc.test_procedure()
    srv_msg.client_requests_option(17)
    srv_msg.client_send_msg('DISCOVER')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', 'OFFER')
    srv_msg.response_check_option_content(17, 'value', '/opt/var/stuff')
    srv_msg.response_check_option_content(61, 'value', '63666731323334')

    # Send DISCOVER WITHOUT client-id but a PRL which does asks for client-id
    # Should get configured client-id in OFFER
    misc.test_procedure()
    srv_msg.client_requests_option(17)
    srv_msg.client_requests_option(61)
    srv_msg.client_send_msg('DISCOVER')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', 'OFFER')
    srv_msg.response_check_option_content(17, 'value', '/opt/var/stuff')
    srv_msg.response_check_option_content(61, 'value', '63666731323334')
