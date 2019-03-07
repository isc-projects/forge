"""Standard DHCPv6 address validation"""

# pylint: disable=invalid-name,line-too-long

import pytest

import references
import misc
import srv_control
import srv_msg


@pytest.mark.basic
@pytest.mark.v6
@pytest.mark.dhcp6
@pytest.mark.unicast
def test_v6_basic_message_unicast_global_solicit():
    #  Server MUST discard any Solicit it receives with
    #  a unicast address destination
    #  Message details 		Client		Server
    #  GLOBAL_UNICAST dest  SOLICIT -->
    #  		   						 X	ADVERTISE
    #  correct message		SOLICIT -->
    #  		   						<--	ADVERTISE
    misc.test_setup()
    srv_control.config_srv_subnet_with_iface('$(SERVER_IFACE)',
                                             '$(SRV_IPV6_ADDR_GLOBAL)',
                                             '3000::/64',
                                             '3000::1-3000::ff')
    # Server is configured with
    srv_control.build_and_send_config_files('SSH', 'config-file')
    srv_control.start_srv('DHCP', 'started')

    misc.test_procedure()
    srv_msg.client_requests_option('7')
    srv_msg.unicast_addres('GLOBAL', None)
    srv_msg.client_does_include('Client', None, 'client-id')
    srv_msg.client_does_include('Client', None, 'IA-NA')
    srv_msg.client_send_msg('SOLICIT')

    misc.pass_criteria()
    srv_msg.send_dont_wait_for_message()

    misc.test_procedure()
    srv_msg.client_requests_option('7')
    srv_msg.client_does_include('Client', None, 'client-id')
    srv_msg.client_does_include('Client', None, 'IA-NA')
    srv_msg.client_send_msg('SOLICIT')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', None, 'ADVERTISE')
    srv_msg.response_check_include_option('Response', None, '3')
    srv_msg.response_check_option_content('Response', '3', None, 'sub-option', '5')

    references.references_check('RFC3315')


@pytest.mark.basic
@pytest.mark.v6
@pytest.mark.dhcp6
@pytest.mark.unicast
def test_v6_basic_message_unicast_global_confirm():
    #  Server MUST discard any Confirm it receives with
    #  a unicast address destination
    #  Message details 		Client		Server
    #  						SOLICIT -->
    #  		   						<--	ADVERTISE
    #  						REQUEST -->
    #  		   						<--	REPLY
    #  GLOBAL_UNICAST dest	CONFIRM -->
    # 					  		     X	REPLY
    #  correct message 		CONFIRM -->
    # 					  		    <--	REPLY
    #  Pass Criteria:
    #  				REPLY MUST include option:
    # 					client-id
    # 					server-id

    misc.test_setup()
    # Server is configured with 3000::/64 subnet with 3000::1-3000::ff pool.
    srv_control.config_srv_subnet_with_iface('$(SERVER_IFACE)',
                                             '$(SRV_IPV6_ADDR_GLOBAL)',
                                             '3000::/64',
                                             '3000::1-3000::ff')
    srv_control.build_and_send_config_files('SSH', 'config-file')
    srv_control.start_srv('DHCP', 'started')

    misc.test_procedure()
    srv_msg.client_requests_option('7')
    srv_msg.client_does_include('Client', None, 'client-id')
    srv_msg.client_does_include('Client', None, 'IA-NA')
    srv_msg.client_send_msg('SOLICIT')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', None, 'ADVERTISE')
    srv_msg.response_check_include_option('Response', None, '3')
    srv_msg.response_check_option_content('Response', '3', None, 'sub-option', '5')

    misc.test_procedure()
    srv_msg.client_copy_option('IA_NA')
    srv_msg.client_copy_option('server-id')
    srv_msg.client_requests_option('7')
    srv_msg.client_does_include('Client', None, 'client-id')
    srv_msg.client_send_msg('REQUEST')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', None, 'REPLY')

    misc.test_procedure()
    srv_msg.client_save_option('IA_NA')
    srv_msg.client_add_saved_option('DONT ')
    srv_msg.unicast_addres('GLOBAL', None)
    srv_msg.client_does_include('Client', None, 'client-id')
    srv_msg.client_send_msg('CONFIRM')

    misc.pass_criteria()
    srv_msg.send_dont_wait_for_message()

    misc.test_procedure()
    srv_msg.client_add_saved_option(None)
    srv_msg.client_does_include('Client', None, 'client-id')
    srv_msg.client_send_msg('CONFIRM')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', None, 'REPLY')
    srv_msg.response_check_include_option('Response', None, '1')
    srv_msg.response_check_include_option('Response', None, '2')
    srv_msg.response_check_include_option('Response', None, '13')

    references.references_check('RFC3315')


@pytest.mark.basic
@pytest.mark.v6
@pytest.mark.dhcp6
@pytest.mark.unicast
def test_v6_basic_message_unicast_global_rebind():
    #  Server MUST discard any Rebind it receives with
    #  a unicast address destination.
    #  Message details		Client		Server
    #  						SOLICIT -->
    #  		   						<--	ADVERTISE
    #  						REQUEST -->
    #  		   						<--	REPLY
    #  GLOBAL_UNICAST dest	 REBIND -->
    # 					  	     	 X	REPLY
    #  correct message 		 REBIND -->
    # 					  	    	<--	REPLY
    #  Pass Criteria:
    #  				REPLY MUST include option:
    # 					client-id
    # 					server-id
    # 					IA-NA

    misc.test_setup()
    srv_control.config_srv_subnet_with_iface('$(SERVER_IFACE)',
                                             '$(SRV_IPV6_ADDR_GLOBAL)',
                                             '3000::/64',
                                             '3000::1-3000::ff')
    srv_control.build_and_send_config_files('SSH', 'config-file')
    srv_control.start_srv('DHCP', 'started')

    misc.test_procedure()
    srv_msg.client_requests_option('7')
    srv_msg.client_does_include('Client', None, 'client-id')
    srv_msg.client_does_include('Client', None, 'IA-NA')
    srv_msg.client_send_msg('SOLICIT')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', None, 'ADVERTISE')
    srv_msg.response_check_include_option('Response', None, '3')
    srv_msg.response_check_option_content('Response', '3', None, 'sub-option', '5')

    misc.test_procedure()
    srv_msg.client_copy_option('IA_NA')
    srv_msg.client_copy_option('server-id')
    srv_msg.client_does_include('Client', None, 'client-id')
    srv_msg.client_send_msg('REQUEST')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', None, 'REPLY')

    misc.test_procedure()
    srv_msg.unicast_addres('GLOBAL', None)
    srv_msg.client_save_option('IA_NA')
    srv_msg.client_add_saved_option('DONT ')
    srv_msg.client_does_include('Client', None, 'client-id')
    srv_msg.client_send_msg('REBIND')

    misc.pass_criteria()
    srv_msg.send_dont_wait_for_message()

    misc.test_procedure()
    srv_msg.client_add_saved_option(None)
    srv_msg.client_does_include('Client', None, 'client-id')
    srv_msg.client_send_msg('REBIND')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', None, 'REPLY')
    srv_msg.response_check_include_option('Response', None, '1')
    srv_msg.response_check_include_option('Response', None, '2')
    srv_msg.response_check_include_option('Response', None, '3')

    references.references_check('RFC3315')


@pytest.mark.basic
@pytest.mark.v6
@pytest.mark.dhcp6
@pytest.mark.unicast
def test_v6_basic_message_unicast_global_inforequest():
    #  Server MUST discard any Information-Request it receives with
    #  a unicast address destination.
    #  Message details 		Client		Server
    #  GLOBAL_UNICAST dest INFOREQUEST -->
    # 					  		       X	REPLY
    #  correct message 	   INFOREQUEST -->
    # 					  		       <--	REPLY
    #  Pass Criteria:
    #  				REPLY MUST include option:
    # 					client-id
    # 					server-id

    misc.test_setup()
    srv_control.config_srv_subnet_with_iface('$(SERVER_IFACE)',
                                             '$(SRV_IPV6_ADDR_GLOBAL)',
                                             '3000::/64',
                                             '3000::1-3000::ff')
    srv_control.config_srv_opt('preference', '123')
    srv_control.build_and_send_config_files('SSH', 'config-file')
    srv_control.start_srv('DHCP', 'started')

    misc.test_procedure()
    srv_msg.client_requests_option('7')
    srv_msg.unicast_addres('GLOBAL', None)
    # message wont contain client-id option
    srv_msg.client_send_msg('INFOREQUEST')

    misc.pass_criteria()
    srv_msg.send_dont_wait_for_message()

    misc.test_procedure()
    # message wont contain client-id option
    srv_msg.client_requests_option('7')
    srv_msg.client_send_msg('INFOREQUEST')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', None, 'REPLY')
    srv_msg.response_check_include_option('Response', 'NOT ', '1')
    srv_msg.response_check_include_option('Response', None, '2')
    srv_msg.response_check_include_option('Response', None, '7')

    references.references_check('RFC3315')


@pytest.mark.basic
@pytest.mark.v6
@pytest.mark.dhcp6
@pytest.mark.unicast
@pytest.mark.status_code
@pytest.mark.disabled
def test_v6_basic_message_unicast_global_request():
    #  Server MUST discard any Request message it receives with
    #  a unicast address destination, and send back REPLY with
    #  UseMulticast status code.
    #  In this test if it fails with 'NoAddrAvail' at the end
    #  it means that server has send back REPLY with UseMulticast
    #  status code but also assigned address.
    #  Message details		Client		Server
    #  						SOLICIT -->
    #  		   						<--	ADVERTISE
    #  GLOBAL_UNICAST dest	REQUEST -->
    #  		   						<--	REPLY
    #  Pass Criteria:
    #  				REPLY MUST include option:
    # 					client-id
    # 					server-id
    # 					status code option with UseMulticast
    #
    #  						SOLICIT -->
    #  		   						<--	ADVERTISE
    #  correct message		REQUEST -->
    #  		   						<--	REPLY
    #  				REPLY MUST include option:
    # 					client-id
    # 					server-id
    # 					IA_NA
    # 					IA_Address with address 3000::1.

    misc.test_setup()
    srv_control.config_srv_subnet_with_iface('$(SERVER_IFACE)',
                                             '$(SRV_IPV6_ADDR_GLOBAL)',
                                             '3000::/64',
                                             '3000::1-3000::ff')
    srv_control.build_and_send_config_files('SSH', 'config-file')
    srv_control.start_srv('DHCP', 'started')

    misc.test_procedure()
    srv_msg.client_requests_option('7')
    srv_msg.client_does_include('Client', None, 'client-id')
    srv_msg.client_does_include('Client', None, 'IA-NA')
    srv_msg.client_send_msg('SOLICIT')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', None, 'ADVERTISE')
    srv_msg.response_check_include_option('Response', None, '3')
    srv_msg.response_check_option_content('Response', '3', None, 'sub-option', '5')

    misc.test_procedure()
    srv_msg.client_save_option('server-id')
    srv_msg.client_save_option('IA_NA')
    srv_msg.client_add_saved_option('DONT ')
    srv_msg.unicast_addres('GLOBAL', None)
    srv_msg.client_does_include('Client', None, 'client-id')
    srv_msg.client_send_msg('REQUEST')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', None, 'REPLY')
    srv_msg.response_check_include_option('Response', None, '13')
    srv_msg.response_check_option_content('Response', '13', None, 'statuscode', '5')

    misc.test_procedure()
    srv_msg.client_add_saved_option('DONT ')
    srv_msg.client_does_include('Client', None, 'client-id')
    srv_msg.client_send_msg('REQUEST')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', None, 'REPLY')
    srv_msg.response_check_include_option('Response', None, '3')
    srv_msg.response_check_option_content('Response', '3', None, 'sub-option', '5')
    srv_msg.response_check_suboption_content('Response', '5', '3', None, 'address', '3000::1')

    references.references_check('RFC3315')


@pytest.mark.basic
@pytest.mark.v6
@pytest.mark.dhcp6
@pytest.mark.unicast
@pytest.mark.status_code
@pytest.mark.disabled
def test_v6_basic_message_unicast_global_renew():
    #  Server MUST discard any RENEW message it receives with
    #  a unicast address destination, and send back REPLY with
    #  UseMulticast status code.
    #  Message details 		Client		Server
    #  						SOLICIT -->
    #  		   						<--	ADVERTISE
    #  						REQUEST -->
    #  		   						<--	REPLY
    #  GLOBAL UNICAST dest	  RENEW -->
    # 					  		    <--	REPLY
    #  Pass Criteria:
    #  				REPLY MUST include option:
    # 					client-id
    # 					server-id
    # 					status code with UseMulticast
    #  correct message 		  RENEW -->
    # 					  		    <--	REPLY
    #  Pass Criteria:
    #  				REPLY MUST include option:
    # 					client-id
    # 					server-id
    # 					IA-NA
    # 					IA-Address
    misc.test_setup()
    srv_control.config_srv_subnet_with_iface('$(SERVER_IFACE)',
                                             '$(SRV_IPV6_ADDR_GLOBAL)',
                                             '3000::/64',
                                             '3000::1-3000::ff')
    srv_control.build_and_send_config_files('SSH', 'config-file')
    srv_control.start_srv('DHCP', 'started')

    misc.test_procedure()
    srv_msg.client_requests_option('7')
    srv_msg.client_does_include('Client', None, 'IA-NA')
    srv_msg.client_does_include('Client', None, 'client-id')
    srv_msg.client_send_msg('SOLICIT')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', None, 'ADVERTISE')

    misc.test_procedure()
    srv_msg.client_copy_option('IA_NA')
    srv_msg.client_copy_option('server-id')
    srv_msg.client_does_include('Client', None, 'client-id')
    srv_msg.client_send_msg('REQUEST')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', None, 'REPLY')

    misc.test_procedure()
    srv_msg.unicast_addres('GLOBAL', None)
    srv_msg.client_save_option('IA_NA')
    srv_msg.client_save_option('server-id')
    srv_msg.client_add_saved_option('DONT ')
    srv_msg.client_does_include('Client', None, 'client-id')
    srv_msg.client_send_msg('RENEW')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', None, 'REPLY')
    srv_msg.response_check_include_option('Response', None, '13')
    srv_msg.response_check_option_content('Response', '13', None, 'statuscode', '5')

    misc.test_procedure()
    srv_msg.client_add_saved_option(None)
    srv_msg.client_does_include('Client', None, 'client-id')
    srv_msg.client_send_msg('RENEW')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', None, 'REPLY')
    srv_msg.response_check_include_option('Response', None, '1')
    srv_msg.response_check_include_option('Response', None, '2')
    srv_msg.response_check_include_option('Response', None, '3')
    srv_msg.response_check_option_content('Response', '3', None, 'sub-option', '5')

    references.references_check('RFC3315')


@pytest.mark.basic
@pytest.mark.v6
@pytest.mark.dhcp6
@pytest.mark.unicast
@pytest.mark.status_code
@pytest.mark.disabled
def test_v6_basic_message_unicast_global_release():
    #  Server MUST discard any RELEASE message it receives with
    #  a unicast address destination, and send back REPLY with
    #  UseMulticast status code.
    #
    #  Message details 		Client		Server
    #  						SOLICIT -->
    #  		   						<--	ADVERTISE
    #  						REQUEST -->
    #  		   						<--	REPLY
    #  GLOBAL UNICAST dest	RELEASE -->
    # 					  		    <--	REPLY
    #  Pass Criteria:
    #  				REPLY MUST include option:
    # 					client-id
    # 					server-id
    # 					status-code with UseMulticast
    #  correct message 		RELEASE -->
    # 					  		    <--	REPLY
    #  Pass Criteria:
    #  				REPLY MUST include option:
    # 					client-id
    # 					server-id
    # 					status-code with Success
    misc.test_setup()
    # Server is configured with 3000::/64 subnet with 3000::1-3000::ff pool.
    srv_control.config_srv_subnet_with_iface('$(SERVER_IFACE)',
                                             '$(SRV_IPV6_ADDR_GLOBAL)',
                                             '3000::/64',
                                             '3000::1-3000::ff')
    srv_control.build_and_send_config_files('SSH', 'config-file')
    srv_control.start_srv('DHCP', 'started')

    misc.test_procedure()
    srv_msg.client_requests_option('7')
    srv_msg.client_does_include('Client', None, 'client-id')
    srv_msg.client_does_include('Client', None, 'IA-NA')
    srv_msg.client_send_msg('SOLICIT')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', None, 'ADVERTISE')

    misc.test_procedure()
    srv_msg.client_copy_option('IA_NA')
    srv_msg.client_copy_option('server-id')
    srv_msg.client_does_include('Client', None, 'client-id')
    srv_msg.client_send_msg('REQUEST')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', None, 'REPLY')

    misc.test_procedure()
    srv_msg.unicast_addres('GLOBAL', None)
    srv_msg.client_save_option('IA_NA')
    srv_msg.client_save_option('server-id')
    srv_msg.client_add_saved_option('DONT ')
    srv_msg.client_does_include('Client', None, 'client-id')
    srv_msg.client_send_msg('RELEASE')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', None, 'REPLY')
    srv_msg.response_check_include_option('Response', None, '13')
    srv_msg.response_check_option_content('Response', '13', None, 'statuscode', '5')

    misc.test_procedure()
    srv_msg.client_add_saved_option(None)
    srv_msg.client_does_include('Client', None, 'client-id')
    srv_msg.client_send_msg('RELEASE')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', None, 'REPLY')
    srv_msg.response_check_include_option('Response', None, '1')
    srv_msg.response_check_include_option('Response', None, '2')
    srv_msg.response_check_include_option('Response', None, '13')

    references.references_check('RFC3315')


@pytest.mark.basic
@pytest.mark.v6
@pytest.mark.dhcp6
@pytest.mark.unicast
def test_v6_basic_message_unicast_local_solicit():
    #  Server MUST discard any Solicit it receives with
    #  a unicast address destination
    #  Message details 		Client		Server
    #  LINK_LOCAL_UNICAST dest  SOLICIT -->
    #  		   						 X	ADVERTISE
    #  correct message		SOLICIT -->
    #  		   						<--	ADVERTISE
    misc.test_setup()
    srv_control.config_srv_subnet('3000::/64', '3000::1-3000::ff')
    srv_control.build_and_send_config_files('SSH', 'config-file')
    srv_control.start_srv('DHCP', 'started')

    misc.test_procedure()
    srv_msg.client_requests_option('7')
    srv_msg.unicast_addres(None, 'LINK_LOCAL')
    srv_msg.client_does_include('Client', None, 'client-id')
    srv_msg.client_does_include('Client', None, 'IA-NA')
    srv_msg.client_send_msg('SOLICIT')

    misc.pass_criteria()
    srv_msg.send_dont_wait_for_message()

    misc.test_procedure()
    srv_msg.client_requests_option('7')
    srv_msg.client_does_include('Client', None, 'client-id')
    srv_msg.client_does_include('Client', None, 'IA-NA')
    srv_msg.client_send_msg('SOLICIT')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', None, 'ADVERTISE')
    srv_msg.response_check_include_option('Response', None, '3')
    srv_msg.response_check_option_content('Response', '3', None, 'sub-option', '5')

    references.references_check('RFC3315')


@pytest.mark.basic
@pytest.mark.v6
@pytest.mark.dhcp6
@pytest.mark.unicast
def test_v6_basic_message_unicast_local_confirm():
    #  Server MUST discard any Confirm it receives with
    #  a unicast address destination
    #  Message details 		Client		Server
    #  						SOLICIT -->
    #  		   						<--	ADVERTISE
    #  						REQUEST -->
    #  		   						<--	REPLY
    #  LINK_LOCAL_UNICAST dest	CONFIRM -->
    # 					  		     X	REPLY
    #  correct message 		CONFIRM -->
    # 					  		    <--	REPLY
    #  Pass Criteria:
    #  				REPLY MUST include option:
    # 					client-id
    # 					server-id

    misc.test_setup()
    srv_control.config_srv_subnet('3000::/64', '3000::1-3000::ff')
    srv_control.build_and_send_config_files('SSH', 'config-file')
    srv_control.start_srv('DHCP', 'started')

    misc.test_procedure()
    srv_msg.client_requests_option('7')
    srv_msg.client_does_include('Client', None, 'client-id')
    srv_msg.client_does_include('Client', None, 'IA-NA')
    srv_msg.client_send_msg('SOLICIT')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', None, 'ADVERTISE')
    srv_msg.response_check_include_option('Response', None, '3')
    srv_msg.response_check_option_content('Response', '3', None, 'sub-option', '5')

    misc.test_procedure()
    srv_msg.client_copy_option('IA_NA')
    srv_msg.client_copy_option('server-id')
    srv_msg.client_requests_option('7')
    srv_msg.client_does_include('Client', None, 'client-id')
    srv_msg.client_send_msg('REQUEST')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', None, 'REPLY')

    misc.test_procedure()
    srv_msg.client_save_option('IA_NA')
    srv_msg.client_add_saved_option('DONT ')
    srv_msg.unicast_addres(None, 'LINK_LOCAL')
    srv_msg.client_does_include('Client', None, 'client-id')
    srv_msg.client_send_msg('CONFIRM')

    misc.pass_criteria()
    srv_msg.send_dont_wait_for_message()

    misc.test_procedure()
    srv_msg.client_add_saved_option(None)
    srv_msg.client_does_include('Client', None, 'client-id')
    srv_msg.client_send_msg('CONFIRM')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', None, 'REPLY')
    srv_msg.response_check_include_option('Response', None, '1')
    srv_msg.response_check_include_option('Response', None, '2')
    srv_msg.response_check_include_option('Response', None, '13')

    references.references_check('RFC3315')


@pytest.mark.basic
@pytest.mark.v6
@pytest.mark.dhcp6
@pytest.mark.unicast
def test_v6_basic_message_unicast_local_rebind():
    #  Server MUST discard any Rebind it receives with
    #  a unicast address destination.
    #  Message details		Client		Server
    #  						SOLICIT -->
    #  		   						<--	ADVERTISE
    #  						REQUEST -->
    #  		   						<--	REPLY
    #  LINK_LOCAL
    #  UNICAST dest	 		 REBIND -->
    # 					  	     	 X	REPLY
    #  correct message 		 REBIND -->
    # 					  	    	<--	REPLY
    #  Pass Criteria:
    #  				REPLY MUST include option:
    # 					client-id
    # 					server-id
    # 					IA-NA

    misc.test_setup()
    srv_control.config_srv_subnet('3000::/64', '3000::1-3000::ff')
    srv_control.build_and_send_config_files('SSH', 'config-file')
    srv_control.start_srv('DHCP', 'started')

    misc.test_procedure()
    srv_msg.client_requests_option('7')
    srv_msg.client_does_include('Client', None, 'client-id')
    srv_msg.client_does_include('Client', None, 'IA-NA')
    srv_msg.client_send_msg('SOLICIT')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', None, 'ADVERTISE')
    srv_msg.response_check_include_option('Response', None, '3')
    srv_msg.response_check_option_content('Response', '3', None, 'sub-option', '5')

    misc.test_procedure()
    srv_msg.client_copy_option('IA_NA')
    srv_msg.client_copy_option('server-id')
    srv_msg.client_does_include('Client', None, 'client-id')
    srv_msg.client_send_msg('REQUEST')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', None, 'REPLY')

    misc.test_procedure()
    srv_msg.unicast_addres(None, 'LINK_LOCAL')
    srv_msg.client_save_option('IA_NA')
    srv_msg.client_add_saved_option('DONT ')
    srv_msg.client_does_include('Client', None, 'client-id')
    srv_msg.client_send_msg('REBIND')

    misc.pass_criteria()
    srv_msg.send_dont_wait_for_message()

    misc.test_procedure()
    srv_msg.client_add_saved_option(None)
    srv_msg.client_does_include('Client', None, 'client-id')
    srv_msg.client_send_msg('REBIND')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', None, 'REPLY')
    srv_msg.response_check_include_option('Response', None, '1')
    srv_msg.response_check_include_option('Response', None, '2')
    srv_msg.response_check_include_option('Response', None, '3')

    references.references_check('RFC3315')


@pytest.mark.basic
@pytest.mark.v6
@pytest.mark.dhcp6
@pytest.mark.unicast
def test_v6_basic_message_unicast_local_inforequest():
    #  Server MUST discard any Information-Request it receives with
    #  a unicast address destination.
    #  Message details 		Client		Server
    #  LINK_LOCAL
    #  UNICAST dest		   INFOREQUEST -->
    # 					  		       X	REPLY
    #  correct message 	   INFOREQUEST -->
    # 					  		       <--	REPLY
    #  Pass Criteria:
    #  				REPLY MUST include option:
    # 					client-id
    # 					server-id

    misc.test_setup()
    srv_control.config_srv_subnet('3000::/64', '3000::1-3000::ff')
    srv_control.config_srv_opt('preference', '123')
    srv_control.build_and_send_config_files('SSH', 'config-file')
    srv_control.start_srv('DHCP', 'started')

    misc.test_procedure()
    srv_msg.client_requests_option('7')
    srv_msg.unicast_addres(None, 'LINK_LOCAL')
    # message wont contain client-id option
    srv_msg.client_send_msg('INFOREQUEST')

    misc.pass_criteria()
    srv_msg.send_dont_wait_for_message()

    misc.test_procedure()
    srv_msg.client_requests_option('7')
    # message wont contain client-id option
    srv_msg.client_send_msg('INFOREQUEST')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', None, 'REPLY')
    srv_msg.response_check_include_option('Response', 'NOT ', '1')
    srv_msg.response_check_include_option('Response', None, '2')
    srv_msg.response_check_include_option('Response', None, '7')

    references.references_check('RFC3315')


@pytest.mark.basic
@pytest.mark.v6
@pytest.mark.dhcp6
@pytest.mark.unicast
@pytest.mark.status_code
@pytest.mark.disabled
def test_v6_basic_message_unicast_local_request():
    #  Server MUST discard any Request message it receives with
    #  a unicast address destination, and send back REPLY with
    #  UseMulticast status code.
    #  In this test if it fails with 'NoAddrAvail' at the end
    #  it means that server has send back REPLY with UseMulticast
    #  status code but also assigned address.
    #  Message details		Client		Server
    #  						SOLICIT -->
    #  		   						<--	ADVERTISE
    #  LINK_LOCAL
    #  UNICAST dest			REQUEST -->
    #  		   						<--	REPLY
    #  Pass Criteria:
    #  				REPLY MUST include option:
    # 					client-id
    # 					server-id
    # 					status code option with UseMulticast
    #
    #  						SOLICIT -->
    #  		   						<--	ADVERTISE
    #  correct message		REQUEST -->
    #  		   						<--	REPLY
    #  				REPLY MUST include option:
    # 					client-id
    # 					server-id
    # 					IA_NA
    # 					IA_Address with address 3000::1.

    misc.test_setup()
    srv_control.config_srv_subnet('3000::/64', '3000::1-3000::1')
    srv_control.build_and_send_config_files('SSH', 'config-file')
    srv_control.start_srv('DHCP', 'started')

    misc.test_procedure()
    srv_msg.client_requests_option('7')
    srv_msg.client_does_include('Client', None, 'client-id')
    srv_msg.client_does_include('Client', None, 'IA-NA')
    srv_msg.client_send_msg('SOLICIT')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', None, 'ADVERTISE')
    srv_msg.response_check_include_option('Response', None, '3')
    srv_msg.response_check_option_content('Response', '3', None, 'sub-option', '5')

    misc.test_procedure()
    srv_msg.client_save_option('server-id')
    srv_msg.client_save_option('IA_NA')
    srv_msg.client_add_saved_option('DONT ')
    srv_msg.unicast_addres(None, 'LINK_LOCAL')
    srv_msg.client_does_include('Client', None, 'client-id')
    srv_msg.client_send_msg('REQUEST')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', None, 'REPLY')
    srv_msg.response_check_include_option('Response', None, '13')
    srv_msg.response_check_option_content('Response', '13', None, 'statuscode', '5')

    misc.test_procedure()
    srv_msg.client_add_saved_option('DONT ')
    srv_msg.client_does_include('Client', None, 'client-id')
    srv_msg.client_send_msg('REQUEST')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', None, 'REPLY')
    srv_msg.response_check_include_option('Response', None, '3')
    srv_msg.response_check_option_content('Response', '3', None, 'sub-option', '5')
    srv_msg.response_check_suboption_content('Response', '5', '3', None, 'address', '3000::1')

    references.references_check('RFC3315')


@pytest.mark.basic
@pytest.mark.v6
@pytest.mark.dhcp6
@pytest.mark.unicast
@pytest.mark.status_code
@pytest.mark.disabled
def test_v6_basic_message_unicast_local_renew():
    #  Server MUST discard any RENEW message it receives with
    #  a unicast address destination, and send back REPLY with
    #  UseMulticast status code.
    #  Message details 		Client		Server
    #  						SOLICIT -->
    #  		   						<--	ADVERTISE
    #  						REQUEST -->
    #  		   						<--	REPLY
    #  LINK_LOCAL
    #  UNICAST dest			  RENEW -->
    # 					  		    <--	REPLY
    #  Pass Criteria:
    #  				REPLY MUST include option:
    # 					client-id
    # 					server-id
    # 					status code with UseMulticast
    #  correct message 		  RENEW -->
    # 					  		    <--	REPLY
    #  Pass Criteria:
    #  				REPLY MUST include option:
    # 					client-id
    # 					server-id
    # 					IA-NA
    # 					IA-Address
    misc.test_setup()
    srv_control.config_srv_subnet('3000::/64', '3000::1-3000::ff')
    srv_control.build_and_send_config_files('SSH', 'config-file')
    srv_control.start_srv('DHCP', 'started')

    misc.test_procedure()
    srv_msg.client_requests_option('7')
    srv_msg.client_does_include('Client', None, 'client-id')
    srv_msg.client_does_include('Client', None, 'IA-NA')
    srv_msg.client_send_msg('SOLICIT')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', None, 'ADVERTISE')

    misc.test_procedure()
    srv_msg.client_copy_option('IA_NA')
    srv_msg.client_copy_option('server-id')
    srv_msg.client_does_include('Client', None, 'client-id')
    srv_msg.client_send_msg('REQUEST')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', None, 'REPLY')

    misc.test_procedure()
    srv_msg.unicast_addres(None, 'LINK_LOCAL')
    srv_msg.client_save_option('IA_NA')
    srv_msg.client_save_option('server-id')
    srv_msg.client_add_saved_option('DONT ')
    srv_msg.client_does_include('Client', None, 'client-id')
    srv_msg.client_send_msg('RENEW')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', None, 'REPLY')
    srv_msg.response_check_include_option('Response', None, '13')
    srv_msg.response_check_option_content('Response', '13', None, 'statuscode', '5')

    misc.test_procedure()
    srv_msg.client_add_saved_option(None)
    srv_msg.client_does_include('Client', None, 'client-id')
    srv_msg.client_send_msg('RENEW')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', None, 'REPLY')
    srv_msg.response_check_include_option('Response', None, '1')
    srv_msg.response_check_include_option('Response', None, '2')
    srv_msg.response_check_include_option('Response', None, '3')
    srv_msg.response_check_option_content('Response', '3', None, 'sub-option', '5')

    references.references_check('RFC3315')


@pytest.mark.basic
@pytest.mark.v6
@pytest.mark.dhcp6
@pytest.mark.unicast
@pytest.mark.status_code
@pytest.mark.disabled
def test_v6_basic_message_unicast_local_release():
    #  Server MUST discard any RELEASE message it receives with
    #  a unicast address destination, and send back REPLY with
    #  UseMulticast status code.
    #
    #  Message details 		Client		Server
    #  						SOLICIT -->
    #  		   						<--	ADVERTISE
    #  						REQUEST -->
    #  		   						<--	REPLY
    #  LINK_LOCAL
    #  UNICAST dest			RELEASE -->
    # 					  		    <--	REPLY
    #  Pass Criteria:
    #  				REPLY MUST include option:
    # 					client-id
    # 					server-id
    # 					status-code with UseMulticast
    #  correct message 		RELEASE -->
    # 					  		    <--	REPLY
    #  Pass Criteria:
    #  				REPLY MUST include option:
    # 					client-id
    # 					server-id
    # 					status-code with Success
    misc.test_setup()
    srv_control.config_srv_subnet('3000::/64', '3000::1-3000::ff')
    srv_control.build_and_send_config_files('SSH', 'config-file')
    srv_control.start_srv('DHCP', 'started')

    misc.test_procedure()
    srv_msg.client_requests_option('7')
    srv_msg.client_does_include('Client', None, 'client-id')
    srv_msg.client_does_include('Client', None, 'IA-NA')
    srv_msg.client_send_msg('SOLICIT')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', None, 'ADVERTISE')

    misc.test_procedure()
    srv_msg.client_copy_option('IA_NA')
    srv_msg.client_copy_option('server-id')
    srv_msg.client_does_include('Client', None, 'client-id')
    srv_msg.client_send_msg('REQUEST')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', None, 'REPLY')

    misc.test_procedure()
    srv_msg.unicast_addres(None, 'LINK_LOCAL')
    srv_msg.client_save_option('IA_NA')
    srv_msg.client_save_option('server-id')
    srv_msg.client_add_saved_option('DONT ')
    srv_msg.client_does_include('Client', None, 'client-id')
    srv_msg.client_send_msg('RELEASE')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', None, 'REPLY')
    srv_msg.response_check_include_option('Response', None, '13')
    srv_msg.response_check_option_content('Response', '13', None, 'statuscode', '5')

    misc.test_procedure()
    srv_msg.client_add_saved_option(None)
    srv_msg.client_does_include('Client', None, 'client-id')
    srv_msg.client_send_msg('RELEASE')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', None, 'REPLY')
    srv_msg.response_check_include_option('Response', None, '1')
    srv_msg.response_check_include_option('Response', None, '2')
    srv_msg.response_check_include_option('Response', None, '13')

    references.references_check('RFC3315')
