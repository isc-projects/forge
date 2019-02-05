"""DDNS without TSIG"""

# pylint: disable=invalid-name,line-too-long

import pytest

from features import srv_msg
from features import misc
from features import srv_control


@pytest.mark.v4
@pytest.mark.ddns
@pytest.mark.tsig
@pytest.mark.forward_reverse_add
def test_ddns4_tsig_sha1_forw_and_rev(step):
    misc.test_setup(step)
    srv_control.config_srv_subnet(step, '192.168.50.0/24', '192.168.50.10-192.168.50.10')
    srv_control.add_ddns_server(step, '127.0.0.1', '53001')
    srv_control.add_ddns_server_options(step, 'enable-updates', 'true')
    srv_control.add_ddns_server_options(step, 'generated-prefix', 'four')
    srv_control.add_ddns_server_options(step, 'qualifying-suffix', 'example.com')
    srv_control.add_forward_ddns(step,
                                 'four.example.com.',
                                 'forge.sha1.key',
                                 '192.168.50.252',
                                 '53')
    srv_control.add_reverse_ddns(step,
                                 '50.168.192.in-addr.arpa.',
                                 'forge.sha1.key',
                                 '192.168.50.252',
                                 '53')
    srv_control.add_keys(step, 'forge.sha1.key', 'HMAC-SHA1', 'PN4xKZ/jDobCMlo4rpr70w==')
    srv_control.build_and_send_config_files(step, 'SSH', 'config-file')
    srv_control.start_srv(step, 'DHCP', 'started')

    srv_control.use_dns_set_number(step, '21')
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
    srv_msg.client_sets_value(step, 'Client', 'FQDN_domain_name', 'aa.four.example.com.')
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
@pytest.mark.tsig
@pytest.mark.forward_reverse_add
def test_ddns4_tsig_sha224_forw_and_rev(step):

    misc.test_setup(step)
    srv_control.config_srv_subnet(step, '192.168.50.0/24', '192.168.50.10-192.168.50.10')
    srv_control.add_ddns_server(step, '127.0.0.1', '53001')
    srv_control.add_ddns_server_options(step, 'enable-updates', 'true')
    srv_control.add_ddns_server_options(step, 'generated-prefix', 'four')
    srv_control.add_ddns_server_options(step, 'qualifying-suffix', 'example.com')
    srv_control.add_forward_ddns(step,
                                 'four.example.com.',
                                 'forge.sha224.key',
                                 '192.168.50.252',
                                 '53')
    srv_control.add_reverse_ddns(step,
                                 '50.168.192.in-addr.arpa.',
                                 'forge.sha224.key',
                                 '192.168.50.252',
                                 '53')
    srv_control.add_keys(step, 'forge.sha224.key', 'HMAC-SHA224', 'TxAiO5TRKkFyHSCa4erQZQ==')
    srv_control.build_and_send_config_files(step, 'SSH', 'config-file')
    srv_control.start_srv(step, 'DHCP', 'started')

    srv_control.use_dns_set_number(step, '22')
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
    srv_msg.client_sets_value(step, 'Client', 'FQDN_domain_name', 'aa.four.example.com.')
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
@pytest.mark.tsig
@pytest.mark.forward_reverse_add
def test_ddns4_tsig_sha256_forw_and_rev(step):

    misc.test_setup(step)
    srv_control.config_srv_subnet(step, '192.168.50.0/24', '192.168.50.10-192.168.50.10')
    srv_control.add_ddns_server(step, '127.0.0.1', '53001')
    srv_control.add_ddns_server_options(step, 'enable-updates', 'true')
    srv_control.add_ddns_server_options(step, 'generated-prefix', 'four')
    srv_control.add_ddns_server_options(step, 'qualifying-suffix', 'example.com')
    srv_control.add_forward_ddns(step,
                                 'four.example.com.',
                                 'forge.sha256.key',
                                 '192.168.50.252',
                                 '53')
    srv_control.add_reverse_ddns(step,
                                 '50.168.192.in-addr.arpa.',
                                 'forge.sha256.key',
                                 '192.168.50.252',
                                 '53')
    srv_control.add_keys(step, 'forge.sha256.key', 'HMAC-SHA256', '5AYMijv0rhZJyQqK/caV7g==')
    srv_control.build_and_send_config_files(step, 'SSH', 'config-file')
    srv_control.start_srv(step, 'DHCP', 'started')

    srv_control.use_dns_set_number(step, '23')
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
    srv_msg.client_sets_value(step, 'Client', 'FQDN_domain_name', 'aa.four.example.com.')
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
@pytest.mark.tsig
@pytest.mark.forward_reverse_add
def test_ddns4_tsig_sha384_forw_and_rev(step):

    misc.test_setup(step)
    srv_control.config_srv_subnet(step, '192.168.50.0/24', '192.168.50.10-192.168.50.10')
    srv_control.add_ddns_server(step, '127.0.0.1', '53001')
    srv_control.add_ddns_server_options(step, 'enable-updates', 'true')
    srv_control.add_ddns_server_options(step, 'generated-prefix', 'four')
    srv_control.add_ddns_server_options(step, 'qualifying-suffix', 'example.com')
    srv_control.add_forward_ddns(step,
                                 'four.example.com.',
                                 'forge.sha384.key',
                                 '192.168.50.252',
                                 '53')
    srv_control.add_reverse_ddns(step,
                                 '50.168.192.in-addr.arpa.',
                                 'forge.sha384.key',
                                 '192.168.50.252',
                                 '53')
    srv_control.add_keys(step, 'forge.sha384.key', 'HMAC-SHA384', '21upyvp7zcG0S2PB4+kuQQ==')
    srv_control.build_and_send_config_files(step, 'SSH', 'config-file')
    srv_control.start_srv(step, 'DHCP', 'started')

    srv_control.use_dns_set_number(step, '24')
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
    srv_msg.client_sets_value(step, 'Client', 'FQDN_domain_name', 'aa.four.example.com.')
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
@pytest.mark.tsig
@pytest.mark.forward_reverse_add
def test_ddns4_tsig_sha512_forw_and_rev(step):

    misc.test_setup(step)
    srv_control.config_srv_subnet(step, '192.168.50.0/24', '192.168.50.10-192.168.50.10')
    srv_control.add_ddns_server(step, '127.0.0.1', '53001')
    srv_control.add_ddns_server_options(step, 'enable-updates', 'true')
    srv_control.add_ddns_server_options(step, 'generated-prefix', 'four')
    srv_control.add_ddns_server_options(step, 'qualifying-suffix', 'example.com')
    srv_control.add_forward_ddns(step,
                                 'four.example.com.',
                                 'forge.sha512.key',
                                 '192.168.50.252',
                                 '53')
    srv_control.add_reverse_ddns(step,
                                 '50.168.192.in-addr.arpa.',
                                 'forge.sha512.key',
                                 '192.168.50.252',
                                 '53')
    srv_control.add_keys(step, 'forge.sha512.key', 'HMAC-SHA512', 'jBng5D6QL4f8cfLUUwE7OQ==')
    srv_control.build_and_send_config_files(step, 'SSH', 'config-file')
    srv_control.start_srv(step, 'DHCP', 'started')

    srv_control.use_dns_set_number(step, '25')
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
    srv_msg.client_sets_value(step, 'Client', 'FQDN_domain_name', 'aa.four.example.com.')
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
@pytest.mark.tsig
@pytest.mark.forward_reverse_add
def test_ddns4_tsig_md5_forw_and_rev(step):

    misc.test_setup(step)
    srv_control.config_srv_subnet(step, '192.168.50.0/24', '192.168.50.10-192.168.50.10')
    srv_control.add_ddns_server(step, '127.0.0.1', '53001')
    srv_control.add_ddns_server_options(step, 'enable-updates', 'true')
    srv_control.add_ddns_server_options(step, 'generated-prefix', 'four')
    srv_control.add_ddns_server_options(step, 'qualifying-suffix', 'example.com')
    srv_control.add_forward_ddns(step,
                                 'four.example.com.',
                                 'forge.md5.key',
                                 '192.168.50.252',
                                 '53')
    srv_control.add_reverse_ddns(step,
                                 '50.168.192.in-addr.arpa.',
                                 'forge.md5.key',
                                 '192.168.50.252',
                                 '53')
    srv_control.add_keys(step, 'forge.md5.key', 'HMAC-MD5', 'bX3Hs+fG/tThidQPuhK1mA==')
    srv_control.build_and_send_config_files(step, 'SSH', 'config-file')
    srv_control.start_srv(step, 'DHCP', 'started')

    srv_control.use_dns_set_number(step, '26')
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
    srv_msg.client_sets_value(step, 'Client', 'FQDN_domain_name', 'aa.four.example.com.')
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
@pytest.mark.tsig
@pytest.mark.forward_reverse_add
def test_ddns4_tsig_multi_key_forw_and_rev(step):

    misc.test_setup(step)
    srv_control.config_srv_subnet(step, '192.168.50.0/24', '192.168.50.10-192.168.50.10')
    srv_control.add_ddns_server(step, '127.0.0.1', '53001')
    srv_control.add_ddns_server_options(step, 'enable-updates', 'true')
    srv_control.add_ddns_server_options(step, 'generated-prefix', 'four')
    srv_control.add_ddns_server_options(step, 'qualifying-suffix', 'example.com')
    srv_control.add_forward_ddns(step,
                                 'four.example.com.',
                                 'forge.md5.key',
                                 '192.168.50.252',
                                 '53')
    srv_control.add_reverse_ddns(step,
                                 '50.168.192.in-addr.arpa.',
                                 'forge.sha512.key',
                                 '192.168.50.252',
                                 '53')
    srv_control.add_keys(step, 'forge.sha512.key', 'HMAC-SHA512', 'jBng5D6QL4f8cfLUUwE7OQ==')
    srv_control.add_keys(step, 'forge.md5.key', 'HMAC-MD5', 'bX3Hs+fG/tThidQPuhK1mA==')
    srv_control.build_and_send_config_files(step, 'SSH', 'config-file')
    srv_control.start_srv(step, 'DHCP', 'started')

    srv_control.use_dns_set_number(step, '27')
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
    srv_msg.client_sets_value(step, 'Client', 'FQDN_domain_name', 'aa.four.example.com.')
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
