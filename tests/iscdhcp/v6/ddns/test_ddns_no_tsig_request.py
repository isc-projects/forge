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
@pytest.mark.notsig
@pytest.mark.forward_reverse_add
def test_ddns6_notsig_forw_and_rev_add_success_Sflag(step):
    """new-ddns6.notsig-forw_and_rev-add-success-Sflag"""

    misc.test_setup(step)
    srv_control.config_srv_subnet(step, '2001:db8:1::/64', '2001:db8:1::50-2001:db8:1::50')
    srv_control.add_ddns_server(step, '127.0.0.1', '53001')
    srv_control.add_ddns_server_options(step, 'ddns-update-style', 'interim')
    # DDNS server is configured with generated-prefix option set to six.
    # DDNS server is configured with qualifying-suffix option set to example.com.
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
@pytest.mark.notsig
@pytest.mark.forward_reverse_add
def test_ddns6_notsig_forw_and_rev_add_fail_Sflag(step):
    """new-ddns6.notsig-forw_and_rev-add-fail-Sflag"""

    misc.test_setup(step)
    srv_control.config_srv_subnet(step, '2001:db8:1::/64', '2001:db8:1::50-2001:db8:1::50')
    srv_control.add_ddns_server(step, '127.0.0.1', '53001')
    srv_control.add_ddns_server_options(step, 'ddns-update-style', 'interim')
    # DDNS server is configured with generated-prefix option set to six.
    # DDNS server is configured with qualifying-suffix option set to example.com.
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
    srv_msg.dns_question_record(step,
                                '0.5.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.1.0.0.0.8.b.d.0.1.0.0.2.ip6.arpa.',
                                'PTR',
                                'IN')
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
    # # Update for different zone
    srv_msg.client_sets_value(step, 'Client', 'FQDN_domain_name', 'sth6.six.com.')
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
    # Response option 39 MUST contain fqdn sth6.six.com.

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



@pytest.mark.py_test
@pytest.mark.v6
@pytest.mark.ddns
@pytest.mark.notsig
@pytest.mark.forward_reverse_add
def test_ddns6_notsig_forw_and_rev_notenabled_Sflag(step):
    """new-ddns6.notsig-forw_and_rev-notenabled-Sflag"""

    misc.test_setup(step)
    srv_control.config_srv_subnet(step, '2001:db8:1::/64', '2001:db8:1::50-2001:db8:1::50')
    srv_control.add_ddns_server(step, '127.0.0.1', '53001')
    # DDNS server is configured with ddns-update-style option set to off.
    # DDNS server is configured with generated-prefix option set to six.
    # DDNS server is configured with qualifying-suffix option set to example.com.
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
    srv_msg.dns_question_record(step,
                                '0.5.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.1.0.0.0.8.b.d.0.1.0.0.2.ip6.arpa.',
                                'PTR',
                                'IN')
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
    # Response option 39 MUST contain flags 6. #later make it 's' 'n' and 'o' 6 - NO
    # Response option 39 MUST contain fqdn sth6.six.example.com.

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



@pytest.mark.py_test
@pytest.mark.v6
@pytest.mark.ddns
@pytest.mark.notsig
@pytest.mark.forward_update
def test_ddns6_notsig_forw_and_rev_update_success_Sflag(step):
    """new-ddns6.notsig-forw_and_rev-update-success-Sflag"""

    misc.test_setup(step)
    srv_control.config_srv_subnet(step, '2001:db8:1::/64', '2001:db8:1::50-2001:db8:1::50')
    srv_control.add_ddns_server(step, '127.0.0.1', '53001')
    srv_control.add_ddns_server_options(step, 'ddns-update-style', 'interim')
    # DDNS server is configured with generated-prefix option set to six.
    # DDNS server is configured with qualifying-suffix option set to example.com.
    srv_control.add_forward_ddns(step, 'six.example.com.', 'EMPTY_KEY', '2001:db8:1::1000', '53')
    srv_control.add_reverse_ddns(step,
                                 '1.0.0.0.8.b.d.0.1.0.0.2.ip6.arpa.',
                                 'EMPTY_KEY',
                                 '2001:db8:1::1000',
                                 '53')
    srv_control.build_and_send_config_files(step, 'SSH', 'config-file')
    srv_control.start_srv(step, 'DHCP', 'started')

    srv_control.use_dns_set_number(step, '2')
    srv_control.start_srv(step, 'DNS', 'started')

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

    misc.test_setup(step)
    srv_control.start_srv(step, 'DHCP', 'stopped')
    srv_control.clear_leases(step, 'leases')

    misc.test_setup(step)
    srv_control.config_srv_subnet(step, '2001:db8:1::/64', '2001:db8:1::51-2001:db8:1::51')
    srv_control.add_ddns_server(step, '127.0.0.1', '53001')
    srv_control.add_ddns_server_options(step, 'ddns-update-style', 'interim')
    # DDNS server is configured with generated-prefix option set to six.
    # DDNS server is configured with qualifying-suffix option set to example.com.
    srv_control.add_forward_ddns(step, 'six.example.com.', 'EMPTY_KEY', '2001:db8:1::1000', '53')
    srv_control.add_reverse_ddns(step,
                                 '1.0.0.0.8.b.d.0.1.0.0.2.ip6.arpa.',
                                 'EMPTY_KEY',
                                 '2001:db8:1::1000',
                                 '53')
    srv_control.build_and_send_config_files(step, 'SSH', 'config-file')
    srv_control.start_srv(step, 'DHCP', 'started')

    misc.test_procedure(step)
    srv_msg.dns_question_record(step, 'sth6.six.example.com', 'AAAA', 'IN')
    srv_msg.client_send_dns_query(step)

    misc.pass_criteria(step)
    srv_msg.send_wait_for_query(step, 'MUST', None)
    srv_msg.dns_option(step, 'NOT ', 'ANSWER')
    srv_msg.dns_option_content(step, 'ANSWER', None, 'rdata', '2001:db8:1::50')

    misc.test_procedure(step)
    srv_msg.dns_question_record(step,
                                '1.5.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.1.0.0.0.8.b.d.0.1.0.0.2.ip6.arpa.',
                                'PTR',
                                'IN')
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
    srv_msg.dns_option(step, 'NOT ', 'ANSWER')
    srv_msg.dns_option_content(step, 'ANSWER', None, 'rdata', 'sth6.six.example.com.')
    srv_msg.dns_option_content(step,
                               'ANSWER',
                               None,
                               'rrname',
                               '0.5.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.1.0.0.0.8.b.d.0.1.0.0.2.ip6.arpa.')


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
    srv_msg.dns_option_content(step, 'ANSWER', None, 'rdata', '2001:db8:1::51')
    srv_msg.dns_option_content(step, 'ANSWER', None, 'rrname', 'sth6.six.example.com.')

    misc.test_procedure(step)
    srv_msg.dns_question_record(step,
                                '1.5.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.1.0.0.0.8.b.d.0.1.0.0.2.ip6.arpa.',
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
                               '1.5.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.1.0.0.0.8.b.d.0.1.0.0.2.ip6.arpa.')



@pytest.mark.py_test
@pytest.mark.v6
@pytest.mark.ddns
@pytest.mark.notsig
@pytest.mark.forward_reverse_add
def test_ddns6_notsig_forw_and_rev_two_dhci_Sflag(step):
    """new-ddns6.notsig-forw_and_rev-two-dhci-Sflag"""

    misc.test_setup(step)
    srv_control.config_srv_subnet(step, '2001:db8:1::/64', '2001:db8:1::51-2001:db8:1::52')
    srv_control.add_ddns_server(step, '127.0.0.1', '53001')
    srv_control.add_ddns_server_options(step, 'ddns-update-style', 'interim')
    # DDNS server is configured with generated-prefix option set to six.
    # DDNS server is configured with qualifying-suffix option set to example.com.
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

    # # Client 1 add
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
    srv_msg.client_add_saved_option_count(step, '1', 'DONT ')
    srv_msg.client_copy_option(step, 'server-id')
    srv_msg.client_sets_value(step, 'Client', 'FQDN_domain_name', 'client1.six.example.com.')
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
    # Response option 39 MUST contain fqdn client1.six.example.com.

    misc.test_procedure(step)
    srv_msg.dns_question_record(step, 'client1.six.example.com', 'AAAA', 'IN')
    srv_msg.client_send_dns_query(step)

    misc.pass_criteria(step)
    srv_msg.send_wait_for_query(step, 'MUST', None)
    srv_msg.dns_option(step, 'NOT ', 'ANSWER')
    # Received DNS part ANSWER MUST contain rdata with value 2001:db8:1::51.
    srv_msg.dns_option_content(step, 'ANSWER', None, 'rrname', 'client1.six.example.com.')


    # # Client 2 add
    misc.test_procedure(step)
    srv_msg.client_sets_value(step, 'Client', 'DUID', '00:03:00:01:ff:ff:ff:ff:ff:02')
    srv_msg.client_does_include(step, 'Client', None, 'client-id')
    srv_msg.client_does_include(step, 'Client', None, 'IA-NA')
    srv_msg.client_send_msg(step, 'SOLICIT')

    misc.pass_criteria(step)
    srv_msg.send_wait_for_message(step, 'MUST', None, 'ADVERTISE')
    srv_msg.response_check_include_option(step, 'Response', None, '1')
    srv_msg.response_check_include_option(step, 'Response', None, '2')

    misc.test_procedure(step)
    srv_msg.client_sets_value(step, 'Client', 'DUID', '00:03:00:01:ff:ff:ff:ff:ff:02')
    srv_msg.client_save_option_count(step, '2', 'IA_NA')
    srv_msg.client_add_saved_option_count(step, '2', 'DONT ')
    srv_msg.client_copy_option(step, 'server-id')
    srv_msg.client_sets_value(step, 'Client', 'FQDN_domain_name', 'client2.six.example.com.')
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
    # Response option 39 MUST contain fqdn client2.six.example.com.

    misc.test_procedure(step)
    srv_msg.dns_question_record(step, 'client2.six.example.com', 'AAAA', 'IN')
    srv_msg.client_send_dns_query(step)

    misc.pass_criteria(step)
    srv_msg.send_wait_for_query(step, 'MUST', None)
    srv_msg.dns_option(step, 'NOT ', 'ANSWER')
    # Received DNS part ANSWER MUST contain rdata with value 2001:db8:1::52.
    srv_msg.dns_option_content(step, 'ANSWER', None, 'rrname', 'client2.six.example.com.')



@pytest.mark.py_test
@pytest.mark.v6
@pytest.mark.ddns
@pytest.mark.notsig
@pytest.mark.forward_reverse_add
@pytest.mark.disabled
def test_ddns6_notsig_forw_and_rev_dhci_conflicts_Sflag(step):
    """new-ddns6.notsig-forw_and_rev-dhci-conflicts-Sflag"""

    misc.test_setup(step)
    srv_control.config_srv_subnet(step, '2001:db8:1::/64', '2001:db8:1::51-2001:db8:1::52')
    srv_control.add_ddns_server(step, '127.0.0.1', '53001')
    srv_control.add_ddns_server_options(step, 'ddns-update-style', 'interim')
    # DDNS server is configured with generated-prefix option set to six.
    # DDNS server is configured with qualifying-suffix option set to example.com.
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

    # # Client 1 add
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
    srv_msg.client_add_saved_option_count(step, '1', 'DONT ')
    srv_msg.client_copy_option(step, 'server-id')
    srv_msg.client_sets_value(step, 'Client', 'FQDN_domain_name', 'client1.six.example.com.')
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
    # Response option 39 MUST contain fqdn client1.six.example.com.

    misc.test_procedure(step)
    srv_msg.dns_question_record(step, 'client1.six.example.com', 'AAAA', 'IN')
    srv_msg.client_send_dns_query(step)

    misc.pass_criteria(step)
    srv_msg.send_wait_for_query(step, 'MUST', None)
    srv_msg.dns_option(step, 'NOT ', 'ANSWER')
    srv_msg.dns_option_content(step, 'ANSWER', None, 'rdata', '2001:db8:1::51')
    srv_msg.dns_option_content(step, 'ANSWER', None, 'rrname', 'client1.six.example.com.')

    # # Client 2 add
    misc.test_procedure(step)
    srv_msg.client_sets_value(step, 'Client', 'DUID', '00:03:00:01:ff:ff:ff:ff:ff:02')
    srv_msg.client_does_include(step, 'Client', None, 'client-id')
    srv_msg.client_does_include(step, 'Client', None, 'IA-NA')
    srv_msg.client_send_msg(step, 'SOLICIT')

    misc.pass_criteria(step)
    srv_msg.send_wait_for_message(step, 'MUST', None, 'ADVERTISE')
    srv_msg.response_check_include_option(step, 'Response', None, '1')
    srv_msg.response_check_include_option(step, 'Response', None, '2')

    misc.test_procedure(step)
    srv_msg.client_sets_value(step, 'Client', 'DUID', '00:03:00:01:ff:ff:ff:ff:ff:02')
    srv_msg.client_save_option_count(step, '2', 'IA_NA')
    srv_msg.client_save_option_count(step, '2', 'server-id')
    srv_msg.client_add_saved_option_count(step, '2', 'DONT ')
    srv_msg.client_sets_value(step, 'Client', 'FQDN_domain_name', 'client1.six.example.com.')
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
    # Response option 39 MUST contain fqdn client1.six.example.com.

    misc.test_procedure(step)
    srv_msg.dns_question_record(step, 'client1.six.example.com', 'AAAA', 'IN')
    srv_msg.client_send_dns_query(step)

    misc.pass_criteria(step)
    srv_msg.send_wait_for_query(step, 'MUST', None)
    srv_msg.dns_option(step, 'NOT ', 'ANSWER')
    srv_msg.dns_option_content(step, 'ANSWER', None, 'rdata', '2001:db8:1::51')
    srv_msg.dns_option_content(step, 'ANSWER', None, 'rrname', 'client1.six.example.com.')

    misc.test_procedure(step)
    srv_msg.dns_question_record(step, 'client2.six.example.com', 'AAAA', 'IN')
    srv_msg.client_send_dns_query(step)

    misc.pass_criteria(step)
    srv_msg.send_wait_for_query(step, 'MUST', None)
    srv_msg.dns_option(step, None, 'ANSWER')

    misc.test_procedure(step)
    srv_msg.client_sets_value(step, 'Client', 'DUID', '00:03:00:01:ff:ff:ff:ff:ff:02')
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
    # Response MUST include option 39.
    # Response option 39 MUST contain flags 1. #later make it 's' 'n' and 'o'
    # Response option 39 MUST contain fqdn client2.six.example.com.

    misc.test_procedure(step)
    srv_msg.dns_question_record(step, 'client2.six.example.com', 'AAAA', 'IN')
    srv_msg.client_send_dns_query(step)

    misc.pass_criteria(step)
    srv_msg.send_wait_for_query(step, 'MUST', None)
    srv_msg.dns_option(step, 'NOT ', 'ANSWER')
    srv_msg.dns_option_content(step, 'ANSWER', None, 'rdata', '2001:db8:1::52')
    srv_msg.dns_option_content(step, 'ANSWER', None, 'rrname', 'client2.six.example.com.')

    misc.test_procedure(step)
    srv_msg.dns_question_record(step,
                                '1.5.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.1.0.0.0.8.b.d.0.1.0.0.2.ip6.arpa.',
                                'PTR',
                                'IN')
    srv_msg.client_send_dns_query(step)

    misc.pass_criteria(step)
    srv_msg.send_wait_for_query(step, 'MUST', None)
    srv_msg.dns_option(step, 'NOT ', 'ANSWER')
    srv_msg.dns_option_content(step, 'ANSWER', None, 'rdata', 'client1.six.example.com.')
    srv_msg.dns_option_content(step,
                               'ANSWER',
                               None,
                               'rrname',
                               '1.5.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.1.0.0.0.8.b.d.0.1.0.0.2.ip6.arpa.')

    misc.test_procedure(step)
    srv_msg.dns_question_record(step,
                                '2.5.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.1.0.0.0.8.b.d.0.1.0.0.2.ip6.arpa.',
                                'PTR',
                                'IN')
    srv_msg.client_send_dns_query(step)

    misc.pass_criteria(step)
    srv_msg.send_wait_for_query(step, 'MUST', None)
    srv_msg.dns_option(step, 'NOT ', 'ANSWER')
    srv_msg.dns_option_content(step, 'ANSWER', None, 'rdata', 'client2.six.example.com.')
    srv_msg.dns_option_content(step,
                               'ANSWER',
                               None,
                               'rrname',
                               '2.5.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.1.0.0.0.8.b.d.0.1.0.0.2.ip6.arpa.')




@pytest.mark.py_test
@pytest.mark.v6
@pytest.mark.ddns
@pytest.mark.notsig
@pytest.mark.forward_reverse_add
@pytest.mark.disabled
def test_ddns6_notsig_forw_and_rev_dhci_conflicts_remove_Sflag(step):
    """new-ddns6.notsig-forw_and_rev-dhci-conflicts-remove-Sflag"""

    misc.test_setup(step)
    srv_control.config_srv_subnet(step, '2001:db8:1::/64', '2001:db8:1::51-2001:db8:1::52')
    srv_control.add_ddns_server(step, '127.0.0.1', '53001')
    srv_control.add_ddns_server_options(step, 'ddns-update-style', 'interim')
    # DDNS server is configured with generated-prefix option set to six.
    # DDNS server is configured with qualifying-suffix option set to example.com.
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

    # # Client 1 add
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
    srv_msg.client_add_saved_option_count(step, '1', 'DONT ')
    srv_msg.client_copy_option(step, 'server-id')
    srv_msg.client_sets_value(step, 'Client', 'FQDN_domain_name', 'client1.six.example.com.')
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
    # Response option 39 MUST contain fqdn client1.six.example.com.

    misc.test_procedure(step)
    srv_msg.dns_question_record(step, 'client1.six.example.com', 'AAAA', 'IN')
    srv_msg.client_send_dns_query(step)

    misc.pass_criteria(step)
    srv_msg.send_wait_for_query(step, 'MUST', None)
    srv_msg.dns_option(step, 'NOT ', 'ANSWER')
    srv_msg.dns_option_content(step, 'ANSWER', None, 'rdata', '2001:db8:1::51')
    srv_msg.dns_option_content(step, 'ANSWER', None, 'rrname', 'client1.six.example.com.')

    # # Client 2 add
    misc.test_procedure(step)
    srv_msg.client_sets_value(step, 'Client', 'DUID', '00:03:00:01:ff:ff:ff:ff:ff:02')
    srv_msg.client_does_include(step, 'Client', None, 'client-id')
    srv_msg.client_does_include(step, 'Client', None, 'IA-NA')
    srv_msg.client_send_msg(step, 'SOLICIT')

    misc.pass_criteria(step)
    srv_msg.send_wait_for_message(step, 'MUST', None, 'ADVERTISE')
    srv_msg.response_check_include_option(step, 'Response', None, '1')
    srv_msg.response_check_include_option(step, 'Response', None, '2')

    misc.test_procedure(step)
    srv_msg.client_sets_value(step, 'Client', 'DUID', '00:03:00:01:ff:ff:ff:ff:ff:02')
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
    # Response MUST include option 39.
    # Response option 39 MUST contain flags 1. #later make it 's' 'n' and 'o'
    # Response option 39 MUST contain fqdn client2.six.example.com.

    misc.test_procedure(step)
    srv_msg.dns_question_record(step, 'client1.six.example.com', 'AAAA', 'IN')
    srv_msg.client_send_dns_query(step)

    misc.pass_criteria(step)
    srv_msg.send_wait_for_query(step, 'MUST', None)
    srv_msg.dns_option(step, 'NOT ', 'ANSWER')
    srv_msg.dns_option_content(step, 'ANSWER', None, 'rdata', '2001:db8:1::51')
    srv_msg.dns_option_content(step, 'ANSWER', None, 'rrname', 'client1.six.example.com.')

    misc.test_procedure(step)
    srv_msg.dns_question_record(step, 'client2.six.example.com', 'AAAA', 'IN')
    srv_msg.client_send_dns_query(step)

    misc.pass_criteria(step)
    srv_msg.send_wait_for_query(step, 'MUST', None)
    srv_msg.dns_option(step, 'NOT ', 'ANSWER')
    srv_msg.dns_option_content(step, 'ANSWER', None, 'rdata', '2001:db8:1::52')
    srv_msg.dns_option_content(step, 'ANSWER', None, 'rrname', 'client2.six.example.com.')

    misc.test_procedure(step)
    srv_msg.client_sets_value(step, 'Client', 'DUID', '00:03:00:01:ff:ff:ff:ff:ff:02')
    srv_msg.client_add_saved_option_count(step, '2', 'DONT ')
    srv_msg.client_sets_value(step, 'Client', 'FQDN_domain_name', 'client1.six.example.com.')
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
    # Response option 39 MUST contain fqdn client1.six.example.com.

    misc.test_procedure(step)
    srv_msg.dns_question_record(step, 'client2.six.example.com', 'AAAA', 'IN')
    srv_msg.client_send_dns_query(step)

    misc.pass_criteria(step)
    srv_msg.send_wait_for_query(step, 'MUST', None)
    srv_msg.dns_option(step, None, 'ANSWER')

    misc.test_procedure(step)
    srv_msg.dns_question_record(step,
                                '1.5.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.1.0.0.0.8.b.d.0.1.0.0.2.ip6.arpa.',
                                'PTR',
                                'IN')
    srv_msg.client_send_dns_query(step)

    misc.pass_criteria(step)
    srv_msg.send_wait_for_query(step, 'MUST', None)
    srv_msg.dns_option(step, 'NOT ', 'ANSWER')
    srv_msg.dns_option_content(step, 'ANSWER', None, 'rdata', 'client1.six.example.com.')
    srv_msg.dns_option_content(step,
                               'ANSWER',
                               None,
                               'rrname',
                               '1.5.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.1.0.0.0.8.b.d.0.1.0.0.2.ip6.arpa.')

    misc.test_procedure(step)
    srv_msg.dns_question_record(step,
                                '2.5.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.1.0.0.0.8.b.d.0.1.0.0.2.ip6.arpa.',
                                'PTR',
                                'IN')
    srv_msg.client_send_dns_query(step)

    misc.pass_criteria(step)
    srv_msg.send_wait_for_query(step, 'MUST', None)
    srv_msg.dns_option(step, None, 'ANSWER')



@pytest.mark.py_test
@pytest.mark.v6
@pytest.mark.ddns
@pytest.mark.notsig
@pytest.mark.forward_reverse_add
@pytest.mark.disabled
def test_ddns6_notsig_forw_and_rev_add_success_withoutflag_override_client(step):
    """new-ddns6.notsig-forw_and_rev-add-success-withoutflag-override-client"""

    misc.test_setup(step)
    # I can't figure out how to configure that... yet.
    srv_control.config_srv_subnet(step, '2001:db8:1::/64', '2001:db8:1::50-2001:db8:1::50')
    srv_control.add_ddns_server(step, '127.0.0.1', '53001')
    srv_control.add_ddns_server_options(step, 'ddns-update-style', 'interim')
    srv_control.add_ddns_server_options(step, 'ignore', 'client-update')
    # DDNS server is configured with generated-prefix option set to six.
    # DDNS server is configured with qualifying-suffix option set to example.com.
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
    srv_msg.dns_question_record(step,
                                '0.5.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.1.0.0.0.8.b.d.0.1.0.0.2.ip6.arpa.',
                                'PTR',
                                'IN')
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
    srv_msg.client_does_include(step, 'Client', None, 'fqdn')
    srv_msg.client_does_include(step, 'Client', None, 'client-id')
    srv_msg.client_send_msg(step, 'REQUEST')

    misc.pass_criteria(step)
    srv_msg.send_wait_for_message(step, 'MUST', None, 'REPLY')
    srv_msg.response_check_include_option(step, 'Response', None, '1')
    srv_msg.response_check_include_option(step, 'Response', None, '2')
    # Response MUST include option 39.
    # Response option 39 MUST contain flags 3. #later make it 's' 'n' and 'o' 3 - SO
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
@pytest.mark.notsig
@pytest.mark.reverse_add
def test_ddns6_notsig_rev_success_withoutflag(step):
    """new-ddns6.notsig-rev-success-withoutflag"""

    misc.test_setup(step)
    srv_control.config_srv_subnet(step, '2001:db8:1::/64', '2001:db8:1::50-2001:db8:1::50')
    srv_control.add_ddns_server(step, '127.0.0.1', '53001')
    srv_control.add_ddns_server_options(step, 'ddns-update-style', 'interim')
    # DDNS server is configured with generated-prefix option set to six.
    # DDNS server is configured with qualifying-suffix option set to example.com.
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
    srv_msg.dns_question_record(step,
                                '0.5.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.1.0.0.0.8.b.d.0.1.0.0.2.ip6.arpa.',
                                'PTR',
                                'IN')
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
    srv_msg.client_does_include(step, 'Client', None, 'fqdn')
    srv_msg.client_does_include(step, 'Client', None, 'client-id')
    srv_msg.client_send_msg(step, 'REQUEST')

    misc.pass_criteria(step)
    srv_msg.send_wait_for_message(step, 'MUST', None, 'REPLY')
    srv_msg.response_check_include_option(step, 'Response', None, '1')
    srv_msg.response_check_include_option(step, 'Response', None, '2')
    # Response MUST include option 39.
    # Response option 39 MUST contain flags 0. #later make it 's' 'n' and 'o'
    # Response option 39 MUST contain fqdn sth6.six.example.com.
    srv_msg.log_contains_line(step,
                              'DNS',
                              None,
                              'adding an RR at \'0.5.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.1.0.0.0.8.b.d.0.1.0.0.2.ip6.arpa\' PTR sth6.six.example.com.')

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
@pytest.mark.notsig
@pytest.mark.reverse_add
def test_ddns6_notsig_rev_withoutflag_notenabled(step):
    """new-ddns6.notsig-rev-withoutflag-notenabled"""

    misc.test_setup(step)
    srv_control.config_srv_subnet(step, '2001:db8:1::/64', '2001:db8:1::50-2001:db8:1::50')
    srv_control.add_ddns_server(step, '127.0.0.1', '53001')
    # DDNS server is configured with ddns-update-style option set to off.
    # DDNS server is configured with generated-prefix option set to six.
    # DDNS server is configured with qualifying-suffix option set to example.com.
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
    srv_msg.client_copy_option(step, 'IA_NA')
    srv_msg.client_copy_option(step, 'server-id')
    srv_msg.client_sets_value(step, 'Client', 'FQDN_domain_name', 'sth6.six.example.com.')
    srv_msg.client_does_include(step, 'Client', None, 'fqdn')
    srv_msg.client_does_include(step, 'Client', None, 'client-id')
    srv_msg.client_send_msg(step, 'REQUEST')

    misc.pass_criteria(step)
    srv_msg.send_wait_for_message(step, 'MUST', None, 'REPLY')
    srv_msg.response_check_include_option(step, 'Response', None, '1')
    srv_msg.response_check_include_option(step, 'Response', None, '2')
    # Response MUST include option 39.
    # Response option 39 MUST contain flags 4. #later make it 's' 'n' and 'o' 4 -N
    # Response option 39 MUST contain fqdn sth6.six.example.com.
    srv_msg.log_contains_line(step,
                              'DNS',
                              'NOT ',
                              'adding an RR at \'0.5.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.1.0.0.0.8.b.d.0.1.0.0.2.ip6.arpa\' PTR sth6.six.example.com.')

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



@pytest.mark.py_test
@pytest.mark.v6
@pytest.mark.ddns
@pytest.mark.notsig
@pytest.mark.reverse_add
@pytest.mark.disabled
def test_ddns6_notsig_rev_Nflag_override_no_update(step):
    """new-ddns6.notsig-rev-Nflag-override-no-update"""

    misc.test_setup(step)
    # for now disabled, I don't know how to configure override yet.
    srv_control.config_srv_subnet(step, '2001:db8:1::/64', '2001:db8:1::50-2001:db8:1::50')
    srv_control.add_ddns_server(step, '127.0.0.1', '53001')
    srv_control.add_ddns_server_options(step, 'ddns-update-style', 'interim')
    srv_control.add_ddns_server_options(step, 'override-no-update', 'true')
    # DDNS server is configured with generated-prefix option set to six.
    # DDNS server is configured with qualifying-suffix option set to example.com.
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
    srv_msg.client_copy_option(step, 'IA_NA')
    srv_msg.client_copy_option(step, 'server-id')
    srv_msg.client_sets_value(step, 'Client', 'FQDN_domain_name', 'sth6.six.example.com.')
    srv_msg.client_sets_value(step, 'Client', 'FQDN_flags', 'N')
    srv_msg.client_does_include(step, 'Client', None, 'fqdn')
    srv_msg.client_does_include(step, 'Client', None, 'client-id')
    srv_msg.client_send_msg(step, 'REQUEST')

    misc.pass_criteria(step)
    srv_msg.send_wait_for_message(step, 'MUST', None, 'REPLY')
    srv_msg.response_check_include_option(step, 'Response', None, '1')
    srv_msg.response_check_include_option(step, 'Response', None, '2')
    # Response MUST include option 39.
    # Response option 39 MUST contain flags 3. #later make it 's' 'n' and 'o' 3 - SO
    # Response option 39 MUST contain fqdn sth6.six.example.com.
    srv_msg.log_contains_line(step,
                              'DNS',
                              None,
                              'adding an RR at \'0.5.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.1.0.0.0.8.b.d.0.1.0.0.2.ip6.arpa\' PTR sth6.six.example.com.')

    misc.test_procedure(step)
    srv_msg.dns_question_record(step, 'sth6.six.example.com', 'AAAA', 'IN')
    srv_msg.client_send_dns_query(step)

    misc.pass_criteria(step)
    srv_msg.send_wait_for_query(step, 'MUST', None)
    srv_msg.dns_option(step, 'NOT ', 'ANSWER')
    srv_msg.dns_option_content(step, 'ANSWER', None, 'rdata', '2001:db8:1::50')
    srv_msg.dns_option_content(step, 'ANSWER', None, 'rrname', 'sth6.six.example.com.')

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



