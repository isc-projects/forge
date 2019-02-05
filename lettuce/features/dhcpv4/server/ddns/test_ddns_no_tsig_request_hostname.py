"""DDNS without TSIG"""

# pylint: disable=invalid-name,line-too-long

import pytest

from features import misc
from features import srv_msg
from features import srv_control


@pytest.mark.v4
@pytest.mark.ddns
@pytest.mark.notsig
@pytest.mark.forward_reverse_add
def test_ddns4_notsig_forw_and_rev_add_success_hostname(step):

    misc.test_setup(step)
    srv_control.config_srv_subnet(step, '192.168.50.0/24', '192.168.50.10-192.168.50.10')
    srv_control.add_ddns_server(step, '127.0.0.1', '53001')
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
    srv_msg.client_copy_option(step, 'server_id')
    srv_msg.client_does_include_with_value(step, 'requested_addr', '192.168.50.10')
    srv_msg.client_requests_option(step, '1')
    srv_msg.client_does_include_with_value(step, 'hostname', 'aa.four.example.com')
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
                                          'aa.four.example.com')

    misc.test_procedure(step)
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


@pytest.mark.v4
@pytest.mark.ddns
@pytest.mark.notsig
@pytest.mark.forward_reverse_add
def test_ddns4_notsig_forw_and_rev_add_fail_hostname(step):

    misc.test_setup(step)
    srv_control.config_srv_subnet(step, '192.168.50.0/24', '192.168.50.10-192.168.50.10')
    srv_control.add_ddns_server(step, '127.0.0.1', '53001')
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
    srv_msg.client_copy_option(step, 'server_id')
    srv_msg.client_does_include_with_value(step, 'requested_addr', '192.168.50.10')
    srv_msg.client_requests_option(step, '1')
    srv_msg.client_does_include_with_value(step, 'hostname', 'aa.four.exae.com')
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
                                          'aa.four.exae.com')

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
@pytest.mark.forward_reverse_add
def test_ddns4_notsig_forw_and_rev_notenabled_hostname(step):

    misc.test_setup(step)
    srv_control.config_srv_subnet(step, '192.168.50.0/24', '192.168.50.10-192.168.50.10')
    srv_control.add_ddns_server(step, '127.0.0.1', '53001')
    srv_control.add_ddns_server_options(step, 'enable-updates', 'false')
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
    srv_msg.client_copy_option(step, 'server_id')
    srv_msg.client_does_include_with_value(step, 'requested_addr', '192.168.50.10')
    srv_msg.client_requests_option(step, '1')
    srv_msg.client_does_include_with_value(step, 'hostname', 'aa.four.example.com')
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
                                          'aa.four.example.com')

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
@pytest.mark.forward_update
def test_ddns4_notsig_forw_and_rev_update_success_hostname(step):

    misc.test_setup(step)
    srv_control.config_srv_subnet(step, '192.168.50.0/24', '192.168.50.10-192.168.50.10')
    srv_control.add_ddns_server(step, '127.0.0.1', '53001')
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
    srv_msg.client_copy_option(step, 'server_id')
    srv_msg.client_does_include_with_value(step, 'requested_addr', '192.168.50.10')
    srv_msg.client_requests_option(step, '1')
    srv_msg.client_does_include_with_value(step, 'hostname', 'aa.four.example.com')
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
                                          'aa.four.example.com')

    misc.test_procedure(step)
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

    misc.test_setup(step)
    srv_control.start_srv(step, 'DHCP', 'stopped')
    srv_control.clear_leases(step, 'leases')

    misc.test_setup(step)
    srv_control.config_srv_subnet(step, '192.168.50.0/24', '192.168.50.11-192.168.50.11')
    srv_control.add_ddns_server(step, '127.0.0.1', '53001')
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

    misc.test_procedure(step)
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
    srv_msg.client_requests_option(step, '1')
    srv_msg.client_send_msg(step, 'DISCOVER')

    misc.pass_criteria(step)
    srv_msg.send_wait_for_message(step, 'MUST', None, 'OFFER')
    srv_msg.response_check_include_option(step, 'Response', None, '1')
    srv_msg.response_check_content(step, 'Response', None, 'yiaddr', '192.168.50.11')
    srv_msg.response_check_option_content(step, 'Response', '1', None, 'value', '255.255.255.0')

    misc.test_procedure(step)
    srv_msg.client_copy_option(step, 'server_id')
    srv_msg.client_does_include_with_value(step, 'requested_addr', '192.168.50.11')
    srv_msg.client_requests_option(step, '1')
    srv_msg.client_does_include_with_value(step, 'hostname', 'aa.four.example.com')
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
                                          'aa.four.example.com')

    misc.test_procedure(step)
    srv_msg.dns_question_record(step, 'aa.four.example.com', 'A', 'IN')
    srv_msg.client_send_dns_query(step)

    misc.pass_criteria(step)
    srv_msg.send_wait_for_query(step, 'MUST', None)
    srv_msg.dns_option(step, 'NOT ', 'ANSWER')
    srv_msg.dns_option_content(step, 'ANSWER', None, 'rdata', '192.168.50.11')
    srv_msg.dns_option_content(step, 'ANSWER', None, 'rrname', 'aa.four.example.com.')

    misc.test_procedure(step)
    srv_msg.dns_question_record(step, '11.50.168.192.in-addr.arpa.', 'PTR', 'IN')
    srv_msg.client_send_dns_query(step)

    misc.pass_criteria(step)
    srv_msg.send_wait_for_query(step, 'MUST', None)
    srv_msg.dns_option(step, 'NOT ', 'ANSWER')
    srv_msg.dns_option_content(step, 'ANSWER', None, 'rdata', 'aa.four.example.com.')
    srv_msg.dns_option_content(step, 'ANSWER', None, 'rrname', '11.50.168.192.in-addr.arpa.')


@pytest.mark.v4
@pytest.mark.ddns
@pytest.mark.notsig
@pytest.mark.forward_reverse_add
def test_ddns4_notsig_forw_and_rev_two_dhci_hostname(step):

    misc.test_setup(step)
    srv_control.config_srv_subnet(step, '192.168.50.0/24', '192.168.50.10-192.168.50.11')
    srv_control.add_ddns_server(step, '127.0.0.1', '53001')
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
    srv_msg.client_sets_value(step, 'Client', 'chaddr', '00:00:00:00:00:11')
    srv_msg.client_send_msg(step, 'DISCOVER')

    misc.pass_criteria(step)
    srv_msg.send_wait_for_message(step, 'MUST', None, 'OFFER')
    srv_msg.response_check_include_option(step, 'Response', None, '1')
    srv_msg.response_check_content(step, 'Response', None, 'yiaddr', '192.168.50.10')
    srv_msg.response_check_option_content(step, 'Response', '1', None, 'value', '255.255.255.0')

    misc.test_procedure(step)
    srv_msg.client_sets_value(step, 'Client', 'chaddr', '00:00:00:00:00:11')
    srv_msg.client_copy_option(step, 'server_id')
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
                                          'client1.four.example.com')

    misc.test_procedure(step)
    srv_msg.dns_question_record(step, 'client1.four.example.com', 'A', 'IN')
    srv_msg.client_send_dns_query(step)

    misc.pass_criteria(step)
    srv_msg.send_wait_for_query(step, 'MUST', None)
    srv_msg.dns_option(step, 'NOT ', 'ANSWER')
    srv_msg.dns_option_content(step, 'ANSWER', None, 'rdata', '192.168.50.10')
    srv_msg.dns_option_content(step, 'ANSWER', None, 'rrname', 'client1.four.example.com.')

    #  Client 2 add
    misc.test_procedure(step)
    srv_msg.client_sets_value(step, 'Client', 'chaddr', '00:00:00:00:00:12')
    srv_msg.client_send_msg(step, 'DISCOVER')

    misc.pass_criteria(step)
    srv_msg.send_wait_for_message(step, 'MUST', None, 'OFFER')
    srv_msg.response_check_include_option(step, 'Response', None, '1')
    srv_msg.response_check_content(step, 'Response', None, 'yiaddr', '192.168.50.11')
    srv_msg.response_check_option_content(step, 'Response', '1', None, 'value', '255.255.255.0')

    misc.test_procedure(step)
    srv_msg.client_sets_value(step, 'Client', 'chaddr', '00:00:00:00:00:12')
    srv_msg.client_copy_option(step, 'server_id')
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
                                          'client2.four.example.com')

    misc.test_procedure(step)
    srv_msg.dns_question_record(step, 'client2.four.example.com', 'A', 'IN')
    srv_msg.client_send_dns_query(step)

    misc.pass_criteria(step)
    srv_msg.send_wait_for_query(step, 'MUST', None)
    srv_msg.dns_option(step, 'NOT ', 'ANSWER')
    srv_msg.dns_option_content(step, 'ANSWER', None, 'rdata', '192.168.50.11')
    srv_msg.dns_option_content(step, 'ANSWER', None, 'rrname', 'client2.four.example.com.')


@pytest.mark.v4
@pytest.mark.ddns
@pytest.mark.notsig
@pytest.mark.forward_reverse_add
def test_ddns4_notsig_forw_and_rev_dhci_conflicts_hostname(step):

    misc.test_setup(step)
    srv_control.config_srv_subnet(step, '192.168.50.0/24', '192.168.50.10-192.168.50.11')
    srv_control.add_ddns_server(step, '127.0.0.1', '53001')
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
    srv_msg.dns_question_record(step, 'client1.four.example.com', 'A', 'IN')
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
    srv_msg.dns_question_record(step, 'client2.four.example.com', 'A', 'IN')
    srv_msg.client_send_dns_query(step)

    misc.pass_criteria(step)
    srv_msg.send_wait_for_query(step, 'MUST', None)
    srv_msg.dns_option(step, None, 'ANSWER')

    misc.test_procedure(step)
    srv_msg.dns_question_record(step, '11.50.168.192.in-addr.arpa.', 'PTR', 'IN')
    srv_msg.client_send_dns_query(step)

    misc.pass_criteria(step)
    srv_msg.send_wait_for_query(step, 'MUST', None)
    srv_msg.dns_option(step, None, 'ANSWER')

    misc.test_procedure(step)
    srv_msg.client_sets_value(step, 'Client', 'chaddr', '00:00:00:00:00:11')
    srv_msg.client_send_msg(step, 'DISCOVER')

    misc.pass_criteria(step)
    srv_msg.send_wait_for_message(step, 'MUST', None, 'OFFER')
    srv_msg.response_check_include_option(step, 'Response', None, '1')
    srv_msg.response_check_content(step, 'Response', None, 'yiaddr', '192.168.50.10')
    srv_msg.response_check_option_content(step, 'Response', '1', None, 'value', '255.255.255.0')

    misc.test_procedure(step)
    srv_msg.client_sets_value(step, 'Client', 'chaddr', '00:00:00:00:00:11')
    srv_msg.client_copy_option(step, 'server_id')
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
                                          'client1.four.example.com')

    misc.test_procedure(step)
    srv_msg.dns_question_record(step, 'client1.four.example.com', 'A', 'IN')
    srv_msg.client_send_dns_query(step)

    misc.pass_criteria(step)
    srv_msg.send_wait_for_query(step, 'MUST', None)
    srv_msg.dns_option(step, 'NOT ', 'ANSWER')
    srv_msg.dns_option_content(step, 'ANSWER', None, 'rdata', '192.168.50.10')
    srv_msg.dns_option_content(step, 'ANSWER', None, 'rrname', 'client1.four.example.com.')

    misc.test_procedure(step)
    srv_msg.dns_question_record(step, '10.50.168.192.in-addr.arpa.', 'PTR', 'IN')
    srv_msg.client_send_dns_query(step)

    misc.pass_criteria(step)
    srv_msg.send_wait_for_query(step, 'MUST', None)
    srv_msg.dns_option(step, 'NOT ', 'ANSWER')
    srv_msg.dns_option_content(step, 'ANSWER', None, 'rdata', 'client1.four.example.com.')
    srv_msg.dns_option_content(step, 'ANSWER', None, 'rrname', '10.50.168.192.in-addr.arpa.')

    #  Client 2 add
    misc.test_procedure(step)
    srv_msg.client_sets_value(step, 'Client', 'chaddr', '00:00:00:00:00:12')
    srv_msg.client_send_msg(step, 'DISCOVER')

    misc.pass_criteria(step)
    srv_msg.send_wait_for_message(step, 'MUST', None, 'OFFER')
    srv_msg.response_check_include_option(step, 'Response', None, '1')
    srv_msg.response_check_content(step, 'Response', None, 'yiaddr', '192.168.50.11')
    srv_msg.response_check_option_content(step, 'Response', '1', None, 'value', '255.255.255.0')

    misc.test_procedure(step)
    srv_msg.client_sets_value(step, 'Client', 'chaddr', '00:00:00:00:00:12')
    srv_msg.client_copy_option(step, 'server_id')
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
                                          'client2.four.example.com')

    misc.test_procedure(step)
    srv_msg.dns_question_record(step, 'client2.four.example.com', 'A', 'IN')
    srv_msg.client_send_dns_query(step)

    misc.pass_criteria(step)
    srv_msg.send_wait_for_query(step, 'MUST', None)
    srv_msg.dns_option(step, 'NOT ', 'ANSWER')
    srv_msg.dns_option_content(step, 'ANSWER', None, 'rdata', '192.168.50.11')
    srv_msg.dns_option_content(step, 'ANSWER', None, 'rrname', 'client2.four.example.com.')

    misc.test_procedure(step)
    srv_msg.dns_question_record(step, '11.50.168.192.in-addr.arpa.', 'PTR', 'IN')
    srv_msg.client_send_dns_query(step)

    misc.pass_criteria(step)
    srv_msg.send_wait_for_query(step, 'MUST', None)
    srv_msg.dns_option(step, 'NOT ', 'ANSWER')
    srv_msg.dns_option_content(step, 'ANSWER', None, 'rdata', 'client2.four.example.com.')
    srv_msg.dns_option_content(step, 'ANSWER', None, 'rrname', '11.50.168.192.in-addr.arpa.')

    #  Client 2 try to update client's 1 domain
    misc.test_procedure(step)
    srv_msg.client_sets_value(step, 'Client', 'chaddr', '00:00:00:00:00:12')
    srv_msg.client_send_msg(step, 'DISCOVER')

    misc.pass_criteria(step)
    srv_msg.send_wait_for_message(step, 'MUST', None, 'OFFER')
    srv_msg.response_check_include_option(step, 'Response', None, '1')
    srv_msg.response_check_content(step, 'Response', None, 'yiaddr', '192.168.50.11')
    srv_msg.response_check_option_content(step, 'Response', '1', None, 'value', '255.255.255.0')

    misc.test_procedure(step)
    srv_msg.client_sets_value(step, 'Client', 'chaddr', '00:00:00:00:00:12')
    srv_msg.client_copy_option(step, 'server_id')
    srv_msg.client_does_include_with_value(step, 'requested_addr', '192.168.50.11')
    srv_msg.client_does_include_with_value(step, 'hostname', 'client1.four.example.com')
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
                                          'client1.four.example.com')

    #  address and domain name should not be changed!
    misc.test_procedure(step)
    srv_msg.dns_question_record(step, 'client1.four.example.com', 'A', 'IN')
    srv_msg.client_send_dns_query(step)

    misc.pass_criteria(step)
    srv_msg.send_wait_for_query(step, 'MUST', None)
    srv_msg.dns_option(step, 'NOT ', 'ANSWER')
    srv_msg.dns_option_content(step, 'ANSWER', None, 'rdata', '192.168.50.10')
    srv_msg.dns_option_content(step, 'ANSWER', None, 'rrname', 'client1.four.example.com.')

    misc.test_procedure(step)
    srv_msg.dns_question_record(step, '10.50.168.192.in-addr.arpa.', 'PTR', 'IN')
    srv_msg.client_send_dns_query(step)

    misc.pass_criteria(step)
    srv_msg.send_wait_for_query(step, 'MUST', None)
    srv_msg.dns_option(step, 'NOT ', 'ANSWER')
    srv_msg.dns_option_content(step, 'ANSWER', None, 'rdata', 'client1.four.example.com.')
    srv_msg.dns_option_content(step, 'ANSWER', None, 'rrname', '10.50.168.192.in-addr.arpa.')

    misc.test_procedure(step)
    srv_msg.dns_question_record(step, 'client2.four.example.com', 'A', 'IN')
    srv_msg.client_send_dns_query(step)

    misc.pass_criteria(step)
    srv_msg.send_wait_for_query(step, 'MUST', None)
    srv_msg.dns_option(step, None, 'ANSWER')

    misc.test_procedure(step)
    srv_msg.dns_question_record(step, '11.50.168.192.in-addr.arpa.', 'PTR', 'IN')
    srv_msg.client_send_dns_query(step)

    misc.pass_criteria(step)
    srv_msg.send_wait_for_query(step, 'MUST', None)
    srv_msg.dns_option(step, None, 'ANSWER')
