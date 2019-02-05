"""Multiple Identity Association Option in single DHCPv6 message"""

# pylint: disable=invalid-name,line-too-long

import pytest

from features import srv_control
from features import srv_msg
from features import misc


@pytest.mark.v6
@pytest.mark.dhcp6
@pytest.mark.multipleIA
def test_v6_multipleIA_addresses(step):
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
    misc.test_setup(step)
    srv_control.config_srv_subnet(step, '3000::/64', '3000::1-3000::3')
    srv_control.build_and_send_config_files(step, 'SSH', 'config-file')
    srv_control.start_srv(step, 'DHCP', 'started')

    misc.test_procedure(step)
    srv_msg.client_does_include(step, 'Client', None, 'client-id')
    srv_msg.client_does_include(step, 'Client', None, 'IA-NA')
    srv_msg.client_send_msg(step, 'SOLICIT')

    misc.pass_criteria(step)
    srv_msg.send_wait_for_message(step, 'MUST', None, 'ADVERTISE')
    srv_msg.response_check_include_option(step, 'Response', None, '3')
    srv_msg.response_check_option_content(step, 'Response', '3', None, 'sub-option', '5')

    misc.test_procedure(step)
    srv_msg.client_save_option(step, 'IA_NA')
    srv_msg.generate_new(step, 'IA')
    srv_msg.client_requests_option(step, '7')
    srv_msg.client_does_include(step, 'Client', None, 'client-id')
    srv_msg.client_does_include(step, 'Client', None, 'IA-NA')
    srv_msg.client_send_msg(step, 'SOLICIT')

    misc.pass_criteria(step)
    srv_msg.send_wait_for_message(step, 'MUST', None, 'ADVERTISE')
    srv_msg.response_check_include_option(step, 'Response', None, '3')
    srv_msg.response_check_option_content(step, 'Response', '3', None, 'sub-option', '5')

    misc.test_procedure(step)
    srv_msg.client_save_option(step, 'IA_NA')
    srv_msg.generate_new(step, 'IA')
    srv_msg.client_requests_option(step, '7')
    srv_msg.client_does_include(step, 'Client', None, 'client-id')
    srv_msg.client_does_include(step, 'Client', None, 'IA-NA')
    srv_msg.client_send_msg(step, 'SOLICIT')

    misc.pass_criteria(step)
    srv_msg.send_wait_for_message(step, 'MUST', None, 'ADVERTISE')
    srv_msg.response_check_include_option(step, 'Response', None, '3')
    srv_msg.response_check_option_content(step, 'Response', '3', None, 'sub-option', '5')

    misc.test_procedure(step)
    srv_msg.client_save_option(step, 'IA_NA')
    srv_msg.client_copy_option(step, 'server-id')
    srv_msg.client_add_saved_option(step, None)
    srv_msg.client_does_include(step, 'Client', None, 'client-id')
    srv_msg.client_send_msg(step, 'REQUEST')

    misc.pass_criteria(step)
    srv_msg.send_wait_for_message(step, 'MUST', None, 'REPLY')
    srv_msg.response_check_include_option(step, 'Response', None, '3')
    srv_msg.response_check_option_content(step, 'Response', '3', None, 'sub-option', '5')
    srv_msg.response_check_suboption_content(step,
                                             'Response',
                                             '5',
                                             '3',
                                             None,
                                             'address',
                                             '3000::1')
    srv_msg.response_check_suboption_content(step,
                                             'Response',
                                             '5',
                                             '3',
                                             None,
                                             'address',
                                             '3000::2')
    srv_msg.response_check_suboption_content(step,
                                             'Response',
                                             '5',
                                             '3',
                                             None,
                                             'address',
                                             '3000::3')


@pytest.mark.v6
@pytest.mark.dhcp6
@pytest.mark.multipleIA
def test_v6_multipleIA_addresses_multiple_pools(step):
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
    misc.test_setup(step)
    srv_control.config_srv_subnet(step, '3000::/64', '3000::1-3000::1')
    srv_control.new_pool(step, '3000::2-3000::2', '0')
    srv_control.new_pool(step, '3000::3-3000::3', '0')
    srv_control.build_and_send_config_files(step, 'SSH', 'config-file')
    srv_control.start_srv(step, 'DHCP', 'started')

    misc.test_procedure(step)
    srv_msg.client_does_include(step, 'Client', None, 'client-id')
    srv_msg.client_does_include(step, 'Client', None, 'IA-NA')
    srv_msg.client_send_msg(step, 'SOLICIT')

    misc.pass_criteria(step)
    srv_msg.send_wait_for_message(step, 'MUST', None, 'ADVERTISE')
    srv_msg.response_check_include_option(step, 'Response', None, '3')
    srv_msg.response_check_option_content(step, 'Response', '3', None, 'sub-option', '5')

    misc.test_procedure(step)
    srv_msg.client_save_option(step, 'IA_NA')
    srv_msg.generate_new(step, 'IA')
    srv_msg.client_requests_option(step, '7')
    srv_msg.client_does_include(step, 'Client', None, 'client-id')
    srv_msg.client_does_include(step, 'Client', None, 'IA-NA')
    srv_msg.client_send_msg(step, 'SOLICIT')

    misc.pass_criteria(step)
    srv_msg.send_wait_for_message(step, 'MUST', None, 'ADVERTISE')
    srv_msg.response_check_include_option(step, 'Response', None, '3')
    srv_msg.response_check_option_content(step, 'Response', '3', None, 'sub-option', '5')

    misc.test_procedure(step)
    srv_msg.client_save_option(step, 'IA_NA')
    srv_msg.generate_new(step, 'IA')
    srv_msg.client_requests_option(step, '7')
    srv_msg.client_does_include(step, 'Client', None, 'client-id')
    srv_msg.client_does_include(step, 'Client', None, 'IA-NA')
    srv_msg.client_send_msg(step, 'SOLICIT')

    misc.pass_criteria(step)
    srv_msg.send_wait_for_message(step, 'MUST', None, 'ADVERTISE')
    srv_msg.response_check_include_option(step, 'Response', None, '3')
    srv_msg.response_check_option_content(step, 'Response', '3', None, 'sub-option', '5')

    misc.test_procedure(step)
    srv_msg.client_save_option(step, 'IA_NA')
    srv_msg.client_copy_option(step, 'server-id')
    srv_msg.client_add_saved_option(step, None)
    srv_msg.client_does_include(step, 'Client', None, 'client-id')
    srv_msg.client_send_msg(step, 'REQUEST')

    misc.pass_criteria(step)
    srv_msg.send_wait_for_message(step, 'MUST', None, 'REPLY')
    srv_msg.response_check_include_option(step, 'Response', None, '3')
    srv_msg.response_check_option_content(step, 'Response', '3', None, 'sub-option', '5')
    srv_msg.response_check_suboption_content(step,
                                             'Response',
                                             '5',
                                             '3',
                                             None,
                                             'address',
                                             '3000::1')
    srv_msg.response_check_suboption_content(step,
                                             'Response',
                                             '5',
                                             '3',
                                             None,
                                             'address',
                                             '3000::2')
    srv_msg.response_check_suboption_content(step,
                                             'Response',
                                             '5',
                                             '3',
                                             None,
                                             'address',
                                             '3000::3')


@pytest.mark.v6
@pytest.mark.dhcp6
@pytest.mark.multipleIA
def test_v6_multipleIA_addresses_release_success(step):
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
    misc.test_setup(step)
    srv_control.config_srv_subnet(step, '3000::/64', '3000::1-3000::3')
    srv_control.build_and_send_config_files(step, 'SSH', 'config-file')
    srv_control.start_srv(step, 'DHCP', 'started')

    misc.test_procedure(step)
    srv_msg.client_does_include(step, 'Client', None, 'client-id')
    srv_msg.client_does_include(step, 'Client', None, 'IA-NA')
    srv_msg.client_send_msg(step, 'SOLICIT')

    misc.pass_criteria(step)
    srv_msg.send_wait_for_message(step, 'MUST', None, 'ADVERTISE')
    srv_msg.response_check_include_option(step, 'Response', None, '3')
    srv_msg.response_check_option_content(step, 'Response', '3', None, 'sub-option', '5')

    misc.test_procedure(step)
    srv_msg.client_copy_option(step, 'IA_NA')
    srv_msg.client_copy_option(step, 'server-id')
    srv_msg.client_does_include(step, 'Client', None, 'client-id')
    srv_msg.client_send_msg(step, 'REQUEST')

    misc.pass_criteria(step)
    srv_msg.send_wait_for_message(step, 'MUST', None, 'REPLY')

    misc.test_procedure(step)
    srv_msg.client_save_option(step, 'IA_NA')
    srv_msg.generate_new(step, 'IA')
    srv_msg.client_does_include(step, 'Client', None, 'client-id')
    srv_msg.client_does_include(step, 'Client', None, 'IA-NA')
    srv_msg.client_send_msg(step, 'SOLICIT')

    misc.pass_criteria(step)
    srv_msg.send_wait_for_message(step, 'MUST', None, 'ADVERTISE')
    srv_msg.response_check_include_option(step, 'Response', None, '3')
    srv_msg.response_check_option_content(step, 'Response', '3', None, 'sub-option', '5')

    misc.test_procedure(step)
    srv_msg.client_copy_option(step, 'IA_NA')
    srv_msg.client_copy_option(step, 'server-id')
    srv_msg.client_does_include(step, 'Client', None, 'client-id')
    srv_msg.client_send_msg(step, 'REQUEST')

    misc.pass_criteria(step)
    srv_msg.send_wait_for_message(step, 'MUST', None, 'REPLY')

    misc.test_procedure(step)
    srv_msg.client_save_option(step, 'IA_NA')
    srv_msg.generate_new(step, 'IA')
    srv_msg.client_does_include(step, 'Client', None, 'client-id')
    srv_msg.client_does_include(step, 'Client', None, 'IA-NA')
    srv_msg.client_send_msg(step, 'SOLICIT')

    misc.pass_criteria(step)
    srv_msg.send_wait_for_message(step, 'MUST', None, 'ADVERTISE')
    srv_msg.response_check_include_option(step, 'Response', None, '3')
    srv_msg.response_check_option_content(step, 'Response', '3', None, 'sub-option', '5')

    misc.test_procedure(step)
    srv_msg.client_copy_option(step, 'IA_NA')
    srv_msg.client_copy_option(step, 'server-id')
    srv_msg.client_does_include(step, 'Client', None, 'client-id')
    srv_msg.client_send_msg(step, 'REQUEST')

    misc.pass_criteria(step)
    srv_msg.send_wait_for_message(step, 'MUST', None, 'REPLY')

    misc.test_procedure(step)
    srv_msg.client_save_option(step, 'IA_NA')
    srv_msg.client_copy_option(step, 'server-id')
    srv_msg.client_add_saved_option(step, 'DONT ')
    srv_msg.client_does_include(step, 'Client', None, 'client-id')
    srv_msg.client_send_msg(step, 'RELEASE')

    misc.pass_criteria(step)
    srv_msg.send_wait_for_message(step, 'MUST', None, 'REPLY')
    srv_msg.response_check_include_option(step, 'Response', None, '13')
    srv_msg.response_check_option_content(step, 'Response', '13', None, 'status-code', '0')


@pytest.mark.v6
@pytest.mark.dhcp6
@pytest.mark.multipleIA
def test_v6_multipleIA_addresses_release_partial_success(step):
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
    misc.test_setup(step)
    srv_control.config_srv_subnet(step, '3000::/64', '3000::1-3000::3')
    srv_control.build_and_send_config_files(step, 'SSH', 'config-file')
    srv_control.start_srv(step, 'DHCP', 'started')

    misc.test_procedure(step)
    srv_msg.client_does_include(step, 'Client', None, 'client-id')
    srv_msg.client_does_include(step, 'Client', None, 'IA-NA')
    srv_msg.client_send_msg(step, 'SOLICIT')

    misc.pass_criteria(step)
    srv_msg.send_wait_for_message(step, 'MUST', None, 'ADVERTISE')
    srv_msg.response_check_include_option(step, 'Response', None, '3')
    srv_msg.response_check_option_content(step, 'Response', '3', None, 'sub-option', '5')

    misc.test_procedure(step)
    srv_msg.client_copy_option(step, 'IA_NA')
    srv_msg.client_copy_option(step, 'server-id')
    srv_msg.client_does_include(step, 'Client', None, 'client-id')
    srv_msg.client_send_msg(step, 'REQUEST')

    misc.pass_criteria(step)
    srv_msg.send_wait_for_message(step, 'MUST', None, 'REPLY')

    misc.test_procedure(step)
    srv_msg.client_save_option(step, 'IA_NA')
    srv_msg.generate_new(step, 'IA')
    srv_msg.client_does_include(step, 'Client', None, 'client-id')
    srv_msg.client_does_include(step, 'Client', None, 'IA-NA')
    srv_msg.client_send_msg(step, 'SOLICIT')

    misc.pass_criteria(step)
    srv_msg.send_wait_for_message(step, 'MUST', None, 'ADVERTISE')
    srv_msg.response_check_include_option(step, 'Response', None, '3')
    srv_msg.response_check_option_content(step, 'Response', '3', None, 'sub-option', '5')

    misc.test_procedure(step)
    srv_msg.client_copy_option(step, 'IA_NA')
    srv_msg.client_copy_option(step, 'server-id')
    srv_msg.client_does_include(step, 'Client', None, 'client-id')
    srv_msg.client_send_msg(step, 'REQUEST')

    misc.pass_criteria(step)
    srv_msg.send_wait_for_message(step, 'MUST', None, 'REPLY')

    misc.test_procedure(step)
    srv_msg.client_save_option(step, 'IA_NA')
    srv_msg.generate_new(step, 'IA')
    srv_msg.client_does_include(step, 'Client', None, 'client-id')
    srv_msg.client_does_include(step, 'Client', None, 'IA-NA')
    srv_msg.client_send_msg(step, 'SOLICIT')

    misc.pass_criteria(step)
    srv_msg.send_wait_for_message(step, 'MUST', None, 'ADVERTISE')
    srv_msg.response_check_include_option(step, 'Response', None, '3')
    srv_msg.response_check_option_content(step, 'Response', '3', None, 'sub-option', '5')

    misc.test_procedure(step)
    srv_msg.client_copy_option(step, 'IA_NA')
    srv_msg.client_copy_option(step, 'server-id')
    srv_msg.client_does_include(step, 'Client', None, 'client-id')
    srv_msg.client_send_msg(step, 'REQUEST')

    misc.pass_criteria(step)
    srv_msg.send_wait_for_message(step, 'MUST', None, 'REPLY')

    misc.test_procedure(step)
    srv_msg.client_save_option(step, 'IA_NA')
    srv_msg.client_copy_option(step, 'IA_NA')
    srv_msg.client_copy_option(step, 'server-id')
    srv_msg.client_does_include(step, 'Client', None, 'client-id')
    srv_msg.client_send_msg(step, 'RELEASE')

    misc.pass_criteria(step)
    srv_msg.send_wait_for_message(step, 'MUST', None, 'REPLY')
    srv_msg.response_check_include_option(step, 'Response', None, '13')
    srv_msg.response_check_option_content(step, 'Response', '13', None, 'status-code', '0')

    misc.test_procedure(step)
    srv_msg.client_copy_option(step, 'server-id')
    srv_msg.client_add_saved_option(step, 'DONT ')
    srv_msg.client_does_include(step, 'Client', None, 'client-id')
    srv_msg.client_send_msg(step, 'RELEASE')

    misc.pass_criteria(step)
    srv_msg.send_wait_for_message(step, 'MUST', None, 'REPLY')
    srv_msg.response_check_include_option(step, 'Response', None, '13')
    # Response option 13 MUST contain status-code 0. IS IT TRURE? RFC 3315 is not clear about that.
    srv_msg.response_check_include_option(step, 'Response', None, '3')
    srv_msg.response_check_option_content(step, 'Response', '3', None, 'sub-option', '13')
    srv_msg.response_check_suboption_content(step, 'Response', '13', '3', None, 'statuscode', '3')


@pytest.mark.v6
@pytest.mark.dhcp6
@pytest.mark.multipleIA
def test_v6_multipleIA_addresses_rebind_partial_success(step):
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
    misc.test_setup(step)
    srv_control.config_srv_subnet(step, '3000::/64', '3000::1-3000::3')
    srv_control.build_and_send_config_files(step, 'SSH', 'config-file')
    srv_control.start_srv(step, 'DHCP', 'started')

    misc.test_procedure(step)
    srv_msg.client_does_include(step, 'Client', None, 'client-id')
    srv_msg.client_does_include(step, 'Client', None, 'IA-NA')
    srv_msg.client_send_msg(step, 'SOLICIT')

    misc.pass_criteria(step)
    srv_msg.send_wait_for_message(step, 'MUST', None, 'ADVERTISE')
    srv_msg.response_check_include_option(step, 'Response', None, '3')
    srv_msg.response_check_option_content(step, 'Response', '3', None, 'sub-option', '5')

    misc.test_procedure(step)
    srv_msg.client_copy_option(step, 'IA_NA')
    srv_msg.client_copy_option(step, 'server-id')
    srv_msg.client_does_include(step, 'Client', None, 'client-id')
    srv_msg.client_send_msg(step, 'REQUEST')

    misc.pass_criteria(step)
    srv_msg.send_wait_for_message(step, 'MUST', None, 'REPLY')

    misc.test_procedure(step)
    srv_msg.client_save_option(step, 'IA_NA')
    srv_msg.generate_new(step, 'IA')
    srv_msg.client_does_include(step, 'Client', None, 'client-id')
    srv_msg.client_does_include(step, 'Client', None, 'IA-NA')
    srv_msg.client_send_msg(step, 'SOLICIT')

    misc.pass_criteria(step)
    srv_msg.send_wait_for_message(step, 'MUST', None, 'ADVERTISE')
    srv_msg.response_check_include_option(step, 'Response', None, '3')
    srv_msg.response_check_option_content(step, 'Response', '3', None, 'sub-option', '5')

    misc.test_procedure(step)
    srv_msg.client_copy_option(step, 'IA_NA')
    srv_msg.client_copy_option(step, 'server-id')
    srv_msg.client_does_include(step, 'Client', None, 'client-id')
    srv_msg.client_send_msg(step, 'REQUEST')

    misc.pass_criteria(step)
    srv_msg.send_wait_for_message(step, 'MUST', None, 'REPLY')

    misc.test_procedure(step)
    srv_msg.client_save_option(step, 'IA_NA')
    srv_msg.generate_new(step, 'IA')
    srv_msg.client_does_include(step, 'Client', None, 'client-id')
    srv_msg.client_does_include(step, 'Client', None, 'IA-NA')
    srv_msg.client_send_msg(step, 'SOLICIT')

    misc.pass_criteria(step)
    srv_msg.send_wait_for_message(step, 'MUST', None, 'ADVERTISE')
    srv_msg.response_check_include_option(step, 'Response', None, '3')
    srv_msg.response_check_option_content(step, 'Response', '3', None, 'sub-option', '5')

    misc.test_procedure(step)
    srv_msg.client_copy_option(step, 'IA_NA')
    srv_msg.client_copy_option(step, 'server-id')
    srv_msg.client_does_include(step, 'Client', None, 'client-id')
    srv_msg.client_send_msg(step, 'REQUEST')

    misc.pass_criteria(step)
    srv_msg.send_wait_for_message(step, 'MUST', None, 'REPLY')

    misc.test_procedure(step)
    srv_msg.client_save_option(step, 'IA_NA')
    srv_msg.client_copy_option(step, 'IA_NA')
    srv_msg.client_copy_option(step, 'server-id')
    srv_msg.client_does_include(step, 'Client', None, 'client-id')
    srv_msg.client_send_msg(step, 'RELEASE')

    misc.pass_criteria(step)
    srv_msg.send_wait_for_message(step, 'MUST', None, 'REPLY')
    srv_msg.response_check_include_option(step, 'Response', None, '13')
    srv_msg.response_check_option_content(step, 'Response', '13', None, 'status-code', '0')

    misc.test_procedure(step)
    srv_msg.client_add_saved_option(step, None)
    srv_msg.client_does_include(step, 'Client', None, 'client-id')
    srv_msg.client_send_msg(step, 'REBIND')

    misc.pass_criteria(step)
    srv_msg.send_wait_for_message(step, 'MUST', None, 'REPLY')
    srv_msg.response_check_include_option(step, 'Response', None, '3')
    srv_msg.response_check_option_content(step, 'Response', '3', None, 'sub-option', '5')
    # Response option 3 MUST contain sub-option 13. changed due to RFC 7550
    # Response sub-option 13 from option 3 MUST contain statuscode 3.


@pytest.mark.v6
@pytest.mark.dhcp6
@pytest.mark.multipleIA
def test_v6_multipleIA_addresses_noaddravail(step):
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

    misc.test_setup(step)
    srv_control.config_srv_subnet(step, '3000::/64', '3000::1-3000::2')
    srv_control.build_and_send_config_files(step, 'SSH', 'config-file')
    srv_control.start_srv(step, 'DHCP', 'started')

    misc.test_procedure(step)
    srv_msg.client_does_include(step, 'Client', None, 'client-id')
    srv_msg.client_does_include(step, 'Client', None, 'IA-NA')
    srv_msg.client_send_msg(step, 'SOLICIT')

    misc.pass_criteria(step)
    srv_msg.send_wait_for_message(step, 'MUST', None, 'ADVERTISE')
    srv_msg.response_check_include_option(step, 'Response', None, '3')
    srv_msg.response_check_option_content(step, 'Response', '3', None, 'sub-option', '5')

    misc.test_procedure(step)
    srv_msg.client_save_option(step, 'IA_NA')
    srv_msg.generate_new(step, 'IA')
    srv_msg.client_requests_option(step, '7')
    srv_msg.client_does_include(step, 'Client', None, 'client-id')
    srv_msg.client_does_include(step, 'Client', None, 'IA-NA')
    srv_msg.client_send_msg(step, 'SOLICIT')

    misc.pass_criteria(step)
    srv_msg.send_wait_for_message(step, 'MUST', None, 'ADVERTISE')
    srv_msg.response_check_include_option(step, 'Response', None, '3')
    srv_msg.response_check_option_content(step, 'Response', '3', None, 'sub-option', '5')

    misc.test_procedure(step)
    srv_msg.client_save_option(step, 'IA_NA')
    srv_msg.generate_new(step, 'IA')
    srv_msg.client_requests_option(step, '7')
    srv_msg.client_does_include(step, 'Client', None, 'client-id')
    srv_msg.client_does_include(step, 'Client', None, 'IA-NA')
    srv_msg.client_send_msg(step, 'SOLICIT')

    misc.pass_criteria(step)
    srv_msg.send_wait_for_message(step, 'MUST', None, 'ADVERTISE')
    srv_msg.response_check_include_option(step, 'Response', None, '3')
    srv_msg.response_check_option_content(step, 'Response', '3', None, 'sub-option', '5')

    misc.test_procedure(step)
    srv_msg.client_save_option(step, 'IA_NA')
    srv_msg.client_copy_option(step, 'server-id')
    srv_msg.client_add_saved_option(step, 'DONT ')
    srv_msg.client_does_include(step, 'Client', None, 'client-id')
    srv_msg.client_send_msg(step, 'REQUEST')

    misc.pass_criteria(step)
    srv_msg.send_wait_for_message(step, 'MUST', None, 'REPLY')
    srv_msg.response_check_include_option(step, 'Response', None, '3')
    srv_msg.response_check_option_content(step, 'Response', '3', None, 'sub-option', '5')
    srv_msg.response_check_suboption_content(step,
                                             'Response',
                                             '5',
                                             '3',
                                             None,
                                             'address',
                                             '3000::1')
    srv_msg.response_check_suboption_content(step,
                                             'Response',
                                             '5',
                                             '3',
                                             None,
                                             'address',
                                             '3000::2')
    srv_msg.response_check_option_content(step, 'Response', '3', None, 'sub-option', '13')
    srv_msg.response_check_suboption_content(step, 'Response', '13', '3', None, 'statuscode', '2')
