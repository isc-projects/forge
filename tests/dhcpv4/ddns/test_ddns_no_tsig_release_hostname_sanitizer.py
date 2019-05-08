"""DDNS without TSIG"""

# pylint: disable=invalid-name,line-too-long

import pytest

import srv_control
import misc
import srv_msg


@pytest.mark.v4
@pytest.mark.ddns
@pytest.mark.notsig
@pytest.mark.forward_reverse_remove
@pytest.mark.hostname_sanitization
def test_ddns4_notsig_forw_and_rev_release_hostname_sanitization_replace_1():

    misc.test_setup()
    srv_control.config_srv_subnet('192.168.50.0/24', '192.168.50.10-192.168.50.10')
    srv_control.add_ddns_server('127.0.0.1', '53001')
    srv_control.add_ddns_server_options('enable-updates', 'true')
    srv_control.add_ddns_server_options('qualifying-suffix', 'example.com')
    srv_control.add_ddns_server_options('hostname-char-set', '[^A-Za-z0-9.-]')
    srv_control.add_ddns_server_options('hostname-char-replacement', 'x')
    srv_control.add_forward_ddns('four.example.com.', 'EMPTY_KEY')
    srv_control.add_reverse_ddns('50.168.192.in-addr.arpa.', 'EMPTY_KEY')
    srv_control.build_and_send_config_files('SSH', 'config-file')
    srv_control.start_srv('DHCP', 'started')

    srv_control.use_dns_set_number('20')
    srv_control.start_srv('DNS', 'started')

    misc.test_procedure()
    srv_msg.dns_question_record('xaax.four.example.com', 'A', 'IN')
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
    srv_msg.client_save_option_count('1', 'server_id')
    srv_msg.client_add_saved_option_count('1', 'DONT ')
    srv_msg.client_does_include_with_value('requested_addr', '192.168.50.10')
    srv_msg.client_requests_option('1')
    srv_msg.client_does_include_with_value('hostname', '*aa$(WHITE_SPACE).four.example.com')
    srv_msg.client_send_msg('REQUEST')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', None, 'ACK')
    srv_msg.response_check_content('Response', None, 'yiaddr', '192.168.50.10')
    srv_msg.response_check_include_option('Response', None, '1')
    srv_msg.response_check_option_content('Response', '1', None, 'value', '255.255.255.0')
    srv_msg.response_check_include_option('Response', None, '12')
    srv_msg.response_check_option_content('Response',
                                          '12',
                                          None,
                                          'value',
                                          'xaax.four.example.com')

    misc.test_procedure()
    srv_msg.client_save_option('server_id')
    srv_msg.dns_question_record('xaax.four.example.com', 'A', 'IN')
    srv_msg.client_send_dns_query()

    misc.pass_criteria()
    srv_msg.send_wait_for_query('MUST', None)
    srv_msg.dns_option('NOT ', 'ANSWER')
    srv_msg.dns_option_content('ANSWER', None, 'rdata', '192.168.50.10')
    srv_msg.dns_option_content('ANSWER', None, 'rrname', 'xaax.four.example.com.')

    misc.test_procedure()
    srv_msg.dns_question_record('10.50.168.192.in-addr.arpa.', 'PTR', 'IN')
    srv_msg.client_send_dns_query()

    misc.pass_criteria()
    srv_msg.send_wait_for_query('MUST', None)
    srv_msg.dns_option('NOT ', 'ANSWER')
    srv_msg.dns_option_content('ANSWER', None, 'rdata', 'xaax.four.example.com.')
    srv_msg.dns_option_content('ANSWER', None, 'rrname', '10.50.168.192.in-addr.arpa.')

    misc.test_procedure()
    srv_msg.client_add_saved_option_count('1', 'DONT ')
    srv_msg.client_sets_value('Client', 'ciaddr', '192.168.50.10')
    srv_msg.client_does_include_with_value('hostname', '*aa$(WHITE_SPACE).four.example.com')
    srv_msg.client_send_msg('RELEASE')

    misc.pass_criteria()
    srv_msg.send_dont_wait_for_message()

    misc.test_procedure()
    srv_msg.dns_question_record('xaax.four.example.com', 'A', 'IN')
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
@pytest.mark.forward_reverse_remove
@pytest.mark.hostname_sanitization
def test_ddns4_notsig_forw_and_rev_release_fqdn_sanitization_replace_1():

    misc.test_setup()
    srv_control.config_srv_subnet('192.168.50.0/24', '192.168.50.10-192.168.50.10')
    srv_control.add_ddns_server('127.0.0.1', '53001')
    srv_control.add_ddns_server_options('enable-updates', 'true')
    srv_control.add_ddns_server_options('qualifying-suffix', 'example.com')
    srv_control.add_ddns_server_options('hostname-char-set', '[^A-Za-z0-9.-]')
    srv_control.add_ddns_server_options('hostname-char-replacement', 'x')
    srv_control.add_forward_ddns('four.example.com.', 'EMPTY_KEY')
    srv_control.add_reverse_ddns('50.168.192.in-addr.arpa.', 'EMPTY_KEY')
    srv_control.build_and_send_config_files('SSH', 'config-file')
    srv_control.start_srv('DHCP', 'started')

    srv_control.use_dns_set_number('20')
    srv_control.start_srv('DNS', 'started')

    misc.test_procedure()
    srv_msg.dns_question_record('xaax.four.example.com', 'A', 'IN')
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
    srv_msg.client_save_option_count('1', 'server_id')
    srv_msg.client_add_saved_option_count('1', 'DONT ')
    srv_msg.client_does_include_with_value('requested_addr', '192.168.50.10')
    srv_msg.client_sets_value('Client', 'FQDN_domain_name', '*aa$(WHITE_SPACE).four.example.com.')
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
                                          'xaax.four.example.com.')

    misc.test_procedure()
    srv_msg.client_save_option('server_id')
    srv_msg.dns_question_record('xaax.four.example.com', 'A', 'IN')
    srv_msg.client_send_dns_query()

    misc.pass_criteria()
    srv_msg.send_wait_for_query('MUST', None)
    srv_msg.dns_option('NOT ', 'ANSWER')
    srv_msg.dns_option_content('ANSWER', None, 'rdata', '192.168.50.10')
    srv_msg.dns_option_content('ANSWER', None, 'rrname', 'xaax.four.example.com.')

    misc.test_procedure()
    srv_msg.dns_question_record('10.50.168.192.in-addr.arpa.', 'PTR', 'IN')
    srv_msg.client_send_dns_query()

    misc.pass_criteria()
    srv_msg.send_wait_for_query('MUST', None)
    srv_msg.dns_option('NOT ', 'ANSWER')
    srv_msg.dns_option_content('ANSWER', None, 'rdata', 'xaax.four.example.com.')
    srv_msg.dns_option_content('ANSWER', None, 'rrname', '10.50.168.192.in-addr.arpa.')

    misc.test_procedure()
    srv_msg.client_add_saved_option_count('1', 'DONT ')
    srv_msg.client_sets_value('Client', 'ciaddr', '192.168.50.10')
    srv_msg.client_sets_value('Client', 'FQDN_domain_name', '*aa$(WHITE_SPACE).four.example.com.')
    srv_msg.client_sets_value('Client', 'FQDN_flags', 'S')
    srv_msg.client_does_include('Client', None, 'fqdn')
    srv_msg.client_send_msg('RELEASE')

    misc.pass_criteria()
    srv_msg.send_dont_wait_for_message()

    misc.test_procedure()
    srv_msg.dns_question_record('xaax.four.example.com', 'A', 'IN')
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
@pytest.mark.forward_reverse_remove
@pytest.mark.hostname_sanitization
def test_ddns4_notsig_forw_and_rev_release_hostname_sanitization_replace_2():

    misc.test_setup()
    srv_control.config_srv_subnet('192.168.50.0/24', '192.168.50.10-192.168.50.10')
    srv_control.add_ddns_server('127.0.0.1', '53001')
    srv_control.add_ddns_server_options('enable-updates', 'true')
    srv_control.add_ddns_server_options('qualifying-suffix', 'example.com')
    srv_control.add_ddns_server_options('hostname-char-set', '[^A-Za-z]')
    srv_control.add_ddns_server_options('hostname-char-replacement', 'x')
    srv_control.add_forward_ddns('four.example.com.', 'EMPTY_KEY')
    srv_control.add_reverse_ddns('50.168.192.in-addr.arpa.', 'EMPTY_KEY')
    srv_control.build_and_send_config_files('SSH', 'config-file')
    srv_control.start_srv('DHCP', 'started')

    misc.test_procedure()
    srv_msg.client_sets_value('Client', 'chaddr', '00:1F:D0:00:00:11')
    srv_msg.client_requests_option('1')
    srv_msg.client_send_msg('DISCOVER')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', None, 'OFFER')
    srv_msg.response_check_include_option('Response', None, '1')
    srv_msg.response_check_content('Response', None, 'yiaddr', '192.168.50.10')
    srv_msg.response_check_option_content('Response', '1', None, 'value', '255.255.255.0')

    misc.test_procedure()
    srv_msg.client_sets_value('Client', 'chaddr', '00:1F:D0:00:00:11')
    srv_msg.client_save_option_count('1', 'server_id')
    srv_msg.client_add_saved_option_count('1', 'DONT ')
    srv_msg.client_does_include_with_value('requested_addr', '192.168.50.10')
    srv_msg.client_requests_option('1')
    srv_msg.client_does_include_with_value('hostname', '*a$(WHITE_SPACE).8723()+')
    srv_msg.client_send_msg('REQUEST')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', None, 'ACK')
    srv_msg.response_check_content('Response', None, 'yiaddr', '192.168.50.10')
    srv_msg.response_check_include_option('Response', None, '1')
    srv_msg.response_check_option_content('Response', '1', None, 'value', '255.255.255.0')
    srv_msg.response_check_include_option('Response', None, '12')
    srv_msg.response_check_option_content('Response', '12', None, 'value', 'xaxxxxxxxxx')

    misc.test_procedure()
    srv_msg.client_sets_value('Client', 'chaddr', '00:1F:D0:00:00:11')
    srv_msg.client_add_saved_option_count('1', 'DONT ')
    srv_msg.client_sets_value('Client', 'ciaddr', '192.168.50.10')
    srv_msg.client_does_include_with_value('hostname', '*a$(WHITE_SPACE).8723()+')
    srv_msg.client_send_msg('RELEASE')

    misc.pass_criteria()
    srv_msg.send_dont_wait_for_message()

    misc.test_procedure()
    srv_msg.client_sets_value('Client', 'chaddr', '00:1F:D0:00:00:22')
    srv_msg.client_requests_option('1')
    srv_msg.client_send_msg('DISCOVER')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', None, 'OFFER')
    srv_msg.response_check_include_option('Response', None, '1')
    srv_msg.response_check_content('Response', None, 'yiaddr', '192.168.50.10')
    srv_msg.response_check_option_content('Response', '1', None, 'value', '255.255.255.0')


@pytest.mark.v4
@pytest.mark.ddns
@pytest.mark.notsig
@pytest.mark.forward_reverse_remove
@pytest.mark.hostname_sanitization
def test_ddns4_notsig_forw_and_rev_release_fqdn_sanitization_replace_2():

    misc.test_setup()
    srv_control.config_srv_subnet('192.168.50.0/24', '192.168.50.10-192.168.50.10')
    srv_control.add_ddns_server('127.0.0.1', '53001')
    srv_control.add_ddns_server_options('enable-updates', 'true')
    srv_control.add_ddns_server_options('qualifying-suffix', 'example.com')
    srv_control.add_ddns_server_options('hostname-char-set', '[^A-Za-z]')
    srv_control.add_ddns_server_options('hostname-char-replacement', 'x')
    srv_control.add_forward_ddns('four.example.com.', 'EMPTY_KEY')
    srv_control.add_reverse_ddns('50.168.192.in-addr.arpa.', 'EMPTY_KEY')
    srv_control.build_and_send_config_files('SSH', 'config-file')
    srv_control.start_srv('DHCP', 'started')

    misc.test_procedure()
    srv_msg.client_sets_value('Client', 'chaddr', '00:1F:D0:00:00:11')
    srv_msg.client_requests_option('1')
    srv_msg.client_send_msg('DISCOVER')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', None, 'OFFER')
    srv_msg.response_check_include_option('Response', None, '1')
    srv_msg.response_check_content('Response', None, 'yiaddr', '192.168.50.10')
    srv_msg.response_check_option_content('Response', '1', None, 'value', '255.255.255.0')

    misc.test_procedure()
    srv_msg.client_sets_value('Client', 'chaddr', '00:1F:D0:00:00:11')
    srv_msg.client_save_option_count('1', 'server_id')
    srv_msg.client_add_saved_option_count('1', 'DONT ')
    srv_msg.client_does_include_with_value('requested_addr', '192.168.50.10')
    srv_msg.client_sets_value('Client', 'FQDN_domain_name', '*a$(WHITE_SPACE).8723()+.')
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
    srv_msg.response_check_option_content('Response', '81', None, 'fqdn', 'xax.xxxxxxx.')

    misc.test_procedure()
    srv_msg.client_sets_value('Client', 'chaddr', '00:1F:D0:00:00:11')
    srv_msg.client_add_saved_option_count('1', 'DONT ')
    srv_msg.client_sets_value('Client', 'ciaddr', '192.168.50.10')
    srv_msg.client_sets_value('Client', 'FQDN_domain_name', '*a$(WHITE_SPACE).8723()+.')
    srv_msg.client_sets_value('Client', 'FQDN_flags', 'S')
    srv_msg.client_does_include('Client', None, 'fqdn')
    srv_msg.client_send_msg('RELEASE')

    misc.pass_criteria()
    srv_msg.send_dont_wait_for_message()

    misc.test_procedure()
    srv_msg.client_sets_value('Client', 'chaddr', '00:1F:D0:00:00:22')
    srv_msg.client_requests_option('1')
    srv_msg.client_send_msg('DISCOVER')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', None, 'OFFER')
    srv_msg.response_check_include_option('Response', None, '1')
    srv_msg.response_check_content('Response', None, 'yiaddr', '192.168.50.10')
    srv_msg.response_check_option_content('Response', '1', None, 'value', '255.255.255.0')


@pytest.mark.v4
@pytest.mark.ddns
@pytest.mark.notsig
@pytest.mark.forward_reverse_remove
@pytest.mark.hostname_sanitization
def test_ddns4_notsig_forw_and_rev_release_hostname_sanitization_omit_1():

    misc.test_setup()
    srv_control.config_srv_subnet('192.168.50.0/24', '192.168.50.10-192.168.50.10')
    srv_control.add_ddns_server('127.0.0.1', '53001')
    srv_control.add_ddns_server_options('enable-updates', 'true')
    srv_control.add_ddns_server_options('qualifying-suffix', 'example.com')
    srv_control.add_ddns_server_options('hostname-char-set', '[^A-Za-z0-9.-]')
    srv_control.add_ddns_server_options('hostname-char-replacement', '$(EMPTY)')
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
    srv_msg.client_save_option_count('1', 'server_id')
    srv_msg.client_add_saved_option_count('1', 'DONT ')
    srv_msg.client_does_include_with_value('requested_addr', '192.168.50.10')
    srv_msg.client_requests_option('1')
    srv_msg.client_does_include_with_value('hostname',
                                           '$(WHITE_SPACE)*aa*.fo^ur.exa(mple.c)om.$(WHITE_SPACE)')
    srv_msg.client_send_msg('REQUEST')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', None, 'ACK')
    srv_msg.response_check_content('Response', None, 'yiaddr', '192.168.50.10')
    srv_msg.response_check_include_option('Response', None, '1')
    srv_msg.response_check_option_content('Response', '1', None, 'value', '255.255.255.0')
    srv_msg.response_check_include_option('Response', None, '12')
    srv_msg.response_check_option_content('Response', '12', None, 'value', 'aa.four.example.com.')

    misc.test_procedure()
    srv_msg.client_save_option('server_id')
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
    srv_msg.client_add_saved_option_count('1', 'DONT ')
    srv_msg.client_sets_value('Client', 'ciaddr', '192.168.50.10')
    srv_msg.client_does_include_with_value('hostname',
                                           '$(WHITE_SPACE)*aa*.fo^ur.exa(mple.c)om$(WHITE_SPACE)')
    srv_msg.client_send_msg('RELEASE')

    misc.pass_criteria()
    srv_msg.send_dont_wait_for_message()

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
@pytest.mark.forward_reverse_remove
@pytest.mark.hostname_sanitization
def test_ddns4_notsig_forw_and_rev_release_fqdn_sanitization_omit_1():

    misc.test_setup()
    srv_control.config_srv_subnet('192.168.50.0/24', '192.168.50.10-192.168.50.10')
    srv_control.add_ddns_server('127.0.0.1', '53001')
    srv_control.add_ddns_server_options('enable-updates', 'true')
    srv_control.add_ddns_server_options('qualifying-suffix', 'example.com')
    srv_control.add_ddns_server_options('hostname-char-set', '[^A-Za-z0-9.-]')
    srv_control.add_ddns_server_options('hostname-char-replacement', '$(EMPTY)')
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
    srv_msg.client_save_option_count('1', 'server_id')
    srv_msg.client_add_saved_option_count('1', 'DONT ')
    srv_msg.client_does_include_with_value('requested_addr', '192.168.50.10')
    srv_msg.client_sets_value('Client',
                              'FQDN_domain_name',
                              '$(WHITE_SPACE)*(a^)a*^')
    # Client sets FQDN_domain_name value to aa.four.example.com.
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
    srv_msg.client_save_option('server_id')
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
    srv_msg.client_add_saved_option_count('1', 'DONT ')
    srv_msg.client_sets_value('Client', 'ciaddr', '192.168.50.10')
    srv_msg.client_sets_value('Client',
                              'FQDN_domain_name',
                              '$(WHITE_SPACE)*aa*.fo^ur.exa(mple.c)om.')
    srv_msg.client_sets_value('Client', 'FQDN_flags', 'S')
    srv_msg.client_does_include('Client', None, 'fqdn')
    srv_msg.client_send_msg('RELEASE')

    misc.pass_criteria()
    srv_msg.send_dont_wait_for_message()

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
@pytest.mark.forward_reverse_remove
@pytest.mark.hostname_sanitization
def test_ddns4_notsig_forw_and_rev_release_hostname_sanitization_omit_identical_name():
    # Two clients are using different hostnames which after sanitization end up being identical
    misc.test_setup()
    srv_control.config_srv_subnet('192.168.50.0/24', '192.168.50.10-192.168.50.11')
    srv_control.add_ddns_server('127.0.0.1', '53001')
    srv_control.add_ddns_server_options('enable-updates', 'true')
    srv_control.add_ddns_server_options('qualifying-suffix', 'example.com')
    srv_control.add_ddns_server_options('hostname-char-set', '[^A-Za-z.-]')
    srv_control.add_ddns_server_options('hostname-char-replacement', '$(EMPTY)')
    srv_control.add_forward_ddns('four.example.com.', 'EMPTY_KEY')
    srv_control.add_reverse_ddns('50.168.192.in-addr.arpa.', 'EMPTY_KEY')
    srv_control.build_and_send_config_files('SSH', 'config-file')
    srv_control.start_srv('DHCP', 'started')

    srv_control.use_dns_set_number('20')
    srv_control.start_srv('DNS', 'started')

    misc.test_procedure()
    srv_msg.dns_question_record('client.four.example.com', 'A', 'IN')
    srv_msg.client_send_dns_query()

    misc.pass_criteria()
    srv_msg.send_wait_for_query('MUST', None)
    srv_msg.dns_option(None, 'ANSWER')

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
    srv_msg.client_sets_value('Client', 'chaddr', '00:1F:D0:00:00:11')
    srv_msg.client_requests_option('1')
    srv_msg.client_send_msg('DISCOVER')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', None, 'OFFER')
    srv_msg.response_check_include_option('Response', None, '1')
    srv_msg.response_check_content('Response', None, 'yiaddr', '192.168.50.10')
    srv_msg.response_check_option_content('Response', '1', None, 'value', '255.255.255.0')

    misc.test_procedure()
    srv_msg.client_sets_value('Client', 'chaddr', '00:1F:D0:00:00:11')
    srv_msg.client_save_option_count('1', 'server_id')
    srv_msg.client_add_saved_option_count('1', 'DONT ')
    srv_msg.client_does_include_with_value('requested_addr', '192.168.50.10')
    srv_msg.client_requests_option('1')
    srv_msg.client_does_include_with_value('hostname', 'client1.four.example.com')
    srv_msg.client_send_msg('REQUEST')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', None, 'ACK')
    srv_msg.response_check_content('Response', None, 'yiaddr', '192.168.50.10')
    srv_msg.response_check_include_option('Response', None, '1')
    srv_msg.response_check_option_content('Response', '1', None, 'value', '255.255.255.0')
    srv_msg.response_check_include_option('Response', None, '12')
    srv_msg.response_check_option_content('Response',
                                          '12',
                                          None,
                                          'value',
                                          'client.four.example.com')

    misc.test_procedure()
    srv_msg.client_save_option('server_id')
    srv_msg.dns_question_record('client.four.example.com', 'A', 'IN')
    srv_msg.client_send_dns_query()

    misc.pass_criteria()
    srv_msg.send_wait_for_query('MUST', None)
    srv_msg.dns_option('NOT ', 'ANSWER')
    srv_msg.dns_option_content('ANSWER', None, 'rdata', '192.168.50.10')
    srv_msg.dns_option_content('ANSWER', None, 'rrname', 'client.four.example.com.')

    misc.test_procedure()
    srv_msg.dns_question_record('10.50.168.192.in-addr.arpa.', 'PTR', 'IN')
    srv_msg.client_send_dns_query()

    misc.pass_criteria()
    srv_msg.send_wait_for_query('MUST', None)
    srv_msg.dns_option('NOT ', 'ANSWER')
    srv_msg.dns_option_content('ANSWER', None, 'rdata', 'client.four.example.com.')
    srv_msg.dns_option_content('ANSWER', None, 'rrname', '10.50.168.192.in-addr.arpa.')

    misc.test_procedure()
    srv_msg.client_sets_value('Client', 'chaddr', '00:1F:D0:00:00:22')
    srv_msg.client_requests_option('1')
    srv_msg.client_send_msg('DISCOVER')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', None, 'OFFER')
    srv_msg.response_check_include_option('Response', None, '1')
    srv_msg.response_check_content('Response', None, 'yiaddr', '192.168.50.11')
    srv_msg.response_check_option_content('Response', '1', None, 'value', '255.255.255.0')

    misc.test_procedure()
    srv_msg.client_sets_value('Client', 'chaddr', '00:1F:D0:00:00:22')
    srv_msg.client_save_option_count('1', 'server_id')
    srv_msg.client_add_saved_option_count('1', 'DONT ')
    srv_msg.client_does_include_with_value('requested_addr', '192.168.50.11')
    srv_msg.client_requests_option('1')
    srv_msg.client_does_include_with_value('hostname', 'client2.four.example.com')
    srv_msg.client_send_msg('REQUEST')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', None, 'ACK')
    srv_msg.response_check_content('Response', None, 'yiaddr', '192.168.50.11')
    srv_msg.response_check_include_option('Response', None, '1')
    srv_msg.response_check_option_content('Response', '1', None, 'value', '255.255.255.0')
    srv_msg.response_check_include_option('Response', None, '12')
    srv_msg.response_check_option_content('Response',
                                          '12',
                                          None,
                                          'value',
                                          'client.four.example.com')

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
    srv_msg.client_sets_value('Client', 'chaddr', '00:1F:D0:00:00:11')
    srv_msg.client_add_saved_option_count('1', 'DONT ')
    srv_msg.client_sets_value('Client', 'ciaddr', '192.168.50.10')
    srv_msg.client_does_include_with_value('hostname', 'client1.four.example.com')
    srv_msg.client_send_msg('RELEASE')

    misc.pass_criteria()
    srv_msg.send_dont_wait_for_message()

    misc.test_procedure()
    srv_msg.dns_question_record('client.four.example.com', 'A', 'IN')
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
@pytest.mark.forward_reverse_remove
@pytest.mark.hostname_sanitization
def test_ddns4_notsig_forw_and_rev_release_fqdn_sanitization_omit_identical_name():
    # Two clients are using different hostnames which after sanitization end up being identical
    misc.test_setup()
    srv_control.config_srv_subnet('192.168.50.0/24', '192.168.50.10-192.168.50.11')
    srv_control.add_ddns_server('127.0.0.1', '53001')
    srv_control.add_ddns_server_options('enable-updates', 'true')
    srv_control.add_ddns_server_options('qualifying-suffix', 'example.com')
    srv_control.add_ddns_server_options('hostname-char-set', '[^A-Za-z.-]')
    srv_control.add_ddns_server_options('hostname-char-replacement', '$(EMPTY)')
    srv_control.add_forward_ddns('four.example.com.', 'EMPTY_KEY')
    srv_control.add_reverse_ddns('50.168.192.in-addr.arpa.', 'EMPTY_KEY')
    srv_control.build_and_send_config_files('SSH', 'config-file')
    srv_control.start_srv('DHCP', 'started')

    srv_control.use_dns_set_number('20')
    srv_control.start_srv('DNS', 'started')

    misc.test_procedure()
    srv_msg.dns_question_record('client.four.example.com', 'A', 'IN')
    srv_msg.client_send_dns_query()

    misc.pass_criteria()
    srv_msg.send_wait_for_query('MUST', None)
    srv_msg.dns_option(None, 'ANSWER')

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
    srv_msg.client_sets_value('Client', 'chaddr', '00:1F:D0:00:00:11')
    srv_msg.client_requests_option('1')
    srv_msg.client_send_msg('DISCOVER')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', None, 'OFFER')
    srv_msg.response_check_include_option('Response', None, '1')
    srv_msg.response_check_content('Response', None, 'yiaddr', '192.168.50.10')
    srv_msg.response_check_option_content('Response', '1', None, 'value', '255.255.255.0')

    misc.test_procedure()
    srv_msg.client_sets_value('Client', 'chaddr', '00:1F:D0:00:00:11')
    srv_msg.client_save_option_count('1', 'server_id')
    srv_msg.client_add_saved_option_count('1', 'DONT ')
    srv_msg.client_does_include_with_value('requested_addr', '192.168.50.10')
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
                                          'client.four.example.com.')

    misc.test_procedure()
    srv_msg.client_save_option('server_id')
    srv_msg.dns_question_record('client.four.example.com', 'A', 'IN')
    srv_msg.client_send_dns_query()

    misc.pass_criteria()
    srv_msg.send_wait_for_query('MUST', None)
    srv_msg.dns_option('NOT ', 'ANSWER')
    srv_msg.dns_option_content('ANSWER', None, 'rdata', '192.168.50.10')
    srv_msg.dns_option_content('ANSWER', None, 'rrname', 'client.four.example.com.')

    misc.test_procedure()
    srv_msg.dns_question_record('10.50.168.192.in-addr.arpa.', 'PTR', 'IN')
    srv_msg.client_send_dns_query()

    misc.pass_criteria()
    srv_msg.send_wait_for_query('MUST', None)
    srv_msg.dns_option('NOT ', 'ANSWER')
    srv_msg.dns_option_content('ANSWER', None, 'rdata', 'client.four.example.com.')
    srv_msg.dns_option_content('ANSWER', None, 'rrname', '10.50.168.192.in-addr.arpa.')

    misc.test_procedure()
    srv_msg.client_sets_value('Client', 'chaddr', '00:1F:D0:00:00:22')
    srv_msg.client_requests_option('1')
    srv_msg.client_send_msg('DISCOVER')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', None, 'OFFER')
    srv_msg.response_check_include_option('Response', None, '1')
    srv_msg.response_check_content('Response', None, 'yiaddr', '192.168.50.11')
    srv_msg.response_check_option_content('Response', '1', None, 'value', '255.255.255.0')

    misc.test_procedure()
    srv_msg.client_sets_value('Client', 'chaddr', '00:1F:D0:00:00:22')
    srv_msg.client_save_option_count('1', 'server_id')
    srv_msg.client_add_saved_option_count('1', 'DONT ')
    srv_msg.client_does_include_with_value('requested_addr', '192.168.50.11')
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
                                          'client.four.example.com.')

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
    srv_msg.client_sets_value('Client', 'chaddr', '00:1F:D0:00:00:11')
    srv_msg.client_add_saved_option_count('1', 'DONT ')
    srv_msg.client_sets_value('Client', 'ciaddr', '192.168.50.10')
    srv_msg.client_sets_value('Client', 'FQDN_domain_name', 'client1.four.example.com.')
    srv_msg.client_sets_value('Client', 'FQDN_flags', 'S')
    srv_msg.client_does_include('Client', None, 'fqdn')
    srv_msg.client_send_msg('RELEASE')

    misc.pass_criteria()
    srv_msg.send_dont_wait_for_message()

    misc.test_procedure()
    srv_msg.dns_question_record('client.four.example.com', 'A', 'IN')
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
@pytest.mark.forward_reverse_remove
@pytest.mark.hostname_sanitization
def test_ddns4_notsig_forw_and_rev_release_hostname_sanitization_omit_2():

    misc.test_setup()
    srv_control.config_srv_subnet('192.168.50.0/24', '192.168.50.10-192.168.50.10')
    srv_control.add_ddns_server('127.0.0.1', '53001')
    srv_control.add_ddns_server_options('enable-updates', 'true')
    srv_control.add_ddns_server_options('qualifying-suffix', 'example.com')
    srv_control.add_ddns_server_options('hostname-char-set', '[^A-Za-z]')
    srv_control.add_ddns_server_options('hostname-char-replacement', '$(EMPTY)')
    srv_control.add_forward_ddns('four.example.com.', 'EMPTY_KEY')
    srv_control.add_reverse_ddns('50.168.192.in-addr.arpa.', 'EMPTY_KEY')
    srv_control.build_and_send_config_files('SSH', 'config-file')
    srv_control.start_srv('DHCP', 'started')

    misc.test_procedure()
    srv_msg.client_sets_value('Client', 'chaddr', '00:1F:D0:00:00:11')
    srv_msg.client_requests_option('1')
    srv_msg.client_send_msg('DISCOVER')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', None, 'OFFER')
    srv_msg.response_check_include_option('Response', None, '1')
    srv_msg.response_check_content('Response', None, 'yiaddr', '192.168.50.10')
    srv_msg.response_check_option_content('Response', '1', None, 'value', '255.255.255.0')

    misc.test_procedure()
    srv_msg.client_sets_value('Client', 'chaddr', '00:1F:D0:00:00:11')
    srv_msg.client_save_option_count('1', 'server_id')
    srv_msg.client_add_saved_option_count('1', 'DONT ')
    srv_msg.client_does_include_with_value('requested_addr', '192.168.50.10')
    srv_msg.client_requests_option('1')
    srv_msg.client_does_include_with_value('hostname', '*a$(WHITE_SPACE).8723()+')
    srv_msg.client_send_msg('REQUEST')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', None, 'ACK')
    srv_msg.response_check_content('Response', None, 'yiaddr', '192.168.50.10')
    srv_msg.response_check_include_option('Response', None, '1')
    srv_msg.response_check_option_content('Response', '1', None, 'value', '255.255.255.0')
    srv_msg.response_check_include_option('Response', None, '12')
    srv_msg.response_check_option_content('Response', '12', None, 'value', 'a')

    misc.test_procedure()
    srv_msg.client_sets_value('Client', 'chaddr', '00:1F:D0:00:00:11')
    srv_msg.client_add_saved_option_count('1', 'DONT ')
    srv_msg.client_sets_value('Client', 'ciaddr', '192.168.50.10')
    srv_msg.client_does_include_with_value('hostname', '*a$(WHITE_SPACE).8723()+')
    srv_msg.client_send_msg('RELEASE')

    misc.pass_criteria()
    srv_msg.send_dont_wait_for_message()

    misc.test_procedure()
    srv_msg.client_sets_value('Client', 'chaddr', '00:1F:D0:00:00:22')
    srv_msg.client_requests_option('1')
    srv_msg.client_send_msg('DISCOVER')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', None, 'OFFER')
    srv_msg.response_check_include_option('Response', None, '1')
    srv_msg.response_check_content('Response', None, 'yiaddr', '192.168.50.10')
    srv_msg.response_check_option_content('Response', '1', None, 'value', '255.255.255.0')


@pytest.mark.v4
@pytest.mark.ddns
@pytest.mark.notsig
@pytest.mark.forward_reverse_remove
@pytest.mark.hostname_sanitization
def test_ddns4_notsig_forw_and_rev_release_fqdn_sanitization_omit_2():

    misc.test_setup()
    srv_control.config_srv_subnet('192.168.50.0/24', '192.168.50.10-192.168.50.10')
    srv_control.add_ddns_server('127.0.0.1', '53001')
    srv_control.add_ddns_server_options('enable-updates', 'true')
    srv_control.add_ddns_server_options('qualifying-suffix', 'example.com')
    srv_control.add_ddns_server_options('hostname-char-set', '[^A-Za-z]')
    srv_control.add_ddns_server_options('hostname-char-replacement', '$(EMPTY)')
    srv_control.add_forward_ddns('four.example.com.', 'EMPTY_KEY')
    srv_control.add_reverse_ddns('50.168.192.in-addr.arpa.', 'EMPTY_KEY')
    srv_control.build_and_send_config_files('SSH', 'config-file')
    srv_control.start_srv('DHCP', 'started')

    misc.test_procedure()
    srv_msg.client_sets_value('Client', 'chaddr', '00:1F:D0:00:00:11')
    srv_msg.client_requests_option('1')
    srv_msg.client_send_msg('DISCOVER')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', None, 'OFFER')
    srv_msg.response_check_include_option('Response', None, '1')
    srv_msg.response_check_content('Response', None, 'yiaddr', '192.168.50.10')
    srv_msg.response_check_option_content('Response', '1', None, 'value', '255.255.255.0')

    misc.test_procedure()
    srv_msg.client_sets_value('Client', 'chaddr', '00:1F:D0:00:00:11')
    srv_msg.client_save_option_count('1', 'server_id')
    srv_msg.client_add_saved_option_count('1', 'DONT ')
    srv_msg.client_does_include_with_value('requested_addr', '192.168.50.10')
    srv_msg.client_sets_value('Client', 'FQDN_domain_name', '*a$(WHITE_SPACE).8723()+com.pl.')
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
    srv_msg.response_check_option_content('Response', '81', None, 'fqdn', 'a.com.pl.')

    misc.test_procedure()
    srv_msg.client_sets_value('Client', 'chaddr', '00:1F:D0:00:00:11')
    srv_msg.client_add_saved_option_count('1', 'DONT ')
    srv_msg.client_sets_value('Client', 'ciaddr', '192.168.50.10')
    srv_msg.client_sets_value('Client', 'FQDN_domain_name', '*a$(WHITE_SPACE).8723()+.')
    srv_msg.client_sets_value('Client', 'FQDN_flags', 'S')
    srv_msg.client_does_include('Client', None, 'fqdn')
    srv_msg.client_send_msg('RELEASE')

    misc.pass_criteria()
    srv_msg.send_dont_wait_for_message()

    misc.test_procedure()
    srv_msg.client_sets_value('Client', 'chaddr', '00:1F:D0:00:00:22')
    srv_msg.client_requests_option('1')
    srv_msg.client_send_msg('DISCOVER')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', None, 'OFFER')
    srv_msg.response_check_include_option('Response', None, '1')
    srv_msg.response_check_content('Response', None, 'yiaddr', '192.168.50.10')
    srv_msg.response_check_option_content('Response', '1', None, 'value', '255.255.255.0')


@pytest.mark.v4
@pytest.mark.ddns
@pytest.mark.notsig
@pytest.mark.forward_reverse_remove
@pytest.mark.hostname_sanitization
def test_ddns4_notsig_forw_and_rev_release_hostname_sanitization_omit_3():

    misc.test_setup()
    srv_control.config_srv_subnet('192.168.50.0/24', '192.168.50.10-192.168.50.10')
    srv_control.add_ddns_server('127.0.0.1', '53001')
    srv_control.add_ddns_server_options('enable-updates', 'true')
    srv_control.add_ddns_server_options('qualifying-suffix', 'example.com')
    srv_control.add_ddns_server_options('hostname-char-set', '[^A-Za-z]')
    srv_control.add_ddns_server_options('hostname-char-replacement', '$(EMPTY)')
    srv_control.add_forward_ddns('four.example.com.', 'EMPTY_KEY')
    srv_control.add_reverse_ddns('50.168.192.in-addr.arpa.', 'EMPTY_KEY')
    srv_control.build_and_send_config_files('SSH', 'config-file')
    srv_control.start_srv('DHCP', 'started')

    misc.test_procedure()
    srv_msg.client_sets_value('Client', 'chaddr', '00:1F:D0:00:00:11')
    srv_msg.client_requests_option('1')
    srv_msg.client_send_msg('DISCOVER')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', None, 'OFFER')
    srv_msg.response_check_include_option('Response', None, '1')
    srv_msg.response_check_content('Response', None, 'yiaddr', '192.168.50.10')
    srv_msg.response_check_option_content('Response', '1', None, 'value', '255.255.255.0')

    misc.test_procedure()
    srv_msg.client_sets_value('Client', 'chaddr', '00:1F:D0:00:00:11')
    srv_msg.client_save_option_count('1', 'server_id')
    srv_msg.client_add_saved_option_count('1', 'DONT ')
    srv_msg.client_does_include_with_value('requested_addr', '192.168.50.10')
    srv_msg.client_requests_option('1')
    srv_msg.client_does_include_with_value('hostname', '*$(WHITE_SPACE).8723()+')
    srv_msg.client_send_msg('REQUEST')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', None, 'ACK')
    srv_msg.response_check_content('Response', None, 'yiaddr', '192.168.50.10')
    srv_msg.response_check_include_option('Response', None, '1')
    srv_msg.response_check_option_content('Response', '1', None, 'value', '255.255.255.0')
    srv_msg.response_check_include_option('Response', 'NOT ', '12')

    misc.test_procedure()
    srv_msg.client_sets_value('Client', 'chaddr', '00:1F:D0:00:00:11')
    srv_msg.client_add_saved_option_count('1', 'DONT ')
    srv_msg.client_sets_value('Client', 'ciaddr', '192.168.50.10')
    srv_msg.client_does_include_with_value('hostname', '*$(WHITE_SPACE).8723()+')
    srv_msg.client_send_msg('RELEASE')

    misc.pass_criteria()
    srv_msg.send_dont_wait_for_message()

    misc.test_procedure()
    srv_msg.client_sets_value('Client', 'chaddr', '00:1F:D0:00:00:22')
    srv_msg.client_requests_option('1')
    srv_msg.client_send_msg('DISCOVER')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', None, 'OFFER')
    srv_msg.response_check_include_option('Response', None, '1')
    srv_msg.response_check_content('Response', None, 'yiaddr', '192.168.50.10')
    srv_msg.response_check_option_content('Response', '1', None, 'value', '255.255.255.0')


@pytest.mark.v4
@pytest.mark.ddns
@pytest.mark.notsig
@pytest.mark.forward_reverse_remove
@pytest.mark.hostname_sanitization
def test_ddns4_notsig_forw_and_rev_release_hostname_sanitization_omit_4():

    misc.test_setup()
    srv_control.config_srv_subnet('192.168.50.0/24', '192.168.50.10-192.168.50.10')
    srv_control.add_ddns_server('127.0.0.1', '53001')
    srv_control.add_ddns_server_options('enable-updates', 'true')
    srv_control.add_ddns_server_options('qualifying-suffix', 'example.com')
    srv_control.add_ddns_server_options('hostname-char-set', '[^A-Za-z]')
    srv_control.add_ddns_server_options('hostname-char-replacement', '$(EMPTY)')
    srv_control.add_forward_ddns('four.example.com.', 'EMPTY_KEY')
    srv_control.add_reverse_ddns('50.168.192.in-addr.arpa.', 'EMPTY_KEY')
    srv_control.build_and_send_config_files('SSH', 'config-file')
    srv_control.start_srv('DHCP', 'started')

    misc.test_procedure()
    srv_msg.client_sets_value('Client', 'chaddr', '00:1F:D0:00:00:11')
    srv_msg.client_requests_option('1')
    srv_msg.client_send_msg('DISCOVER')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', None, 'OFFER')
    srv_msg.response_check_include_option('Response', None, '1')
    srv_msg.response_check_content('Response', None, 'yiaddr', '192.168.50.10')
    srv_msg.response_check_option_content('Response', '1', None, 'value', '255.255.255.0')

    misc.test_procedure()
    srv_msg.client_sets_value('Client', 'chaddr', '00:1F:D0:00:00:11')
    srv_msg.client_save_option_count('1', 'server_id')
    srv_msg.client_add_saved_option_count('1', 'DONT ')
    srv_msg.client_does_include_with_value('requested_addr', '192.168.50.10')
    srv_msg.client_sets_value('Client', 'FQDN_domain_name', '*$(WHITE_SPACE).8723()+.')
    srv_msg.client_sets_value('Client', 'FQDN_flags', 'S')
    srv_msg.client_does_include('Client', None, 'fqdn')
    srv_msg.client_send_msg('REQUEST')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', None, 'ACK')
    srv_msg.response_check_content('Response', None, 'yiaddr', '192.168.50.10')
    srv_msg.response_check_include_option('Response', None, '1')
    srv_msg.response_check_option_content('Response', '1', None, 'value', '255.255.255.0')
    srv_msg.response_check_include_option('Response', 'NOT ', '12')
    srv_msg.response_check_include_option('Response', 'NOT ', '81')

    misc.test_procedure()
    srv_msg.client_sets_value('Client', 'chaddr', '00:1F:D0:00:00:11')
    srv_msg.client_add_saved_option_count('1', 'DONT ')
    srv_msg.client_sets_value('Client', 'ciaddr', '192.168.50.10')
    srv_msg.client_sets_value('Client', 'FQDN_domain_name', '*$(WHITE_SPACE).8723()+.')
    srv_msg.client_sets_value('Client', 'FQDN_flags', 'S')
    srv_msg.client_does_include('Client', None, 'fqdn')
    srv_msg.client_send_msg('RELEASE')

    misc.pass_criteria()
    srv_msg.send_dont_wait_for_message()

    misc.test_procedure()
    srv_msg.client_sets_value('Client', 'chaddr', '00:1F:D0:00:00:22')
    srv_msg.client_requests_option('1')
    srv_msg.client_send_msg('DISCOVER')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', None, 'OFFER')
    srv_msg.response_check_include_option('Response', None, '1')
    srv_msg.response_check_content('Response', None, 'yiaddr', '192.168.50.10')
    srv_msg.response_check_option_content('Response', '1', None, 'value', '255.255.255.0')


@pytest.mark.v4
@pytest.mark.ddns
@pytest.mark.notsig
@pytest.mark.expire
def test_ddns4_notsig_expire_hostname_sanitization():

    misc.test_setup()
    srv_control.set_time('renew-timer', '3')
    srv_control.set_time('rebind-timer', '4')
    srv_control.set_time('valid-lifetime', '5')
    srv_control.config_srv_subnet('192.168.50.0/24', '192.168.50.10-192.168.50.10')
    srv_control.add_ddns_server('127.0.0.1', '53001')
    srv_control.add_ddns_server_options('hostname-char-set', '[^A-Za-z0-9.-]')
    srv_control.add_ddns_server_options('hostname-char-replacement', 'x')
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
    srv_msg.dns_question_record('xaax.four.example.com', 'A', 'IN')
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
    srv_msg.client_does_include_with_value('hostname', '^aa$(WHITE_SPACE).four.example.com')
    srv_msg.client_send_msg('REQUEST')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', None, 'ACK')
    srv_msg.response_check_content('Response', None, 'yiaddr', '192.168.50.10')
    srv_msg.response_check_include_option('Response', None, '1')
    srv_msg.response_check_option_content('Response', '1', None, 'value', '255.255.255.0')
    srv_msg.response_check_include_option('Response', None, '12')
    srv_msg.response_check_option_content('Response',
                                          '12',
                                          None,
                                          'value',
                                          'xaax.four.example.com')

    misc.test_procedure()
    srv_msg.dns_question_record('xaax.four.example.com', 'A', 'IN')
    srv_msg.client_send_dns_query()

    misc.pass_criteria()
    srv_msg.send_wait_for_query('MUST', None)
    srv_msg.dns_option('NOT ', 'ANSWER')
    srv_msg.dns_option_content('ANSWER', None, 'rdata', '192.168.50.10')
    srv_msg.dns_option_content('ANSWER', None, 'rrname', 'xaax.four.example.com.')

    misc.test_procedure()
    srv_msg.dns_question_record('10.50.168.192.in-addr.arpa.', 'PTR', 'IN')
    srv_msg.client_send_dns_query()

    misc.pass_criteria()
    srv_msg.send_wait_for_query('MUST', None)
    srv_msg.dns_option('NOT ', 'ANSWER')
    srv_msg.dns_option_content('ANSWER', None, 'rdata', 'xaax.four.example.com.')
    srv_msg.dns_option_content('ANSWER', None, 'rrname', '10.50.168.192.in-addr.arpa.')

    srv_msg.forge_sleep('10', 'seconds')

    misc.test_procedure()
    srv_msg.dns_question_record('xaax.four.example.com', 'A', 'IN')
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
@pytest.mark.expire
def test_ddns4_notsig_expire_fqdn_sanitization():

    misc.test_setup()
    srv_control.set_time('renew-timer', '3')
    srv_control.set_time('rebind-timer', '4')
    srv_control.set_time('valid-lifetime', '5')
    srv_control.config_srv_subnet('192.168.50.0/24', '192.168.50.10-192.168.50.10')
    srv_control.add_ddns_server('127.0.0.1', '53001')
    srv_control.add_ddns_server_options('hostname-char-set', '[^A-Za-z0-9.-]')
    srv_control.add_ddns_server_options('hostname-char-replacement', 'x')
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
    srv_msg.dns_question_record('xaax.four.example.com', 'A', 'IN')
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
    srv_msg.client_sets_value('Client', 'FQDN_domain_name', '^aa$(WHITE_SPACE).four.example.com.')
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
                                          'xaax.four.example.com.')

    misc.test_procedure()
    srv_msg.dns_question_record('xaax.four.example.com', 'A', 'IN')
    srv_msg.client_send_dns_query()

    misc.pass_criteria()
    srv_msg.send_wait_for_query('MUST', None)
    srv_msg.dns_option('NOT ', 'ANSWER')
    srv_msg.dns_option_content('ANSWER', None, 'rdata', '192.168.50.10')
    srv_msg.dns_option_content('ANSWER', None, 'rrname', 'xaax.four.example.com.')

    misc.test_procedure()
    srv_msg.dns_question_record('10.50.168.192.in-addr.arpa.', 'PTR', 'IN')
    srv_msg.client_send_dns_query()

    misc.pass_criteria()
    srv_msg.send_wait_for_query('MUST', None)
    srv_msg.dns_option('NOT ', 'ANSWER')
    srv_msg.dns_option_content('ANSWER', None, 'rdata', 'xaax.four.example.com.')
    srv_msg.dns_option_content('ANSWER', None, 'rrname', '10.50.168.192.in-addr.arpa.')

    srv_msg.forge_sleep('10', 'seconds')

    misc.test_procedure()
    srv_msg.dns_question_record('xaax.four.example.com', 'A', 'IN')
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
