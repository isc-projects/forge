"""DHCPv6 Renew"""

# pylint: disable=invalid-name,line-too-long

import pytest

from features import misc
from features import srv_msg
from features import srv_control
from features import references


@pytest.mark.v6
@pytest.mark.dhcp6
@pytest.mark.renew
def test_v6_message_renew_reply(step):
    #  Testing server ability to perform message exchange RENEW - REPLY
    #  Message details 		Client		Server
    #  						SOLICIT -->
    #  		   						<--	ADVERTISE
    #  						REQUEST -->
    #  		   						<--	REPLY
    #  correct message 		  RENEW -->
    # 					  		    <--	REPLY
    #  Pass Criteria:
    #  				REPLY MUST include option:
    # 					client-id
    # 					server-id
    # 					IA-NA with suboption IA-Address
    #
    misc.test_setup(step)
    srv_control.config_srv_subnet(step, '3000::/64', '3000::5-3000::55')
    srv_control.build_and_send_config_files(step, 'SSH', 'config-file')
    srv_control.start_srv(step, 'DHCP', 'started')

    misc.test_procedure(step)
    srv_msg.client_does_include(step, 'Client', None, 'client-id')
    srv_msg.client_does_include(step, 'Client', None, 'IA-NA')
    srv_msg.client_send_msg(step, 'SOLICIT')

    misc.pass_criteria(step)
    srv_msg.send_wait_for_message(step, 'MUST', None, 'ADVERTISE')
    srv_msg.response_check_include_option(step, 'Response', None, '1')
    srv_msg.response_check_include_option(step, 'Response', None, '2')
    srv_msg.response_check_include_option(step, 'Response', None, '3')
    srv_msg.response_check_option_content(step, 'Response', '3', None, 'sub-option', '5')

    misc.test_procedure(step)
    srv_msg.client_copy_option(step, 'server-id')
    srv_msg.client_copy_option(step, 'IA_NA')
    srv_msg.client_does_include(step, 'Client', None, 'client-id')
    srv_msg.client_send_msg(step, 'REQUEST')

    misc.pass_criteria(step)
    srv_msg.send_wait_for_message(step, 'MUST', None, 'REPLY')
    srv_msg.response_check_include_option(step, 'Response', None, '3')
    srv_msg.response_check_option_content(step, 'Response', '3', None, 'sub-option', '5')

    misc.test_procedure(step)
    srv_msg.client_copy_option(step, 'server-id')
    srv_msg.client_copy_option(step, 'IA_NA')
    srv_msg.client_does_include(step, 'Client', None, 'client-id')
    srv_msg.client_send_msg(step, 'RENEW')

    misc.pass_criteria(step)
    srv_msg.send_wait_for_message(step, 'MUST', None, 'REPLY')
    srv_msg.response_check_include_option(step, 'Response', None, '1')
    srv_msg.response_check_include_option(step, 'Response', None, '2')
    srv_msg.response_check_include_option(step, 'Response', None, '3')
    srv_msg.response_check_option_content(step, 'Response', '3', None, 'sub-option', '5')

    references.references_check(step, 'RFC')


@pytest.mark.v6
@pytest.mark.dhcp6
@pytest.mark.renew
def test_v6_message_renew_reply_different_clients_the_same_iaid(step):
    #  Two clients try to renew address, using the same IA_ID but different Client-ID

    misc.test_setup(step)
    srv_control.set_time(step, 'renew-timer', '50')
    srv_control.set_time(step, 'rebind-timer', '60')
    srv_control.set_time(step, 'preferred-lifetime', '70')
    srv_control.set_time(step, 'valid-lifetime', '80')
    srv_control.config_srv_subnet(step, '3000::/64', '3000::1-3000::2')
    srv_control.build_and_send_config_files(step, 'SSH', 'config-file')
    srv_control.start_srv(step, 'DHCP', 'started')

    misc.test_procedure(step)
    srv_msg.client_sets_value(step, 'Client', 'ia_id', '666')
    srv_msg.client_sets_value(step, 'Client', 'DUID', '00:03:00:01:f6:f5:f4:f3:f2:01')
    srv_msg.client_does_include(step, 'Client', None, 'client-id')
    srv_msg.client_does_include(step, 'Client', None, 'IA-NA')
    srv_msg.client_send_msg(step, 'SOLICIT')

    misc.pass_criteria(step)
    srv_msg.send_wait_for_message(step, 'MUST', None, 'ADVERTISE')
    srv_msg.response_check_include_option(step, 'Response', None, '1')
    srv_msg.response_check_include_option(step, 'Response', None, '2')
    srv_msg.response_check_include_option(step, 'Response', None, '3')
    srv_msg.response_check_option_content(step, 'Response', '3', None, 'sub-option', '5')

    misc.test_procedure(step)
    srv_msg.client_sets_value(step, 'Client', 'ia_id', '666')
    srv_msg.client_sets_value(step, 'Client', 'DUID', '00:03:00:01:f6:f5:f4:f3:f2:01')
    srv_msg.client_copy_option(step, 'server-id')
    srv_msg.client_copy_option(step, 'IA_NA')
    srv_msg.client_does_include(step, 'Client', None, 'client-id')
    srv_msg.client_send_msg(step, 'REQUEST')

    misc.pass_criteria(step)
    srv_msg.send_wait_for_message(step, 'MUST', None, 'REPLY')
    srv_msg.response_check_include_option(step, 'Response', None, '3')
    srv_msg.response_check_option_content(step, 'Response', '3', None, 'sub-option', '5')

    misc.test_procedure(step)
    srv_msg.client_sets_value(step, 'Client', 'ia_id', '666')
    srv_msg.client_sets_value(step, 'Client', 'DUID', '00:03:00:01:f6:f5:f4:f3:f2:22')
    srv_msg.client_does_include(step, 'Client', None, 'client-id')
    srv_msg.client_does_include(step, 'Client', None, 'IA-NA')
    srv_msg.client_send_msg(step, 'SOLICIT')

    misc.pass_criteria(step)
    srv_msg.send_wait_for_message(step, 'MUST', None, 'ADVERTISE')
    srv_msg.response_check_include_option(step, 'Response', None, '1')
    srv_msg.response_check_include_option(step, 'Response', None, '2')
    srv_msg.response_check_include_option(step, 'Response', None, '3')
    srv_msg.response_check_option_content(step, 'Response', '3', None, 'sub-option', '5')

    misc.test_procedure(step)
    srv_msg.client_sets_value(step, 'Client', 'ia_id', '666')
    srv_msg.client_sets_value(step, 'Client', 'DUID', '00:03:00:01:f6:f5:f4:f3:f2:22')
    srv_msg.client_copy_option(step, 'server-id')
    srv_msg.client_copy_option(step, 'IA_NA')
    srv_msg.client_does_include(step, 'Client', None, 'client-id')
    srv_msg.client_send_msg(step, 'REQUEST')

    misc.pass_criteria(step)
    srv_msg.send_wait_for_message(step, 'MUST', None, 'REPLY')
    srv_msg.response_check_include_option(step, 'Response', None, '3')
    srv_msg.response_check_option_content(step, 'Response', '3', None, 'sub-option', '5')

    misc.test_procedure(step)
    # client try to renew address that is not his
    srv_msg.client_sets_value(step, 'Client', 'ia_id', '666')
    srv_msg.client_sets_value(step, 'Client', 'DUID', '00:03:00:01:f6:f5:f4:f3:f2:01')
    srv_msg.client_copy_option(step, 'server-id')
    srv_msg.client_copy_option(step, 'IA_NA')
    srv_msg.client_does_include(step, 'Client', None, 'client-id')
    srv_msg.client_send_msg(step, 'RENEW')

    misc.pass_criteria(step)
    srv_msg.send_wait_for_message(step, 'MUST', None, 'REPLY')
    srv_msg.response_check_include_option(step, 'Response', None, '1')
    srv_msg.response_check_include_option(step, 'Response', None, '2')
    srv_msg.response_check_include_option(step, 'Response', None, '3')
    srv_msg.response_check_option_content(step, 'Response', '3', None, 'sub-option', '5')
    srv_msg.response_check_suboption_content(step, 'Response', '5', '3', None, 'validlft', '0')
    srv_msg.response_check_suboption_content(step,
                                             'Response',
                                             '5',
                                             '3',
                                             None,
                                             'address',
                                             '3000::2')
    srv_msg.response_check_suboption_content(step, 'Response', '5', '3', None, 'validlft', '80')
    srv_msg.response_check_suboption_content(step,
                                             'Response',
                                             '5',
                                             '3',
                                             None,
                                             'address',
                                             '3000::1')
    references.references_check(step, 'RFC')


@pytest.mark.v6
@pytest.mark.dhcp6
@pytest.mark.renew
def test_v6_message_renew_reply_different_clients_the_same_iaid_2(step):
    #  Two clients try to renew address, using the same IA_ID but different Client-ID

    misc.test_setup(step)
    srv_control.set_time(step, 'renew-timer', '50')
    srv_control.set_time(step, 'rebind-timer', '60')
    srv_control.set_time(step, 'preferred-lifetime', '70')
    srv_control.set_time(step, 'valid-lifetime', '80')
    srv_control.config_srv_subnet(step, '3000::/64', '3000::1-3000::2')
    srv_control.build_and_send_config_files(step, 'SSH', 'config-file')
    srv_control.start_srv(step, 'DHCP', 'started')

    misc.test_procedure(step)
    srv_msg.client_sets_value(step, 'Client', 'ia_id', '666')
    srv_msg.client_sets_value(step, 'Client', 'DUID', '00:03:00:01:f6:f5:f4:f3:f2:01')
    srv_msg.client_does_include(step, 'Client', None, 'client-id')
    srv_msg.client_does_include(step, 'Client', None, 'IA-NA')
    srv_msg.client_send_msg(step, 'SOLICIT')

    misc.pass_criteria(step)
    srv_msg.send_wait_for_message(step, 'MUST', None, 'ADVERTISE')
    srv_msg.response_check_include_option(step, 'Response', None, '1')
    srv_msg.response_check_include_option(step, 'Response', None, '2')
    srv_msg.response_check_include_option(step, 'Response', None, '3')
    srv_msg.response_check_option_content(step, 'Response', '3', None, 'sub-option', '5')

    misc.test_procedure(step)
    srv_msg.client_sets_value(step, 'Client', 'ia_id', '666')
    srv_msg.client_sets_value(step, 'Client', 'DUID', '00:03:00:01:f6:f5:f4:f3:f2:01')
    srv_msg.client_copy_option(step, 'server-id')
    srv_msg.client_copy_option(step, 'IA_NA')
    srv_msg.client_does_include(step, 'Client', None, 'client-id')
    srv_msg.client_send_msg(step, 'REQUEST')

    misc.pass_criteria(step)
    srv_msg.send_wait_for_message(step, 'MUST', None, 'REPLY')
    srv_msg.response_check_include_option(step, 'Response', None, '3')
    srv_msg.response_check_option_content(step, 'Response', '3', None, 'sub-option', '5')

    misc.test_procedure(step)
    srv_msg.client_sets_value(step, 'Client', 'ia_id', '666')
    srv_msg.client_sets_value(step, 'Client', 'DUID', '00:03:00:01:f6:f5:f4:f3:f2:22')
    srv_msg.client_does_include(step, 'Client', None, 'client-id')
    srv_msg.client_does_include(step, 'Client', None, 'IA-NA')
    srv_msg.client_send_msg(step, 'SOLICIT')

    misc.pass_criteria(step)
    srv_msg.send_wait_for_message(step, 'MUST', None, 'ADVERTISE')
    srv_msg.response_check_include_option(step, 'Response', None, '1')
    srv_msg.response_check_include_option(step, 'Response', None, '2')
    srv_msg.response_check_include_option(step, 'Response', None, '3')
    srv_msg.response_check_option_content(step, 'Response', '3', None, 'sub-option', '5')

    misc.test_procedure(step)
    srv_msg.client_sets_value(step, 'Client', 'ia_id', '666')
    srv_msg.client_sets_value(step, 'Client', 'DUID', '00:03:00:01:f6:f5:f4:f3:f2:22')
    srv_msg.client_copy_option(step, 'server-id')
    srv_msg.client_copy_option(step, 'IA_NA')
    srv_msg.client_does_include(step, 'Client', None, 'client-id')
    srv_msg.client_send_msg(step, 'REQUEST')

    misc.pass_criteria(step)
    srv_msg.send_wait_for_message(step, 'MUST', None, 'REPLY')
    srv_msg.response_check_include_option(step, 'Response', None, '3')
    srv_msg.response_check_option_content(step, 'Response', '3', None, 'sub-option', '5')

    misc.test_procedure(step)
    # client try to renew address that is his
    srv_msg.client_sets_value(step, 'Client', 'ia_id', '666')
    srv_msg.client_sets_value(step, 'Client', 'DUID', '00:03:00:01:f6:f5:f4:f3:f2:22')
    srv_msg.client_copy_option(step, 'server-id')
    srv_msg.client_copy_option(step, 'IA_NA')
    srv_msg.client_does_include(step, 'Client', None, 'client-id')
    srv_msg.client_send_msg(step, 'RENEW')

    misc.pass_criteria(step)
    srv_msg.send_wait_for_message(step, 'MUST', None, 'REPLY')
    srv_msg.response_check_include_option(step, 'Response', None, '1')
    srv_msg.response_check_include_option(step, 'Response', None, '2')
    srv_msg.response_check_include_option(step, 'Response', None, '3')
    srv_msg.response_check_option_content(step, 'Response', '3', None, 'sub-option', '5')
    # Response sub-option 5 from option 3 MUST contain validlft 0.
    srv_msg.response_check_suboption_content(step,
                                             'Response',
                                             '5',
                                             '3',
                                             None,
                                             'address',
                                             '3000::2')
    srv_msg.response_check_suboption_content(step, 'Response', '5', '3', None, 'validlft', '80')
    srv_msg.response_check_suboption_content(step,
                                             'Response',
                                             '5',
                                             '3',
                                             'NOT ',
                                             'address',
                                             '3000::1')
    references.references_check(step, 'RFC')


@pytest.mark.v6
@pytest.mark.dhcp6
@pytest.mark.renew
def test_v6_message_renew_reply_different_clients_the_same_iaid_expired(step):
    #  Two clients try to renew address, using the same IA_ID but different Client-ID

    misc.test_setup(step)
    srv_control.set_time(step, 'renew-timer', '5')
    srv_control.set_time(step, 'rebind-timer', '6')
    srv_control.set_time(step, 'preferred-lifetime', '7')
    srv_control.set_time(step, 'valid-lifetime', '8')
    srv_control.config_srv_subnet(step, '3000::/64', '3000::1-3000::2')
    srv_control.build_and_send_config_files(step, 'SSH', 'config-file')
    srv_control.start_srv(step, 'DHCP', 'started')

    misc.test_procedure(step)
    srv_msg.client_sets_value(step, 'Client', 'ia_id', '666')
    srv_msg.client_sets_value(step, 'Client', 'DUID', '00:03:00:01:f6:f5:f4:f3:f2:01')
    srv_msg.client_does_include(step, 'Client', None, 'client-id')
    srv_msg.client_does_include(step, 'Client', None, 'IA-NA')
    srv_msg.client_send_msg(step, 'SOLICIT')

    misc.pass_criteria(step)
    srv_msg.send_wait_for_message(step, 'MUST', None, 'ADVERTISE')
    srv_msg.response_check_include_option(step, 'Response', None, '1')
    srv_msg.response_check_include_option(step, 'Response', None, '2')
    srv_msg.response_check_include_option(step, 'Response', None, '3')
    srv_msg.response_check_option_content(step, 'Response', '3', None, 'sub-option', '5')

    misc.test_procedure(step)
    srv_msg.client_sets_value(step, 'Client', 'ia_id', '666')
    srv_msg.client_sets_value(step, 'Client', 'DUID', '00:03:00:01:f6:f5:f4:f3:f2:01')
    srv_msg.client_copy_option(step, 'server-id')
    srv_msg.client_copy_option(step, 'IA_NA')
    srv_msg.client_does_include(step, 'Client', None, 'client-id')
    srv_msg.client_send_msg(step, 'REQUEST')

    misc.pass_criteria(step)
    srv_msg.send_wait_for_message(step, 'MUST', None, 'REPLY')
    srv_msg.response_check_include_option(step, 'Response', None, '3')
    srv_msg.response_check_option_content(step, 'Response', '3', None, 'sub-option', '5')

    misc.test_procedure(step)
    srv_msg.client_sets_value(step, 'Client', 'ia_id', '666')
    srv_msg.client_sets_value(step, 'Client', 'DUID', '00:03:00:01:f6:f5:f4:f3:f2:22')
    srv_msg.client_does_include(step, 'Client', None, 'client-id')
    srv_msg.client_does_include(step, 'Client', None, 'IA-NA')
    srv_msg.client_send_msg(step, 'SOLICIT')

    misc.pass_criteria(step)
    srv_msg.send_wait_for_message(step, 'MUST', None, 'ADVERTISE')
    srv_msg.response_check_include_option(step, 'Response', None, '1')
    srv_msg.response_check_include_option(step, 'Response', None, '2')
    srv_msg.response_check_include_option(step, 'Response', None, '3')
    srv_msg.response_check_option_content(step, 'Response', '3', None, 'sub-option', '5')

    misc.test_procedure(step)
    srv_msg.client_sets_value(step, 'Client', 'ia_id', '666')
    srv_msg.client_sets_value(step, 'Client', 'DUID', '00:03:00:01:f6:f5:f4:f3:f2:22')
    srv_msg.client_copy_option(step, 'server-id')
    srv_msg.client_copy_option(step, 'IA_NA')
    srv_msg.client_does_include(step, 'Client', None, 'client-id')
    srv_msg.client_send_msg(step, 'REQUEST')

    misc.pass_criteria(step)
    srv_msg.send_wait_for_message(step, 'MUST', None, 'REPLY')
    srv_msg.response_check_include_option(step, 'Response', None, '3')
    srv_msg.response_check_option_content(step, 'Response', '3', None, 'sub-option', '5')

    srv_msg.forge_sleep(step, '10', 'seconds')

    misc.test_procedure(step)

    srv_msg.client_sets_value(step, 'Client', 'ia_id', '666')

    srv_msg.client_sets_value(step, 'Client', 'DUID', '00:03:00:01:f6:f5:f4:f3:f2:01')
    srv_msg.client_copy_option(step, 'server-id')
    srv_msg.client_copy_option(step, 'IA_NA')
    srv_msg.client_does_include(step, 'Client', None, 'client-id')
    srv_msg.client_send_msg(step, 'RENEW')

    misc.pass_criteria(step)
    srv_msg.send_wait_for_message(step, 'MUST', None, 'REPLY')
    srv_msg.response_check_include_option(step, 'Response', None, '1')
    srv_msg.response_check_include_option(step, 'Response', None, '2')
    srv_msg.response_check_include_option(step, 'Response', None, '3')
    srv_msg.response_check_option_content(step, 'Response', '3', None, 'sub-option', '5')
    srv_msg.response_check_option_content(step, 'Response', '3', None, 'sub-option', '5')
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
                                             '3000::1')
    references.references_check(step, 'RFC')


@pytest.mark.v6
@pytest.mark.dhcp6
@pytest.mark.renew
def test_v6_message_renew_reply_different_clients_the_same_iaid_expired_2(step):
    #  Two clients try to renew address, using the same IA_ID but different Client-ID

    misc.test_setup(step)
    srv_control.set_time(step, 'renew-timer', '5')
    srv_control.set_time(step, 'rebind-timer', '6')
    srv_control.set_time(step, 'preferred-lifetime', '7')
    srv_control.set_time(step, 'valid-lifetime', '8')
    srv_control.config_srv_subnet(step, '3000::/64', '3000::1-3000::2')
    srv_control.build_and_send_config_files(step, 'SSH', 'config-file')
    srv_control.start_srv(step, 'DHCP', 'started')

    misc.test_procedure(step)
    srv_msg.client_sets_value(step, 'Client', 'ia_id', '666')
    srv_msg.client_sets_value(step, 'Client', 'DUID', '00:03:00:01:f6:f5:f4:f3:f2:01')
    srv_msg.client_does_include(step, 'Client', None, 'client-id')
    srv_msg.client_does_include(step, 'Client', None, 'IA-NA')
    srv_msg.client_send_msg(step, 'SOLICIT')

    misc.pass_criteria(step)
    srv_msg.send_wait_for_message(step, 'MUST', None, 'ADVERTISE')
    srv_msg.response_check_include_option(step, 'Response', None, '1')
    srv_msg.response_check_include_option(step, 'Response', None, '2')
    srv_msg.response_check_include_option(step, 'Response', None, '3')
    srv_msg.response_check_option_content(step, 'Response', '3', None, 'sub-option', '5')

    misc.test_procedure(step)
    srv_msg.client_sets_value(step, 'Client', 'ia_id', '666')
    srv_msg.client_sets_value(step, 'Client', 'DUID', '00:03:00:01:f6:f5:f4:f3:f2:01')
    srv_msg.client_copy_option(step, 'server-id')
    srv_msg.client_copy_option(step, 'IA_NA')
    srv_msg.client_does_include(step, 'Client', None, 'client-id')
    srv_msg.client_send_msg(step, 'REQUEST')

    misc.pass_criteria(step)
    srv_msg.send_wait_for_message(step, 'MUST', None, 'REPLY')
    srv_msg.response_check_include_option(step, 'Response', None, '3')
    srv_msg.response_check_option_content(step, 'Response', '3', None, 'sub-option', '5')

    misc.test_procedure(step)
    srv_msg.client_sets_value(step, 'Client', 'ia_id', '666')
    srv_msg.client_sets_value(step, 'Client', 'DUID', '00:03:00:01:f6:f5:f4:f3:f2:22')
    srv_msg.client_does_include(step, 'Client', None, 'client-id')
    srv_msg.client_does_include(step, 'Client', None, 'IA-NA')
    srv_msg.client_send_msg(step, 'SOLICIT')

    misc.pass_criteria(step)
    srv_msg.send_wait_for_message(step, 'MUST', None, 'ADVERTISE')
    srv_msg.response_check_include_option(step, 'Response', None, '1')
    srv_msg.response_check_include_option(step, 'Response', None, '2')
    srv_msg.response_check_include_option(step, 'Response', None, '3')
    srv_msg.response_check_option_content(step, 'Response', '3', None, 'sub-option', '5')

    misc.test_procedure(step)
    srv_msg.client_sets_value(step, 'Client', 'ia_id', '666')
    srv_msg.client_sets_value(step, 'Client', 'DUID', '00:03:00:01:f6:f5:f4:f3:f2:22')
    srv_msg.client_copy_option(step, 'server-id')
    srv_msg.client_copy_option(step, 'IA_NA')
    srv_msg.client_does_include(step, 'Client', None, 'client-id')
    srv_msg.client_send_msg(step, 'REQUEST')

    misc.pass_criteria(step)
    srv_msg.send_wait_for_message(step, 'MUST', None, 'REPLY')
    srv_msg.response_check_include_option(step, 'Response', None, '3')
    srv_msg.response_check_option_content(step, 'Response', '3', None, 'sub-option', '5')
    srv_msg.forge_sleep(step, '10', 'seconds')

    misc.test_procedure(step)
    # client try to renew address that is his
    srv_msg.client_sets_value(step, 'Client', 'ia_id', '666')
    srv_msg.client_sets_value(step, 'Client', 'DUID', '00:03:00:01:f6:f5:f4:f3:f2:22')
    srv_msg.client_copy_option(step, 'server-id')
    srv_msg.client_copy_option(step, 'IA_NA')
    srv_msg.client_does_include(step, 'Client', None, 'client-id')
    srv_msg.client_send_msg(step, 'RENEW')

    misc.pass_criteria(step)
    srv_msg.send_wait_for_message(step, 'MUST', None, 'REPLY')
    srv_msg.response_check_include_option(step, 'Response', None, '1')
    srv_msg.response_check_include_option(step, 'Response', None, '2')
    srv_msg.response_check_include_option(step, 'Response', None, '3')
    srv_msg.response_check_option_content(step, 'Response', '3', None, 'sub-option', '5')
    # Response sub-option 5 from option 3 MUST contain validlft 0.
    srv_msg.response_check_suboption_content(step,
                                             'Response',
                                             '5',
                                             '3',
                                             None,
                                             'address',
                                             '3000::2')
    srv_msg.response_check_suboption_content(step, 'Response', '5', '3', None, 'validlft', '8')
    srv_msg.response_check_suboption_content(step,
                                             'Response',
                                             '5',
                                             '3',
                                             'NOT ',
                                             'address',
                                             '3000::1')
    references.references_check(step, 'RFC')


@pytest.mark.v6
@pytest.mark.dhcp6
@pytest.mark.renew
def test_v6_message_renew_reply_time_zero(step):
    #  Testing server ability to perform message exchange RENEW - REPLY
    #  In case when we expect that address is not appropriate for the link.
    #  Message details 		Client		Server
    #  						SOLICIT -->
    #  		   						<--	ADVERTISE
    #  						REQUEST -->
    #  Save IA_NA with IA_Addr		<--	REPLY
    #  					Reconfigure Server
    #  						SOLICIT -->
    #  		   						<--	ADVERTISE
    #  Create leases		REQUEST -->
    #  for the same client			<--	REPLY
    #  Use saved IA_NA 		  RENEW -->
    #  (proper client ID, IA_NA, but wrong address)
    # 					  		    <--	REPLY
    #  Pass Criteria:
    #  				REPLY MUST include option:
    # 					client-id
    # 					server-id
    # 					IA-NA with suboption IA-Address with validlft set to 0.
    misc.test_setup(step)
    srv_control.config_srv_subnet(step, '3000::/64', '3000::66-3000::66')
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
    srv_msg.client_copy_option(step, 'server-id')
    srv_msg.client_copy_option(step, 'IA_NA')
    srv_msg.client_does_include(step, 'Client', None, 'client-id')
    srv_msg.client_send_msg(step, 'REQUEST')

    misc.pass_criteria(step)
    srv_msg.send_wait_for_message(step, 'MUST', None, 'REPLY')
    srv_msg.response_check_include_option(step, 'Response', None, '3')
    srv_msg.response_check_option_content(step, 'Response', '3', None, 'sub-option', '5')

    srv_msg.client_save_option(step, 'IA_NA')

    misc.reconfigure(step)
    srv_control.config_srv_subnet(step, '3000::/64', '3000::100-3000::155')
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
    srv_msg.client_copy_option(step, 'server-id')
    srv_msg.client_copy_option(step, 'IA_NA')
    srv_msg.client_does_include(step, 'Client', None, 'client-id')
    srv_msg.client_send_msg(step, 'REQUEST')

    misc.pass_criteria(step)
    srv_msg.send_wait_for_message(step, 'MUST', None, 'REPLY')
    srv_msg.response_check_include_option(step, 'Response', None, '3')
    srv_msg.response_check_option_content(step, 'Response', '3', None, 'sub-option', '5')

    misc.test_procedure(step)
    srv_msg.client_copy_option(step, 'server-id')
    srv_msg.client_add_saved_option(step, 'DONT ')
    srv_msg.client_does_include(step, 'Client', None, 'client-id')
    srv_msg.client_send_msg(step, 'RENEW')

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
                                             '3000::66')
    srv_msg.response_check_suboption_content(step, 'Response', '5', '3', None, 'validlft', '0')

    references.references_check(step, 'RFC')
