"""DDNS without TSIG"""


import sys
if 'features' not in sys.path:
    sys.path.append('features')

if 'pytest' in sys.argv[0]:
    import pytest
else:
    import lettuce as pytest

import misc
import srv_control
import srv_msg


@pytest.mark.py_test
@pytest.mark.v6
@pytest.mark.ddns
@pytest.mark.tsig
@pytest.mark.forward_reverse_add
def test_ddns6_tsig_sha1_forw_and_rev(step):
    """new-ddns6.tsig-sha1-forw_and_rev"""
    misc.test_setup(step)
    srv_control.config_srv_subnet(step, '2001:db8:1::/64', '2001:db8:1::50-2001:db8:1::50')
    srv_control.add_ddns_server(step, '127.0.0.1', '53001')
    srv_control.add_ddns_server_options(step, 'ddns-update-style', 'interim')
    # DDNS server is configured with generated-prefix option set to six.
    # DDNS server is configured with qualifying-suffix option set to example.com.
    srv_control.add_forward_ddns(step,
                                 'six.example.com.',
                                 'forge.sha1.key',
                                 '2001:db8:1::1000',
                                 '53')
    srv_control.add_reverse_ddns(step,
                                 '1.0.0.0.8.b.d.0.1.0.0.2.ip6.arpa.',
                                 'forge.sha1.key',
                                 '2001:db8:1::1000',
                                 '53')
    srv_control.add_keys(step, 'forge.sha1.key', 'HMAC-SHA1', 'PN4xKZ/jDobCMlo4rpr70w==')
    srv_control.build_and_send_config_files(step, 'SSH', 'config-file')
    srv_control.start_srv(step, 'DHCP', 'started')

    srv_control.use_dns_set_number(step, '3')
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
    # Response MUST include option 39.
    # Response option 39 MUST contain flags 1. #later make it 's' 'n' and 'o'
    # Response option 39 MUST contain fqdn sth6.six.example.com.

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



@pytest.mark.py_test
@pytest.mark.v6
@pytest.mark.ddns
@pytest.mark.tsig
@pytest.mark.forward_reverse_add
def test_ddns6_tsig_sha224_forw_and_rev(step):
    """new-ddns6.tsig-sha224-forw_and_rev"""

    misc.test_setup(step)
    srv_control.config_srv_subnet(step, '2001:db8:1::/64', '2001:db8:1::50-2001:db8:1::50')
    srv_control.add_ddns_server(step, '127.0.0.1', '53001')
    srv_control.add_ddns_server_options(step, 'ddns-update-style', 'interim')
    # DDNS server is configured with generated-prefix option set to six.
    # DDNS server is configured with qualifying-suffix option set to example.com.
    srv_control.add_forward_ddns(step,
                                 'six.example.com.',
                                 'forge.sha224.key',
                                 '2001:db8:1::1000',
                                 '53')
    srv_control.add_reverse_ddns(step,
                                 '1.0.0.0.8.b.d.0.1.0.0.2.ip6.arpa.',
                                 'forge.sha224.key',
                                 '2001:db8:1::1000',
                                 '53')
    srv_control.add_keys(step, 'forge.sha224.key', 'HMAC-SHA224', 'TxAiO5TRKkFyHSCa4erQZQ==')
    srv_control.build_and_send_config_files(step, 'SSH', 'config-file')
    srv_control.start_srv(step, 'DHCP', 'started')

    srv_control.use_dns_set_number(step, '4')
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
    # Response MUST include option 39.
    # Response option 39 MUST contain flags 1. #later make it 's' 'n' and 'o'
    # Response option 39 MUST contain fqdn sth6.six.example.com.

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



@pytest.mark.py_test
@pytest.mark.v6
@pytest.mark.ddns
@pytest.mark.tsig
@pytest.mark.forward_reverse_add
def test_ddns6_tsig_sha256_forw_and_rev(step):
    """new-ddns6.tsig-sha256-forw_and_rev"""

    misc.test_setup(step)
    srv_control.config_srv_subnet(step, '2001:db8:1::/64', '2001:db8:1::50-2001:db8:1::50')
    srv_control.add_ddns_server(step, '127.0.0.1', '53001')
    srv_control.add_ddns_server_options(step, 'ddns-update-style', 'interim')
    # DDNS server is configured with generated-prefix option set to six.
    # DDNS server is configured with qualifying-suffix option set to example.com.
    srv_control.add_forward_ddns(step,
                                 'six.example.com.',
                                 'forge.sha256.key',
                                 '2001:db8:1::1000',
                                 '53')
    srv_control.add_reverse_ddns(step,
                                 '1.0.0.0.8.b.d.0.1.0.0.2.ip6.arpa.',
                                 'forge.sha256.key',
                                 '2001:db8:1::1000',
                                 '53')
    srv_control.add_keys(step, 'forge.sha256.key', 'HMAC-SHA256', '5AYMijv0rhZJyQqK/caV7g==')
    srv_control.build_and_send_config_files(step, 'SSH', 'config-file')
    srv_control.start_srv(step, 'DHCP', 'started')

    srv_control.use_dns_set_number(step, '5')
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
    # Response MUST include option 39.
    # Response option 39 MUST contain flags 1. #later make it 's' 'n' and 'o'
    # Response option 39 MUST contain fqdn sth6.six.example.com.

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



@pytest.mark.py_test
@pytest.mark.v6
@pytest.mark.ddns
@pytest.mark.tsig
@pytest.mark.forward_reverse_add
def test_ddns6_tsig_sha384_forw_and_rev(step):
    """new-ddns6.tsig-sha384-forw_and_rev"""

    misc.test_setup(step)
    srv_control.config_srv_subnet(step, '2001:db8:1::/64', '2001:db8:1::50-2001:db8:1::50')
    srv_control.add_ddns_server(step, '127.0.0.1', '53001')
    srv_control.add_ddns_server_options(step, 'ddns-update-style', 'interim')
    # DDNS server is configured with generated-prefix option set to six.
    # DDNS server is configured with qualifying-suffix option set to example.com.
    srv_control.add_forward_ddns(step,
                                 'six.example.com.',
                                 'forge.sha384.key',
                                 '2001:db8:1::1000',
                                 '53')
    srv_control.add_reverse_ddns(step,
                                 '1.0.0.0.8.b.d.0.1.0.0.2.ip6.arpa.',
                                 'forge.sha384.key',
                                 '2001:db8:1::1000',
                                 '53')
    srv_control.add_keys(step, 'forge.sha384.key', 'HMAC-SHA384', '21upyvp7zcG0S2PB4+kuQQ==')
    srv_control.build_and_send_config_files(step, 'SSH', 'config-file')
    srv_control.start_srv(step, 'DHCP', 'started')

    srv_control.use_dns_set_number(step, '6')
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
    # Response MUST include option 39.
    # Response option 39 MUST contain flags 1. #later make it 's' 'n' and 'o'
    # Response option 39 MUST contain fqdn sth6.six.example.com.

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



@pytest.mark.py_test
@pytest.mark.v6
@pytest.mark.ddns
@pytest.mark.tsig
@pytest.mark.forward_reverse_add
def test_ddns6_tsig_sha512_forw_and_rev(step):
    """new-ddns6.tsig-sha512-forw_and_rev"""

    misc.test_setup(step)
    srv_control.config_srv_subnet(step, '2001:db8:1::/64', '2001:db8:1::50-2001:db8:1::50')
    srv_control.add_ddns_server(step, '127.0.0.1', '53001')
    srv_control.add_ddns_server_options(step, 'ddns-update-style', 'interim')
    # DDNS server is configured with generated-prefix option set to six.
    # DDNS server is configured with qualifying-suffix option set to example.com.
    srv_control.add_forward_ddns(step,
                                 'six.example.com.',
                                 'forge.sha512.key',
                                 '2001:db8:1::1000',
                                 '53')
    srv_control.add_reverse_ddns(step,
                                 '1.0.0.0.8.b.d.0.1.0.0.2.ip6.arpa.',
                                 'forge.sha512.key',
                                 '2001:db8:1::1000',
                                 '53')
    srv_control.add_keys(step, 'forge.sha512.key', 'HMAC-SHA512', 'jBng5D6QL4f8cfLUUwE7OQ==')
    srv_control.build_and_send_config_files(step, 'SSH', 'config-file')
    srv_control.start_srv(step, 'DHCP', 'started')

    srv_control.use_dns_set_number(step, '7')
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
    # Response MUST include option 39.
    # Response option 39 MUST contain flags 1. #later make it 's' 'n' and 'o'
    # Response option 39 MUST contain fqdn sth6.six.example.com.

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



@pytest.mark.py_test
@pytest.mark.v6
@pytest.mark.ddns
@pytest.mark.tsig
@pytest.mark.forward_reverse_add
def test_ddns6_tsig_md5_forw_and_rev(step):
    """new-ddns6.tsig-md5-forw_and_rev"""

    misc.test_setup(step)
    srv_control.config_srv_subnet(step, '2001:db8:1::/64', '2001:db8:1::50-2001:db8:1::50')
    srv_control.add_ddns_server(step, '127.0.0.1', '53001')
    srv_control.add_ddns_server_options(step, 'ddns-update-style', 'interim')
    # DDNS server is configured with generated-prefix option set to six.
    # DDNS server is configured with qualifying-suffix option set to example.com.
    srv_control.add_forward_ddns(step,
                                 'six.example.com.',
                                 'forge.md5.key',
                                 '2001:db8:1::1000',
                                 '53')
    srv_control.add_reverse_ddns(step,
                                 '1.0.0.0.8.b.d.0.1.0.0.2.ip6.arpa.',
                                 'forge.md5.key',
                                 '2001:db8:1::1000',
                                 '53')
    srv_control.add_keys(step, 'forge.md5.key', 'HMAC-MD5', 'bX3Hs+fG/tThidQPuhK1mA==')
    srv_control.build_and_send_config_files(step, 'SSH', 'config-file')
    srv_control.start_srv(step, 'DHCP', 'started')

    srv_control.use_dns_set_number(step, '8')
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
    # Response MUST include option 39.
    # Response option 39 MUST contain flags 1. #later make it 's' 'n' and 'o'
    # Response option 39 MUST contain fqdn sth6.six.example.com.

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



@pytest.mark.py_test
@pytest.mark.v6
@pytest.mark.ddns
@pytest.mark.tsig
@pytest.mark.forward_reverse_add
def test_ddns6_tsig_multi_key_forw_and_rev(step):
    """new-ddns6.tsig-multi-key-forw_and_rev"""

    misc.test_setup(step)
    srv_control.config_srv_subnet(step, '2001:db8:1::/64', '2001:db8:1::50-2001:db8:1::50')
    srv_control.add_ddns_server(step, '127.0.0.1', '53001')
    srv_control.add_ddns_server_options(step, 'ddns-update-style', 'interim')
    # DDNS server is configured with generated-prefix option set to six.
    # DDNS server is configured with qualifying-suffix option set to example.com.
    srv_control.add_forward_ddns(step,
                                 'six.example.com.',
                                 'forge.md5.key',
                                 '2001:db8:1::1000',
                                 '53')
    srv_control.add_reverse_ddns(step,
                                 '1.0.0.0.8.b.d.0.1.0.0.2.ip6.arpa.',
                                 'forge.sha512.key',
                                 '2001:db8:1::1000',
                                 '53')
    srv_control.add_keys(step, 'forge.sha512.key', 'HMAC-SHA512', 'jBng5D6QL4f8cfLUUwE7OQ==')
    srv_control.add_keys(step, 'forge.md5.key', 'HMAC-MD5', 'bX3Hs+fG/tThidQPuhK1mA==')
    srv_control.build_and_send_config_files(step, 'SSH', 'config-file')
    srv_control.start_srv(step, 'DHCP', 'started')

    srv_control.use_dns_set_number(step, '9')
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
    # Response MUST include option 39.
    # Response option 39 MUST contain flags 1. #later make it 's' 'n' and 'o'
    # Response option 39 MUST contain fqdn sth6.six.example.com.

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


