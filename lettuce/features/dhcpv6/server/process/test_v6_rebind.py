"""DHCPv6 Rebind"""

# pylint: disable=invalid-name,line-too-long

import pytest

from features import srv_control
from features import misc
from features import srv_msg
from features import references


@pytest.mark.v6
@pytest.mark.dhcp6
@pytest.mark.rebind
def test_v6_message_rebind_reply_zerotime(step):
    #  Testing server ability server ability perform REBIND - REPLY message exchange.
    #  Message details 		Client		Server
    #  						SOLICIT -->
    #  		   						<--	ADVERTISE
    #  						REQUEST -->
    #  		   						<--	REPLY
    #  						Server Reconfiguration
    #  correct message 		REBIND -->
    # 					  		    <--	REPLY
    #  Pass Criteria:
    #  				REPLY MUST include option:
    # 					client-id
    # 					server-id
    # 					IA-NA (with time T1 = 0 T2 = 0)
    # 					IA-Address

    misc.test_setup(step)
    srv_control.config_srv_subnet(step, '3000::/64', '3000::1-3000::ff')
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

    misc.test_setup(step)
    srv_control.config_srv_subnet(step, '2001:db8:1::/64', '2001:db8:1::1-2001:db8:1::ffff')
    srv_control.build_and_send_config_files(step, 'SSH', 'config-file')
    srv_control.start_srv(step, 'DHCP', 'started')

    misc.test_procedure(step)
    srv_msg.client_copy_option(step, 'IA_NA')
    srv_msg.client_does_include(step, 'Client', None, 'client-id')
    srv_msg.client_send_msg(step, 'REBIND')

    # Changed after RFC 7550
    # Pass Criteria:
    # Server MUST respond with REPLY message.
    # Response MUST include option 1.
    # Response MUST include option 2.
    # Response option 3 MUST contain T1 0.
    # Response option 3 MUST contain T2 0.
    misc.pass_criteria(step)
    srv_msg.send_wait_for_message(step, 'MUST', None, 'REPLY')
    srv_msg.response_check_include_option(step, 'Response', None, '1')
    srv_msg.response_check_include_option(step, 'Response', None, '2')
    srv_msg.response_check_option_content(step, 'Response', '3', None, 'sub-option', '5')
    srv_msg.response_check_suboption_content(step,
                                             'Response',
                                             '5',
                                             '3',
                                             None,
                                             'address',
                                             '2001:db8:1::1')
    srv_msg.response_check_suboption_content(step, 'Response', '5', '3', None, 'validlft', '4000')
    srv_msg.response_check_suboption_content(step,
                                             'Response',
                                             '5',
                                             '3',
                                             None,
                                             'address',
                                             '3000::1')
    srv_msg.response_check_suboption_content(step, 'Response', '5', '3', None, 'validlft', '0')

    references.references_check(step, 'RFC3315')


@pytest.mark.v6
@pytest.mark.dhcp6
@pytest.mark.rebind
def test_v6_message_rebind_reply_newtime(step):
    #  Testing server ability server ability perform REBIND - REPLY message exchange.
    #  Additional server configuration:
    #  		renew-timer = 111
    # 		rebind-timer = 222
    #  Message details 		Client		Server
    #  						SOLICIT -->
    #  		   						<--	ADVERTISE
    #  						REQUEST -->
    #  		   						<--	REPLY
    #  correct message 		REBIND -->
    # 					  		    <--	REPLY
    #  Pass Criteria:
    #  				REPLY MUST include option:
    # 					client-id
    # 					server-id
    # 					IA-NA (with time T1 = 111 T2 = 222)
    # 					IA-Address
    misc.test_setup(step)
    srv_control.set_time(step, 'renew-timer', '111')
    srv_control.set_time(step, 'rebind-timer', '222')
    srv_control.config_srv_subnet(step, '3000::/64', '3000::1-3000::ff')
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
    srv_msg.client_copy_option(step, 'IA_NA')
    srv_msg.client_does_include(step, 'Client', None, 'client-id')
    srv_msg.client_send_msg(step, 'REBIND')

    misc.pass_criteria(step)
    srv_msg.send_wait_for_message(step, 'MUST', None, 'REPLY')
    srv_msg.response_check_include_option(step, 'Response', None, '1')
    srv_msg.response_check_include_option(step, 'Response', None, '2')
    srv_msg.response_check_include_option(step, 'Response', None, '3')
    srv_msg.response_check_option_content(step, 'Response', '3', None, 'sub-option', '5')
    srv_msg.response_check_option_content(step, 'Response', '3', None, 'T1', '111')
    srv_msg.response_check_option_content(step, 'Response', '3', None, 'T2', '222')

    references.references_check(step, 'RFC3315')
