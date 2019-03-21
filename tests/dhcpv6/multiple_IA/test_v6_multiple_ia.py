"""Multiple Identity Association Option in single DHCPv6 message"""

# pylint: disable=invalid-name,line-too-long

import pytest

import srv_msg
import srv_control
import misc


@pytest.mark.v6
@pytest.mark.dhcp6
@pytest.mark.multipleIA
def test_v6_multipleIA_addresses():
    #  Testing server ability to parse and allocate addresses
    #  when multiple IA option are included in one message.
    #  					Client		Server
    #  					SOLICIT -->
    #  save IA_NA				<--	ADVERTISE
    #  					SOLICIT -->
    #  save IA_NA				<--	ADVERTISE
    #  					SOLICIT -->
    #  save IA_NA				<--	ADVERTISE
    #  include all IA's REQUEST -->
    #  				 		    <--	REPLY
    #  Pass Criteria:
    #  				REPLY MUST include option:
    # 					IA-NA
    # 					IA-Address with 3000::1 address
    # 					IA-Address with 3000::2 address
    # 					IA-Address with 3000::3 address
    misc.test_setup()
    srv_control.config_srv_subnet('3000::/64', '3000::1-3000::3')
    srv_control.build_and_send_config_files('SSH', 'config-file')
    srv_control.start_srv('DHCP', 'started')

    misc.test_procedure()
    srv_msg.client_does_include('Client', None, 'client-id')
    srv_msg.client_does_include('Client', None, 'IA-NA')
    srv_msg.client_send_msg('SOLICIT')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', None, 'ADVERTISE')
    srv_msg.response_check_include_option('Response', None, '3')
    srv_msg.response_check_option_content('Response', '3', None, 'sub-option', '5')

    misc.test_procedure()
    srv_msg.client_save_option('IA_NA')
    srv_msg.generate_new('IA')
    srv_msg.client_requests_option('7')
    srv_msg.client_does_include('Client', None, 'client-id')
    srv_msg.client_does_include('Client', None, 'IA-NA')
    srv_msg.client_send_msg('SOLICIT')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', None, 'ADVERTISE')
    srv_msg.response_check_include_option('Response', None, '3')
    srv_msg.response_check_option_content('Response', '3', None, 'sub-option', '5')

    misc.test_procedure()
    srv_msg.client_save_option('IA_NA')
    srv_msg.generate_new('IA')
    srv_msg.client_requests_option('7')
    srv_msg.client_does_include('Client', None, 'client-id')
    srv_msg.client_does_include('Client', None, 'IA-NA')
    srv_msg.client_send_msg('SOLICIT')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', None, 'ADVERTISE')
    srv_msg.response_check_include_option('Response', None, '3')
    srv_msg.response_check_option_content('Response', '3', None, 'sub-option', '5')

    misc.test_procedure()
    srv_msg.client_save_option('IA_NA')
    srv_msg.client_copy_option('server-id')
    srv_msg.client_add_saved_option(None)
    srv_msg.client_does_include('Client', None, 'client-id')
    srv_msg.client_send_msg('REQUEST')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', None, 'REPLY')
    srv_msg.response_check_include_option('Response', None, '3')
    srv_msg.response_check_option_content('Response', '3', None, 'sub-option', '5')
    srv_msg.response_check_suboption_content('Response', '5', '3', None, 'addr', '3000::1')
    srv_msg.response_check_suboption_content('Response', '5', '3', None, 'addr', '3000::2')
    srv_msg.response_check_suboption_content('Response', '5', '3', None, 'addr', '3000::3')


@pytest.mark.v6
@pytest.mark.dhcp6
@pytest.mark.multipleIA
def test_v6_multipleIA_addresses_multiple_pools():
    #  Testing server ability to parse and allocate addresses
    #  when multiple IA option are included in one message.
    #  Server is configured with multiple pools within single subnet
    #  					Client		Server
    #  					SOLICIT -->
    #  save IA_NA				<--	ADVERTISE
    #  					SOLICIT -->
    #  save IA_NA				<--	ADVERTISE
    #  					SOLICIT -->
    #  save IA_NA				<--	ADVERTISE
    #  include all IA's REQUEST -->
    #  				 		    <--	REPLY
    #  Pass Criteria:
    #  				REPLY MUST include option:
    # 					IA-NA
    # 					IA-Address with 3000::1 address
    # 					IA-Address with 3000::2 address
    # 					IA-Address with 3000::3 address
    misc.test_setup()
    srv_control.config_srv_subnet('3000::/64', '3000::1-3000::1')
    srv_control.new_pool('3000::2-3000::2', '0')
    srv_control.new_pool('3000::3-3000::3', '0')
    srv_control.build_and_send_config_files('SSH', 'config-file')
    srv_control.start_srv('DHCP', 'started')

    misc.test_procedure()
    srv_msg.client_does_include('Client', None, 'client-id')
    srv_msg.client_does_include('Client', None, 'IA-NA')
    srv_msg.client_send_msg('SOLICIT')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', None, 'ADVERTISE')
    srv_msg.response_check_include_option('Response', None, '3')
    srv_msg.response_check_option_content('Response', '3', None, 'sub-option', '5')

    misc.test_procedure()
    srv_msg.client_save_option('IA_NA')
    srv_msg.generate_new('IA')
    srv_msg.client_requests_option('7')
    srv_msg.client_does_include('Client', None, 'client-id')
    srv_msg.client_does_include('Client', None, 'IA-NA')
    srv_msg.client_send_msg('SOLICIT')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', None, 'ADVERTISE')
    srv_msg.response_check_include_option('Response', None, '3')
    srv_msg.response_check_option_content('Response', '3', None, 'sub-option', '5')

    misc.test_procedure()
    srv_msg.client_save_option('IA_NA')
    srv_msg.generate_new('IA')
    srv_msg.client_requests_option('7')
    srv_msg.client_does_include('Client', None, 'client-id')
    srv_msg.client_does_include('Client', None, 'IA-NA')
    srv_msg.client_send_msg('SOLICIT')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', None, 'ADVERTISE')
    srv_msg.response_check_include_option('Response', None, '3')
    srv_msg.response_check_option_content('Response', '3', None, 'sub-option', '5')

    misc.test_procedure()
    srv_msg.client_save_option('IA_NA')
    srv_msg.client_copy_option('server-id')
    srv_msg.client_add_saved_option(None)
    srv_msg.client_does_include('Client', None, 'client-id')
    srv_msg.client_send_msg('REQUEST')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', None, 'REPLY')
    srv_msg.response_check_include_option('Response', None, '3')
    srv_msg.response_check_option_content('Response', '3', None, 'sub-option', '5')
    srv_msg.response_check_suboption_content('Response', '5', '3', None, 'addr', '3000::1')
    srv_msg.response_check_suboption_content('Response', '5', '3', None, 'addr', '3000::2')
    srv_msg.response_check_suboption_content('Response', '5', '3', None, 'addr', '3000::3')


@pytest.mark.v6
@pytest.mark.dhcp6
@pytest.mark.multipleIA
def test_v6_multipleIA_addresses_release_success():
    #  Testing server ability to parse multiple IA's included into message
    #  and release included addresses.
    #  					Client		Server
    #  					SOLICIT -->
    #  							<--	ADVERTISE
    #  					REQUEST -->
    #  save IA_NA	 		    <--	REPLY
    #  new IA			SOLICIT -->
    #  							<--	ADVERTISE
    #  					REQUEST -->
    #  save IA_NA	 		    <--	REPLY
    #  new IA			SOLICIT -->
    #  							<--	ADVERTISE
    #  					REQUEST -->
    #  save IA_NA	 		    <--	REPLY
    #  include all IA'a RELEASE -->
    #  							<--	REPLY
    #  Pass Criteria:
    #  				REPLY MUST include option:
    # 					Status code 'success'
    misc.test_setup()
    srv_control.config_srv_subnet('3000::/64', '3000::1-3000::3')
    srv_control.build_and_send_config_files('SSH', 'config-file')
    srv_control.start_srv('DHCP', 'started')

    misc.test_procedure()
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
    srv_msg.client_save_option('IA_NA')
    srv_msg.generate_new('IA')
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
    srv_msg.client_save_option('IA_NA')
    srv_msg.generate_new('IA')
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
    srv_msg.client_save_option('IA_NA')
    srv_msg.client_copy_option('server-id')
    srv_msg.client_add_saved_option('DONT ')
    srv_msg.client_does_include('Client', None, 'client-id')
    srv_msg.client_send_msg('RELEASE')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', None, 'REPLY')
    srv_msg.response_check_include_option('Response', None, '13')
    srv_msg.response_check_option_content('Response', '13', None, 'status-code', '0')


@pytest.mark.v6
@pytest.mark.dhcp6
@pytest.mark.multipleIA
def test_v6_multipleIA_addresses_release_partial_success():
    #  Testing server ability to parse multiple IA's included into message
    #  and release included addresses. One of the IA's are released twice.
    #  first time: success, next: NoBinding
    #  					Client		Server
    #  					SOLICIT -->
    #  							<--	ADVERTISE
    #  					REQUEST -->
    #  save IA_NA	 		    <--	REPLY
    #  new IA			SOLICIT -->
    #  							<--	ADVERTISE
    #  					REQUEST -->
    #  save IA_NA	 		    <--	REPLY
    #  new IA			SOLICIT -->
    #  							<--	ADVERTISE
    #  					REQUEST -->
    #  save IA_NA	 		    <--	REPLY
    #  include last IA_NA RELEASE -->
    #  							<--	REPLY
    #  Pass Criteria:
    #  				REPLY MUST include option:
    # 					Status code 'success'
    #
    #  include all IA_NA's RELEASE -->
    #  							<--	REPLY
    #  Pass Criteria:
    #  				REPLY MUST include option:
    # 					IA_NA option
    # 					IA_Address with status code: NoBinding
    misc.test_setup()
    srv_control.config_srv_subnet('3000::/64', '3000::1-3000::3')
    srv_control.build_and_send_config_files('SSH', 'config-file')
    srv_control.start_srv('DHCP', 'started')

    misc.test_procedure()
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
    srv_msg.client_save_option('IA_NA')
    srv_msg.generate_new('IA')
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
    srv_msg.client_save_option('IA_NA')
    srv_msg.generate_new('IA')
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
    srv_msg.client_save_option('IA_NA')
    srv_msg.client_copy_option('IA_NA')
    srv_msg.client_copy_option('server-id')
    srv_msg.client_does_include('Client', None, 'client-id')
    srv_msg.client_send_msg('RELEASE')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', None, 'REPLY')
    srv_msg.response_check_include_option('Response', None, '13')
    srv_msg.response_check_option_content('Response', '13', None, 'status-code', '0')

    misc.test_procedure()
    srv_msg.client_copy_option('server-id')
    srv_msg.client_add_saved_option('DONT ')
    srv_msg.client_does_include('Client', None, 'client-id')
    srv_msg.client_send_msg('RELEASE')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', None, 'REPLY')
    srv_msg.response_check_include_option('Response', None, '13')
    # Response option 13 MUST contain status-code 0. IS IT TRURE? RFC 3315 is not clear about that.
    srv_msg.response_check_include_option('Response', None, '3')
    srv_msg.response_check_option_content('Response', '3', None, 'sub-option', '13')
    srv_msg.response_check_suboption_content('Response', '13', '3', None, 'statuscode', '3')


@pytest.mark.v6
@pytest.mark.dhcp6
@pytest.mark.multipleIA
def test_v6_multipleIA_addresses_rebind_partial_success():
    #  Testing servers ability to rebind two IA form three received
    #  One IA_NA released before.
    #  					Client		Server
    #  					SOLICIT -->
    #  							<--	ADVERTISE
    #  					REQUEST -->
    #  save IA_NA	 		    <--	REPLY
    #  new IA			SOLICIT -->
    #  							<--	ADVERTISE
    #  					REQUEST -->
    #  save IA_NA	 		    <--	REPLY
    #  new IA			SOLICIT -->
    #  							<--	ADVERTISE
    #  					REQUEST -->
    #  save IA_NA	 		    <--	REPLY
    #  include last IA_NA RELEASE -->
    #  							<--	REPLY
    #  include all IA_NA's REBIND -->
    #  							<--	REPLY
    #  Pass Criteria:
    #  				REPLY MUST include option:
    # 					IA_NA option (for T1/T2)
    # 					IA_Address (for lifetimes)
    # 					IA_Address (for lifetimes)
    # 					One status code/error? RFC is not clear
    # 					abut what should happen in such case.
    misc.test_setup()
    srv_control.config_srv_subnet('3000::/64', '3000::1-3000::3')
    srv_control.build_and_send_config_files('SSH', 'config-file')
    srv_control.start_srv('DHCP', 'started')

    misc.test_procedure()
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
    srv_msg.client_save_option('IA_NA')
    srv_msg.generate_new('IA')
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
    srv_msg.client_save_option('IA_NA')
    srv_msg.generate_new('IA')
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
    srv_msg.client_save_option('IA_NA')
    srv_msg.client_copy_option('IA_NA')
    srv_msg.client_copy_option('server-id')
    srv_msg.client_does_include('Client', None, 'client-id')
    srv_msg.client_send_msg('RELEASE')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', None, 'REPLY')
    srv_msg.response_check_include_option('Response', None, '13')
    srv_msg.response_check_option_content('Response', '13', None, 'status-code', '0')

    misc.test_procedure()
    srv_msg.client_add_saved_option(None)
    srv_msg.client_does_include('Client', None, 'client-id')
    srv_msg.client_send_msg('REBIND')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', None, 'REPLY')
    srv_msg.response_check_include_option('Response', None, '3')
    srv_msg.response_check_option_content('Response', '3', None, 'sub-option', '5')
    # Response option 3 MUST contain sub-option 13. changed due to RFC 7550
    # Response sub-option 13 from option 3 MUST contain statuscode 3.


@pytest.mark.v6
@pytest.mark.dhcp6
@pytest.mark.multipleIA
def test_v6_multipleIA_addresses_noaddravail():
    #  Testing server ability to assign two addresses and
    #  send one status code: NoAddrAvail in one message.
    #  					Client		Server
    #  					SOLICIT -->
    #  save IA_NA				<--	ADVERTISE
    #  new IA			SOLICIT -->
    #  save IA_NA				<--	ADVERTISE
    #  new IA			SOLICIT -->
    #  save IA_NA				<--	ADVERTISE
    #  with all IA_NA's	REQUEST -->
    #  				 		    <--	REPLY
    #  Pass Criteria:
    #  				REPLY MUST include option:
    # 					IA_NA option
    # 					IA_Address with address 3000::1
    # 					IA_Address with address 3000::2
    # 					IA_NA with status code: NoAddrAvail

    misc.test_setup()
    srv_control.config_srv_subnet('3000::/64', '3000::1-3000::2')
    srv_control.build_and_send_config_files('SSH', 'config-file')
    srv_control.start_srv('DHCP', 'started')

    misc.test_procedure()
    srv_msg.client_does_include('Client', None, 'client-id')
    srv_msg.client_does_include('Client', None, 'IA-NA')
    srv_msg.client_send_msg('SOLICIT')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', None, 'ADVERTISE')
    srv_msg.response_check_include_option('Response', None, '3')
    srv_msg.response_check_option_content('Response', '3', None, 'sub-option', '5')

    misc.test_procedure()
    srv_msg.client_save_option('IA_NA')
    srv_msg.generate_new('IA')
    srv_msg.client_requests_option('7')
    srv_msg.client_does_include('Client', None, 'client-id')
    srv_msg.client_does_include('Client', None, 'IA-NA')
    srv_msg.client_send_msg('SOLICIT')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', None, 'ADVERTISE')
    srv_msg.response_check_include_option('Response', None, '3')
    srv_msg.response_check_option_content('Response', '3', None, 'sub-option', '5')

    misc.test_procedure()
    srv_msg.client_save_option('IA_NA')
    srv_msg.generate_new('IA')
    srv_msg.client_requests_option('7')
    srv_msg.client_does_include('Client', None, 'client-id')
    srv_msg.client_does_include('Client', None, 'IA-NA')
    srv_msg.client_send_msg('SOLICIT')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', None, 'ADVERTISE')
    srv_msg.response_check_include_option('Response', None, '3')
    srv_msg.response_check_option_content('Response', '3', None, 'sub-option', '5')

    misc.test_procedure()
    srv_msg.client_save_option('IA_NA')
    srv_msg.client_copy_option('server-id')
    srv_msg.client_add_saved_option('DONT ')
    srv_msg.client_does_include('Client', None, 'client-id')
    srv_msg.client_send_msg('REQUEST')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', None, 'REPLY')
    srv_msg.response_check_include_option('Response', None, '3')
    srv_msg.response_check_option_content('Response', '3', None, 'sub-option', '5')
    srv_msg.response_check_suboption_content('Response', '5', '3', None, 'addr', '3000::1')
    srv_msg.response_check_suboption_content('Response', '5', '3', None, 'addr', '3000::2')
    srv_msg.response_check_option_content('Response', '3', None, 'sub-option', '13')
    srv_msg.response_check_suboption_content('Response', '13', '3', None, 'statuscode', '2')
