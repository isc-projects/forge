"""Standard DHCPv6 message types"""

# pylint: disable=invalid-name,line-too-long

import pytest

import srv_msg
import references
import misc
import srv_control


@pytest.mark.basic
@pytest.mark.v6
@pytest.mark.dhcp6
def test_v6_basic_message_solicit_advertise():
    #  Basic message test, testing only server ability to respond with 'ADVERTISE' to received 'SOLICIT'
    #  Client		Server
    #  SOLICIT -->
    #  		   <--	ADVERTISE
    #  Without testing content of a message.

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

    references.references_check('RFC3315')


@pytest.mark.basic
@pytest.mark.v6
@pytest.mark.dhcp6
def test_v6_basic_message_request_reply():
    #  Basic message test, testing only server ability message exchange
    #  between him and client.
    #  Client		Server
    #  SOLICIT -->
    #  		   <--	ADVERTISE
    #  REQUEST -->
    #  		   <--	REPLY
    #  Without testing content of a message.

    misc.test_setup()
    srv_control.config_srv_subnet('3000::/64', '3000::1-3000::ff')
    srv_control.build_and_send_config_files('SSH', 'config-file')
    srv_control.start_srv('DHCP', 'started')

    misc.test_procedure()
    srv_msg.client_does_include('Client', None, 'client-id')
    srv_msg.client_does_include('Client', None, 'IA-NA')
    srv_msg.client_send_msg('SOLICIT')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', None, 'ADVERTISE')

    misc.test_procedure()
    srv_msg.client_copy_option('server-id')
    srv_msg.client_copy_option('IA_NA')
    srv_msg.client_does_include('Client', None, 'client-id')
    srv_msg.client_send_msg('REQUEST')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', None, 'REPLY')

    references.references_check('RFC3315')


@pytest.mark.basic
@pytest.mark.v6
@pytest.mark.dhcp6
def test_v6_basic_message_confirm_reply():
    #  Basic message test, testing only server ability message exchange
    #  between him and client.
    #  Client		Server
    #  SOLICIT -->
    #  		   <--	ADVERTISE
    #  REQUEST -->
    #  		   <--	REPLY
    #  CONFIRM -->
    #  		   <--	REPLY
    #  Without testing content of a message.

    misc.test_setup()
    srv_control.config_srv_subnet('3000::/64', '3000::1-3000::ff')
    srv_control.build_and_send_config_files('SSH', 'config-file')
    srv_control.start_srv('DHCP', 'started')

    misc.test_procedure()
    srv_msg.client_does_include('Client', None, 'client-id')
    srv_msg.client_does_include('Client', None, 'IA-NA')
    srv_msg.client_send_msg('SOLICIT')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', None, 'ADVERTISE')

    misc.test_procedure()
    srv_msg.client_copy_option('IA_NA')
    srv_msg.client_copy_option('server-id')
    srv_msg.client_requests_option('7')
    srv_msg.client_does_include('Client', None, 'client-id')
    srv_msg.client_send_msg('REQUEST')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', None, 'REPLY')

    misc.test_procedure()
    srv_msg.client_copy_option('IA_NA')
    srv_msg.client_does_include('Client', None, 'client-id')
    srv_msg.client_send_msg('CONFIRM')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', None, 'REPLY')

    references.references_check('RFC3315')


@pytest.mark.basic
@pytest.mark.v6
@pytest.mark.dhcp6
def test_v6_basic_message_renew_reply():
    #  Basic message test, testing only server ability message exchange
    #  between him and client.
    #  Client		Server
    #  SOLICIT -->
    #  		   <--	ADVERTISE
    #  REQUEST -->
    #  		   <--	REPLY
    #  RENEW   -->
    #  		   <--	REPLY
    #  Without testing content of a message.

    misc.test_setup()
    srv_control.config_srv_subnet('3000::/64', '3000::1-3000::ff')
    srv_control.build_and_send_config_files('SSH', 'config-file')
    srv_control.start_srv('DHCP', 'started')

    misc.test_procedure()
    srv_msg.client_does_include('Client', None, 'client-id')
    srv_msg.client_does_include('Client', None, 'IA-NA')
    srv_msg.client_send_msg('SOLICIT')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', None, 'ADVERTISE')

    misc.test_procedure()
    srv_msg.client_copy_option('server-id')
    srv_msg.client_copy_option('IA_NA')
    srv_msg.client_does_include('Client', None, 'client-id')
    srv_msg.client_send_msg('REQUEST')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', None, 'REPLY')

    misc.test_procedure()
    srv_msg.client_copy_option('IA_NA')
    srv_msg.client_copy_option('server-id')
    srv_msg.client_does_include('Client', None, 'client-id')
    srv_msg.client_send_msg('RENEW')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', None, 'REPLY')

    references.references_check('RFC3315')


@pytest.mark.basic
@pytest.mark.v6
@pytest.mark.dhcp6
def test_v6_basic_message_rebind_reply():
    #  Basic message test, testing only server ability message exchange
    #  between him and client.
    #  Client		Server
    #  SOLICIT -->
    #  		   <--	ADVERTISE
    #  REQUEST -->
    #  		   <--	REPLY
    #  REBIND  -->
    #  		   <--	REPLY
    #  Without testing content of a message.

    misc.test_setup()
    srv_control.config_srv_subnet('3000::/64', '3000::1-3000::ff')
    srv_control.build_and_send_config_files('SSH', 'config-file')
    srv_control.start_srv('DHCP', 'started')

    misc.test_procedure()
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
    srv_msg.client_copy_option('IA_NA')
    srv_msg.client_does_include('Client', None, 'client-id')
    srv_msg.client_send_msg('REBIND')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', None, 'REPLY')

    references.references_check('RFC3315')


@pytest.mark.basic
@pytest.mark.v6
@pytest.mark.dhcp6
def test_v6_basic_message_release_reply():
    #  Basic message test, testing only server ability message exchange
    #  between him and client.
    #  Client		Server
    #  SOLICIT -->
    #  		   <--	ADVERTISE
    #  REQUEST -->
    #  		   <--	REPLY
    #  RELEASE   -->
    #  		   <--	REPLY
    #  Without testing content of a message.

    misc.test_setup()
    srv_control.config_srv_subnet('3000::/64', '3000::1-3000::ff')
    srv_control.build_and_send_config_files('SSH', 'config-file')
    srv_control.start_srv('DHCP', 'started')

    misc.test_procedure()
    srv_msg.client_does_include('Client', None, 'client-id')
    srv_msg.client_does_include('Client', None, 'IA-NA')
    srv_msg.client_send_msg('SOLICIT')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', None, 'ADVERTISE')

    misc.test_procedure()
    srv_msg.client_copy_option('server-id')
    srv_msg.client_copy_option('IA_NA')
    srv_msg.client_does_include('Client', None, 'client-id')
    srv_msg.client_send_msg('REQUEST')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', None, 'REPLY')

    misc.test_procedure()
    srv_msg.client_copy_option('IA_NA')
    srv_msg.client_copy_option('server-id')
    srv_msg.client_does_include('Client', None, 'client-id')
    srv_msg.client_send_msg('RELEASE')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', None, 'REPLY')

    references.references_check('RFC3315')


@pytest.mark.basic
@pytest.mark.v6
@pytest.mark.dhcp6
def test_v6_basic_message_decline_reply():
    #  Basic message test, testing only server ability message exchange
    #  between him and client.
    #  Client		Server
    #  SOLICIT -->
    #  		   <--	ADVERTISE
    #  REQUEST -->
    #  		   <--	REPLY
    #  DECLINE -->
    #  		   <--	REPLY
    #  Without testing content of a message.

    misc.test_setup()
    srv_control.config_srv_subnet('3000::/64', '3000::1-3000::ff')
    srv_control.build_and_send_config_files('SSH', 'config-file')
    srv_control.start_srv('DHCP', 'started')

    misc.test_procedure()
    srv_msg.client_does_include('Client', None, 'client-id')
    srv_msg.client_does_include('Client', None, 'IA-NA')
    srv_msg.client_send_msg('SOLICIT')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', None, 'ADVERTISE')

    misc.test_procedure()
    srv_msg.client_copy_option('IA_NA')
    srv_msg.client_save_option('server-id')
    srv_msg.client_add_saved_option('DONT ')
    srv_msg.client_does_include('Client', None, 'client-id')
    srv_msg.client_send_msg('REQUEST')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', None, 'REPLY')

    misc.test_procedure()
    srv_msg.client_save_option('IA_NA')
    srv_msg.client_add_saved_option('DONT ')
    srv_msg.client_does_include('Client', None, 'client-id')
    srv_msg.client_send_msg('DECLINE')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', None, 'REPLY')

    references.references_check('RFC3315')


@pytest.mark.basic
@pytest.mark.v6
@pytest.mark.dhcp6
def test_v6_basic_message_information_request_reply():
    #  Basic message test, testing only server ability to respond with 'REPLY'
    #  to received 'INFOREQUEST'. Without testing content of a message.

    misc.test_setup()
    srv_control.config_srv_subnet('3000::/64', '3000::1-3000::ff')
    srv_control.build_and_send_config_files('SSH', 'config-file')
    srv_control.start_srv('DHCP', 'started')

    misc.test_procedure()
    srv_msg.client_does_include('Client', None, 'client-id')
    srv_msg.client_requests_option('7')
    srv_msg.client_send_msg('INFOREQUEST')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', None, 'REPLY')

    references.references_check('RFC3315')


@pytest.mark.basic
@pytest.mark.v6
@pytest.mark.dhcp6
def test_v6_basic_message_information_request_reply_without_client_id():
    #  Basic message test, testing only server ability to respond with 'REPLY'
    #  to received 'INFOREQUEST' message that not include CLIENT-ID option.
    #  Without testing content of a message.

    misc.test_setup()
    srv_control.config_srv_subnet('3000::/64', '3000::1-3000::ff')
    srv_control.build_and_send_config_files('SSH', 'config-file')
    srv_control.start_srv('DHCP', 'started')

    misc.test_procedure()
    srv_msg.client_requests_option('7')
    # message wont contain client-id option
    srv_msg.client_send_msg('INFOREQUEST')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', None, 'REPLY')

    references.references_check('RFC3315')
