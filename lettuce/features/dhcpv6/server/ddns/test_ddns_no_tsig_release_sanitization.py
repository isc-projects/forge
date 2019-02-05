"""DDNS without TSIG"""

# pylint: disable=invalid-name,line-too-long

import pytest

from features import misc
from features import srv_control
from features import srv_msg


@pytest.mark.v6
@pytest.mark.ddns
@pytest.mark.kea_only
@pytest.mark.notsig
@pytest.mark.forward_reverse_remove
@pytest.mark.hostname_sanitization
def test_ddns6_notsig_forw_and_rev_release_fqdn_sanitization_replace_1(step):

    misc.test_setup(step)
    srv_control.config_srv_subnet(step, '2001:db8:1::/64', '2001:db8:1::50-2001:db8:1::50')
    srv_control.add_ddns_server(step, '127.0.0.1', '53001')
    srv_control.add_ddns_server_options(step, 'enable-updates', 'true')
    srv_control.add_ddns_server_options(step, 'generated-prefix', 'six')
    srv_control.add_ddns_server_options(step, 'qualifying-suffix', 'example.com')
    srv_control.add_ddns_server_options(step, 'hostname-char-set', '[^A-Za-z0-9.-]')
    srv_control.add_ddns_server_options(step, 'hostname-char-replacement', 'x')
    srv_control.add_forward_ddns(step, 'six.example.com.', 'EMPTY_KEY', '2001:db8:1::1000', '53')
    srv_control.add_reverse_ddns(step,
                                 '1.0.0.0.8.b.d.0.1.0.0.2.ip6.arpa.',
                                 'EMPTY_KEY',
                                 '2001:db8:1::1000',
                                 '53')
    srv_control.build_and_send_config_files(step, 'SSH', 'config-file')
    srv_control.start_srv(step, 'DHCP', 'started')

    srv_control.use_dns_set_number(step, '1')
    srv_control.start_srv(step, 'DNS', 'started')

    misc.test_procedure(step)
    srv_msg.dns_question_record(step, 'xsth6x.six.example.com', 'AAAA', 'IN')
    srv_msg.client_send_dns_query(step)

    misc.pass_criteria(step)
    srv_msg.send_wait_for_query(step, 'MUST', None)
    srv_msg.dns_option(step, None, 'ANSWER')

    misc.test_procedure(step)
    srv_msg.client_sets_value(step, 'Client', 'DUID', '00:03:00:01:ff:ff:ff:ff:ff:01')
    srv_msg.client_does_include(step, 'Client', None, 'client-id')
    srv_msg.client_does_include(step, 'Client', None, 'IA-NA')
    srv_msg.client_send_msg(step, 'SOLICIT')

    misc.pass_criteria(step)
    srv_msg.send_wait_for_message(step, 'MUST', None, 'ADVERTISE')
    srv_msg.response_check_include_option(step, 'Response', None, '1')
    srv_msg.response_check_include_option(step, 'Response', None, '2')

    misc.test_procedure(step)
    srv_msg.client_sets_value(step, 'Client', 'DUID', '00:03:00:01:ff:ff:ff:ff:ff:01')
    srv_msg.client_save_option_count(step, '1', 'IA_NA')
    srv_msg.client_save_option_count(step, '1', 'server-id')
    srv_msg.client_add_saved_option_count(step, '1', 'DONT ')
    srv_msg.client_sets_value(step,
                              'Client',
                              'FQDN_domain_name',
                              '*sth6$(WHITE_SPACE).six.example.com.')
    srv_msg.client_sets_value(step, 'Client', 'FQDN_flags', 'S')
    srv_msg.client_does_include(step, 'Client', None, 'fqdn')
    srv_msg.client_does_include(step, 'Client', None, 'client-id')
    srv_msg.client_send_msg(step, 'REQUEST')

    misc.pass_criteria(step)
    srv_msg.send_wait_for_message(step, 'MUST', None, 'REPLY')
    srv_msg.response_check_include_option(step, 'Response', None, '1')
    srv_msg.response_check_include_option(step, 'Response', None, '2')
    srv_msg.response_check_include_option(step, 'Response', None, '39')
    srv_msg.response_check_option_content(step, 'Response', '39', None, 'flags', '1.')
    srv_msg.response_check_option_content(step,
                                          'Response',
                                          '39',
                                          None,
                                          'fqdn',
                                          'xsth6x.six.example.com')

    misc.test_procedure(step)
    srv_msg.dns_question_record(step, 'xsth6x.six.example.com', 'AAAA', 'IN')
    srv_msg.client_send_dns_query(step)

    misc.pass_criteria(step)
    srv_msg.send_wait_for_query(step, 'MUST', None)
    srv_msg.dns_option(step, 'NOT ', 'ANSWER')
    srv_msg.dns_option_content(step, 'ANSWER', None, 'rdata', '2001:db8:1::50')

    misc.test_procedure(step)
    srv_msg.dns_question_record(step,
                                '0.5.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.1.0.0.0.8.b.d.0.1.0.0.2.ip6.arpa.',
                                'PTR',
                                'IN')
    srv_msg.client_send_dns_query(step)

    misc.pass_criteria(step)
    srv_msg.send_wait_for_query(step, 'MUST', None)
    srv_msg.dns_option(step, 'NOT ', 'ANSWER')
    srv_msg.dns_option_content(step, 'ANSWER', None, 'rdata', 'xsth6x.six.example.com.')
    srv_msg.dns_option_content(step,
                               'ANSWER',
                               None,
                               'rrname',
                               '0.5.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.1.0.0.0.8.b.d.0.1.0.0.2.ip6.arpa.')

    misc.test_procedure(step)
    srv_msg.client_sets_value(step, 'Client', 'DUID', '00:03:00:01:ff:ff:ff:ff:ff:01')
    srv_msg.client_add_saved_option_count(step, '1', 'DONT ')
    srv_msg.client_does_include(step, 'Client', None, 'client-id')
    srv_msg.client_sets_value(step,
                              'Client',
                              'FQDN_domain_name',
                              '*sth6$(WHITE_SPACE).six.example.com.')
    srv_msg.client_sets_value(step, 'Client', 'FQDN_flags', 'S')
    srv_msg.client_does_include(step, 'Client', None, 'fqdn')
    srv_msg.client_send_msg(step, 'RELEASE')

    misc.pass_criteria(step)
    srv_msg.send_wait_for_message(step, 'MUST', None, 'REPLY')
    srv_msg.response_check_include_option(step, 'Response', None, '1')
    srv_msg.response_check_include_option(step, 'Response', None, '2')

    misc.test_procedure(step)
    srv_msg.dns_question_record(step, 'xsth6x.six.example.com', 'AAAA', 'IN')
    srv_msg.client_send_dns_query(step)

    misc.pass_criteria(step)
    srv_msg.send_wait_for_query(step, 'MUST', None)
    srv_msg.dns_option(step, None, 'ANSWER')

    misc.test_procedure(step)
    srv_msg.dns_question_record(step,
                                '0.5.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.1.0.0.0.8.b.d.0.1.0.0.2.ip6.arpa.',
                                'PTR',
                                'IN')
    srv_msg.client_send_dns_query(step)

    misc.pass_criteria(step)
    srv_msg.send_wait_for_query(step, 'MUST', None)
    srv_msg.dns_option(step, None, 'ANSWER')


@pytest.mark.v6
@pytest.mark.ddns
@pytest.mark.kea_only
@pytest.mark.notsig
@pytest.mark.forward_reverse_remove
@pytest.mark.hostname_sanitization
def test_ddns6_notsig_forw_and_rev_release_fqdn_sanitization_replace_2(step):

    misc.test_setup(step)
    srv_control.config_srv_subnet(step, '2001:db8:1::/64', '2001:db8:1::50-2001:db8:1::50')
    srv_control.add_ddns_server(step, '127.0.0.1', '53001')
    srv_control.add_ddns_server_options(step, 'enable-updates', 'true')
    srv_control.add_ddns_server_options(step, 'generated-prefix', 'six')
    srv_control.add_ddns_server_options(step, 'qualifying-suffix', 'example.com')
    srv_control.add_ddns_server_options(step, 'hostname-char-set', '[^A-Za-z]')
    srv_control.add_ddns_server_options(step, 'hostname-char-replacement', 'x')
    srv_control.add_forward_ddns(step, 'six.example.com.', 'EMPTY_KEY', '2001:db8:1::1000', '53')
    srv_control.add_reverse_ddns(step,
                                 '1.0.0.0.8.b.d.0.1.0.0.2.ip6.arpa.',
                                 'EMPTY_KEY',
                                 '2001:db8:1::1000',
                                 '53')
    srv_control.build_and_send_config_files(step, 'SSH', 'config-file')
    srv_control.start_srv(step, 'DHCP', 'started')

    misc.test_procedure(step)
    srv_msg.client_sets_value(step, 'Client', 'DUID', '00:03:00:01:ff:ff:ff:ff:ff:01')
    srv_msg.client_does_include(step, 'Client', None, 'client-id')
    srv_msg.client_does_include(step, 'Client', None, 'IA-NA')
    srv_msg.client_send_msg(step, 'SOLICIT')

    misc.pass_criteria(step)
    srv_msg.send_wait_for_message(step, 'MUST', None, 'ADVERTISE')
    srv_msg.response_check_include_option(step, 'Response', None, '1')
    srv_msg.response_check_include_option(step, 'Response', None, '2')

    misc.test_procedure(step)
    srv_msg.client_sets_value(step, 'Client', 'DUID', '00:03:00:01:ff:ff:ff:ff:ff:01')
    srv_msg.client_save_option_count(step, '1', 'IA_NA')
    srv_msg.client_save_option_count(step, '1', 'server-id')
    srv_msg.client_add_saved_option_count(step, '1', 'DONT ')
    srv_msg.client_sets_value(step, 'Client', 'FQDN_domain_name', '*a$(WHITE_SPACE).8723()+')
    srv_msg.client_sets_value(step, 'Client', 'FQDN_flags', 'S')
    srv_msg.client_does_include(step, 'Client', None, 'fqdn')
    srv_msg.client_does_include(step, 'Client', None, 'client-id')
    srv_msg.client_send_msg(step, 'REQUEST')

    misc.pass_criteria(step)
    srv_msg.send_wait_for_message(step, 'MUST', None, 'REPLY')
    srv_msg.response_check_include_option(step, 'Response', None, '1')
    srv_msg.response_check_include_option(step, 'Response', None, '2')
    srv_msg.response_check_include_option(step, 'Response', None, '39')
    srv_msg.response_check_option_content(step, 'Response', '39', None, 'flags', '1.')
    srv_msg.response_check_option_content(step, 'Response', '39', None, 'fqdn', 'xax.xxxxxxx')

    misc.test_procedure(step)
    srv_msg.client_sets_value(step, 'Client', 'DUID', '00:03:00:01:ff:ff:ff:ff:ff:01')
    srv_msg.client_add_saved_option_count(step, '1', 'DONT ')
    srv_msg.client_does_include(step, 'Client', None, 'client-id')
    srv_msg.client_sets_value(step, 'Client', 'FQDN_domain_name', '*a$(WHITE_SPACE).8723()+')
    srv_msg.client_sets_value(step, 'Client', 'FQDN_flags', 'S')
    srv_msg.client_does_include(step, 'Client', None, 'fqdn')
    srv_msg.client_send_msg(step, 'RELEASE')

    misc.pass_criteria(step)
    srv_msg.send_wait_for_message(step, 'MUST', None, 'REPLY')
    srv_msg.response_check_include_option(step, 'Response', None, '1')
    srv_msg.response_check_include_option(step, 'Response', None, '2')


@pytest.mark.v6
@pytest.mark.ddns
@pytest.mark.kea_only
@pytest.mark.notsig
@pytest.mark.forward_reverse_remove
@pytest.mark.hostname_sanitization
def test_ddns6_notsig_forw_and_rev_release_fqdn_sanitization_omit_1(step):

    misc.test_setup(step)
    srv_control.config_srv_subnet(step, '2001:db8:1::/64', '2001:db8:1::50-2001:db8:1::50')
    srv_control.add_ddns_server(step, '127.0.0.1', '53001')
    srv_control.add_ddns_server_options(step, 'enable-updates', 'true')
    srv_control.add_ddns_server_options(step, 'generated-prefix', 'six')
    srv_control.add_ddns_server_options(step, 'qualifying-suffix', 'example.com')
    srv_control.add_ddns_server_options(step, 'hostname-char-set', '[^A-Za-z0-9.-]')
    srv_control.add_ddns_server_options(step, 'hostname-char-replacement', '$(EMPTY)')
    srv_control.add_forward_ddns(step, 'six.example.com.', 'EMPTY_KEY', '2001:db8:1::1000', '53')
    srv_control.add_reverse_ddns(step,
                                 '1.0.0.0.8.b.d.0.1.0.0.2.ip6.arpa.',
                                 'EMPTY_KEY',
                                 '2001:db8:1::1000',
                                 '53')
    srv_control.build_and_send_config_files(step, 'SSH', 'config-file')
    srv_control.start_srv(step, 'DHCP', 'started')

    srv_control.use_dns_set_number(step, '1')
    srv_control.start_srv(step, 'DNS', 'started')

    misc.test_procedure(step)
    srv_msg.dns_question_record(step, 'sth6.six.example.com', 'AAAA', 'IN')
    srv_msg.client_send_dns_query(step)

    misc.pass_criteria(step)
    srv_msg.send_wait_for_query(step, 'MUST', None)
    srv_msg.dns_option(step, None, 'ANSWER')

    misc.test_procedure(step)
    srv_msg.client_sets_value(step, 'Client', 'DUID', '00:03:00:01:ff:ff:ff:ff:ff:01')
    srv_msg.client_does_include(step, 'Client', None, 'client-id')
    srv_msg.client_does_include(step, 'Client', None, 'IA-NA')
    srv_msg.client_send_msg(step, 'SOLICIT')

    misc.pass_criteria(step)
    srv_msg.send_wait_for_message(step, 'MUST', None, 'ADVERTISE')
    srv_msg.response_check_include_option(step, 'Response', None, '1')
    srv_msg.response_check_include_option(step, 'Response', None, '2')

    misc.test_procedure(step)
    srv_msg.client_sets_value(step, 'Client', 'DUID', '00:03:00:01:ff:ff:ff:ff:ff:01')
    srv_msg.client_save_option_count(step, '1', 'IA_NA')
    srv_msg.client_save_option_count(step, '1', 'server-id')
    srv_msg.client_add_saved_option_count(step, '1', 'DONT ')
    srv_msg.client_sets_value(step,
                              'Client',
                              'FQDN_domain_name',
                              '$(WHITE_SPACE)*sth6*.si^x.exa(mple.c)om(')
    srv_msg.client_sets_value(step, 'Client', 'FQDN_flags', 'S')
    srv_msg.client_does_include(step, 'Client', None, 'fqdn')
    srv_msg.client_does_include(step, 'Client', None, 'client-id')
    srv_msg.client_send_msg(step, 'REQUEST')

    misc.pass_criteria(step)
    srv_msg.send_wait_for_message(step, 'MUST', None, 'REPLY')
    srv_msg.response_check_include_option(step, 'Response', None, '1')
    srv_msg.response_check_include_option(step, 'Response', None, '2')
    srv_msg.response_check_include_option(step, 'Response', None, '39')
    srv_msg.response_check_option_content(step, 'Response', '39', None, 'flags', '1.')
    srv_msg.response_check_option_content(step,
                                          'Response',
                                          '39',
                                          None,
                                          'fqdn',
                                          'sth6.six.example.com')

    misc.test_procedure(step)
    srv_msg.dns_question_record(step, 'sth6.six.example.com', 'AAAA', 'IN')
    srv_msg.client_send_dns_query(step)

    misc.pass_criteria(step)
    srv_msg.send_wait_for_query(step, 'MUST', None)
    srv_msg.dns_option(step, 'NOT ', 'ANSWER')
    srv_msg.dns_option_content(step, 'ANSWER', None, 'rdata', '2001:db8:1::50')

    misc.test_procedure(step)
    srv_msg.dns_question_record(step,
                                '0.5.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.1.0.0.0.8.b.d.0.1.0.0.2.ip6.arpa.',
                                'PTR',
                                'IN')
    srv_msg.client_send_dns_query(step)

    misc.pass_criteria(step)
    srv_msg.send_wait_for_query(step, 'MUST', None)
    srv_msg.dns_option(step, 'NOT ', 'ANSWER')
    srv_msg.dns_option_content(step, 'ANSWER', None, 'rdata', 'sth6.six.example.com.')
    srv_msg.dns_option_content(step,
                               'ANSWER',
                               None,
                               'rrname',
                               '0.5.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.1.0.0.0.8.b.d.0.1.0.0.2.ip6.arpa.')

    misc.test_procedure(step)
    srv_msg.client_sets_value(step, 'Client', 'DUID', '00:03:00:01:ff:ff:ff:ff:ff:01')
    srv_msg.client_add_saved_option_count(step, '1', 'DONT ')
    srv_msg.client_does_include(step, 'Client', None, 'client-id')
    srv_msg.client_send_msg(step, 'RELEASE')

    misc.pass_criteria(step)
    srv_msg.send_wait_for_message(step, 'MUST', None, 'REPLY')
    srv_msg.response_check_include_option(step, 'Response', None, '1')
    srv_msg.response_check_include_option(step, 'Response', None, '2')

    misc.test_procedure(step)
    srv_msg.dns_question_record(step, 'sth6.six.example.com', 'AAAA', 'IN')
    srv_msg.client_send_dns_query(step)

    misc.pass_criteria(step)
    srv_msg.send_wait_for_query(step, 'MUST', None)
    srv_msg.dns_option(step, None, 'ANSWER')

    misc.test_procedure(step)
    srv_msg.dns_question_record(step,
                                '0.5.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.1.0.0.0.8.b.d.0.1.0.0.2.ip6.arpa.',
                                'PTR',
                                'IN')
    srv_msg.client_send_dns_query(step)

    misc.pass_criteria(step)
    srv_msg.send_wait_for_query(step, 'MUST', None)
    srv_msg.dns_option(step, None, 'ANSWER')


@pytest.mark.v6
@pytest.mark.ddns
@pytest.mark.kea_only
@pytest.mark.notsig
@pytest.mark.forward_reverse_remove
@pytest.mark.hostname_sanitization
def test_ddns6_notsig_forw_and_rev_release_fqdn_sanitization_omit_identical_name(step):

    misc.test_setup(step)
    srv_control.config_srv_subnet(step, '2001:db8:1::/64', '2001:db8:1::50-2001:db8:1::51')
    srv_control.add_ddns_server(step, '127.0.0.1', '53001')
    srv_control.add_ddns_server_options(step, 'enable-updates', 'true')
    srv_control.add_ddns_server_options(step, 'generated-prefix', 'six')
    srv_control.add_ddns_server_options(step, 'qualifying-suffix', 'example.com')
    srv_control.add_ddns_server_options(step, 'hostname-char-set', '[^A-Za-z.-]')
    srv_control.add_ddns_server_options(step, 'hostname-char-replacement', '$(EMPTY)')
    srv_control.add_forward_ddns(step, 'six.example.com.', 'EMPTY_KEY', '2001:db8:1::1000', '53')
    srv_control.add_reverse_ddns(step,
                                 '1.0.0.0.8.b.d.0.1.0.0.2.ip6.arpa.',
                                 'EMPTY_KEY',
                                 '2001:db8:1::1000',
                                 '53')
    srv_control.build_and_send_config_files(step, 'SSH', 'config-file')
    srv_control.start_srv(step, 'DHCP', 'started')

    srv_control.use_dns_set_number(step, '1')
    srv_control.start_srv(step, 'DNS', 'started')

    misc.test_procedure(step)
    srv_msg.dns_question_record(step, 'client.six.example.com', 'AAAA', 'IN')
    srv_msg.client_send_dns_query(step)

    misc.pass_criteria(step)
    srv_msg.send_wait_for_query(step, 'MUST', None)
    srv_msg.dns_option(step, None, 'ANSWER')

    misc.test_procedure(step)
    srv_msg.dns_question_record(step, 'client1.six.example.com', 'AAAA', 'IN')
    srv_msg.client_send_dns_query(step)

    misc.pass_criteria(step)
    srv_msg.send_wait_for_query(step, 'MUST', None)
    srv_msg.dns_option(step, None, 'ANSWER')

    misc.test_procedure(step)
    srv_msg.dns_question_record(step, 'client2.six.example.com', 'AAAA', 'IN')
    srv_msg.client_send_dns_query(step)

    misc.pass_criteria(step)
    srv_msg.send_wait_for_query(step, 'MUST', None)
    srv_msg.dns_option(step, None, 'ANSWER')

    misc.test_procedure(step)
    srv_msg.client_sets_value(step, 'Client', 'DUID', '00:03:00:01:ff:ff:ff:ff:ff:01')
    srv_msg.client_does_include(step, 'Client', None, 'client-id')
    srv_msg.client_does_include(step, 'Client', None, 'IA-NA')
    srv_msg.client_send_msg(step, 'SOLICIT')

    misc.pass_criteria(step)
    srv_msg.send_wait_for_message(step, 'MUST', None, 'ADVERTISE')
    srv_msg.response_check_include_option(step, 'Response', None, '1')
    srv_msg.response_check_include_option(step, 'Response', None, '2')

    misc.test_procedure(step)
    srv_msg.client_sets_value(step, 'Client', 'DUID', '00:03:00:01:ff:ff:ff:ff:ff:01')
    srv_msg.client_save_option_count(step, '1', 'IA_NA')
    srv_msg.client_save_option_count(step, '1', 'server-id')
    srv_msg.client_add_saved_option_count(step, '1', 'DONT ')
    srv_msg.client_sets_value(step, 'Client', 'FQDN_domain_name', 'client1.six.example.com.')
    srv_msg.client_sets_value(step, 'Client', 'FQDN_flags', 'S')
    srv_msg.client_does_include(step, 'Client', None, 'fqdn')
    srv_msg.client_does_include(step, 'Client', None, 'client-id')
    srv_msg.client_send_msg(step, 'REQUEST')

    misc.pass_criteria(step)
    srv_msg.send_wait_for_message(step, 'MUST', None, 'REPLY')
    srv_msg.response_check_include_option(step, 'Response', None, '1')
    srv_msg.response_check_include_option(step, 'Response', None, '2')
    srv_msg.response_check_include_option(step, 'Response', None, '39')
    srv_msg.response_check_option_content(step, 'Response', '39', None, 'flags', '1.')
    srv_msg.response_check_option_content(step,
                                          'Response',
                                          '39',
                                          None,
                                          'fqdn',
                                          'client.six.example.com')

    misc.test_procedure(step)
    srv_msg.dns_question_record(step, 'client.six.example.com', 'AAAA', 'IN')
    srv_msg.client_send_dns_query(step)

    misc.pass_criteria(step)
    srv_msg.send_wait_for_query(step, 'MUST', None)
    srv_msg.dns_option(step, 'NOT ', 'ANSWER')
    srv_msg.dns_option_content(step, 'ANSWER', None, 'rdata', '2001:db8:1::50')

    misc.test_procedure(step)
    srv_msg.dns_question_record(step,
                                '0.5.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.1.0.0.0.8.b.d.0.1.0.0.2.ip6.arpa.',
                                'PTR',
                                'IN')
    srv_msg.client_send_dns_query(step)

    misc.pass_criteria(step)
    srv_msg.send_wait_for_query(step, 'MUST', None)
    srv_msg.dns_option(step, 'NOT ', 'ANSWER')
    srv_msg.dns_option_content(step, 'ANSWER', None, 'rdata', 'client.six.example.com.')
    srv_msg.dns_option_content(step,
                               'ANSWER',
                               None,
                               'rrname',
                               '0.5.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.1.0.0.0.8.b.d.0.1.0.0.2.ip6.arpa.')

    misc.test_procedure(step)
    srv_msg.dns_question_record(step, 'client1.six.example.com', 'AAAA', 'IN')
    srv_msg.client_send_dns_query(step)

    misc.pass_criteria(step)
    srv_msg.send_wait_for_query(step, 'MUST', None)
    srv_msg.dns_option(step, None, 'ANSWER')

    misc.test_procedure(step)
    srv_msg.client_sets_value(step, 'Client', 'DUID', '00:03:00:01:ff:ff:ff:ff:ff:11')
    srv_msg.client_does_include(step, 'Client', None, 'client-id')
    srv_msg.client_does_include(step, 'Client', None, 'IA-NA')
    srv_msg.client_send_msg(step, 'SOLICIT')

    misc.pass_criteria(step)
    srv_msg.send_wait_for_message(step, 'MUST', None, 'ADVERTISE')
    srv_msg.response_check_include_option(step, 'Response', None, '1')
    srv_msg.response_check_include_option(step, 'Response', None, '2')

    misc.test_procedure(step)
    srv_msg.client_sets_value(step, 'Client', 'DUID', '00:03:00:01:ff:ff:ff:ff:ff:11')
    srv_msg.client_save_option_count(step, '2', 'IA_NA')
    srv_msg.client_save_option_count(step, '2', 'server-id')
    srv_msg.client_add_saved_option_count(step, '2', 'DONT ')
    srv_msg.client_sets_value(step, 'Client', 'FQDN_domain_name', 'client2.six.example.com.')
    srv_msg.client_sets_value(step, 'Client', 'FQDN_flags', 'S')
    srv_msg.client_does_include(step, 'Client', None, 'fqdn')
    srv_msg.client_does_include(step, 'Client', None, 'client-id')
    srv_msg.client_send_msg(step, 'REQUEST')

    misc.pass_criteria(step)
    srv_msg.send_wait_for_message(step, 'MUST', None, 'REPLY')
    srv_msg.response_check_include_option(step, 'Response', None, '1')
    srv_msg.response_check_include_option(step, 'Response', None, '2')
    srv_msg.response_check_include_option(step, 'Response', None, '39')
    srv_msg.response_check_option_content(step, 'Response', '39', None, 'flags', '1.')
    srv_msg.response_check_option_content(step,
                                          'Response',
                                          '39',
                                          None,
                                          'fqdn',
                                          'client.six.example.com')

    misc.test_procedure(step)
    srv_msg.dns_question_record(step, 'client2.six.example.com', 'AAAA', 'IN')
    srv_msg.client_send_dns_query(step)

    misc.pass_criteria(step)
    srv_msg.send_wait_for_query(step, 'MUST', None)
    srv_msg.dns_option(step, None, 'ANSWER')

    misc.test_procedure(step)
    srv_msg.dns_question_record(step, 'client.six.example.com', 'AAAA', 'IN')
    srv_msg.client_send_dns_query(step)

    misc.pass_criteria(step)
    srv_msg.send_wait_for_query(step, 'MUST', None)
    srv_msg.dns_option(step, 'NOT ', 'ANSWER')
    srv_msg.dns_option_content(step, 'ANSWER', None, 'rdata', '2001:db8:1::50')

    misc.test_procedure(step)
    srv_msg.dns_question_record(step,
                                '0.5.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.1.0.0.0.8.b.d.0.1.0.0.2.ip6.arpa.',
                                'PTR',
                                'IN')
    srv_msg.client_send_dns_query(step)

    misc.pass_criteria(step)
    srv_msg.send_wait_for_query(step, 'MUST', None)
    srv_msg.dns_option(step, 'NOT ', 'ANSWER')
    srv_msg.dns_option_content(step, 'ANSWER', None, 'rdata', 'client.six.example.com.')
    srv_msg.dns_option_content(step,
                               'ANSWER',
                               None,
                               'rrname',
                               '0.5.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.1.0.0.0.8.b.d.0.1.0.0.2.ip6.arpa.')

    misc.test_procedure(step)
    srv_msg.client_sets_value(step, 'Client', 'DUID', '00:03:00:01:ff:ff:ff:ff:ff:01')
    srv_msg.client_add_saved_option_count(step, '1', 'DONT ')
    srv_msg.client_does_include(step, 'Client', None, 'client-id')
    srv_msg.client_send_msg(step, 'RELEASE')

    misc.pass_criteria(step)
    srv_msg.send_wait_for_message(step, 'MUST', None, 'REPLY')
    srv_msg.response_check_include_option(step, 'Response', None, '1')
    srv_msg.response_check_include_option(step, 'Response', None, '2')

    misc.test_procedure(step)
    srv_msg.dns_question_record(step, 'client.six.example.com', 'AAAA', 'IN')
    srv_msg.client_send_dns_query(step)

    misc.pass_criteria(step)
    srv_msg.send_wait_for_query(step, 'MUST', None)
    srv_msg.dns_option(step, None, 'ANSWER')

    misc.test_procedure(step)
    srv_msg.dns_question_record(step,
                                '0.5.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.1.0.0.0.8.b.d.0.1.0.0.2.ip6.arpa.',
                                'PTR',
                                'IN')
    srv_msg.client_send_dns_query(step)

    misc.pass_criteria(step)
    srv_msg.send_wait_for_query(step, 'MUST', None)
    srv_msg.dns_option(step, None, 'ANSWER')


@pytest.mark.v6
@pytest.mark.ddns
@pytest.mark.kea_only
@pytest.mark.notsig
@pytest.mark.ddns_expired
@pytest.mark.hostname_sanitization
def test_ddns6_notsig_expired_fqdn_sanitization(step):

    misc.test_setup(step)
    srv_control.set_time(step, 'renew-timer', '1')
    srv_control.set_time(step, 'rebind-timer', '2')
    srv_control.set_time(step, 'preferred-lifetime', '3')
    srv_control.set_time(step, 'valid-lifetime', '4')
    srv_control.config_srv_subnet(step, '2001:db8:1::/64', '2001:db8:1::50-2001:db8:1::50')
    srv_control.add_ddns_server(step, '127.0.0.1', '53001')
    srv_control.add_ddns_server_options(step, 'enable-updates', 'true')
    srv_control.add_ddns_server_options(step, 'generated-prefix', 'six')
    srv_control.add_ddns_server_options(step, 'qualifying-suffix', 'example.com')
    srv_control.add_ddns_server_options(step, 'hostname-char-set', '[^A-Za-z.-]')
    srv_control.add_ddns_server_options(step, 'hostname-char-replacement', '$(EMPTY)')
    srv_control.add_forward_ddns(step, 'six.example.com.', 'EMPTY_KEY', '2001:db8:1::1000', '53')
    srv_control.add_reverse_ddns(step,
                                 '1.0.0.0.8.b.d.0.1.0.0.2.ip6.arpa.',
                                 'EMPTY_KEY',
                                 '2001:db8:1::1000',
                                 '53')
    srv_control.build_and_send_config_files(step, 'SSH', 'config-file')
    srv_control.start_srv(step, 'DHCP', 'started')

    srv_control.use_dns_set_number(step, '1')
    srv_control.start_srv(step, 'DNS', 'started')

    misc.test_procedure(step)
    srv_msg.dns_question_record(step, 'sth.six.example.com', 'AAAA', 'IN')
    srv_msg.client_send_dns_query(step)

    misc.pass_criteria(step)
    srv_msg.send_wait_for_query(step, 'MUST', None)
    srv_msg.dns_option(step, None, 'ANSWER')

    misc.test_procedure(step)
    srv_msg.client_sets_value(step, 'Client', 'DUID', '00:03:00:01:ff:ff:ff:ff:ff:01')
    srv_msg.client_does_include(step, 'Client', None, 'client-id')
    srv_msg.client_does_include(step, 'Client', None, 'IA-NA')
    srv_msg.client_send_msg(step, 'SOLICIT')

    misc.pass_criteria(step)
    srv_msg.send_wait_for_message(step, 'MUST', None, 'ADVERTISE')
    srv_msg.response_check_include_option(step, 'Response', None, '1')
    srv_msg.response_check_include_option(step, 'Response', None, '2')

    misc.test_procedure(step)
    srv_msg.client_sets_value(step, 'Client', 'DUID', '00:03:00:01:ff:ff:ff:ff:ff:01')
    srv_msg.client_copy_option(step, 'IA_NA')
    srv_msg.client_copy_option(step, 'server-id')
    srv_msg.client_sets_value(step, 'Client', 'FQDN_domain_name', 'sth6.six.example.com.')
    srv_msg.client_sets_value(step, 'Client', 'FQDN_flags', 'S')
    srv_msg.client_does_include(step, 'Client', None, 'fqdn')
    srv_msg.client_does_include(step, 'Client', None, 'client-id')
    srv_msg.client_send_msg(step, 'REQUEST')

    misc.pass_criteria(step)
    srv_msg.send_wait_for_message(step, 'MUST', None, 'REPLY')
    srv_msg.response_check_include_option(step, 'Response', None, '1')
    srv_msg.response_check_include_option(step, 'Response', None, '2')
    srv_msg.response_check_include_option(step, 'Response', None, '39')
    srv_msg.response_check_option_content(step, 'Response', '39', None, 'flags', '1.')
    srv_msg.response_check_option_content(step,
                                          'Response',
                                          '39',
                                          None,
                                          'fqdn',
                                          'sth.six.example.com')

    misc.test_procedure(step)
    srv_msg.dns_question_record(step, 'sth.six.example.com', 'AAAA', 'IN')
    srv_msg.client_send_dns_query(step)

    misc.pass_criteria(step)
    srv_msg.send_wait_for_query(step, 'MUST', None)
    srv_msg.dns_option(step, 'NOT ', 'ANSWER')
    srv_msg.dns_option_content(step, 'ANSWER', None, 'rdata', '2001:db8:1::50')

    misc.test_procedure(step)
    srv_msg.dns_question_record(step,
                                '0.5.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.1.0.0.0.8.b.d.0.1.0.0.2.ip6.arpa.',
                                'PTR',
                                'IN')
    srv_msg.client_send_dns_query(step)

    misc.pass_criteria(step)
    srv_msg.send_wait_for_query(step, 'MUST', None)
    srv_msg.dns_option(step, 'NOT ', 'ANSWER')
    srv_msg.dns_option_content(step, 'ANSWER', None, 'rdata', 'sth.six.example.com.')
    srv_msg.dns_option_content(step,
                               'ANSWER',
                               None,
                               'rrname',
                               '0.5.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.1.0.0.0.8.b.d.0.1.0.0.2.ip6.arpa.')

    srv_msg.forge_sleep(step, '15', 'seconds')

    misc.test_procedure(step)
    srv_msg.dns_question_record(step, 'sth.six.example.com', 'AAAA', 'IN')
    srv_msg.client_send_dns_query(step)

    misc.pass_criteria(step)
    srv_msg.send_wait_for_query(step, 'MUST', None)
    srv_msg.dns_option(step, None, 'ANSWER')

    misc.test_procedure(step)
    srv_msg.dns_question_record(step,
                                '0.5.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.1.0.0.0.8.b.d.0.1.0.0.2.ip6.arpa.',
                                'PTR',
                                'IN')
    srv_msg.client_send_dns_query(step)

    misc.pass_criteria(step)
    srv_msg.send_wait_for_query(step, 'MUST', None)
    srv_msg.dns_option(step, None, 'ANSWER')
