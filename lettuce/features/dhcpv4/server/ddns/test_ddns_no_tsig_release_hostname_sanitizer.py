"""DDNS without TSIG"""

# pylint: disable=invalid-name,line-too-long

import pytest

from features import srv_control
from features import srv_msg
from features import misc


@pytest.mark.v4
@pytest.mark.ddns
@pytest.mark.notsig
@pytest.mark.forward_reverse_remove
@pytest.mark.hostname_sanitization
def test_ddns4_notsig_forw_and_rev_release_hostname_sanitization_replace_1(step):

    misc.test_setup(step)
    srv_control.config_srv_subnet(step, '192.168.50.0/24', '192.168.50.10-192.168.50.10')
    srv_control.add_ddns_server(step, '127.0.0.1', '53001')
    srv_control.add_ddns_server_options(step, 'enable-updates', 'true')
    srv_control.add_ddns_server_options(step, 'qualifying-suffix', 'example.com')
    srv_control.add_ddns_server_options(step, 'hostname-char-set', '[^A-Za-z0-9.-]')
    srv_control.add_ddns_server_options(step, 'hostname-char-replacement', 'x')
    srv_control.add_forward_ddns(step, 'four.example.com.', 'EMPTY_KEY', '192.168.50.252', '53')
    srv_control.add_reverse_ddns(step,
                                 '50.168.192.in-addr.arpa.',
                                 'EMPTY_KEY',
                                 '192.168.50.252',
                                 '53')
    srv_control.build_and_send_config_files(step, 'SSH', 'config-file')
    srv_control.start_srv(step, 'DHCP', 'started')

    srv_control.use_dns_set_number(step, '20')
    srv_control.start_srv(step, 'DNS', 'started')

    misc.test_procedure(step)
    srv_msg.dns_question_record(step, 'xaax.four.example.com', 'A', 'IN')
    srv_msg.client_send_dns_query(step)

    misc.pass_criteria(step)
    srv_msg.send_wait_for_query(step, 'MUST', None)
    srv_msg.dns_option(step, None, 'ANSWER')

    misc.test_procedure(step)
    srv_msg.client_requests_option(step, '1')
    srv_msg.client_send_msg(step, 'DISCOVER')

    misc.pass_criteria(step)
    srv_msg.send_wait_for_message(step, 'MUST', None, 'OFFER')
    srv_msg.response_check_include_option(step, 'Response', None, '1')
    srv_msg.response_check_content(step, 'Response', None, 'yiaddr', '192.168.50.10')
    srv_msg.response_check_option_content(step, 'Response', '1', None, 'value', '255.255.255.0')

    misc.test_procedure(step)
    srv_msg.client_save_option_count(step, '1', 'server_id')
    srv_msg.client_add_saved_option_count(step, '1', 'DONT ')
    srv_msg.client_does_include_with_value(step, 'requested_addr', '192.168.50.10')
    srv_msg.client_requests_option(step, '1')
    srv_msg.client_does_include_with_value(step, 'hostname', '*aa$(WHITE_SPACE).four.example.com')
    srv_msg.client_send_msg(step, 'REQUEST')

    misc.pass_criteria(step)
    srv_msg.send_wait_for_message(step, 'MUST', None, 'ACK')
    srv_msg.response_check_content(step, 'Response', None, 'yiaddr', '192.168.50.10')
    srv_msg.response_check_include_option(step, 'Response', None, '1')
    srv_msg.response_check_option_content(step, 'Response', '1', None, 'value', '255.255.255.0')
    srv_msg.response_check_include_option(step, 'Response', None, '12')
    srv_msg.response_check_option_content(step,
                                          'Response',
                                          '12',
                                          None,
                                          'value',
                                          'xaax.four.example.com')

    misc.test_procedure(step)
    srv_msg.client_save_option(step, 'server_id')
    srv_msg.dns_question_record(step, 'xaax.four.example.com', 'A', 'IN')
    srv_msg.client_send_dns_query(step)

    misc.pass_criteria(step)
    srv_msg.send_wait_for_query(step, 'MUST', None)
    srv_msg.dns_option(step, 'NOT ', 'ANSWER')
    srv_msg.dns_option_content(step, 'ANSWER', None, 'rdata', '192.168.50.10')
    srv_msg.dns_option_content(step, 'ANSWER', None, 'rrname', 'xaax.four.example.com.')

    misc.test_procedure(step)
    srv_msg.dns_question_record(step, '10.50.168.192.in-addr.arpa.', 'PTR', 'IN')
    srv_msg.client_send_dns_query(step)

    misc.pass_criteria(step)
    srv_msg.send_wait_for_query(step, 'MUST', None)
    srv_msg.dns_option(step, 'NOT ', 'ANSWER')
    srv_msg.dns_option_content(step, 'ANSWER', None, 'rdata', 'xaax.four.example.com.')
    srv_msg.dns_option_content(step, 'ANSWER', None, 'rrname', '10.50.168.192.in-addr.arpa.')

    misc.test_procedure(step)
    srv_msg.client_add_saved_option_count(step, '1', 'DONT ')
    srv_msg.client_sets_value(step, 'Client', 'ciaddr', '192.168.50.10')
    srv_msg.client_does_include_with_value(step, 'hostname', '*aa$(WHITE_SPACE).four.example.com')
    srv_msg.client_send_msg(step, 'RELEASE')

    misc.pass_criteria(step)
    srv_msg.send_dont_wait_for_message(step)

    misc.test_procedure(step)
    srv_msg.dns_question_record(step, 'xaax.four.example.com', 'A', 'IN')
    srv_msg.client_send_dns_query(step)

    misc.pass_criteria(step)
    srv_msg.send_wait_for_query(step, 'MUST', None)
    srv_msg.dns_option(step, None, 'ANSWER')

    misc.test_procedure(step)
    srv_msg.dns_question_record(step, '10.50.168.192.in-addr.arpa.', 'PTR', 'IN')
    srv_msg.client_send_dns_query(step)

    misc.pass_criteria(step)
    srv_msg.send_wait_for_query(step, 'MUST', None)
    srv_msg.dns_option(step, None, 'ANSWER')


@pytest.mark.v4
@pytest.mark.ddns
@pytest.mark.notsig
@pytest.mark.forward_reverse_remove
@pytest.mark.hostname_sanitization
def test_ddns4_notsig_forw_and_rev_release_fqdn_sanitization_replace_1(step):

    misc.test_setup(step)
    srv_control.config_srv_subnet(step, '192.168.50.0/24', '192.168.50.10-192.168.50.10')
    srv_control.add_ddns_server(step, '127.0.0.1', '53001')
    srv_control.add_ddns_server_options(step, 'enable-updates', 'true')
    srv_control.add_ddns_server_options(step, 'qualifying-suffix', 'example.com')
    srv_control.add_ddns_server_options(step, 'hostname-char-set', '[^A-Za-z0-9.-]')
    srv_control.add_ddns_server_options(step, 'hostname-char-replacement', 'x')
    srv_control.add_forward_ddns(step, 'four.example.com.', 'EMPTY_KEY', '192.168.50.252', '53')
    srv_control.add_reverse_ddns(step,
                                 '50.168.192.in-addr.arpa.',
                                 'EMPTY_KEY',
                                 '192.168.50.252',
                                 '53')
    srv_control.build_and_send_config_files(step, 'SSH', 'config-file')
    srv_control.start_srv(step, 'DHCP', 'started')

    srv_control.use_dns_set_number(step, '20')
    srv_control.start_srv(step, 'DNS', 'started')

    misc.test_procedure(step)
    srv_msg.dns_question_record(step, 'xaax.four.example.com', 'A', 'IN')
    srv_msg.client_send_dns_query(step)

    misc.pass_criteria(step)
    srv_msg.send_wait_for_query(step, 'MUST', None)
    srv_msg.dns_option(step, None, 'ANSWER')

    misc.test_procedure(step)
    srv_msg.client_requests_option(step, '1')
    srv_msg.client_send_msg(step, 'DISCOVER')

    misc.pass_criteria(step)
    srv_msg.send_wait_for_message(step, 'MUST', None, 'OFFER')
    srv_msg.response_check_include_option(step, 'Response', None, '1')
    srv_msg.response_check_content(step, 'Response', None, 'yiaddr', '192.168.50.10')
    srv_msg.response_check_option_content(step, 'Response', '1', None, 'value', '255.255.255.0')

    misc.test_procedure(step)
    srv_msg.client_save_option_count(step, '1', 'server_id')
    srv_msg.client_add_saved_option_count(step, '1', 'DONT ')
    srv_msg.client_does_include_with_value(step, 'requested_addr', '192.168.50.10')
    srv_msg.client_sets_value(step,
                              'Client',
                              'FQDN_domain_name',
                              '*aa$(WHITE_SPACE).four.example.com.')
    srv_msg.client_sets_value(step, 'Client', 'FQDN_flags', 'S')
    srv_msg.client_does_include(step, 'Client', None, 'fqdn')
    srv_msg.client_send_msg(step, 'REQUEST')

    misc.pass_criteria(step)
    srv_msg.send_wait_for_message(step, 'MUST', None, 'ACK')
    srv_msg.response_check_content(step, 'Response', None, 'yiaddr', '192.168.50.10')
    srv_msg.response_check_include_option(step, 'Response', None, '1')
    srv_msg.response_check_option_content(step, 'Response', '1', None, 'value', '255.255.255.0')
    srv_msg.response_check_include_option(step, 'Response', None, '81')
    srv_msg.response_check_option_content(step, 'Response', '81', None, 'flags', '1.')
    srv_msg.response_check_option_content(step,
                                          'Response',
                                          '81',
                                          None,
                                          'fqdn',
                                          'xaax.four.example.com.')

    misc.test_procedure(step)
    srv_msg.client_save_option(step, 'server_id')
    srv_msg.dns_question_record(step, 'xaax.four.example.com', 'A', 'IN')
    srv_msg.client_send_dns_query(step)

    misc.pass_criteria(step)
    srv_msg.send_wait_for_query(step, 'MUST', None)
    srv_msg.dns_option(step, 'NOT ', 'ANSWER')
    srv_msg.dns_option_content(step, 'ANSWER', None, 'rdata', '192.168.50.10')
    srv_msg.dns_option_content(step, 'ANSWER', None, 'rrname', 'xaax.four.example.com.')

    misc.test_procedure(step)
    srv_msg.dns_question_record(step, '10.50.168.192.in-addr.arpa.', 'PTR', 'IN')
    srv_msg.client_send_dns_query(step)

    misc.pass_criteria(step)
    srv_msg.send_wait_for_query(step, 'MUST', None)
    srv_msg.dns_option(step, 'NOT ', 'ANSWER')
    srv_msg.dns_option_content(step, 'ANSWER', None, 'rdata', 'xaax.four.example.com.')
    srv_msg.dns_option_content(step, 'ANSWER', None, 'rrname', '10.50.168.192.in-addr.arpa.')

    misc.test_procedure(step)
    srv_msg.client_add_saved_option_count(step, '1', 'DONT ')
    srv_msg.client_sets_value(step, 'Client', 'ciaddr', '192.168.50.10')
    srv_msg.client_sets_value(step,
                              'Client',
                              'FQDN_domain_name',
                              '*aa$(WHITE_SPACE).four.example.com.')
    srv_msg.client_sets_value(step, 'Client', 'FQDN_flags', 'S')
    srv_msg.client_does_include(step, 'Client', None, 'fqdn')
    srv_msg.client_send_msg(step, 'RELEASE')

    misc.pass_criteria(step)
    srv_msg.send_dont_wait_for_message(step)

    misc.test_procedure(step)
    srv_msg.dns_question_record(step, 'xaax.four.example.com', 'A', 'IN')
    srv_msg.client_send_dns_query(step)

    misc.pass_criteria(step)
    srv_msg.send_wait_for_query(step, 'MUST', None)
    srv_msg.dns_option(step, None, 'ANSWER')

    misc.test_procedure(step)
    srv_msg.dns_question_record(step, '10.50.168.192.in-addr.arpa.', 'PTR', 'IN')
    srv_msg.client_send_dns_query(step)

    misc.pass_criteria(step)
    srv_msg.send_wait_for_query(step, 'MUST', None)
    srv_msg.dns_option(step, None, 'ANSWER')


@pytest.mark.v4
@pytest.mark.ddns
@pytest.mark.notsig
@pytest.mark.forward_reverse_remove
@pytest.mark.hostname_sanitization
def test_ddns4_notsig_forw_and_rev_release_hostname_sanitization_replace_2(step):

    misc.test_setup(step)
    srv_control.config_srv_subnet(step, '192.168.50.0/24', '192.168.50.10-192.168.50.10')
    srv_control.add_ddns_server(step, '127.0.0.1', '53001')
    srv_control.add_ddns_server_options(step, 'enable-updates', 'true')
    srv_control.add_ddns_server_options(step, 'qualifying-suffix', 'example.com')
    srv_control.add_ddns_server_options(step, 'hostname-char-set', '[^A-Za-z]')
    srv_control.add_ddns_server_options(step, 'hostname-char-replacement', 'x')
    srv_control.add_forward_ddns(step, 'four.example.com.', 'EMPTY_KEY', '192.168.50.252', '53')
    srv_control.add_reverse_ddns(step,
                                 '50.168.192.in-addr.arpa.',
                                 'EMPTY_KEY',
                                 '192.168.50.252',
                                 '53')
    srv_control.build_and_send_config_files(step, 'SSH', 'config-file')
    srv_control.start_srv(step, 'DHCP', 'started')

    misc.test_procedure(step)
    srv_msg.client_sets_value(step, 'Client', 'chaddr', '00:1F:D0:00:00:11')
    srv_msg.client_requests_option(step, '1')
    srv_msg.client_send_msg(step, 'DISCOVER')

    misc.pass_criteria(step)
    srv_msg.send_wait_for_message(step, 'MUST', None, 'OFFER')
    srv_msg.response_check_include_option(step, 'Response', None, '1')
    srv_msg.response_check_content(step, 'Response', None, 'yiaddr', '192.168.50.10')
    srv_msg.response_check_option_content(step, 'Response', '1', None, 'value', '255.255.255.0')

    misc.test_procedure(step)
    srv_msg.client_sets_value(step, 'Client', 'chaddr', '00:1F:D0:00:00:11')
    srv_msg.client_save_option_count(step, '1', 'server_id')
    srv_msg.client_add_saved_option_count(step, '1', 'DONT ')
    srv_msg.client_does_include_with_value(step, 'requested_addr', '192.168.50.10')
    srv_msg.client_requests_option(step, '1')
    srv_msg.client_does_include_with_value(step, 'hostname', '*a$(WHITE_SPACE).8723()+')
    srv_msg.client_send_msg(step, 'REQUEST')

    misc.pass_criteria(step)
    srv_msg.send_wait_for_message(step, 'MUST', None, 'ACK')
    srv_msg.response_check_content(step, 'Response', None, 'yiaddr', '192.168.50.10')
    srv_msg.response_check_include_option(step, 'Response', None, '1')
    srv_msg.response_check_option_content(step, 'Response', '1', None, 'value', '255.255.255.0')
    srv_msg.response_check_include_option(step, 'Response', None, '12')
    srv_msg.response_check_option_content(step, 'Response', '12', None, 'value', 'xaxxxxxxxxx')

    misc.test_procedure(step)
    srv_msg.client_sets_value(step, 'Client', 'chaddr', '00:1F:D0:00:00:11')
    srv_msg.client_add_saved_option_count(step, '1', 'DONT ')
    srv_msg.client_sets_value(step, 'Client', 'ciaddr', '192.168.50.10')
    srv_msg.client_does_include_with_value(step, 'hostname', '*a$(WHITE_SPACE).8723()+')
    srv_msg.client_send_msg(step, 'RELEASE')

    misc.pass_criteria(step)
    srv_msg.send_dont_wait_for_message(step)

    misc.test_procedure(step)
    srv_msg.client_sets_value(step, 'Client', 'chaddr', '00:1F:D0:00:00:22')
    srv_msg.client_requests_option(step, '1')
    srv_msg.client_send_msg(step, 'DISCOVER')

    misc.pass_criteria(step)
    srv_msg.send_wait_for_message(step, 'MUST', None, 'OFFER')
    srv_msg.response_check_include_option(step, 'Response', None, '1')
    srv_msg.response_check_content(step, 'Response', None, 'yiaddr', '192.168.50.10')
    srv_msg.response_check_option_content(step, 'Response', '1', None, 'value', '255.255.255.0')


@pytest.mark.v4
@pytest.mark.ddns
@pytest.mark.notsig
@pytest.mark.forward_reverse_remove
@pytest.mark.hostname_sanitization
def test_ddns4_notsig_forw_and_rev_release_fqdn_sanitization_replace_2(step):

    misc.test_setup(step)
    srv_control.config_srv_subnet(step, '192.168.50.0/24', '192.168.50.10-192.168.50.10')
    srv_control.add_ddns_server(step, '127.0.0.1', '53001')
    srv_control.add_ddns_server_options(step, 'enable-updates', 'true')
    srv_control.add_ddns_server_options(step, 'qualifying-suffix', 'example.com')
    srv_control.add_ddns_server_options(step, 'hostname-char-set', '[^A-Za-z]')
    srv_control.add_ddns_server_options(step, 'hostname-char-replacement', 'x')
    srv_control.add_forward_ddns(step, 'four.example.com.', 'EMPTY_KEY', '192.168.50.252', '53')
    srv_control.add_reverse_ddns(step,
                                 '50.168.192.in-addr.arpa.',
                                 'EMPTY_KEY',
                                 '192.168.50.252',
                                 '53')
    srv_control.build_and_send_config_files(step, 'SSH', 'config-file')
    srv_control.start_srv(step, 'DHCP', 'started')

    misc.test_procedure(step)
    srv_msg.client_sets_value(step, 'Client', 'chaddr', '00:1F:D0:00:00:11')
    srv_msg.client_requests_option(step, '1')
    srv_msg.client_send_msg(step, 'DISCOVER')

    misc.pass_criteria(step)
    srv_msg.send_wait_for_message(step, 'MUST', None, 'OFFER')
    srv_msg.response_check_include_option(step, 'Response', None, '1')
    srv_msg.response_check_content(step, 'Response', None, 'yiaddr', '192.168.50.10')
    srv_msg.response_check_option_content(step, 'Response', '1', None, 'value', '255.255.255.0')

    misc.test_procedure(step)
    srv_msg.client_sets_value(step, 'Client', 'chaddr', '00:1F:D0:00:00:11')
    srv_msg.client_save_option_count(step, '1', 'server_id')
    srv_msg.client_add_saved_option_count(step, '1', 'DONT ')
    srv_msg.client_does_include_with_value(step, 'requested_addr', '192.168.50.10')
    srv_msg.client_sets_value(step, 'Client', 'FQDN_domain_name', '*a$(WHITE_SPACE).8723()+.')
    srv_msg.client_sets_value(step, 'Client', 'FQDN_flags', 'S')
    srv_msg.client_does_include(step, 'Client', None, 'fqdn')
    srv_msg.client_send_msg(step, 'REQUEST')

    misc.pass_criteria(step)
    srv_msg.send_wait_for_message(step, 'MUST', None, 'ACK')
    srv_msg.response_check_content(step, 'Response', None, 'yiaddr', '192.168.50.10')
    srv_msg.response_check_include_option(step, 'Response', None, '1')
    srv_msg.response_check_option_content(step, 'Response', '1', None, 'value', '255.255.255.0')
    srv_msg.response_check_include_option(step, 'Response', None, '81')
    srv_msg.response_check_option_content(step, 'Response', '81', None, 'flags', '1.')
    srv_msg.response_check_option_content(step, 'Response', '81', None, 'fqdn', 'xax.xxxxxxx.')

    misc.test_procedure(step)
    srv_msg.client_sets_value(step, 'Client', 'chaddr', '00:1F:D0:00:00:11')
    srv_msg.client_add_saved_option_count(step, '1', 'DONT ')
    srv_msg.client_sets_value(step, 'Client', 'ciaddr', '192.168.50.10')
    srv_msg.client_sets_value(step, 'Client', 'FQDN_domain_name', '*a$(WHITE_SPACE).8723()+.')
    srv_msg.client_sets_value(step, 'Client', 'FQDN_flags', 'S')
    srv_msg.client_does_include(step, 'Client', None, 'fqdn')
    srv_msg.client_send_msg(step, 'RELEASE')

    misc.pass_criteria(step)
    srv_msg.send_dont_wait_for_message(step)

    misc.test_procedure(step)
    srv_msg.client_sets_value(step, 'Client', 'chaddr', '00:1F:D0:00:00:22')
    srv_msg.client_requests_option(step, '1')
    srv_msg.client_send_msg(step, 'DISCOVER')

    misc.pass_criteria(step)
    srv_msg.send_wait_for_message(step, 'MUST', None, 'OFFER')
    srv_msg.response_check_include_option(step, 'Response', None, '1')
    srv_msg.response_check_content(step, 'Response', None, 'yiaddr', '192.168.50.10')
    srv_msg.response_check_option_content(step, 'Response', '1', None, 'value', '255.255.255.0')


@pytest.mark.v4
@pytest.mark.ddns
@pytest.mark.notsig
@pytest.mark.forward_reverse_remove
@pytest.mark.hostname_sanitization
def test_ddns4_notsig_forw_and_rev_release_hostname_sanitization_omit_1(step):

    misc.test_setup(step)
    srv_control.config_srv_subnet(step, '192.168.50.0/24', '192.168.50.10-192.168.50.10')
    srv_control.add_ddns_server(step, '127.0.0.1', '53001')
    srv_control.add_ddns_server_options(step, 'enable-updates', 'true')
    srv_control.add_ddns_server_options(step, 'qualifying-suffix', 'example.com')
    srv_control.add_ddns_server_options(step, 'hostname-char-set', '[^A-Za-z0-9.-]')
    srv_control.add_ddns_server_options(step, 'hostname-char-replacement', '$(EMPTY)')
    srv_control.add_forward_ddns(step, 'four.example.com.', 'EMPTY_KEY', '192.168.50.252', '53')
    srv_control.add_reverse_ddns(step,
                                 '50.168.192.in-addr.arpa.',
                                 'EMPTY_KEY',
                                 '192.168.50.252',
                                 '53')
    srv_control.build_and_send_config_files(step, 'SSH', 'config-file')
    srv_control.start_srv(step, 'DHCP', 'started')

    srv_control.use_dns_set_number(step, '20')
    srv_control.start_srv(step, 'DNS', 'started')

    misc.test_procedure(step)
    srv_msg.dns_question_record(step, 'aa.four.example.com', 'A', 'IN')
    srv_msg.client_send_dns_query(step)

    misc.pass_criteria(step)
    srv_msg.send_wait_for_query(step, 'MUST', None)
    srv_msg.dns_option(step, None, 'ANSWER')

    misc.test_procedure(step)
    srv_msg.client_requests_option(step, '1')
    srv_msg.client_send_msg(step, 'DISCOVER')

    misc.pass_criteria(step)
    srv_msg.send_wait_for_message(step, 'MUST', None, 'OFFER')
    srv_msg.response_check_include_option(step, 'Response', None, '1')
    srv_msg.response_check_content(step, 'Response', None, 'yiaddr', '192.168.50.10')
    srv_msg.response_check_option_content(step, 'Response', '1', None, 'value', '255.255.255.0')

    misc.test_procedure(step)
    srv_msg.client_save_option_count(step, '1', 'server_id')
    srv_msg.client_add_saved_option_count(step, '1', 'DONT ')
    srv_msg.client_does_include_with_value(step, 'requested_addr', '192.168.50.10')
    srv_msg.client_requests_option(step, '1')
    srv_msg.client_does_include_with_value(step,
                                           'hostname',
                                           '$(WHITE_SPACE)*aa*.fo^ur.exa(mple.c)om.$(WHITE_SPACE)')
    srv_msg.client_send_msg(step, 'REQUEST')

    misc.pass_criteria(step)
    srv_msg.send_wait_for_message(step, 'MUST', None, 'ACK')
    srv_msg.response_check_content(step, 'Response', None, 'yiaddr', '192.168.50.10')
    srv_msg.response_check_include_option(step, 'Response', None, '1')
    srv_msg.response_check_option_content(step, 'Response', '1', None, 'value', '255.255.255.0')
    srv_msg.response_check_include_option(step, 'Response', None, '12')
    srv_msg.response_check_option_content(step,
                                          'Response',
                                          '12',
                                          None,
                                          'value',
                                          'aa.four.example.com.')

    misc.test_procedure(step)
    srv_msg.client_save_option(step, 'server_id')
    srv_msg.dns_question_record(step, 'aa.four.example.com', 'A', 'IN')
    srv_msg.client_send_dns_query(step)

    misc.pass_criteria(step)
    srv_msg.send_wait_for_query(step, 'MUST', None)
    srv_msg.dns_option(step, 'NOT ', 'ANSWER')
    srv_msg.dns_option_content(step, 'ANSWER', None, 'rdata', '192.168.50.10')
    srv_msg.dns_option_content(step, 'ANSWER', None, 'rrname', 'aa.four.example.com.')

    misc.test_procedure(step)
    srv_msg.dns_question_record(step, '10.50.168.192.in-addr.arpa.', 'PTR', 'IN')
    srv_msg.client_send_dns_query(step)

    misc.pass_criteria(step)
    srv_msg.send_wait_for_query(step, 'MUST', None)
    srv_msg.dns_option(step, 'NOT ', 'ANSWER')
    srv_msg.dns_option_content(step, 'ANSWER', None, 'rdata', 'aa.four.example.com.')
    srv_msg.dns_option_content(step, 'ANSWER', None, 'rrname', '10.50.168.192.in-addr.arpa.')

    misc.test_procedure(step)
    srv_msg.client_add_saved_option_count(step, '1', 'DONT ')
    srv_msg.client_sets_value(step, 'Client', 'ciaddr', '192.168.50.10')
    srv_msg.client_does_include_with_value(step,
                                           'hostname',
                                           '$(WHITE_SPACE)*aa*.fo^ur.exa(mple.c)om$(WHITE_SPACE)')
    srv_msg.client_send_msg(step, 'RELEASE')

    misc.pass_criteria(step)
    srv_msg.send_dont_wait_for_message(step)

    misc.test_procedure(step)
    srv_msg.dns_question_record(step, 'aa.four.example.com', 'A', 'IN')
    srv_msg.client_send_dns_query(step)

    misc.pass_criteria(step)
    srv_msg.send_wait_for_query(step, 'MUST', None)
    srv_msg.dns_option(step, None, 'ANSWER')

    misc.test_procedure(step)
    srv_msg.dns_question_record(step, '10.50.168.192.in-addr.arpa.', 'PTR', 'IN')
    srv_msg.client_send_dns_query(step)

    misc.pass_criteria(step)
    srv_msg.send_wait_for_query(step, 'MUST', None)
    srv_msg.dns_option(step, None, 'ANSWER')


@pytest.mark.v4
@pytest.mark.ddns
@pytest.mark.notsig
@pytest.mark.forward_reverse_remove
@pytest.mark.hostname_sanitization
def test_ddns4_notsig_forw_and_rev_release_fqdn_sanitization_omit_1(step):

    misc.test_setup(step)
    srv_control.config_srv_subnet(step, '192.168.50.0/24', '192.168.50.10-192.168.50.10')
    srv_control.add_ddns_server(step, '127.0.0.1', '53001')
    srv_control.add_ddns_server_options(step, 'enable-updates', 'true')
    srv_control.add_ddns_server_options(step, 'qualifying-suffix', 'example.com')
    srv_control.add_ddns_server_options(step, 'hostname-char-set', '[^A-Za-z0-9.-]')
    srv_control.add_ddns_server_options(step, 'hostname-char-replacement', '$(EMPTY)')
    srv_control.add_forward_ddns(step, 'four.example.com.', 'EMPTY_KEY', '192.168.50.252', '53')
    srv_control.add_reverse_ddns(step,
                                 '50.168.192.in-addr.arpa.',
                                 'EMPTY_KEY',
                                 '192.168.50.252',
                                 '53')
    srv_control.build_and_send_config_files(step, 'SSH', 'config-file')
    srv_control.start_srv(step, 'DHCP', 'started')

    srv_control.use_dns_set_number(step, '20')
    srv_control.start_srv(step, 'DNS', 'started')

    misc.test_procedure(step)
    srv_msg.dns_question_record(step, 'aa.four.example.com', 'A', 'IN')
    srv_msg.client_send_dns_query(step)

    misc.pass_criteria(step)
    srv_msg.send_wait_for_query(step, 'MUST', None)
    srv_msg.dns_option(step, None, 'ANSWER')

    misc.test_procedure(step)
    srv_msg.client_requests_option(step, '1')
    srv_msg.client_send_msg(step, 'DISCOVER')

    misc.pass_criteria(step)
    srv_msg.send_wait_for_message(step, 'MUST', None, 'OFFER')
    srv_msg.response_check_include_option(step, 'Response', None, '1')
    srv_msg.response_check_content(step, 'Response', None, 'yiaddr', '192.168.50.10')
    srv_msg.response_check_option_content(step, 'Response', '1', None, 'value', '255.255.255.0')

    misc.test_procedure(step)
    srv_msg.client_save_option_count(step, '1', 'server_id')
    srv_msg.client_add_saved_option_count(step, '1', 'DONT ')
    srv_msg.client_does_include_with_value(step, 'requested_addr', '192.168.50.10')
    srv_msg.client_sets_value(step,
                              'Client',
                              'FQDN_domain_name',
                              '$(WHITE_SPACE)*aa*.fo^ur.exa(mple.c)om.^')
    # Client sets FQDN_domain_name value to aa.four.example.com.
    srv_msg.client_sets_value(step, 'Client', 'FQDN_flags', 'S')
    srv_msg.client_does_include(step, 'Client', None, 'fqdn')
    srv_msg.client_send_msg(step, 'REQUEST')

    misc.pass_criteria(step)
    srv_msg.send_wait_for_message(step, 'MUST', None, 'ACK')
    srv_msg.response_check_content(step, 'Response', None, 'yiaddr', '192.168.50.10')
    srv_msg.response_check_include_option(step, 'Response', None, '1')
    srv_msg.response_check_option_content(step, 'Response', '1', None, 'value', '255.255.255.0')
    srv_msg.response_check_include_option(step, 'Response', None, '81')
    srv_msg.response_check_option_content(step, 'Response', '81', None, 'flags', '1.')
    srv_msg.response_check_option_content(step,
                                          'Response',
                                          '81',
                                          None,
                                          'fqdn',
                                          'aa.four.example.com.')

    misc.test_procedure(step)
    srv_msg.client_save_option(step, 'server_id')
    srv_msg.dns_question_record(step, 'aa.four.example.com', 'A', 'IN')
    srv_msg.client_send_dns_query(step)

    misc.pass_criteria(step)
    srv_msg.send_wait_for_query(step, 'MUST', None)
    srv_msg.dns_option(step, 'NOT ', 'ANSWER')
    srv_msg.dns_option_content(step, 'ANSWER', None, 'rdata', '192.168.50.10')
    srv_msg.dns_option_content(step, 'ANSWER', None, 'rrname', 'aa.four.example.com.')

    misc.test_procedure(step)
    srv_msg.dns_question_record(step, '10.50.168.192.in-addr.arpa.', 'PTR', 'IN')
    srv_msg.client_send_dns_query(step)

    misc.pass_criteria(step)
    srv_msg.send_wait_for_query(step, 'MUST', None)
    srv_msg.dns_option(step, 'NOT ', 'ANSWER')
    srv_msg.dns_option_content(step, 'ANSWER', None, 'rdata', 'aa.four.example.com.')
    srv_msg.dns_option_content(step, 'ANSWER', None, 'rrname', '10.50.168.192.in-addr.arpa.')

    misc.test_procedure(step)
    srv_msg.client_add_saved_option_count(step, '1', 'DONT ')
    srv_msg.client_sets_value(step, 'Client', 'ciaddr', '192.168.50.10')
    srv_msg.client_sets_value(step,
                              'Client',
                              'FQDN_domain_name',
                              '$(WHITE_SPACE)*aa*.fo^ur.exa(mple.c)om.')
    srv_msg.client_sets_value(step, 'Client', 'FQDN_flags', 'S')
    srv_msg.client_does_include(step, 'Client', None, 'fqdn')
    srv_msg.client_send_msg(step, 'RELEASE')

    misc.pass_criteria(step)
    srv_msg.send_dont_wait_for_message(step)

    misc.test_procedure(step)
    srv_msg.dns_question_record(step, 'aa.four.example.com', 'A', 'IN')
    srv_msg.client_send_dns_query(step)

    misc.pass_criteria(step)
    srv_msg.send_wait_for_query(step, 'MUST', None)
    srv_msg.dns_option(step, None, 'ANSWER')

    misc.test_procedure(step)
    srv_msg.dns_question_record(step, '10.50.168.192.in-addr.arpa.', 'PTR', 'IN')
    srv_msg.client_send_dns_query(step)

    misc.pass_criteria(step)
    srv_msg.send_wait_for_query(step, 'MUST', None)
    srv_msg.dns_option(step, None, 'ANSWER')

    misc.test_procedure(step)
    srv_msg.dns_question_record(step, 'aa.four.example.com', 'A', 'IN')
    srv_msg.client_send_dns_query(step)

    misc.pass_criteria(step)
    srv_msg.send_wait_for_query(step, 'MUST', None)
    srv_msg.dns_option(step, None, 'ANSWER')

    misc.test_procedure(step)
    srv_msg.dns_question_record(step, '10.50.168.192.in-addr.arpa.', 'PTR', 'IN')
    srv_msg.client_send_dns_query(step)

    misc.pass_criteria(step)
    srv_msg.send_wait_for_query(step, 'MUST', None)
    srv_msg.dns_option(step, None, 'ANSWER')


@pytest.mark.v4
@pytest.mark.ddns
@pytest.mark.notsig
@pytest.mark.forward_reverse_remove
@pytest.mark.hostname_sanitization
def test_ddns4_notsig_forw_and_rev_release_hostname_sanitization_omit_identical_name(step):
    # Two clients are using different hostnames which after sanitization end up being identical
    misc.test_setup(step)
    srv_control.config_srv_subnet(step, '192.168.50.0/24', '192.168.50.10-192.168.50.11')
    srv_control.add_ddns_server(step, '127.0.0.1', '53001')
    srv_control.add_ddns_server_options(step, 'enable-updates', 'true')
    srv_control.add_ddns_server_options(step, 'qualifying-suffix', 'example.com')
    srv_control.add_ddns_server_options(step, 'hostname-char-set', '[^A-Za-z.-]')
    srv_control.add_ddns_server_options(step, 'hostname-char-replacement', '$(EMPTY)')
    srv_control.add_forward_ddns(step, 'four.example.com.', 'EMPTY_KEY', '192.168.50.252', '53')
    srv_control.add_reverse_ddns(step,
                                 '50.168.192.in-addr.arpa.',
                                 'EMPTY_KEY',
                                 '192.168.50.252',
                                 '53')
    srv_control.build_and_send_config_files(step, 'SSH', 'config-file')
    srv_control.start_srv(step, 'DHCP', 'started')

    srv_control.use_dns_set_number(step, '20')
    srv_control.start_srv(step, 'DNS', 'started')

    misc.test_procedure(step)
    srv_msg.dns_question_record(step, 'client.four.example.com', 'A', 'IN')
    srv_msg.client_send_dns_query(step)

    misc.pass_criteria(step)
    srv_msg.send_wait_for_query(step, 'MUST', None)
    srv_msg.dns_option(step, None, 'ANSWER')

    misc.test_procedure(step)
    srv_msg.dns_question_record(step, 'client1.four.example.com', 'A', 'IN')
    srv_msg.client_send_dns_query(step)

    misc.pass_criteria(step)
    srv_msg.send_wait_for_query(step, 'MUST', None)
    srv_msg.dns_option(step, None, 'ANSWER')

    misc.test_procedure(step)
    srv_msg.dns_question_record(step, 'client2.four.example.com', 'A', 'IN')
    srv_msg.client_send_dns_query(step)

    misc.pass_criteria(step)
    srv_msg.send_wait_for_query(step, 'MUST', None)
    srv_msg.dns_option(step, None, 'ANSWER')

    misc.test_procedure(step)
    srv_msg.client_sets_value(step, 'Client', 'chaddr', '00:1F:D0:00:00:11')
    srv_msg.client_requests_option(step, '1')
    srv_msg.client_send_msg(step, 'DISCOVER')

    misc.pass_criteria(step)
    srv_msg.send_wait_for_message(step, 'MUST', None, 'OFFER')
    srv_msg.response_check_include_option(step, 'Response', None, '1')
    srv_msg.response_check_content(step, 'Response', None, 'yiaddr', '192.168.50.10')
    srv_msg.response_check_option_content(step, 'Response', '1', None, 'value', '255.255.255.0')

    misc.test_procedure(step)
    srv_msg.client_sets_value(step, 'Client', 'chaddr', '00:1F:D0:00:00:11')
    srv_msg.client_save_option_count(step, '1', 'server_id')
    srv_msg.client_add_saved_option_count(step, '1', 'DONT ')
    srv_msg.client_does_include_with_value(step, 'requested_addr', '192.168.50.10')
    srv_msg.client_requests_option(step, '1')
    srv_msg.client_does_include_with_value(step, 'hostname', 'client1.four.example.com')
    srv_msg.client_send_msg(step, 'REQUEST')

    misc.pass_criteria(step)
    srv_msg.send_wait_for_message(step, 'MUST', None, 'ACK')
    srv_msg.response_check_content(step, 'Response', None, 'yiaddr', '192.168.50.10')
    srv_msg.response_check_include_option(step, 'Response', None, '1')
    srv_msg.response_check_option_content(step, 'Response', '1', None, 'value', '255.255.255.0')
    srv_msg.response_check_include_option(step, 'Response', None, '12')
    srv_msg.response_check_option_content(step,
                                          'Response',
                                          '12',
                                          None,
                                          'value',
                                          'client.four.example.com')

    misc.test_procedure(step)
    srv_msg.client_save_option(step, 'server_id')
    srv_msg.dns_question_record(step, 'client.four.example.com', 'A', 'IN')
    srv_msg.client_send_dns_query(step)

    misc.pass_criteria(step)
    srv_msg.send_wait_for_query(step, 'MUST', None)
    srv_msg.dns_option(step, 'NOT ', 'ANSWER')
    srv_msg.dns_option_content(step, 'ANSWER', None, 'rdata', '192.168.50.10')
    srv_msg.dns_option_content(step, 'ANSWER', None, 'rrname', 'client.four.example.com.')

    misc.test_procedure(step)
    srv_msg.dns_question_record(step, '10.50.168.192.in-addr.arpa.', 'PTR', 'IN')
    srv_msg.client_send_dns_query(step)

    misc.pass_criteria(step)
    srv_msg.send_wait_for_query(step, 'MUST', None)
    srv_msg.dns_option(step, 'NOT ', 'ANSWER')
    srv_msg.dns_option_content(step, 'ANSWER', None, 'rdata', 'client.four.example.com.')
    srv_msg.dns_option_content(step, 'ANSWER', None, 'rrname', '10.50.168.192.in-addr.arpa.')

    misc.test_procedure(step)
    srv_msg.client_sets_value(step, 'Client', 'chaddr', '00:1F:D0:00:00:22')
    srv_msg.client_requests_option(step, '1')
    srv_msg.client_send_msg(step, 'DISCOVER')

    misc.pass_criteria(step)
    srv_msg.send_wait_for_message(step, 'MUST', None, 'OFFER')
    srv_msg.response_check_include_option(step, 'Response', None, '1')
    srv_msg.response_check_content(step, 'Response', None, 'yiaddr', '192.168.50.11')
    srv_msg.response_check_option_content(step, 'Response', '1', None, 'value', '255.255.255.0')

    misc.test_procedure(step)
    srv_msg.client_sets_value(step, 'Client', 'chaddr', '00:1F:D0:00:00:22')
    srv_msg.client_save_option_count(step, '1', 'server_id')
    srv_msg.client_add_saved_option_count(step, '1', 'DONT ')
    srv_msg.client_does_include_with_value(step, 'requested_addr', '192.168.50.11')
    srv_msg.client_requests_option(step, '1')
    srv_msg.client_does_include_with_value(step, 'hostname', 'client2.four.example.com')
    srv_msg.client_send_msg(step, 'REQUEST')

    misc.pass_criteria(step)
    srv_msg.send_wait_for_message(step, 'MUST', None, 'ACK')
    srv_msg.response_check_content(step, 'Response', None, 'yiaddr', '192.168.50.11')
    srv_msg.response_check_include_option(step, 'Response', None, '1')
    srv_msg.response_check_option_content(step, 'Response', '1', None, 'value', '255.255.255.0')
    srv_msg.response_check_include_option(step, 'Response', None, '12')
    srv_msg.response_check_option_content(step,
                                          'Response',
                                          '12',
                                          None,
                                          'value',
                                          'client.four.example.com')

    misc.test_procedure(step)
    srv_msg.dns_question_record(step, 'client1.four.example.com', 'A', 'IN')
    srv_msg.client_send_dns_query(step)

    misc.pass_criteria(step)
    srv_msg.send_wait_for_query(step, 'MUST', None)
    srv_msg.dns_option(step, None, 'ANSWER')

    misc.test_procedure(step)
    srv_msg.dns_question_record(step, 'client2.four.example.com', 'A', 'IN')
    srv_msg.client_send_dns_query(step)

    misc.pass_criteria(step)
    srv_msg.send_wait_for_query(step, 'MUST', None)
    srv_msg.dns_option(step, None, 'ANSWER')

    misc.test_procedure(step)
    srv_msg.client_sets_value(step, 'Client', 'chaddr', '00:1F:D0:00:00:11')
    srv_msg.client_add_saved_option_count(step, '1', 'DONT ')
    srv_msg.client_sets_value(step, 'Client', 'ciaddr', '192.168.50.10')
    srv_msg.client_does_include_with_value(step, 'hostname', 'client1.four.example.com')
    srv_msg.client_send_msg(step, 'RELEASE')

    misc.pass_criteria(step)
    srv_msg.send_dont_wait_for_message(step)

    misc.test_procedure(step)
    srv_msg.dns_question_record(step, 'client.four.example.com', 'A', 'IN')
    srv_msg.client_send_dns_query(step)

    misc.pass_criteria(step)
    srv_msg.send_wait_for_query(step, 'MUST', None)
    srv_msg.dns_option(step, None, 'ANSWER')

    misc.test_procedure(step)
    srv_msg.dns_question_record(step, '10.50.168.192.in-addr.arpa.', 'PTR', 'IN')
    srv_msg.client_send_dns_query(step)

    misc.pass_criteria(step)
    srv_msg.send_wait_for_query(step, 'MUST', None)
    srv_msg.dns_option(step, None, 'ANSWER')


@pytest.mark.v4
@pytest.mark.ddns
@pytest.mark.notsig
@pytest.mark.forward_reverse_remove
@pytest.mark.hostname_sanitization
def test_ddns4_notsig_forw_and_rev_release_fqdn_sanitization_omit_identical_name(step):
    # Two clients are using different hostnames which after sanitization end up being identical
    misc.test_setup(step)
    srv_control.config_srv_subnet(step, '192.168.50.0/24', '192.168.50.10-192.168.50.11')
    srv_control.add_ddns_server(step, '127.0.0.1', '53001')
    srv_control.add_ddns_server_options(step, 'enable-updates', 'true')
    srv_control.add_ddns_server_options(step, 'qualifying-suffix', 'example.com')
    srv_control.add_ddns_server_options(step, 'hostname-char-set', '[^A-Za-z.-]')
    srv_control.add_ddns_server_options(step, 'hostname-char-replacement', '$(EMPTY)')
    srv_control.add_forward_ddns(step, 'four.example.com.', 'EMPTY_KEY', '192.168.50.252', '53')
    srv_control.add_reverse_ddns(step,
                                 '50.168.192.in-addr.arpa.',
                                 'EMPTY_KEY',
                                 '192.168.50.252',
                                 '53')
    srv_control.build_and_send_config_files(step, 'SSH', 'config-file')
    srv_control.start_srv(step, 'DHCP', 'started')

    srv_control.use_dns_set_number(step, '20')
    srv_control.start_srv(step, 'DNS', 'started')

    misc.test_procedure(step)
    srv_msg.dns_question_record(step, 'client.four.example.com', 'A', 'IN')
    srv_msg.client_send_dns_query(step)

    misc.pass_criteria(step)
    srv_msg.send_wait_for_query(step, 'MUST', None)
    srv_msg.dns_option(step, None, 'ANSWER')

    misc.test_procedure(step)
    srv_msg.dns_question_record(step, 'client1.four.example.com', 'A', 'IN')
    srv_msg.client_send_dns_query(step)

    misc.pass_criteria(step)
    srv_msg.send_wait_for_query(step, 'MUST', None)
    srv_msg.dns_option(step, None, 'ANSWER')

    misc.test_procedure(step)
    srv_msg.dns_question_record(step, 'client2.four.example.com', 'A', 'IN')
    srv_msg.client_send_dns_query(step)

    misc.pass_criteria(step)
    srv_msg.send_wait_for_query(step, 'MUST', None)
    srv_msg.dns_option(step, None, 'ANSWER')

    misc.test_procedure(step)
    srv_msg.client_sets_value(step, 'Client', 'chaddr', '00:1F:D0:00:00:11')
    srv_msg.client_requests_option(step, '1')
    srv_msg.client_send_msg(step, 'DISCOVER')

    misc.pass_criteria(step)
    srv_msg.send_wait_for_message(step, 'MUST', None, 'OFFER')
    srv_msg.response_check_include_option(step, 'Response', None, '1')
    srv_msg.response_check_content(step, 'Response', None, 'yiaddr', '192.168.50.10')
    srv_msg.response_check_option_content(step, 'Response', '1', None, 'value', '255.255.255.0')

    misc.test_procedure(step)
    srv_msg.client_sets_value(step, 'Client', 'chaddr', '00:1F:D0:00:00:11')
    srv_msg.client_save_option_count(step, '1', 'server_id')
    srv_msg.client_add_saved_option_count(step, '1', 'DONT ')
    srv_msg.client_does_include_with_value(step, 'requested_addr', '192.168.50.10')
    srv_msg.client_sets_value(step, 'Client', 'FQDN_domain_name', 'client1.four.example.com.')
    srv_msg.client_sets_value(step, 'Client', 'FQDN_flags', 'S')
    srv_msg.client_does_include(step, 'Client', None, 'fqdn')
    srv_msg.client_send_msg(step, 'REQUEST')

    misc.pass_criteria(step)
    srv_msg.send_wait_for_message(step, 'MUST', None, 'ACK')
    srv_msg.response_check_content(step, 'Response', None, 'yiaddr', '192.168.50.10')
    srv_msg.response_check_include_option(step, 'Response', None, '1')
    srv_msg.response_check_option_content(step, 'Response', '1', None, 'value', '255.255.255.0')
    srv_msg.response_check_include_option(step, 'Response', None, '81')
    srv_msg.response_check_option_content(step, 'Response', '81', None, 'flags', '1.')
    srv_msg.response_check_option_content(step,
                                          'Response',
                                          '81',
                                          None,
                                          'fqdn',
                                          'client.four.example.com.')

    misc.test_procedure(step)
    srv_msg.client_save_option(step, 'server_id')
    srv_msg.dns_question_record(step, 'client.four.example.com', 'A', 'IN')
    srv_msg.client_send_dns_query(step)

    misc.pass_criteria(step)
    srv_msg.send_wait_for_query(step, 'MUST', None)
    srv_msg.dns_option(step, 'NOT ', 'ANSWER')
    srv_msg.dns_option_content(step, 'ANSWER', None, 'rdata', '192.168.50.10')
    srv_msg.dns_option_content(step, 'ANSWER', None, 'rrname', 'client.four.example.com.')

    misc.test_procedure(step)
    srv_msg.dns_question_record(step, '10.50.168.192.in-addr.arpa.', 'PTR', 'IN')
    srv_msg.client_send_dns_query(step)

    misc.pass_criteria(step)
    srv_msg.send_wait_for_query(step, 'MUST', None)
    srv_msg.dns_option(step, 'NOT ', 'ANSWER')
    srv_msg.dns_option_content(step, 'ANSWER', None, 'rdata', 'client.four.example.com.')
    srv_msg.dns_option_content(step, 'ANSWER', None, 'rrname', '10.50.168.192.in-addr.arpa.')

    misc.test_procedure(step)
    srv_msg.client_sets_value(step, 'Client', 'chaddr', '00:1F:D0:00:00:22')
    srv_msg.client_requests_option(step, '1')
    srv_msg.client_send_msg(step, 'DISCOVER')

    misc.pass_criteria(step)
    srv_msg.send_wait_for_message(step, 'MUST', None, 'OFFER')
    srv_msg.response_check_include_option(step, 'Response', None, '1')
    srv_msg.response_check_content(step, 'Response', None, 'yiaddr', '192.168.50.11')
    srv_msg.response_check_option_content(step, 'Response', '1', None, 'value', '255.255.255.0')

    misc.test_procedure(step)
    srv_msg.client_sets_value(step, 'Client', 'chaddr', '00:1F:D0:00:00:22')
    srv_msg.client_save_option_count(step, '1', 'server_id')
    srv_msg.client_add_saved_option_count(step, '1', 'DONT ')
    srv_msg.client_does_include_with_value(step, 'requested_addr', '192.168.50.11')
    srv_msg.client_sets_value(step, 'Client', 'FQDN_domain_name', 'client2.four.example.com.')
    srv_msg.client_sets_value(step, 'Client', 'FQDN_flags', 'S')
    srv_msg.client_does_include(step, 'Client', None, 'fqdn')
    srv_msg.client_send_msg(step, 'REQUEST')

    misc.pass_criteria(step)
    srv_msg.send_wait_for_message(step, 'MUST', None, 'ACK')
    srv_msg.response_check_content(step, 'Response', None, 'yiaddr', '192.168.50.11')
    srv_msg.response_check_include_option(step, 'Response', None, '1')
    srv_msg.response_check_option_content(step, 'Response', '1', None, 'value', '255.255.255.0')
    srv_msg.response_check_include_option(step, 'Response', None, '81')
    srv_msg.response_check_option_content(step, 'Response', '81', None, 'flags', '1.')
    srv_msg.response_check_option_content(step,
                                          'Response',
                                          '81',
                                          None,
                                          'fqdn',
                                          'client.four.example.com.')

    misc.test_procedure(step)
    srv_msg.dns_question_record(step, 'client1.four.example.com', 'A', 'IN')
    srv_msg.client_send_dns_query(step)

    misc.pass_criteria(step)
    srv_msg.send_wait_for_query(step, 'MUST', None)
    srv_msg.dns_option(step, None, 'ANSWER')

    misc.test_procedure(step)
    srv_msg.dns_question_record(step, 'client2.four.example.com', 'A', 'IN')
    srv_msg.client_send_dns_query(step)

    misc.pass_criteria(step)
    srv_msg.send_wait_for_query(step, 'MUST', None)
    srv_msg.dns_option(step, None, 'ANSWER')

    misc.test_procedure(step)
    srv_msg.client_sets_value(step, 'Client', 'chaddr', '00:1F:D0:00:00:11')
    srv_msg.client_add_saved_option_count(step, '1', 'DONT ')
    srv_msg.client_sets_value(step, 'Client', 'ciaddr', '192.168.50.10')
    srv_msg.client_sets_value(step, 'Client', 'FQDN_domain_name', 'client1.four.example.com.')
    srv_msg.client_sets_value(step, 'Client', 'FQDN_flags', 'S')
    srv_msg.client_does_include(step, 'Client', None, 'fqdn')
    srv_msg.client_send_msg(step, 'RELEASE')

    misc.pass_criteria(step)
    srv_msg.send_dont_wait_for_message(step)

    misc.test_procedure(step)
    srv_msg.dns_question_record(step, 'client.four.example.com', 'A', 'IN')
    srv_msg.client_send_dns_query(step)

    misc.pass_criteria(step)
    srv_msg.send_wait_for_query(step, 'MUST', None)
    srv_msg.dns_option(step, None, 'ANSWER')

    misc.test_procedure(step)
    srv_msg.dns_question_record(step, '10.50.168.192.in-addr.arpa.', 'PTR', 'IN')
    srv_msg.client_send_dns_query(step)

    misc.pass_criteria(step)
    srv_msg.send_wait_for_query(step, 'MUST', None)
    srv_msg.dns_option(step, None, 'ANSWER')


@pytest.mark.v4
@pytest.mark.ddns
@pytest.mark.notsig
@pytest.mark.forward_reverse_remove
@pytest.mark.hostname_sanitization
def test_ddns4_notsig_forw_and_rev_release_hostname_sanitization_omit_2(step):

    misc.test_setup(step)
    srv_control.config_srv_subnet(step, '192.168.50.0/24', '192.168.50.10-192.168.50.10')
    srv_control.add_ddns_server(step, '127.0.0.1', '53001')
    srv_control.add_ddns_server_options(step, 'enable-updates', 'true')
    srv_control.add_ddns_server_options(step, 'qualifying-suffix', 'example.com')
    srv_control.add_ddns_server_options(step, 'hostname-char-set', '[^A-Za-z]')
    srv_control.add_ddns_server_options(step, 'hostname-char-replacement', '$(EMPTY)')
    srv_control.add_forward_ddns(step, 'four.example.com.', 'EMPTY_KEY', '192.168.50.252', '53')
    srv_control.add_reverse_ddns(step,
                                 '50.168.192.in-addr.arpa.',
                                 'EMPTY_KEY',
                                 '192.168.50.252',
                                 '53')
    srv_control.build_and_send_config_files(step, 'SSH', 'config-file')
    srv_control.start_srv(step, 'DHCP', 'started')

    misc.test_procedure(step)
    srv_msg.client_sets_value(step, 'Client', 'chaddr', '00:1F:D0:00:00:11')
    srv_msg.client_requests_option(step, '1')
    srv_msg.client_send_msg(step, 'DISCOVER')

    misc.pass_criteria(step)
    srv_msg.send_wait_for_message(step, 'MUST', None, 'OFFER')
    srv_msg.response_check_include_option(step, 'Response', None, '1')
    srv_msg.response_check_content(step, 'Response', None, 'yiaddr', '192.168.50.10')
    srv_msg.response_check_option_content(step, 'Response', '1', None, 'value', '255.255.255.0')

    misc.test_procedure(step)
    srv_msg.client_sets_value(step, 'Client', 'chaddr', '00:1F:D0:00:00:11')
    srv_msg.client_save_option_count(step, '1', 'server_id')
    srv_msg.client_add_saved_option_count(step, '1', 'DONT ')
    srv_msg.client_does_include_with_value(step, 'requested_addr', '192.168.50.10')
    srv_msg.client_requests_option(step, '1')
    srv_msg.client_does_include_with_value(step, 'hostname', '*a$(WHITE_SPACE).8723()+')
    srv_msg.client_send_msg(step, 'REQUEST')

    misc.pass_criteria(step)
    srv_msg.send_wait_for_message(step, 'MUST', None, 'ACK')
    srv_msg.response_check_content(step, 'Response', None, 'yiaddr', '192.168.50.10')
    srv_msg.response_check_include_option(step, 'Response', None, '1')
    srv_msg.response_check_option_content(step, 'Response', '1', None, 'value', '255.255.255.0')
    srv_msg.response_check_include_option(step, 'Response', None, '12')
    srv_msg.response_check_option_content(step, 'Response', '12', None, 'value', 'a')

    misc.test_procedure(step)
    srv_msg.client_sets_value(step, 'Client', 'chaddr', '00:1F:D0:00:00:11')
    srv_msg.client_add_saved_option_count(step, '1', 'DONT ')
    srv_msg.client_sets_value(step, 'Client', 'ciaddr', '192.168.50.10')
    srv_msg.client_does_include_with_value(step, 'hostname', '*a$(WHITE_SPACE).8723()+')
    srv_msg.client_send_msg(step, 'RELEASE')

    misc.pass_criteria(step)
    srv_msg.send_dont_wait_for_message(step)

    misc.test_procedure(step)
    srv_msg.client_sets_value(step, 'Client', 'chaddr', '00:1F:D0:00:00:22')
    srv_msg.client_requests_option(step, '1')
    srv_msg.client_send_msg(step, 'DISCOVER')

    misc.pass_criteria(step)
    srv_msg.send_wait_for_message(step, 'MUST', None, 'OFFER')
    srv_msg.response_check_include_option(step, 'Response', None, '1')
    srv_msg.response_check_content(step, 'Response', None, 'yiaddr', '192.168.50.10')
    srv_msg.response_check_option_content(step, 'Response', '1', None, 'value', '255.255.255.0')


@pytest.mark.v4
@pytest.mark.ddns
@pytest.mark.notsig
@pytest.mark.forward_reverse_remove
@pytest.mark.hostname_sanitization
def test_ddns4_notsig_forw_and_rev_release_fqdn_sanitization_omit_2(step):

    misc.test_setup(step)
    srv_control.config_srv_subnet(step, '192.168.50.0/24', '192.168.50.10-192.168.50.10')
    srv_control.add_ddns_server(step, '127.0.0.1', '53001')
    srv_control.add_ddns_server_options(step, 'enable-updates', 'true')
    srv_control.add_ddns_server_options(step, 'qualifying-suffix', 'example.com')
    srv_control.add_ddns_server_options(step, 'hostname-char-set', '[^A-Za-z]')
    srv_control.add_ddns_server_options(step, 'hostname-char-replacement', '$(EMPTY)')
    srv_control.add_forward_ddns(step, 'four.example.com.', 'EMPTY_KEY', '192.168.50.252', '53')
    srv_control.add_reverse_ddns(step,
                                 '50.168.192.in-addr.arpa.',
                                 'EMPTY_KEY',
                                 '192.168.50.252',
                                 '53')
    srv_control.build_and_send_config_files(step, 'SSH', 'config-file')
    srv_control.start_srv(step, 'DHCP', 'started')

    misc.test_procedure(step)
    srv_msg.client_sets_value(step, 'Client', 'chaddr', '00:1F:D0:00:00:11')
    srv_msg.client_requests_option(step, '1')
    srv_msg.client_send_msg(step, 'DISCOVER')

    misc.pass_criteria(step)
    srv_msg.send_wait_for_message(step, 'MUST', None, 'OFFER')
    srv_msg.response_check_include_option(step, 'Response', None, '1')
    srv_msg.response_check_content(step, 'Response', None, 'yiaddr', '192.168.50.10')
    srv_msg.response_check_option_content(step, 'Response', '1', None, 'value', '255.255.255.0')

    misc.test_procedure(step)
    srv_msg.client_sets_value(step, 'Client', 'chaddr', '00:1F:D0:00:00:11')
    srv_msg.client_save_option_count(step, '1', 'server_id')
    srv_msg.client_add_saved_option_count(step, '1', 'DONT ')
    srv_msg.client_does_include_with_value(step, 'requested_addr', '192.168.50.10')
    srv_msg.client_sets_value(step,
                              'Client',
                              'FQDN_domain_name',
                              '*a$(WHITE_SPACE).8723()+com.pl.')
    srv_msg.client_sets_value(step, 'Client', 'FQDN_flags', 'S')
    srv_msg.client_does_include(step, 'Client', None, 'fqdn')
    srv_msg.client_send_msg(step, 'REQUEST')

    misc.pass_criteria(step)
    srv_msg.send_wait_for_message(step, 'MUST', None, 'ACK')
    srv_msg.response_check_content(step, 'Response', None, 'yiaddr', '192.168.50.10')
    srv_msg.response_check_include_option(step, 'Response', None, '1')
    srv_msg.response_check_option_content(step, 'Response', '1', None, 'value', '255.255.255.0')
    srv_msg.response_check_include_option(step, 'Response', None, '81')
    srv_msg.response_check_option_content(step, 'Response', '81', None, 'flags', '1.')
    srv_msg.response_check_option_content(step, 'Response', '81', None, 'fqdn', 'a.com.pl.')

    misc.test_procedure(step)
    srv_msg.client_sets_value(step, 'Client', 'chaddr', '00:1F:D0:00:00:11')
    srv_msg.client_add_saved_option_count(step, '1', 'DONT ')
    srv_msg.client_sets_value(step, 'Client', 'ciaddr', '192.168.50.10')
    srv_msg.client_sets_value(step, 'Client', 'FQDN_domain_name', '*a$(WHITE_SPACE).8723()+.')
    srv_msg.client_sets_value(step, 'Client', 'FQDN_flags', 'S')
    srv_msg.client_does_include(step, 'Client', None, 'fqdn')
    srv_msg.client_send_msg(step, 'RELEASE')

    misc.pass_criteria(step)
    srv_msg.send_dont_wait_for_message(step)

    misc.test_procedure(step)
    srv_msg.client_sets_value(step, 'Client', 'chaddr', '00:1F:D0:00:00:22')
    srv_msg.client_requests_option(step, '1')
    srv_msg.client_send_msg(step, 'DISCOVER')

    misc.pass_criteria(step)
    srv_msg.send_wait_for_message(step, 'MUST', None, 'OFFER')
    srv_msg.response_check_include_option(step, 'Response', None, '1')
    srv_msg.response_check_content(step, 'Response', None, 'yiaddr', '192.168.50.10')
    srv_msg.response_check_option_content(step, 'Response', '1', None, 'value', '255.255.255.0')


@pytest.mark.v4
@pytest.mark.ddns
@pytest.mark.notsig
@pytest.mark.forward_reverse_remove
@pytest.mark.hostname_sanitization
def test_ddns4_notsig_forw_and_rev_release_hostname_sanitization_omit_3(step):

    misc.test_setup(step)
    srv_control.config_srv_subnet(step, '192.168.50.0/24', '192.168.50.10-192.168.50.10')
    srv_control.add_ddns_server(step, '127.0.0.1', '53001')
    srv_control.add_ddns_server_options(step, 'enable-updates', 'true')
    srv_control.add_ddns_server_options(step, 'qualifying-suffix', 'example.com')
    srv_control.add_ddns_server_options(step, 'hostname-char-set', '[^A-Za-z]')
    srv_control.add_ddns_server_options(step, 'hostname-char-replacement', '$(EMPTY)')
    srv_control.add_forward_ddns(step, 'four.example.com.', 'EMPTY_KEY', '192.168.50.252', '53')
    srv_control.add_reverse_ddns(step,
                                 '50.168.192.in-addr.arpa.',
                                 'EMPTY_KEY',
                                 '192.168.50.252',
                                 '53')
    srv_control.build_and_send_config_files(step, 'SSH', 'config-file')
    srv_control.start_srv(step, 'DHCP', 'started')

    misc.test_procedure(step)
    srv_msg.client_sets_value(step, 'Client', 'chaddr', '00:1F:D0:00:00:11')
    srv_msg.client_requests_option(step, '1')
    srv_msg.client_send_msg(step, 'DISCOVER')

    misc.pass_criteria(step)
    srv_msg.send_wait_for_message(step, 'MUST', None, 'OFFER')
    srv_msg.response_check_include_option(step, 'Response', None, '1')
    srv_msg.response_check_content(step, 'Response', None, 'yiaddr', '192.168.50.10')
    srv_msg.response_check_option_content(step, 'Response', '1', None, 'value', '255.255.255.0')

    misc.test_procedure(step)
    srv_msg.client_sets_value(step, 'Client', 'chaddr', '00:1F:D0:00:00:11')
    srv_msg.client_save_option_count(step, '1', 'server_id')
    srv_msg.client_add_saved_option_count(step, '1', 'DONT ')
    srv_msg.client_does_include_with_value(step, 'requested_addr', '192.168.50.10')
    srv_msg.client_requests_option(step, '1')
    srv_msg.client_does_include_with_value(step, 'hostname', '*$(WHITE_SPACE).8723()+')
    srv_msg.client_send_msg(step, 'REQUEST')

    misc.pass_criteria(step)
    srv_msg.send_wait_for_message(step, 'MUST', None, 'ACK')
    srv_msg.response_check_content(step, 'Response', None, 'yiaddr', '192.168.50.10')
    srv_msg.response_check_include_option(step, 'Response', None, '1')
    srv_msg.response_check_option_content(step, 'Response', '1', None, 'value', '255.255.255.0')
    srv_msg.response_check_include_option(step, 'Response', 'NOT ', '12')

    misc.test_procedure(step)
    srv_msg.client_sets_value(step, 'Client', 'chaddr', '00:1F:D0:00:00:11')
    srv_msg.client_add_saved_option_count(step, '1', 'DONT ')
    srv_msg.client_sets_value(step, 'Client', 'ciaddr', '192.168.50.10')
    srv_msg.client_does_include_with_value(step, 'hostname', '*$(WHITE_SPACE).8723()+')
    srv_msg.client_send_msg(step, 'RELEASE')

    misc.pass_criteria(step)
    srv_msg.send_dont_wait_for_message(step)

    misc.test_procedure(step)
    srv_msg.client_sets_value(step, 'Client', 'chaddr', '00:1F:D0:00:00:22')
    srv_msg.client_requests_option(step, '1')
    srv_msg.client_send_msg(step, 'DISCOVER')

    misc.pass_criteria(step)
    srv_msg.send_wait_for_message(step, 'MUST', None, 'OFFER')
    srv_msg.response_check_include_option(step, 'Response', None, '1')
    srv_msg.response_check_content(step, 'Response', None, 'yiaddr', '192.168.50.10')
    srv_msg.response_check_option_content(step, 'Response', '1', None, 'value', '255.255.255.0')


@pytest.mark.v4
@pytest.mark.ddns
@pytest.mark.notsig
@pytest.mark.forward_reverse_remove
@pytest.mark.hostname_sanitization
def test_ddns4_notsig_forw_and_rev_release_hostname_sanitization_omit_4(step):

    misc.test_setup(step)
    srv_control.config_srv_subnet(step, '192.168.50.0/24', '192.168.50.10-192.168.50.10')
    srv_control.add_ddns_server(step, '127.0.0.1', '53001')
    srv_control.add_ddns_server_options(step, 'enable-updates', 'true')
    srv_control.add_ddns_server_options(step, 'qualifying-suffix', 'example.com')
    srv_control.add_ddns_server_options(step, 'hostname-char-set', '[^A-Za-z]')
    srv_control.add_ddns_server_options(step, 'hostname-char-replacement', '$(EMPTY)')
    srv_control.add_forward_ddns(step, 'four.example.com.', 'EMPTY_KEY', '192.168.50.252', '53')
    srv_control.add_reverse_ddns(step,
                                 '50.168.192.in-addr.arpa.',
                                 'EMPTY_KEY',
                                 '192.168.50.252',
                                 '53')
    srv_control.build_and_send_config_files(step, 'SSH', 'config-file')
    srv_control.start_srv(step, 'DHCP', 'started')

    misc.test_procedure(step)
    srv_msg.client_sets_value(step, 'Client', 'chaddr', '00:1F:D0:00:00:11')
    srv_msg.client_requests_option(step, '1')
    srv_msg.client_send_msg(step, 'DISCOVER')

    misc.pass_criteria(step)
    srv_msg.send_wait_for_message(step, 'MUST', None, 'OFFER')
    srv_msg.response_check_include_option(step, 'Response', None, '1')
    srv_msg.response_check_content(step, 'Response', None, 'yiaddr', '192.168.50.10')
    srv_msg.response_check_option_content(step, 'Response', '1', None, 'value', '255.255.255.0')

    misc.test_procedure(step)
    srv_msg.client_sets_value(step, 'Client', 'chaddr', '00:1F:D0:00:00:11')
    srv_msg.client_save_option_count(step, '1', 'server_id')
    srv_msg.client_add_saved_option_count(step, '1', 'DONT ')
    srv_msg.client_does_include_with_value(step, 'requested_addr', '192.168.50.10')
    srv_msg.client_sets_value(step, 'Client', 'FQDN_domain_name', '*$(WHITE_SPACE).8723()+.')
    srv_msg.client_sets_value(step, 'Client', 'FQDN_flags', 'S')
    srv_msg.client_does_include(step, 'Client', None, 'fqdn')
    srv_msg.client_send_msg(step, 'REQUEST')

    misc.pass_criteria(step)
    srv_msg.send_wait_for_message(step, 'MUST', None, 'ACK')
    srv_msg.response_check_content(step, 'Response', None, 'yiaddr', '192.168.50.10')
    srv_msg.response_check_include_option(step, 'Response', None, '1')
    srv_msg.response_check_option_content(step, 'Response', '1', None, 'value', '255.255.255.0')
    srv_msg.response_check_include_option(step, 'Response', 'NOT ', '12')
    srv_msg.response_check_include_option(step, 'Response', 'NOT ', '81')

    misc.test_procedure(step)
    srv_msg.client_sets_value(step, 'Client', 'chaddr', '00:1F:D0:00:00:11')
    srv_msg.client_add_saved_option_count(step, '1', 'DONT ')
    srv_msg.client_sets_value(step, 'Client', 'ciaddr', '192.168.50.10')
    srv_msg.client_sets_value(step, 'Client', 'FQDN_domain_name', '*$(WHITE_SPACE).8723()+.')
    srv_msg.client_sets_value(step, 'Client', 'FQDN_flags', 'S')
    srv_msg.client_does_include(step, 'Client', None, 'fqdn')
    srv_msg.client_send_msg(step, 'RELEASE')

    misc.pass_criteria(step)
    srv_msg.send_dont_wait_for_message(step)

    misc.test_procedure(step)
    srv_msg.client_sets_value(step, 'Client', 'chaddr', '00:1F:D0:00:00:22')
    srv_msg.client_requests_option(step, '1')
    srv_msg.client_send_msg(step, 'DISCOVER')

    misc.pass_criteria(step)
    srv_msg.send_wait_for_message(step, 'MUST', None, 'OFFER')
    srv_msg.response_check_include_option(step, 'Response', None, '1')
    srv_msg.response_check_content(step, 'Response', None, 'yiaddr', '192.168.50.10')
    srv_msg.response_check_option_content(step, 'Response', '1', None, 'value', '255.255.255.0')


@pytest.mark.v4
@pytest.mark.ddns
@pytest.mark.notsig
@pytest.mark.expire
def test_ddns4_notsig_expire_hostname_sanitization(step):

    misc.test_setup(step)
    srv_control.set_time(step, 'renew-timer', '3')
    srv_control.set_time(step, 'rebind-timer', '4')
    srv_control.set_time(step, 'valid-lifetime', '5')
    srv_control.config_srv_subnet(step, '192.168.50.0/24', '192.168.50.10-192.168.50.10')
    srv_control.add_ddns_server(step, '127.0.0.1', '53001')
    srv_control.add_ddns_server_options(step, 'hostname-char-set', '[^A-Za-z0-9.-]')
    srv_control.add_ddns_server_options(step, 'hostname-char-replacement', 'x')
    srv_control.add_ddns_server_options(step, 'enable-updates', 'true')
    srv_control.add_ddns_server_options(step, 'generated-prefix', 'four')
    srv_control.add_ddns_server_options(step, 'qualifying-suffix', 'example.com')
    srv_control.add_forward_ddns(step, 'four.example.com.', 'EMPTY_KEY', '192.168.50.252', '53')
    srv_control.add_reverse_ddns(step,
                                 '50.168.192.in-addr.arpa.',
                                 'EMPTY_KEY',
                                 '192.168.50.252',
                                 '53')
    srv_control.build_and_send_config_files(step, 'SSH', 'config-file')
    srv_control.start_srv(step, 'DHCP', 'started')

    srv_control.use_dns_set_number(step, '20')
    srv_control.start_srv(step, 'DNS', 'started')

    misc.test_procedure(step)
    srv_msg.dns_question_record(step, 'xaax.four.example.com', 'A', 'IN')
    srv_msg.client_send_dns_query(step)

    misc.pass_criteria(step)
    srv_msg.send_wait_for_query(step, 'MUST', None)
    srv_msg.dns_option(step, None, 'ANSWER')

    misc.test_procedure(step)
    srv_msg.dns_question_record(step, '10.50.168.192.in-addr.arpa.', 'PTR', 'IN')
    srv_msg.client_send_dns_query(step)

    misc.pass_criteria(step)
    srv_msg.send_wait_for_query(step, 'MUST', None)
    srv_msg.dns_option(step, None, 'ANSWER')

    misc.test_procedure(step)
    srv_msg.client_requests_option(step, '1')
    srv_msg.client_send_msg(step, 'DISCOVER')

    misc.pass_criteria(step)
    srv_msg.send_wait_for_message(step, 'MUST', None, 'OFFER')
    srv_msg.response_check_include_option(step, 'Response', None, '1')
    srv_msg.response_check_content(step, 'Response', None, 'yiaddr', '192.168.50.10')
    srv_msg.response_check_option_content(step, 'Response', '1', None, 'value', '255.255.255.0')

    misc.test_procedure(step)
    srv_msg.client_copy_option(step, 'server_id')
    srv_msg.client_does_include_with_value(step, 'requested_addr', '192.168.50.10')
    srv_msg.client_does_include_with_value(step, 'hostname', '^aa$(WHITE_SPACE).four.example.com')
    srv_msg.client_send_msg(step, 'REQUEST')

    misc.pass_criteria(step)
    srv_msg.send_wait_for_message(step, 'MUST', None, 'ACK')
    srv_msg.response_check_content(step, 'Response', None, 'yiaddr', '192.168.50.10')
    srv_msg.response_check_include_option(step, 'Response', None, '1')
    srv_msg.response_check_option_content(step, 'Response', '1', None, 'value', '255.255.255.0')
    srv_msg.response_check_include_option(step, 'Response', None, '12')
    srv_msg.response_check_option_content(step,
                                          'Response',
                                          '12',
                                          None,
                                          'value',
                                          'xaax.four.example.com')

    misc.test_procedure(step)
    srv_msg.dns_question_record(step, 'xaax.four.example.com', 'A', 'IN')
    srv_msg.client_send_dns_query(step)

    misc.pass_criteria(step)
    srv_msg.send_wait_for_query(step, 'MUST', None)
    srv_msg.dns_option(step, 'NOT ', 'ANSWER')
    srv_msg.dns_option_content(step, 'ANSWER', None, 'rdata', '192.168.50.10')
    srv_msg.dns_option_content(step, 'ANSWER', None, 'rrname', 'xaax.four.example.com.')

    misc.test_procedure(step)
    srv_msg.dns_question_record(step, '10.50.168.192.in-addr.arpa.', 'PTR', 'IN')
    srv_msg.client_send_dns_query(step)

    misc.pass_criteria(step)
    srv_msg.send_wait_for_query(step, 'MUST', None)
    srv_msg.dns_option(step, 'NOT ', 'ANSWER')
    srv_msg.dns_option_content(step, 'ANSWER', None, 'rdata', 'xaax.four.example.com.')
    srv_msg.dns_option_content(step, 'ANSWER', None, 'rrname', '10.50.168.192.in-addr.arpa.')

    srv_msg.forge_sleep(step, '10', 'seconds')

    misc.test_procedure(step)
    srv_msg.dns_question_record(step, 'xaax.four.example.com', 'A', 'IN')
    srv_msg.client_send_dns_query(step)

    misc.pass_criteria(step)
    srv_msg.send_wait_for_query(step, 'MUST', None)
    srv_msg.dns_option(step, None, 'ANSWER')

    misc.test_procedure(step)
    srv_msg.dns_question_record(step, '10.50.168.192.in-addr.arpa.', 'PTR', 'IN')
    srv_msg.client_send_dns_query(step)

    misc.pass_criteria(step)
    srv_msg.send_wait_for_query(step, 'MUST', None)
    srv_msg.dns_option(step, None, 'ANSWER')


@pytest.mark.v4
@pytest.mark.ddns
@pytest.mark.notsig
@pytest.mark.expire
def test_ddns4_notsig_expire_fqdn_sanitization(step):

    misc.test_setup(step)
    srv_control.set_time(step, 'renew-timer', '3')
    srv_control.set_time(step, 'rebind-timer', '4')
    srv_control.set_time(step, 'valid-lifetime', '5')
    srv_control.config_srv_subnet(step, '192.168.50.0/24', '192.168.50.10-192.168.50.10')
    srv_control.add_ddns_server(step, '127.0.0.1', '53001')
    srv_control.add_ddns_server_options(step, 'hostname-char-set', '[^A-Za-z0-9.-]')
    srv_control.add_ddns_server_options(step, 'hostname-char-replacement', 'x')
    srv_control.add_ddns_server_options(step, 'enable-updates', 'true')
    srv_control.add_ddns_server_options(step, 'generated-prefix', 'four')
    srv_control.add_ddns_server_options(step, 'qualifying-suffix', 'example.com')
    srv_control.add_forward_ddns(step, 'four.example.com.', 'EMPTY_KEY', '192.168.50.252', '53')
    srv_control.add_reverse_ddns(step,
                                 '50.168.192.in-addr.arpa.',
                                 'EMPTY_KEY',
                                 '192.168.50.252',
                                 '53')
    srv_control.build_and_send_config_files(step, 'SSH', 'config-file')
    srv_control.start_srv(step, 'DHCP', 'started')

    srv_control.use_dns_set_number(step, '20')
    srv_control.start_srv(step, 'DNS', 'started')

    misc.test_procedure(step)
    srv_msg.dns_question_record(step, 'xaax.four.example.com', 'A', 'IN')
    srv_msg.client_send_dns_query(step)

    misc.pass_criteria(step)
    srv_msg.send_wait_for_query(step, 'MUST', None)
    srv_msg.dns_option(step, None, 'ANSWER')

    misc.test_procedure(step)
    srv_msg.dns_question_record(step, '10.50.168.192.in-addr.arpa.', 'PTR', 'IN')
    srv_msg.client_send_dns_query(step)

    misc.pass_criteria(step)
    srv_msg.send_wait_for_query(step, 'MUST', None)
    srv_msg.dns_option(step, None, 'ANSWER')

    misc.test_procedure(step)
    srv_msg.client_requests_option(step, '1')
    srv_msg.client_send_msg(step, 'DISCOVER')

    misc.pass_criteria(step)
    srv_msg.send_wait_for_message(step, 'MUST', None, 'OFFER')
    srv_msg.response_check_include_option(step, 'Response', None, '1')
    srv_msg.response_check_content(step, 'Response', None, 'yiaddr', '192.168.50.10')
    srv_msg.response_check_option_content(step, 'Response', '1', None, 'value', '255.255.255.0')

    misc.test_procedure(step)
    srv_msg.client_copy_option(step, 'server_id')
    srv_msg.client_does_include_with_value(step, 'requested_addr', '192.168.50.10')
    srv_msg.client_sets_value(step,
                              'Client',
                              'FQDN_domain_name',
                              '^aa$(WHITE_SPACE).four.example.com.')
    srv_msg.client_sets_value(step, 'Client', 'FQDN_flags', 'S')
    srv_msg.client_does_include(step, 'Client', None, 'fqdn')
    srv_msg.client_send_msg(step, 'REQUEST')

    misc.pass_criteria(step)
    srv_msg.send_wait_for_message(step, 'MUST', None, 'ACK')
    srv_msg.response_check_content(step, 'Response', None, 'yiaddr', '192.168.50.10')
    srv_msg.response_check_include_option(step, 'Response', None, '1')
    srv_msg.response_check_option_content(step, 'Response', '1', None, 'value', '255.255.255.0')
    srv_msg.response_check_include_option(step, 'Response', None, '81')
    srv_msg.response_check_option_content(step, 'Response', '81', None, 'flags', '1.')
    srv_msg.response_check_option_content(step,
                                          'Response',
                                          '81',
                                          None,
                                          'fqdn',
                                          'xaax.four.example.com.')

    misc.test_procedure(step)
    srv_msg.dns_question_record(step, 'xaax.four.example.com', 'A', 'IN')
    srv_msg.client_send_dns_query(step)

    misc.pass_criteria(step)
    srv_msg.send_wait_for_query(step, 'MUST', None)
    srv_msg.dns_option(step, 'NOT ', 'ANSWER')
    srv_msg.dns_option_content(step, 'ANSWER', None, 'rdata', '192.168.50.10')
    srv_msg.dns_option_content(step, 'ANSWER', None, 'rrname', 'xaax.four.example.com.')

    misc.test_procedure(step)
    srv_msg.dns_question_record(step, '10.50.168.192.in-addr.arpa.', 'PTR', 'IN')
    srv_msg.client_send_dns_query(step)

    misc.pass_criteria(step)
    srv_msg.send_wait_for_query(step, 'MUST', None)
    srv_msg.dns_option(step, 'NOT ', 'ANSWER')
    srv_msg.dns_option_content(step, 'ANSWER', None, 'rdata', 'xaax.four.example.com.')
    srv_msg.dns_option_content(step, 'ANSWER', None, 'rrname', '10.50.168.192.in-addr.arpa.')

    srv_msg.forge_sleep(step, '10', 'seconds')

    misc.test_procedure(step)
    srv_msg.dns_question_record(step, 'xaax.four.example.com', 'A', 'IN')
    srv_msg.client_send_dns_query(step)

    misc.pass_criteria(step)
    srv_msg.send_wait_for_query(step, 'MUST', None)
    srv_msg.dns_option(step, None, 'ANSWER')

    misc.test_procedure(step)
    srv_msg.dns_question_record(step, '10.50.168.192.in-addr.arpa.', 'PTR', 'IN')
    srv_msg.client_send_dns_query(step)

    misc.pass_criteria(step)
    srv_msg.send_wait_for_query(step, 'MUST', None)
    srv_msg.dns_option(step, None, 'ANSWER')
