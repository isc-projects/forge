"""DDNS without TSIG"""

# pylint: disable=invalid-name,line-too-long

import pytest

import misc
import srv_control
import srv_msg


@pytest.mark.v4
@pytest.mark.ddns
@pytest.mark.notsig
@pytest.mark.forward_reverse_add
def test_ddns4_notsig_forw_and_rev_add_success_Sflag():

    misc.test_setup()
    srv_control.config_srv_subnet('192.168.50.0/24', '192.168.50.10-192.168.50.10')
    srv_control.add_ddns_server('127.0.0.1', '53001')
    srv_control.add_ddns_server_options('enable-updates', 'true')
    srv_control.add_ddns_server_options('generated-prefix', 'four')
    srv_control.add_ddns_server_options('qualifying-suffix', 'example.com')
    srv_control.add_forward_ddns('four.example.com.', 'EMPTY_KEY')
    srv_control.add_reverse_ddns('50.168.192.in-addr.arpa.', 'EMPTY_KEY')
    srv_control.build_and_send_config_files('SSH', 'config-file')
    srv_control.start_srv('DHCP', 'started')

    srv_control.use_dns_set_number('20')
    srv_control.start_srv('DNS', 'started')

    misc.test_procedure()
    srv_msg.dns_question_record('aa.four.example.com', 'A', 'IN')
    srv_msg.client_send_dns_query()

    misc.pass_criteria()
    srv_msg.send_wait_for_query('MUST', None)
    srv_msg.dns_option(None, 'ANSWER')

    misc.test_procedure()
    srv_msg.client_requests_option('1')
    srv_msg.client_send_msg('DISCOVER')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', None, 'OFFER')
    srv_msg.response_check_include_option('Response', None, '1')
    srv_msg.response_check_content('Response', None, 'yiaddr', '192.168.50.10')
    srv_msg.response_check_option_content('Response', '1', None, 'value', '255.255.255.0')

    misc.test_procedure()
    srv_msg.client_copy_option('server_id')
    srv_msg.client_does_include_with_value('requested_addr', '192.168.50.10')
    srv_msg.client_requests_option('1')
    srv_msg.client_sets_value('Client', 'FQDN_domain_name', 'aa.four.example.com.')
    srv_msg.client_sets_value('Client', 'FQDN_flags', 'S')
    srv_msg.client_does_include('Client', None, 'fqdn')
    srv_msg.client_send_msg('REQUEST')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', None, 'ACK')
    srv_msg.response_check_content('Response', None, 'yiaddr', '192.168.50.10')
    srv_msg.response_check_include_option('Response', None, '1')
    srv_msg.response_check_option_content('Response', '1', None, 'value', '255.255.255.0')
    srv_msg.response_check_include_option('Response', None, '81')
    srv_msg.response_check_option_content('Response', '81', None, 'flags', '1')
    srv_msg.response_check_option_content('Response', '81', None, 'fqdn', 'aa.four.example.com.')

    misc.test_procedure()
    srv_msg.dns_question_record('aa.four.example.com', 'A', 'IN')
    srv_msg.client_send_dns_query()

    misc.pass_criteria()
    srv_msg.send_wait_for_query('MUST', None)
    srv_msg.dns_option('NOT ', 'ANSWER')
    srv_msg.dns_option_content('ANSWER', None, 'rdata', '192.168.50.10')
    srv_msg.dns_option_content('ANSWER', None, 'rrname', 'aa.four.example.com.')

    misc.test_procedure()
    srv_msg.dns_question_record('10.50.168.192.in-addr.arpa.', 'PTR', 'IN')
    srv_msg.client_send_dns_query()

    misc.pass_criteria()
    srv_msg.send_wait_for_query('MUST', None)
    srv_msg.dns_option('NOT ', 'ANSWER')
    srv_msg.dns_option_content('ANSWER', None, 'rdata', 'aa.four.example.com.')
    srv_msg.dns_option_content('ANSWER', None, 'rrname', '10.50.168.192.in-addr.arpa.')


@pytest.mark.v4
@pytest.mark.ddns
@pytest.mark.notsig
@pytest.mark.forward_reverse_add
def test_ddns4_notsig_forw_and_rev_add_fail_Sflag():

    misc.test_setup()
    srv_control.config_srv_subnet('192.168.50.0/24', '192.168.50.10-192.168.50.10')
    srv_control.add_ddns_server('127.0.0.1', '53001')
    srv_control.add_ddns_server_options('enable-updates', 'true')
    srv_control.add_ddns_server_options('generated-prefix', 'four')
    srv_control.add_ddns_server_options('qualifying-suffix', 'example.com')
    srv_control.add_forward_ddns('four.example.com.', 'EMPTY_KEY')
    srv_control.add_reverse_ddns('50.168.192.in-addr.arpa.', 'EMPTY_KEY')
    srv_control.build_and_send_config_files('SSH', 'config-file')
    srv_control.start_srv('DHCP', 'started')

    srv_control.use_dns_set_number('20')
    srv_control.start_srv('DNS', 'started')

    misc.test_procedure()
    srv_msg.dns_question_record('aa.four.example.com', 'A', 'IN')
    srv_msg.client_send_dns_query()

    misc.pass_criteria()
    srv_msg.send_wait_for_query('MUST', None)
    srv_msg.dns_option(None, 'ANSWER')

    misc.test_procedure()
    srv_msg.client_requests_option('1')
    srv_msg.client_send_msg('DISCOVER')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', None, 'OFFER')
    srv_msg.response_check_include_option('Response', None, '1')
    srv_msg.response_check_content('Response', None, 'yiaddr', '192.168.50.10')
    srv_msg.response_check_option_content('Response', '1', None, 'value', '255.255.255.0')

    misc.test_procedure()
    srv_msg.client_copy_option('server_id')
    srv_msg.client_does_include_with_value('requested_addr', '192.168.50.10')
    srv_msg.client_requests_option('1')
    srv_msg.client_sets_value('Client', 'FQDN_domain_name', 'aa.four.exae.com.')
    srv_msg.client_sets_value('Client', 'FQDN_flags', 'S')
    srv_msg.client_does_include('Client', None, 'fqdn')
    srv_msg.client_send_msg('REQUEST')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', None, 'ACK')
    srv_msg.response_check_content('Response', None, 'yiaddr', '192.168.50.10')
    srv_msg.response_check_include_option('Response', None, '1')
    srv_msg.response_check_option_content('Response', '1', None, 'value', '255.255.255.0')
    srv_msg.response_check_include_option('Response', None, '81')
    srv_msg.response_check_option_content('Response', '81', None, 'flags', '1')
    srv_msg.response_check_option_content('Response', '81', None, 'fqdn', 'aa.four.exae.com.')

    misc.test_procedure()
    srv_msg.dns_question_record('aa.four.example.com', 'A', 'IN')
    srv_msg.client_send_dns_query()

    misc.pass_criteria()
    srv_msg.send_wait_for_query('MUST', None)
    srv_msg.dns_option(None, 'ANSWER')

    misc.test_procedure()
    srv_msg.dns_question_record('10.50.168.192.in-addr.arpa.', 'PTR', 'IN')
    srv_msg.client_send_dns_query()

    misc.pass_criteria()
    srv_msg.send_wait_for_query('MUST', None)
    srv_msg.dns_option(None, 'ANSWER')


@pytest.mark.v4
@pytest.mark.ddns
@pytest.mark.notsig
@pytest.mark.forward_reverse_add
def test_ddns4_notsig_forw_and_rev_notenabled_Sflag():

    misc.test_setup()
    srv_control.config_srv_subnet('192.168.50.0/24', '192.168.50.10-192.168.50.10')
    srv_control.add_ddns_server('127.0.0.1', '53001')
    srv_control.add_ddns_server_options('enable-updates', 'false')
    srv_control.add_ddns_server_options('generated-prefix', 'four')
    srv_control.add_ddns_server_options('qualifying-suffix', 'example.com')
    srv_control.add_forward_ddns('four.example.com.', 'EMPTY_KEY')
    srv_control.add_reverse_ddns('50.168.192.in-addr.arpa.', 'EMPTY_KEY')
    srv_control.build_and_send_config_files('SSH', 'config-file')
    srv_control.start_srv('DHCP', 'started')

    srv_control.use_dns_set_number('20')
    srv_control.start_srv('DNS', 'started')

    misc.test_procedure()
    srv_msg.dns_question_record('aa.four.example.com', 'A', 'IN')
    srv_msg.client_send_dns_query()

    misc.pass_criteria()
    srv_msg.send_wait_for_query('MUST', None)
    srv_msg.dns_option(None, 'ANSWER')

    misc.test_procedure()
    srv_msg.client_requests_option('1')
    srv_msg.client_send_msg('DISCOVER')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', None, 'OFFER')
    srv_msg.response_check_include_option('Response', None, '1')
    srv_msg.response_check_content('Response', None, 'yiaddr', '192.168.50.10')
    srv_msg.response_check_option_content('Response', '1', None, 'value', '255.255.255.0')

    misc.test_procedure()
    srv_msg.client_copy_option('server_id')
    srv_msg.client_does_include_with_value('requested_addr', '192.168.50.10')
    srv_msg.client_requests_option('1')
    srv_msg.client_sets_value('Client', 'FQDN_domain_name', 'aa.four.example.com.')
    srv_msg.client_sets_value('Client', 'FQDN_flags', 'S')
    srv_msg.client_does_include('Client', None, 'fqdn')
    srv_msg.client_send_msg('REQUEST')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', None, 'ACK')
    srv_msg.response_check_content('Response', None, 'yiaddr', '192.168.50.10')
    srv_msg.response_check_include_option('Response', None, '1')
    srv_msg.response_check_option_content('Response', '1', None, 'value', '255.255.255.0')
    srv_msg.response_check_include_option('Response', None, '81')
    # Response option 81 MUST contain flags 10. #later make it 's' 'n' and 'o' should be 10
    srv_msg.response_check_option_content('Response', '81', None, 'fqdn', 'aa.four.example.com.')

    misc.test_procedure()
    srv_msg.dns_question_record('aa.four.example.com', 'A', 'IN')
    srv_msg.client_send_dns_query()

    misc.pass_criteria()
    srv_msg.send_wait_for_query('MUST', None)
    srv_msg.dns_option(None, 'ANSWER')

    misc.test_procedure()
    srv_msg.dns_question_record('10.50.168.192.in-addr.arpa.', 'PTR', 'IN')
    srv_msg.client_send_dns_query()

    misc.pass_criteria()
    srv_msg.send_wait_for_query('MUST', None)
    srv_msg.dns_option(None, 'ANSWER')


@pytest.mark.v4
@pytest.mark.ddns
@pytest.mark.notsig
@pytest.mark.forward_update
def test_ddns4_notsig_forw_and_rev_update_success_Sflag():

    misc.test_setup()
    srv_control.config_srv_subnet('192.168.50.0/24', '192.168.50.10-192.168.50.10')
    srv_control.add_ddns_server('127.0.0.1', '53001')
    srv_control.add_ddns_server_options('enable-updates', 'true')
    srv_control.add_ddns_server_options('generated-prefix', 'four')
    srv_control.add_ddns_server_options('qualifying-suffix', 'example.com')
    srv_control.add_forward_ddns('four.example.com.', 'EMPTY_KEY')
    srv_control.add_reverse_ddns('50.168.192.in-addr.arpa.', 'EMPTY_KEY')
    srv_control.build_and_send_config_files('SSH', 'config-file')
    srv_control.start_srv('DHCP', 'started')

    srv_control.use_dns_set_number('20')
    srv_control.start_srv('DNS', 'started')

    misc.test_procedure()
    srv_msg.dns_question_record('aa.four.example.com', 'A', 'IN')
    srv_msg.client_send_dns_query()

    misc.pass_criteria()
    srv_msg.send_wait_for_query('MUST', None)
    srv_msg.dns_option(None, 'ANSWER')

    misc.test_procedure()
    srv_msg.client_requests_option('1')
    srv_msg.client_send_msg('DISCOVER')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', None, 'OFFER')
    srv_msg.response_check_include_option('Response', None, '1')
    srv_msg.response_check_content('Response', None, 'yiaddr', '192.168.50.10')
    srv_msg.response_check_option_content('Response', '1', None, 'value', '255.255.255.0')

    misc.test_procedure()
    srv_msg.client_copy_option('server_id')
    srv_msg.client_does_include_with_value('requested_addr', '192.168.50.10')
    srv_msg.client_requests_option('1')
    srv_msg.client_sets_value('Client', 'FQDN_domain_name', 'aa.four.example.com.')
    srv_msg.client_sets_value('Client', 'FQDN_flags', 'S')
    srv_msg.client_does_include('Client', None, 'fqdn')
    srv_msg.client_send_msg('REQUEST')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', None, 'ACK')
    srv_msg.response_check_content('Response', None, 'yiaddr', '192.168.50.10')
    srv_msg.response_check_include_option('Response', None, '1')
    srv_msg.response_check_option_content('Response', '1', None, 'value', '255.255.255.0')
    srv_msg.response_check_include_option('Response', None, '81')
    srv_msg.response_check_option_content('Response', '81', None, 'flags', '1')
    srv_msg.response_check_option_content('Response', '81', None, 'fqdn', 'aa.four.example.com.')

    misc.test_procedure()
    srv_msg.dns_question_record('aa.four.example.com', 'A', 'IN')
    srv_msg.client_send_dns_query()

    misc.pass_criteria()
    srv_msg.send_wait_for_query('MUST', None)
    srv_msg.dns_option('NOT ', 'ANSWER')
    srv_msg.dns_option_content('ANSWER', None, 'rdata', '192.168.50.10')
    srv_msg.dns_option_content('ANSWER', None, 'rrname', 'aa.four.example.com.')

    misc.test_procedure()
    srv_msg.dns_question_record('10.50.168.192.in-addr.arpa.', 'PTR', 'IN')
    srv_msg.client_send_dns_query()

    misc.pass_criteria()
    srv_msg.send_wait_for_query('MUST', None)
    srv_msg.dns_option('NOT ', 'ANSWER')
    srv_msg.dns_option_content('ANSWER', None, 'rdata', 'aa.four.example.com.')
    srv_msg.dns_option_content('ANSWER', None, 'rrname', '10.50.168.192.in-addr.arpa.')

    misc.test_setup()
    srv_control.start_srv('DHCP', 'stopped')
    srv_control.clear_leases('leases')

    misc.test_setup()
    srv_control.config_srv_subnet('192.168.50.0/24', '192.168.50.11-192.168.50.11')
    srv_control.add_ddns_server('127.0.0.1', '53001')
    srv_control.add_ddns_server_options('enable-updates', 'true')
    srv_control.add_ddns_server_options('generated-prefix', 'four')
    srv_control.add_ddns_server_options('qualifying-suffix', 'example.com')
    srv_control.add_forward_ddns('four.example.com.', 'EMPTY_KEY')
    srv_control.add_reverse_ddns('50.168.192.in-addr.arpa.', 'EMPTY_KEY')
    srv_control.build_and_send_config_files('SSH', 'config-file')
    srv_control.start_srv('DHCP', 'started')

    misc.test_procedure()
    srv_msg.dns_question_record('aa.four.example.com', 'A', 'IN')
    srv_msg.client_send_dns_query()

    misc.pass_criteria()
    srv_msg.send_wait_for_query('MUST', None)
    srv_msg.dns_option('NOT ', 'ANSWER')
    srv_msg.dns_option_content('ANSWER', None, 'rdata', '192.168.50.10')
    srv_msg.dns_option_content('ANSWER', None, 'rrname', 'aa.four.example.com.')

    misc.test_procedure()
    srv_msg.dns_question_record('10.50.168.192.in-addr.arpa.', 'PTR', 'IN')
    srv_msg.client_send_dns_query()

    misc.pass_criteria()
    srv_msg.send_wait_for_query('MUST', None)
    srv_msg.dns_option('NOT ', 'ANSWER')
    srv_msg.dns_option_content('ANSWER', None, 'rdata', 'aa.four.example.com.')
    srv_msg.dns_option_content('ANSWER', None, 'rrname', '10.50.168.192.in-addr.arpa.')

    misc.test_procedure()
    srv_msg.client_requests_option('1')
    srv_msg.client_send_msg('DISCOVER')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', None, 'OFFER')
    srv_msg.response_check_include_option('Response', None, '1')
    srv_msg.response_check_content('Response', None, 'yiaddr', '192.168.50.11')
    srv_msg.response_check_option_content('Response', '1', None, 'value', '255.255.255.0')

    misc.test_procedure()
    srv_msg.client_copy_option('server_id')
    srv_msg.client_does_include_with_value('requested_addr', '192.168.50.11')
    srv_msg.client_requests_option('1')
    srv_msg.client_sets_value('Client', 'FQDN_domain_name', 'aa.four.example.com.')
    srv_msg.client_sets_value('Client', 'FQDN_flags', 'S')
    srv_msg.client_does_include('Client', None, 'fqdn')
    srv_msg.client_send_msg('REQUEST')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', None, 'ACK')
    srv_msg.response_check_content('Response', None, 'yiaddr', '192.168.50.11')
    srv_msg.response_check_include_option('Response', None, '1')
    srv_msg.response_check_option_content('Response', '1', None, 'value', '255.255.255.0')
    srv_msg.response_check_include_option('Response', None, '81')
    srv_msg.response_check_option_content('Response', '81', None, 'flags', '1')
    srv_msg.response_check_option_content('Response', '81', None, 'fqdn', 'aa.four.example.com.')

    misc.test_procedure()
    srv_msg.dns_question_record('aa.four.example.com', 'A', 'IN')
    srv_msg.client_send_dns_query()

    misc.pass_criteria()
    srv_msg.send_wait_for_query('MUST', None)
    srv_msg.dns_option('NOT ', 'ANSWER')
    srv_msg.dns_option_content('ANSWER', None, 'rdata', '192.168.50.11')
    srv_msg.dns_option_content('ANSWER', None, 'rrname', 'aa.four.example.com.')

    misc.test_procedure()
    srv_msg.dns_question_record('11.50.168.192.in-addr.arpa.', 'PTR', 'IN')
    srv_msg.client_send_dns_query()

    misc.pass_criteria()
    srv_msg.send_wait_for_query('MUST', None)
    srv_msg.dns_option('NOT ', 'ANSWER')
    srv_msg.dns_option_content('ANSWER', None, 'rdata', 'aa.four.example.com.')
    srv_msg.dns_option_content('ANSWER', None, 'rrname', '11.50.168.192.in-addr.arpa.')


@pytest.mark.v4
@pytest.mark.ddns
@pytest.mark.notsig
@pytest.mark.forward_reverse_add
def test_ddns4_notsig_forw_and_rev_two_dhci_Sflag():

    misc.test_setup()
    srv_control.config_srv_subnet('192.168.50.0/24', '192.168.50.10-192.168.50.11')
    srv_control.add_ddns_server('127.0.0.1', '53001')
    srv_control.add_ddns_server_options('enable-updates', 'true')
    srv_control.add_ddns_server_options('generated-prefix', 'four')
    srv_control.add_ddns_server_options('qualifying-suffix', 'example.com')
    srv_control.add_forward_ddns('four.example.com.', 'EMPTY_KEY')
    srv_control.add_reverse_ddns('50.168.192.in-addr.arpa.', 'EMPTY_KEY')
    srv_control.build_and_send_config_files('SSH', 'config-file')
    srv_control.start_srv('DHCP', 'started')

    srv_control.use_dns_set_number('20')
    srv_control.start_srv('DNS', 'started')

    misc.test_procedure()
    srv_msg.dns_question_record('client1.four.example.com', 'A', 'IN')
    srv_msg.client_send_dns_query()

    misc.pass_criteria()
    srv_msg.send_wait_for_query('MUST', None)
    srv_msg.dns_option(None, 'ANSWER')

    misc.test_procedure()
    srv_msg.dns_question_record('client2.four.example.com', 'A', 'IN')
    srv_msg.client_send_dns_query()

    misc.pass_criteria()
    srv_msg.send_wait_for_query('MUST', None)
    srv_msg.dns_option(None, 'ANSWER')

    misc.test_procedure()
    srv_msg.client_sets_value('Client', 'chaddr', '00:00:00:00:00:11')
    srv_msg.client_send_msg('DISCOVER')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', None, 'OFFER')
    srv_msg.response_check_include_option('Response', None, '1')
    srv_msg.response_check_content('Response', None, 'yiaddr', '192.168.50.10')
    srv_msg.response_check_option_content('Response', '1', None, 'value', '255.255.255.0')

    misc.test_procedure()
    srv_msg.client_sets_value('Client', 'chaddr', '00:00:00:00:00:11')
    srv_msg.client_copy_option('server_id')
    srv_msg.client_does_include_with_value('requested_addr', '192.168.50.10')
    srv_msg.client_requests_option('1')
    srv_msg.client_sets_value('Client', 'FQDN_domain_name', 'client1.four.example.com.')
    srv_msg.client_sets_value('Client', 'FQDN_flags', 'S')
    srv_msg.client_does_include('Client', None, 'fqdn')
    srv_msg.client_send_msg('REQUEST')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', None, 'ACK')
    srv_msg.response_check_content('Response', None, 'yiaddr', '192.168.50.10')
    srv_msg.response_check_include_option('Response', None, '1')
    srv_msg.response_check_option_content('Response', '1', None, 'value', '255.255.255.0')
    srv_msg.response_check_include_option('Response', None, '81')
    srv_msg.response_check_option_content('Response', '81', None, 'flags', '1')
    srv_msg.response_check_option_content('Response',
                                          '81',
                                          None,
                                          'fqdn',
                                          'client1.four.example.com.')

    misc.test_procedure()
    srv_msg.dns_question_record('client1.four.example.com', 'A', 'IN')
    srv_msg.client_send_dns_query()

    misc.pass_criteria()
    srv_msg.send_wait_for_query('MUST', None)
    srv_msg.dns_option('NOT ', 'ANSWER')
    srv_msg.dns_option_content('ANSWER', None, 'rdata', '192.168.50.10')
    srv_msg.dns_option_content('ANSWER', None, 'rrname', 'client1.four.example.com.')

    #  Client 2 add
    misc.test_procedure()
    srv_msg.client_sets_value('Client', 'chaddr', '00:00:00:00:00:12')
    srv_msg.client_send_msg('DISCOVER')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', None, 'OFFER')
    srv_msg.response_check_include_option('Response', None, '1')
    srv_msg.response_check_content('Response', None, 'yiaddr', '192.168.50.11')
    srv_msg.response_check_option_content('Response', '1', None, 'value', '255.255.255.0')

    misc.test_procedure()
    srv_msg.client_sets_value('Client', 'chaddr', '00:00:00:00:00:12')
    srv_msg.client_copy_option('server_id')
    srv_msg.client_does_include_with_value('requested_addr', '192.168.50.11')
    srv_msg.client_requests_option('1')
    srv_msg.client_sets_value('Client', 'FQDN_domain_name', 'client2.four.example.com.')
    srv_msg.client_sets_value('Client', 'FQDN_flags', 'S')
    srv_msg.client_does_include('Client', None, 'fqdn')
    srv_msg.client_send_msg('REQUEST')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', None, 'ACK')
    srv_msg.response_check_content('Response', None, 'yiaddr', '192.168.50.11')
    srv_msg.response_check_include_option('Response', None, '1')
    srv_msg.response_check_option_content('Response', '1', None, 'value', '255.255.255.0')
    srv_msg.response_check_include_option('Response', None, '81')
    srv_msg.response_check_option_content('Response', '81', None, 'flags', '1')
    srv_msg.response_check_option_content('Response',
                                          '81',
                                          None,
                                          'fqdn',
                                          'client2.four.example.com.')

    misc.test_procedure()
    srv_msg.dns_question_record('client2.four.example.com', 'A', 'IN')
    srv_msg.client_send_dns_query()

    misc.pass_criteria()
    srv_msg.send_wait_for_query('MUST', None)
    srv_msg.dns_option('NOT ', 'ANSWER')
    srv_msg.dns_option_content('ANSWER', None, 'rdata', '192.168.50.11')
    srv_msg.dns_option_content('ANSWER', None, 'rrname', 'client2.four.example.com.')


@pytest.mark.v4
@pytest.mark.ddns
@pytest.mark.notsig
@pytest.mark.forward_reverse_add
def test_ddns4_notsig_forw_and_rev_dhci_conflicts_Sflag():

    misc.test_setup()
    srv_control.config_srv_subnet('192.168.50.0/24', '192.168.50.10-192.168.50.11')
    srv_control.add_ddns_server('127.0.0.1', '53001')
    srv_control.add_ddns_server_options('enable-updates', 'true')
    srv_control.add_ddns_server_options('generated-prefix', 'four')
    srv_control.add_ddns_server_options('qualifying-suffix', 'example.com')
    srv_control.add_forward_ddns('four.example.com.', 'EMPTY_KEY')
    srv_control.add_reverse_ddns('50.168.192.in-addr.arpa.', 'EMPTY_KEY')
    srv_control.build_and_send_config_files('SSH', 'config-file')
    srv_control.start_srv('DHCP', 'started')

    srv_control.use_dns_set_number('20')
    srv_control.start_srv('DNS', 'started')

    misc.test_procedure()
    srv_msg.dns_question_record('client1.four.example.com', 'A', 'IN')
    srv_msg.client_send_dns_query()

    misc.pass_criteria()
    srv_msg.send_wait_for_query('MUST', None)
    srv_msg.dns_option(None, 'ANSWER')

    misc.test_procedure()
    srv_msg.dns_question_record('10.50.168.192.in-addr.arpa.', 'PTR', 'IN')
    srv_msg.client_send_dns_query()

    misc.pass_criteria()
    srv_msg.send_wait_for_query('MUST', None)
    srv_msg.dns_option(None, 'ANSWER')

    misc.test_procedure()
    srv_msg.dns_question_record('client2.four.example.com', 'A', 'IN')
    srv_msg.client_send_dns_query()

    misc.pass_criteria()
    srv_msg.send_wait_for_query('MUST', None)
    srv_msg.dns_option(None, 'ANSWER')

    misc.test_procedure()
    srv_msg.dns_question_record('11.50.168.192.in-addr.arpa.', 'PTR', 'IN')
    srv_msg.client_send_dns_query()

    misc.pass_criteria()
    srv_msg.send_wait_for_query('MUST', None)
    srv_msg.dns_option(None, 'ANSWER')

    misc.test_procedure()
    srv_msg.client_sets_value('Client', 'chaddr', '00:00:00:00:00:11')
    srv_msg.client_send_msg('DISCOVER')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', None, 'OFFER')
    srv_msg.response_check_include_option('Response', None, '1')
    srv_msg.response_check_content('Response', None, 'yiaddr', '192.168.50.10')
    srv_msg.response_check_option_content('Response', '1', None, 'value', '255.255.255.0')

    misc.test_procedure()
    srv_msg.client_sets_value('Client', 'chaddr', '00:00:00:00:00:11')
    srv_msg.client_copy_option('server_id')
    srv_msg.client_does_include_with_value('requested_addr', '192.168.50.10')
    srv_msg.client_requests_option('1')
    srv_msg.client_sets_value('Client', 'FQDN_domain_name', 'client1.four.example.com.')
    srv_msg.client_sets_value('Client', 'FQDN_flags', 'S')
    srv_msg.client_does_include('Client', None, 'fqdn')
    srv_msg.client_send_msg('REQUEST')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', None, 'ACK')
    srv_msg.response_check_content('Response', None, 'yiaddr', '192.168.50.10')
    srv_msg.response_check_include_option('Response', None, '1')
    srv_msg.response_check_option_content('Response', '1', None, 'value', '255.255.255.0')
    srv_msg.response_check_include_option('Response', None, '81')
    srv_msg.response_check_option_content('Response', '81', None, 'flags', '1')
    srv_msg.response_check_option_content('Response',
                                          '81',
                                          None,
                                          'fqdn',
                                          'client1.four.example.com.')

    misc.test_procedure()
    srv_msg.dns_question_record('client1.four.example.com', 'A', 'IN')
    srv_msg.client_send_dns_query()

    misc.pass_criteria()
    srv_msg.send_wait_for_query('MUST', None)
    srv_msg.dns_option('NOT ', 'ANSWER')
    srv_msg.dns_option_content('ANSWER', None, 'rdata', '192.168.50.10')
    srv_msg.dns_option_content('ANSWER', None, 'rrname', 'client1.four.example.com.')

    misc.test_procedure()
    srv_msg.dns_question_record('10.50.168.192.in-addr.arpa.', 'PTR', 'IN')
    srv_msg.client_send_dns_query()

    misc.pass_criteria()
    srv_msg.send_wait_for_query('MUST', None)
    srv_msg.dns_option('NOT ', 'ANSWER')
    srv_msg.dns_option_content('ANSWER', None, 'rdata', 'client1.four.example.com.')
    srv_msg.dns_option_content('ANSWER', None, 'rrname', '10.50.168.192.in-addr.arpa.')

    #  Client 2 add
    misc.test_procedure()
    srv_msg.client_sets_value('Client', 'chaddr', '00:00:00:00:00:12')
    srv_msg.client_send_msg('DISCOVER')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', None, 'OFFER')
    srv_msg.response_check_include_option('Response', None, '1')
    srv_msg.response_check_content('Response', None, 'yiaddr', '192.168.50.11')
    srv_msg.response_check_option_content('Response', '1', None, 'value', '255.255.255.0')

    misc.test_procedure()
    srv_msg.client_sets_value('Client', 'chaddr', '00:00:00:00:00:12')
    srv_msg.client_copy_option('server_id')
    srv_msg.client_does_include_with_value('requested_addr', '192.168.50.11')
    srv_msg.client_requests_option('1')
    srv_msg.client_sets_value('Client', 'FQDN_domain_name', 'client2.four.example.com.')
    srv_msg.client_sets_value('Client', 'FQDN_flags', 'S')
    srv_msg.client_does_include('Client', None, 'fqdn')
    srv_msg.client_send_msg('REQUEST')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', None, 'ACK')
    srv_msg.response_check_content('Response', None, 'yiaddr', '192.168.50.11')
    srv_msg.response_check_include_option('Response', None, '1')
    srv_msg.response_check_option_content('Response', '1', None, 'value', '255.255.255.0')
    srv_msg.response_check_include_option('Response', None, '81')
    srv_msg.response_check_option_content('Response', '81', None, 'flags', '1')
    srv_msg.response_check_option_content('Response',
                                          '81',
                                          None,
                                          'fqdn',
                                          'client2.four.example.com.')

    misc.test_procedure()
    srv_msg.dns_question_record('client2.four.example.com', 'A', 'IN')
    srv_msg.client_send_dns_query()

    misc.pass_criteria()
    srv_msg.send_wait_for_query('MUST', None)
    srv_msg.dns_option('NOT ', 'ANSWER')
    srv_msg.dns_option_content('ANSWER', None, 'rdata', '192.168.50.11')
    srv_msg.dns_option_content('ANSWER', None, 'rrname', 'client2.four.example.com.')

    misc.test_procedure()
    srv_msg.dns_question_record('11.50.168.192.in-addr.arpa.', 'PTR', 'IN')
    srv_msg.client_send_dns_query()

    misc.pass_criteria()
    srv_msg.send_wait_for_query('MUST', None)
    srv_msg.dns_option('NOT ', 'ANSWER')
    srv_msg.dns_option_content('ANSWER', None, 'rdata', 'client2.four.example.com.')
    srv_msg.dns_option_content('ANSWER', None, 'rrname', '11.50.168.192.in-addr.arpa.')

    #  Client 2 try to update client's 1 domain
    misc.test_procedure()
    srv_msg.client_sets_value('Client', 'chaddr', '00:00:00:00:00:12')
    srv_msg.client_send_msg('DISCOVER')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', None, 'OFFER')
    srv_msg.response_check_include_option('Response', None, '1')
    srv_msg.response_check_content('Response', None, 'yiaddr', '192.168.50.11')
    srv_msg.response_check_option_content('Response', '1', None, 'value', '255.255.255.0')

    misc.test_procedure()
    srv_msg.client_sets_value('Client', 'chaddr', '00:00:00:00:00:12')
    srv_msg.client_copy_option('server_id')
    srv_msg.client_does_include_with_value('requested_addr', '192.168.50.11')
    srv_msg.client_requests_option('1')
    srv_msg.client_sets_value('Client', 'FQDN_domain_name', 'client1.four.example.com.')
    srv_msg.client_sets_value('Client', 'FQDN_flags', 'S')
    srv_msg.client_does_include('Client', None, 'fqdn')
    srv_msg.client_send_msg('REQUEST')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', None, 'ACK')
    srv_msg.response_check_content('Response', None, 'yiaddr', '192.168.50.11')
    srv_msg.response_check_include_option('Response', None, '1')
    srv_msg.response_check_option_content('Response', '1', None, 'value', '255.255.255.0')
    srv_msg.response_check_include_option('Response', None, '81')
    srv_msg.response_check_option_content('Response', '81', None, 'flags', '1')
    srv_msg.response_check_option_content('Response',
                                          '81',
                                          None,
                                          'fqdn',
                                          'client1.four.example.com.')

    #  address and domain name should not be changed!
    misc.test_procedure()
    srv_msg.dns_question_record('client1.four.example.com', 'A', 'IN')
    srv_msg.client_send_dns_query()

    misc.pass_criteria()
    srv_msg.send_wait_for_query('MUST', None)
    srv_msg.dns_option('NOT ', 'ANSWER')
    srv_msg.dns_option_content('ANSWER', None, 'rdata', '192.168.50.10')
    srv_msg.dns_option_content('ANSWER', None, 'rrname', 'client1.four.example.com.')

    misc.test_procedure()
    srv_msg.dns_question_record('10.50.168.192.in-addr.arpa.', 'PTR', 'IN')
    srv_msg.client_send_dns_query()

    misc.pass_criteria()
    srv_msg.send_wait_for_query('MUST', None)
    srv_msg.dns_option('NOT ', 'ANSWER')
    srv_msg.dns_option_content('ANSWER', None, 'rdata', 'client1.four.example.com.')
    srv_msg.dns_option_content('ANSWER', None, 'rrname', '10.50.168.192.in-addr.arpa.')

    misc.test_procedure()
    srv_msg.dns_question_record('client2.four.example.com', 'A', 'IN')
    srv_msg.client_send_dns_query()

    misc.pass_criteria()
    srv_msg.send_wait_for_query('MUST', None)
    srv_msg.dns_option(None, 'ANSWER')

    misc.test_procedure()
    srv_msg.dns_question_record('11.50.168.192.in-addr.arpa.', 'PTR', 'IN')
    srv_msg.client_send_dns_query()

    misc.pass_criteria()
    srv_msg.send_wait_for_query('MUST', None)
    srv_msg.dns_option(None, 'ANSWER')


@pytest.mark.v4
@pytest.mark.ddns
@pytest.mark.notsig
@pytest.mark.forward_reverse_add
def test_ddns4_notsig_forw_and_rev_add_success_withoutflag_override_client():

    misc.test_setup()
    srv_control.config_srv_subnet('192.168.50.0/24', '192.168.50.10-192.168.50.10')
    srv_control.add_ddns_server('127.0.0.1', '53001')
    srv_control.add_ddns_server_options('override-client-update', 'true')
    srv_control.add_ddns_server_options('enable-updates', 'true')
    srv_control.add_ddns_server_options('generated-prefix', 'four')
    srv_control.add_ddns_server_options('qualifying-suffix', 'example.com')
    srv_control.add_forward_ddns('four.example.com.', 'EMPTY_KEY')
    srv_control.add_reverse_ddns('50.168.192.in-addr.arpa.', 'EMPTY_KEY')
    srv_control.build_and_send_config_files('SSH', 'config-file')
    srv_control.start_srv('DHCP', 'started')

    srv_control.use_dns_set_number('20')
    srv_control.start_srv('DNS', 'started')

    misc.test_procedure()
    srv_msg.dns_question_record('aa.four.example.com', 'A', 'IN')
    srv_msg.client_send_dns_query()

    misc.pass_criteria()
    srv_msg.send_wait_for_query('MUST', None)
    srv_msg.dns_option(None, 'ANSWER')

    misc.test_procedure()
    srv_msg.client_requests_option('1')
    srv_msg.client_send_msg('DISCOVER')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', None, 'OFFER')
    srv_msg.response_check_include_option('Response', None, '1')
    srv_msg.response_check_content('Response', None, 'yiaddr', '192.168.50.10')
    srv_msg.response_check_option_content('Response', '1', None, 'value', '255.255.255.0')

    misc.test_procedure()
    srv_msg.client_copy_option('server_id')
    srv_msg.client_does_include_with_value('requested_addr', '192.168.50.10')
    srv_msg.client_requests_option('1')
    srv_msg.client_sets_value('Client', 'FQDN_domain_name', 'aa.four.example.com.')
    srv_msg.client_does_include('Client', None, 'fqdn')
    srv_msg.client_send_msg('REQUEST')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', None, 'ACK')
    srv_msg.response_check_content('Response', None, 'yiaddr', '192.168.50.10')
    srv_msg.response_check_include_option('Response', None, '1')
    srv_msg.response_check_option_content('Response', '1', None, 'value', '255.255.255.0')
    srv_msg.response_check_include_option('Response', None, '81')
    srv_msg.response_check_option_content('Response', '81', None, 'flags', '3')
    srv_msg.response_check_option_content('Response', '81', None, 'fqdn', 'aa.four.example.com.')

    misc.test_procedure()
    srv_msg.dns_question_record('aa.four.example.com', 'A', 'IN')
    srv_msg.client_send_dns_query()

    misc.pass_criteria()
    srv_msg.send_wait_for_query('MUST', None)
    srv_msg.dns_option('NOT ', 'ANSWER')
    srv_msg.dns_option_content('ANSWER', None, 'rdata', '192.168.50.10')
    srv_msg.dns_option_content('ANSWER', None, 'rrname', 'aa.four.example.com.')

    misc.test_procedure()
    srv_msg.dns_question_record('10.50.168.192.in-addr.arpa.', 'PTR', 'IN')
    srv_msg.client_send_dns_query()

    misc.pass_criteria()
    srv_msg.send_wait_for_query('MUST', None)
    srv_msg.dns_option('NOT ', 'ANSWER')
    srv_msg.dns_option_content('ANSWER', None, 'rdata', 'aa.four.example.com.')
    srv_msg.dns_option_content('ANSWER', None, 'rrname', '10.50.168.192.in-addr.arpa.')


@pytest.mark.v4
@pytest.mark.ddns
@pytest.mark.notsig
@pytest.mark.reverse_add
def test_ddns4_notsig_rev_success_withoutflag():

    misc.test_setup()
    srv_control.config_srv_subnet('192.168.50.0/24', '192.168.50.10-192.168.50.10')
    srv_control.add_ddns_server('127.0.0.1', '53001')
    srv_control.add_ddns_server_options('enable-updates', 'true')
    srv_control.add_ddns_server_options('generated-prefix', 'four')
    srv_control.add_ddns_server_options('qualifying-suffix', 'example.com')
    srv_control.add_forward_ddns('four.example.com.', 'EMPTY_KEY')
    srv_control.add_reverse_ddns('50.168.192.in-addr.arpa.', 'EMPTY_KEY')
    srv_control.build_and_send_config_files('SSH', 'config-file')
    srv_control.start_srv('DHCP', 'started')

    srv_control.use_dns_set_number('20')
    srv_control.start_srv('DNS', 'started')

    misc.test_procedure()
    srv_msg.dns_question_record('aa.four.example.com', 'A', 'IN')
    srv_msg.client_send_dns_query()

    misc.pass_criteria()
    srv_msg.send_wait_for_query('MUST', None)
    srv_msg.dns_option(None, 'ANSWER')

    misc.test_procedure()
    srv_msg.dns_question_record('10.50.168.192.in-addr.arpa.', 'PTR', 'IN')
    srv_msg.client_send_dns_query()

    misc.pass_criteria()
    srv_msg.send_wait_for_query('MUST', None)
    srv_msg.dns_option(None, 'ANSWER')

    misc.test_procedure()
    srv_msg.client_requests_option('1')
    srv_msg.client_send_msg('DISCOVER')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', None, 'OFFER')
    srv_msg.response_check_include_option('Response', None, '1')
    srv_msg.response_check_content('Response', None, 'yiaddr', '192.168.50.10')
    srv_msg.response_check_option_content('Response', '1', None, 'value', '255.255.255.0')

    misc.test_procedure()
    srv_msg.client_copy_option('server_id')
    srv_msg.client_does_include_with_value('requested_addr', '192.168.50.10')
    srv_msg.client_requests_option('1')
    srv_msg.client_sets_value('Client', 'FQDN_domain_name', 'aa.four.example.com.')
    srv_msg.client_does_include('Client', None, 'fqdn')
    srv_msg.client_send_msg('REQUEST')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', None, 'ACK')
    srv_msg.response_check_content('Response', None, 'yiaddr', '192.168.50.10')
    srv_msg.response_check_include_option('Response', None, '1')
    srv_msg.response_check_option_content('Response', '1', None, 'value', '255.255.255.0')
    srv_msg.response_check_include_option('Response', None, '81')
    srv_msg.response_check_option_content('Response', '81', None, 'flags', '0')
    srv_msg.response_check_option_content('Response', '81', None, 'fqdn', 'aa.four.example.com.')

    misc.test_procedure()
    srv_msg.dns_question_record('10.50.168.192.in-addr.arpa.', 'PTR', 'IN')
    srv_msg.client_send_dns_query()

    misc.pass_criteria()
    srv_msg.send_wait_for_query('MUST', None)
    srv_msg.dns_option('NOT ', 'ANSWER')
    srv_msg.dns_option_content('ANSWER', None, 'rdata', 'aa.four.example.com.')
    srv_msg.dns_option_content('ANSWER', None, 'rrname', '10.50.168.192.in-addr.arpa.')

    misc.test_procedure()
    srv_msg.dns_question_record('aa.four.example.com', 'A', 'IN')
    srv_msg.client_send_dns_query()

    misc.pass_criteria()
    srv_msg.send_wait_for_query('MUST', None)
    srv_msg.dns_option(None, 'ANSWER')


@pytest.mark.v4
@pytest.mark.ddns
@pytest.mark.notsig
@pytest.mark.reverse_add
def test_ddns4_notsig_rev_withoutflag_notenabled():

    misc.test_setup()
    srv_control.config_srv_subnet('192.168.50.0/24', '192.168.50.10-192.168.50.10')
    srv_control.add_ddns_server('127.0.0.1', '53001')
    srv_control.add_ddns_server_options('enable-updates', 'false')
    srv_control.add_ddns_server_options('generated-prefix', 'four')
    srv_control.add_ddns_server_options('qualifying-suffix', 'example.com')
    srv_control.add_forward_ddns('four.example.com.', 'EMPTY_KEY')
    srv_control.add_reverse_ddns('50.168.192.in-addr.arpa.', 'EMPTY_KEY')
    srv_control.build_and_send_config_files('SSH', 'config-file')
    srv_control.start_srv('DHCP', 'started')

    srv_control.use_dns_set_number('20')
    srv_control.start_srv('DNS', 'started')

    misc.test_procedure()
    srv_msg.dns_question_record('aa.four.example.com', 'A', 'IN')
    srv_msg.client_send_dns_query()

    misc.pass_criteria()
    srv_msg.send_wait_for_query('MUST', None)
    srv_msg.dns_option(None, 'ANSWER')

    misc.test_procedure()
    srv_msg.dns_question_record('10.50.168.192.in-addr.arpa.', 'PTR', 'IN')
    srv_msg.client_send_dns_query()

    misc.pass_criteria()
    srv_msg.send_wait_for_query('MUST', None)
    srv_msg.dns_option(None, 'ANSWER')

    misc.test_procedure()
    srv_msg.client_requests_option('1')
    srv_msg.client_send_msg('DISCOVER')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', None, 'OFFER')
    srv_msg.response_check_include_option('Response', None, '1')
    srv_msg.response_check_content('Response', None, 'yiaddr', '192.168.50.10')
    srv_msg.response_check_option_content('Response', '1', None, 'value', '255.255.255.0')

    misc.test_procedure()
    srv_msg.client_copy_option('server_id')
    srv_msg.client_does_include_with_value('requested_addr', '192.168.50.10')
    srv_msg.client_requests_option('1')
    srv_msg.client_sets_value('Client', 'FQDN_domain_name', 'aa.four.example.com.')
    srv_msg.client_does_include('Client', None, 'fqdn')
    srv_msg.client_send_msg('REQUEST')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', None, 'ACK')
    srv_msg.response_check_content('Response', None, 'yiaddr', '192.168.50.10')
    srv_msg.response_check_include_option('Response', None, '1')
    srv_msg.response_check_option_content('Response', '1', None, 'value', '255.255.255.0')
    srv_msg.response_check_include_option('Response', None, '81')
    # Response option 81 MUST contain flags 0. #later make it 's' 'n' and 'o' should be 10
    srv_msg.response_check_option_content('Response', '81', None, 'fqdn', 'aa.four.example.com.')

    misc.test_procedure()
    srv_msg.dns_question_record('10.50.168.192.in-addr.arpa.', 'PTR', 'IN')
    srv_msg.client_send_dns_query()

    misc.pass_criteria()
    srv_msg.send_wait_for_query('MUST', None)
    srv_msg.dns_option(None, 'ANSWER')

    misc.test_procedure()
    srv_msg.dns_question_record('aa.four.example.com', 'A', 'IN')
    srv_msg.client_send_dns_query()

    misc.pass_criteria()
    srv_msg.send_wait_for_query('MUST', None)
    srv_msg.dns_option(None, 'ANSWER')


@pytest.mark.v4
@pytest.mark.ddns
@pytest.mark.notsig
@pytest.mark.reverse_add
def test_ddns4_notsig_rev_Nflag_override_no_update():

    misc.test_setup()
    srv_control.config_srv_subnet('192.168.50.0/24', '192.168.50.10-192.168.50.10')
    srv_control.add_ddns_server('127.0.0.1', '53001')
    srv_control.add_ddns_server_options('override-no-update', 'true')
    srv_control.add_ddns_server_options('enable-updates', 'true')
    srv_control.add_ddns_server_options('generated-prefix', 'four')
    srv_control.add_ddns_server_options('qualifying-suffix', 'example.com')
    srv_control.add_forward_ddns('four.example.com.', 'EMPTY_KEY')
    srv_control.add_reverse_ddns('50.168.192.in-addr.arpa.', 'EMPTY_KEY')
    srv_control.build_and_send_config_files('SSH', 'config-file')
    srv_control.start_srv('DHCP', 'started')

    srv_control.use_dns_set_number('20')
    srv_control.start_srv('DNS', 'started')

    misc.test_procedure()
    srv_msg.dns_question_record('aa.four.example.com', 'A', 'IN')
    srv_msg.client_send_dns_query()

    misc.pass_criteria()
    srv_msg.send_wait_for_query('MUST', None)
    srv_msg.dns_option(None, 'ANSWER')

    misc.test_procedure()
    srv_msg.client_requests_option('1')
    srv_msg.client_send_msg('DISCOVER')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', None, 'OFFER')
    srv_msg.response_check_include_option('Response', None, '1')
    srv_msg.response_check_content('Response', None, 'yiaddr', '192.168.50.10')
    srv_msg.response_check_option_content('Response', '1', None, 'value', '255.255.255.0')

    misc.test_procedure()
    srv_msg.client_copy_option('server_id')
    srv_msg.client_does_include_with_value('requested_addr', '192.168.50.10')
    srv_msg.client_requests_option('1')
    srv_msg.client_sets_value('Client', 'FQDN_flags', 'N')
    srv_msg.client_sets_value('Client', 'FQDN_domain_name', 'aa.four.example.com.')
    srv_msg.client_does_include('Client', None, 'fqdn')
    srv_msg.client_send_msg('REQUEST')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', None, 'ACK')
    srv_msg.response_check_content('Response', None, 'yiaddr', '192.168.50.10')
    srv_msg.response_check_include_option('Response', None, '1')
    srv_msg.response_check_option_content('Response', '1', None, 'value', '255.255.255.0')
    srv_msg.response_check_include_option('Response', None, '81')
    srv_msg.response_check_option_content('Response', '81', None, 'flags', '3')
    srv_msg.response_check_option_content('Response', '81', None, 'fqdn', 'aa.four.example.com.')

    misc.test_procedure()
    srv_msg.dns_question_record('10.50.168.192.in-addr.arpa.', 'PTR', 'IN')
    srv_msg.client_send_dns_query()

    misc.pass_criteria()
    srv_msg.send_wait_for_query('MUST', None)
    srv_msg.dns_option('NOT ', 'ANSWER')
    srv_msg.dns_option_content('ANSWER', None, 'rdata', 'aa.four.example.com.')
    srv_msg.dns_option_content('ANSWER', None, 'rrname', '10.50.168.192.in-addr.arpa.')

    misc.test_procedure()
    srv_msg.dns_question_record('aa.four.example.com.', 'A', 'IN')
    srv_msg.client_send_dns_query()

    misc.pass_criteria()
    srv_msg.send_wait_for_query('MUST', None)
    srv_msg.dns_option('NOT ', 'ANSWER')
    srv_msg.dns_option_content('ANSWER', None, 'rdata', '192.168.50.10')
    srv_msg.dns_option_content('ANSWER', None, 'rrname', 'aa.four.example.com.')
