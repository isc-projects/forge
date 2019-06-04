"""DDNS without TSIG"""

# pylint: disable=invalid-name,line-too-long

import pytest

import misc
import srv_control
import srv_msg


@pytest.mark.v6
@pytest.mark.ddns
@pytest.mark.kea_only
@pytest.mark.notsig
@pytest.mark.forward_reverse_add
def test_ddns6_notsig_forw_and_rev_add_success_Sflag():

    misc.test_setup()
    srv_control.config_srv_subnet('2001:db8:1::/64', '2001:db8:1::50-2001:db8:1::50')
    srv_control.add_ddns_server('127.0.0.1', '53001')
    srv_control.add_ddns_server_options('enable-updates', 'true')
    srv_control.add_ddns_server_options('generated-prefix', 'six')
    srv_control.add_ddns_server_options('qualifying-suffix', 'example.com')
    srv_control.add_forward_ddns('six.example.com.', 'EMPTY_KEY')
    srv_control.add_reverse_ddns('1.0.0.0.8.b.d.0.1.0.0.2.ip6.arpa.', 'EMPTY_KEY')
    srv_control.build_and_send_config_files('SSH', 'config-file')
    srv_control.start_srv('DHCP', 'started')

    srv_control.use_dns_set_number('1')
    srv_control.start_srv('DNS', 'started')

    misc.test_procedure()
    srv_msg.dns_question_record('sth6.six.example.com', 'AAAA', 'IN')
    srv_msg.client_send_dns_query()

    misc.pass_criteria()
    srv_msg.send_wait_for_query('MUST', None)
    srv_msg.dns_option(None, 'ANSWER')

    misc.test_procedure()
    srv_msg.client_sets_value('Client', 'DUID', '00:03:00:01:ff:ff:ff:ff:ff:01')
    srv_msg.client_does_include('Client', None, 'client-id')
    srv_msg.client_does_include('Client', None, 'IA-NA')
    srv_msg.client_send_msg('SOLICIT')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', None, 'ADVERTISE')
    srv_msg.response_check_include_option('Response', None, '1')
    srv_msg.response_check_include_option('Response', None, '2')

    misc.test_procedure()
    srv_msg.client_sets_value('Client', 'DUID', '00:03:00:01:ff:ff:ff:ff:ff:01')
    srv_msg.client_copy_option('IA_NA')
    srv_msg.client_copy_option('server-id')
    srv_msg.client_sets_value('Client', 'FQDN_domain_name', 'sth6.six.example.com.')
    srv_msg.client_sets_value('Client', 'FQDN_flags', 'S')
    srv_msg.client_does_include('Client', None, 'fqdn')
    srv_msg.client_does_include('Client', None, 'client-id')
    srv_msg.client_send_msg('REQUEST')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', None, 'REPLY')
    srv_msg.response_check_include_option('Response', None, '1')
    srv_msg.response_check_include_option('Response', None, '2')
    srv_msg.response_check_include_option('Response', None, '39')
    srv_msg.response_check_option_content('Response', '39', None, 'flags', 'S')
    srv_msg.response_check_option_content('Response', '39', None, 'fqdn', 'sth6.six.example.com.')

    misc.test_procedure()
    srv_msg.dns_question_record('sth6.six.example.com', 'AAAA', 'IN')
    srv_msg.client_send_dns_query()

    misc.pass_criteria()
    srv_msg.send_wait_for_query('MUST', None)
    srv_msg.dns_option('NOT ', 'ANSWER')
    srv_msg.dns_option_content('ANSWER', None, 'rdata', '2001:db8:1::50')

    misc.test_procedure()
    srv_msg.dns_question_record('0.5.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.1.0.0.0.8.b.d.0.1.0.0.2.ip6.arpa.',
                                'PTR',
                                'IN')
    srv_msg.client_send_dns_query()

    misc.pass_criteria()
    srv_msg.send_wait_for_query('MUST', None)
    srv_msg.dns_option('NOT ', 'ANSWER')
    srv_msg.dns_option_content('ANSWER', None, 'rdata', 'sth6.six.example.com.')
    srv_msg.dns_option_content('ANSWER',
                               None,
                               'rrname',
                               '0.5.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.1.0.0.0.8.b.d.0.1.0.0.2.ip6.arpa.')


@pytest.mark.v6
@pytest.mark.ddns
@pytest.mark.kea_only
@pytest.mark.notsig
@pytest.mark.forward_reverse_add
def test_ddns6_notsig_forw_and_rev_add_fail_Sflag():

    misc.test_setup()
    srv_control.config_srv_subnet('2001:db8:1::/64', '2001:db8:1::50-2001:db8:1::50')
    srv_control.add_ddns_server('127.0.0.1', '53001')
    srv_control.add_ddns_server_options('enable-updates', 'true')
    srv_control.add_ddns_server_options('generated-prefix', 'six')
    srv_control.add_ddns_server_options('qualifying-suffix', 'example.com')
    srv_control.add_forward_ddns('six.example.com.', 'EMPTY_KEY')
    srv_control.add_reverse_ddns('1.0.0.0.8.b.d.0.1.0.0.2.ip6.arpa.', 'EMPTY_KEY')
    srv_control.build_and_send_config_files('SSH', 'config-file')
    srv_control.start_srv('DHCP', 'started')

    srv_control.use_dns_set_number('1')
    srv_control.start_srv('DNS', 'started')

    misc.test_procedure()
    srv_msg.dns_question_record('sth6.six.example.com', 'AAAA', 'IN')
    srv_msg.client_send_dns_query()

    misc.pass_criteria()
    srv_msg.send_wait_for_query('MUST', None)
    srv_msg.dns_option(None, 'ANSWER')

    misc.test_procedure()
    srv_msg.dns_question_record('0.5.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.1.0.0.0.8.b.d.0.1.0.0.2.ip6.arpa.',
                                'PTR',
                                'IN')
    srv_msg.client_send_dns_query()

    misc.pass_criteria()
    srv_msg.send_wait_for_query('MUST', None)
    srv_msg.dns_option(None, 'ANSWER')

    misc.test_procedure()
    srv_msg.client_sets_value('Client', 'DUID', '00:03:00:01:ff:ff:ff:ff:ff:01')
    srv_msg.client_does_include('Client', None, 'client-id')
    srv_msg.client_does_include('Client', None, 'IA-NA')
    srv_msg.client_send_msg('SOLICIT')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', None, 'ADVERTISE')
    srv_msg.response_check_include_option('Response', None, '1')
    srv_msg.response_check_include_option('Response', None, '2')

    misc.test_procedure()
    srv_msg.client_sets_value('Client', 'DUID', '00:03:00:01:ff:ff:ff:ff:ff:01')
    srv_msg.client_copy_option('IA_NA')
    srv_msg.client_copy_option('server-id')
    #  Update for different zone
    srv_msg.client_sets_value('Client', 'FQDN_domain_name', 'sth6.six.com.')
    srv_msg.client_sets_value('Client', 'FQDN_flags', 'S')
    srv_msg.client_does_include('Client', None, 'fqdn')
    srv_msg.client_does_include('Client', None, 'client-id')
    srv_msg.client_send_msg('REQUEST')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', None, 'REPLY')
    srv_msg.response_check_include_option('Response', None, '1')
    srv_msg.response_check_include_option('Response', None, '2')
    srv_msg.response_check_include_option('Response', None, '39')
    srv_msg.response_check_option_content('Response', '39', None, 'flags', 'S')
    srv_msg.response_check_option_content('Response', '39', None, 'fqdn', 'sth6.six.com.')

    misc.test_procedure()
    srv_msg.dns_question_record('sth6.six.example.com', 'AAAA', 'IN')
    srv_msg.client_send_dns_query()

    misc.pass_criteria()
    srv_msg.send_wait_for_query('MUST', None)
    srv_msg.dns_option(None, 'ANSWER')

    misc.test_procedure()
    srv_msg.dns_question_record('0.5.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.1.0.0.0.8.b.d.0.1.0.0.2.ip6.arpa.',
                                'PTR',
                                'IN')
    srv_msg.client_send_dns_query()

    misc.pass_criteria()
    srv_msg.send_wait_for_query('MUST', None)
    srv_msg.dns_option(None, 'ANSWER')


@pytest.mark.v6
@pytest.mark.ddns
@pytest.mark.kea_only
@pytest.mark.notsig
@pytest.mark.forward_reverse_add
def test_ddns6_notsig_forw_and_rev_notenabled_Sflag():

    misc.test_setup()
    srv_control.config_srv_subnet('2001:db8:1::/64', '2001:db8:1::50-2001:db8:1::50')
    srv_control.add_ddns_server('127.0.0.1', '53001')
    srv_control.add_ddns_server_options('enable-updates', 'false')
    srv_control.add_ddns_server_options('generated-prefix', 'six')
    srv_control.add_ddns_server_options('qualifying-suffix', 'example.com')
    srv_control.add_forward_ddns('six.example.com.', 'EMPTY_KEY')
    srv_control.add_reverse_ddns('1.0.0.0.8.b.d.0.1.0.0.2.ip6.arpa.', 'EMPTY_KEY')
    srv_control.build_and_send_config_files('SSH', 'config-file')
    srv_control.start_srv('DHCP', 'started')

    srv_control.use_dns_set_number('1')
    srv_control.start_srv('DNS', 'started')

    misc.test_procedure()
    srv_msg.dns_question_record('sth6.six.example.com', 'AAAA', 'IN')
    srv_msg.client_send_dns_query()

    misc.pass_criteria()
    srv_msg.send_wait_for_query('MUST', None)
    srv_msg.dns_option(None, 'ANSWER')

    misc.test_procedure()
    srv_msg.dns_question_record('0.5.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.1.0.0.0.8.b.d.0.1.0.0.2.ip6.arpa.',
                                'PTR',
                                'IN')
    srv_msg.client_send_dns_query()

    misc.pass_criteria()
    srv_msg.send_wait_for_query('MUST', None)
    srv_msg.dns_option(None, 'ANSWER')

    misc.test_procedure()
    srv_msg.client_sets_value('Client', 'DUID', '00:03:00:01:ff:ff:ff:ff:ff:01')
    srv_msg.client_does_include('Client', None, 'client-id')
    srv_msg.client_does_include('Client', None, 'IA-NA')
    srv_msg.client_send_msg('SOLICIT')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', None, 'ADVERTISE')
    srv_msg.response_check_include_option('Response', None, '1')
    srv_msg.response_check_include_option('Response', None, '2')

    misc.test_procedure()
    srv_msg.client_sets_value('Client', 'DUID', '00:03:00:01:ff:ff:ff:ff:ff:01')
    srv_msg.client_copy_option('IA_NA')
    srv_msg.client_copy_option('server-id')
    srv_msg.client_sets_value('Client', 'FQDN_domain_name', 'sth6.six.example.com.')
    srv_msg.client_sets_value('Client', 'FQDN_flags', 'S')
    srv_msg.client_does_include('Client', None, 'fqdn')
    srv_msg.client_does_include('Client', None, 'client-id')
    srv_msg.client_send_msg('REQUEST')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', None, 'REPLY')
    srv_msg.response_check_include_option('Response', None, '1')
    srv_msg.response_check_include_option('Response', None, '2')
    srv_msg.response_check_include_option('Response', None, '39')
    srv_msg.response_check_option_content('Response', '39', None, 'flags', 'ON')
    srv_msg.response_check_option_content('Response', '39', None, 'fqdn', 'sth6.six.example.com.')

    misc.test_procedure()
    srv_msg.dns_question_record('sth6.six.example.com', 'AAAA', 'IN')
    srv_msg.client_send_dns_query()

    misc.pass_criteria()
    srv_msg.send_wait_for_query('MUST', None)
    srv_msg.dns_option(None, 'ANSWER')

    misc.test_procedure()
    srv_msg.dns_question_record('0.5.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.1.0.0.0.8.b.d.0.1.0.0.2.ip6.arpa.',
                                'PTR',
                                'IN')
    srv_msg.client_send_dns_query()

    misc.pass_criteria()
    srv_msg.send_wait_for_query('MUST', None)
    srv_msg.dns_option(None, 'ANSWER')


@pytest.mark.v6
@pytest.mark.ddns
@pytest.mark.kea_only
@pytest.mark.notsig
@pytest.mark.forward_update
def test_ddns6_notsig_forw_and_rev_update_success_Sflag():

    misc.test_setup()
    srv_control.config_srv_subnet('2001:db8:1::/64', '2001:db8:1::50-2001:db8:1::50')
    srv_control.add_ddns_server('127.0.0.1', '53001')
    srv_control.add_ddns_server_options('enable-updates', 'true')
    srv_control.add_ddns_server_options('generated-prefix', 'six')
    srv_control.add_ddns_server_options('qualifying-suffix', 'example.com')
    srv_control.add_forward_ddns('six.example.com.', 'EMPTY_KEY')
    srv_control.add_reverse_ddns('1.0.0.0.8.b.d.0.1.0.0.2.ip6.arpa.', 'EMPTY_KEY')
    srv_control.build_and_send_config_files('SSH', 'config-file')
    srv_control.start_srv('DHCP', 'started')

    srv_control.use_dns_set_number('2')
    srv_control.start_srv('DNS', 'started')

    misc.test_procedure()
    srv_msg.dns_question_record('sth6.six.example.com', 'AAAA', 'IN')
    srv_msg.client_send_dns_query()

    misc.pass_criteria()
    srv_msg.send_wait_for_query('MUST', None)
    srv_msg.dns_option(None, 'ANSWER')

    misc.test_procedure()
    srv_msg.dns_question_record('0.5.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.1.0.0.0.8.b.d.0.1.0.0.2.ip6.arpa.',
                                'PTR',
                                'IN')
    srv_msg.client_send_dns_query()

    misc.pass_criteria()
    srv_msg.send_wait_for_query('MUST', None)
    srv_msg.dns_option(None, 'ANSWER')

    misc.test_procedure()
    srv_msg.client_sets_value('Client', 'DUID', '00:03:00:01:ff:ff:ff:ff:ff:01')
    srv_msg.client_does_include('Client', None, 'client-id')
    srv_msg.client_does_include('Client', None, 'IA-NA')
    srv_msg.client_send_msg('SOLICIT')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', None, 'ADVERTISE')
    srv_msg.response_check_include_option('Response', None, '1')
    srv_msg.response_check_include_option('Response', None, '2')

    misc.test_procedure()
    srv_msg.client_sets_value('Client', 'DUID', '00:03:00:01:ff:ff:ff:ff:ff:01')
    srv_msg.client_copy_option('IA_NA')
    srv_msg.client_copy_option('server-id')
    srv_msg.client_sets_value('Client', 'FQDN_domain_name', 'sth6.six.example.com.')
    srv_msg.client_sets_value('Client', 'FQDN_flags', 'S')
    srv_msg.client_does_include('Client', None, 'fqdn')
    srv_msg.client_does_include('Client', None, 'client-id')
    srv_msg.client_send_msg('REQUEST')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', None, 'REPLY')
    srv_msg.response_check_include_option('Response', None, '1')
    srv_msg.response_check_include_option('Response', None, '2')
    srv_msg.response_check_include_option('Response', None, '39')
    srv_msg.response_check_option_content('Response', '39', None, 'flags', 'S')
    srv_msg.response_check_option_content('Response', '39', None, 'fqdn', 'sth6.six.example.com.')

    misc.test_procedure()
    srv_msg.dns_question_record('sth6.six.example.com', 'AAAA', 'IN')
    srv_msg.client_send_dns_query()

    misc.pass_criteria()
    srv_msg.send_wait_for_query('MUST', None)
    srv_msg.dns_option('NOT ', 'ANSWER')
    srv_msg.dns_option_content('ANSWER', None, 'rdata', '2001:db8:1::50')

    misc.test_procedure()
    srv_msg.dns_question_record('0.5.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.1.0.0.0.8.b.d.0.1.0.0.2.ip6.arpa.',
                                'PTR',
                                'IN')
    srv_msg.client_send_dns_query()

    misc.pass_criteria()
    srv_msg.send_wait_for_query('MUST', None)
    srv_msg.dns_option('NOT ', 'ANSWER')
    srv_msg.dns_option_content('ANSWER', None, 'rdata', 'sth6.six.example.com.')
    srv_msg.dns_option_content('ANSWER',
                               None,
                               'rrname',
                               '0.5.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.1.0.0.0.8.b.d.0.1.0.0.2.ip6.arpa.')

    misc.test_setup()
    srv_control.start_srv('DHCP', 'stopped')
    srv_control.clear_leases('leases')

    misc.test_setup()
    srv_control.config_srv_subnet('2001:db8:1::/64', '2001:db8:1::51-2001:db8:1::51')
    srv_control.add_ddns_server('127.0.0.1', '53001')
    srv_control.add_ddns_server_options('enable-updates', 'true')
    srv_control.add_ddns_server_options('generated-prefix', 'six')
    srv_control.add_ddns_server_options('qualifying-suffix', 'example.com')
    srv_control.add_forward_ddns('six.example.com.', 'EMPTY_KEY')
    srv_control.add_reverse_ddns('1.0.0.0.8.b.d.0.1.0.0.2.ip6.arpa.', 'EMPTY_KEY')
    srv_control.build_and_send_config_files('SSH', 'config-file')
    srv_control.start_srv('DHCP', 'started')

    misc.test_procedure()
    srv_msg.dns_question_record('sth6.six.example.com', 'AAAA', 'IN')
    srv_msg.client_send_dns_query()

    misc.pass_criteria()
    srv_msg.send_wait_for_query('MUST', None)
    srv_msg.dns_option('NOT ', 'ANSWER')
    srv_msg.dns_option_content('ANSWER', None, 'rdata', '2001:db8:1::50')

    misc.test_procedure()
    srv_msg.dns_question_record('1.5.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.1.0.0.0.8.b.d.0.1.0.0.2.ip6.arpa.',
                                'PTR',
                                'IN')
    srv_msg.client_send_dns_query()

    misc.pass_criteria()
    srv_msg.send_wait_for_query('MUST', None)
    srv_msg.dns_option(None, 'ANSWER')

    misc.test_procedure()
    srv_msg.dns_question_record('0.5.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.1.0.0.0.8.b.d.0.1.0.0.2.ip6.arpa.',
                                'PTR',
                                'IN')
    srv_msg.client_send_dns_query()

    misc.pass_criteria()
    srv_msg.send_wait_for_query('MUST', None)
    srv_msg.dns_option('NOT ', 'ANSWER')
    srv_msg.dns_option_content('ANSWER', None, 'rdata', 'sth6.six.example.com.')
    srv_msg.dns_option_content('ANSWER',
                               None,
                               'rrname',
                               '0.5.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.1.0.0.0.8.b.d.0.1.0.0.2.ip6.arpa.')

    misc.test_procedure()
    srv_msg.client_sets_value('Client', 'DUID', '00:03:00:01:ff:ff:ff:ff:ff:01')
    srv_msg.client_does_include('Client', None, 'client-id')
    srv_msg.client_does_include('Client', None, 'IA-NA')
    srv_msg.client_send_msg('SOLICIT')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', None, 'ADVERTISE')
    srv_msg.response_check_include_option('Response', None, '1')
    srv_msg.response_check_include_option('Response', None, '2')

    misc.test_procedure()
    srv_msg.client_sets_value('Client', 'DUID', '00:03:00:01:ff:ff:ff:ff:ff:01')
    srv_msg.client_copy_option('IA_NA')
    srv_msg.client_copy_option('server-id')
    srv_msg.client_sets_value('Client', 'FQDN_domain_name', 'sth6.six.example.com.')
    srv_msg.client_sets_value('Client', 'FQDN_flags', 'S')
    srv_msg.client_does_include('Client', None, 'fqdn')
    srv_msg.client_does_include('Client', None, 'client-id')
    srv_msg.client_send_msg('REQUEST')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', None, 'REPLY')
    srv_msg.response_check_include_option('Response', None, '1')
    srv_msg.response_check_include_option('Response', None, '2')
    srv_msg.response_check_include_option('Response', None, '39')
    srv_msg.response_check_option_content('Response', '39', None, 'flags', 'S')
    srv_msg.response_check_option_content('Response', '39', None, 'fqdn', 'sth6.six.example.com.')

    misc.test_procedure()
    srv_msg.dns_question_record('sth6.six.example.com', 'AAAA', 'IN')
    srv_msg.client_send_dns_query()

    misc.pass_criteria()
    srv_msg.send_wait_for_query('MUST', None)
    srv_msg.dns_option('NOT ', 'ANSWER')
    srv_msg.dns_option_content('ANSWER', None, 'rdata', '2001:db8:1::51')
    srv_msg.dns_option_content('ANSWER', None, 'rrname', 'sth6.six.example.com.')

    misc.test_procedure()
    srv_msg.dns_question_record('1.5.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.1.0.0.0.8.b.d.0.1.0.0.2.ip6.arpa.',
                                'PTR',
                                'IN')
    srv_msg.client_send_dns_query()

    misc.pass_criteria()
    srv_msg.send_wait_for_query('MUST', None)
    srv_msg.dns_option('NOT ', 'ANSWER')
    srv_msg.dns_option_content('ANSWER', None, 'rdata', 'sth6.six.example.com.')
    srv_msg.dns_option_content('ANSWER',
                               None,
                               'rrname',
                               '1.5.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.1.0.0.0.8.b.d.0.1.0.0.2.ip6.arpa.')


@pytest.mark.v6
@pytest.mark.ddns
@pytest.mark.kea_only
@pytest.mark.notsig
@pytest.mark.forward_reverse_add
def test_ddns6_notsig_forw_and_rev_two_dhci_Sflag():

    misc.test_setup()
    srv_control.config_srv_subnet('2001:db8:1::/64', '2001:db8:1::51-2001:db8:1::52')
    srv_control.add_ddns_server('127.0.0.1', '53001')
    srv_control.add_ddns_server_options('enable-updates', 'true')
    srv_control.add_ddns_server_options('generated-prefix', 'six')
    srv_control.add_ddns_server_options('qualifying-suffix', 'example.com')
    srv_control.add_forward_ddns('six.example.com.', 'EMPTY_KEY')
    srv_control.add_reverse_ddns('1.0.0.0.8.b.d.0.1.0.0.2.ip6.arpa.', 'EMPTY_KEY')
    srv_control.build_and_send_config_files('SSH', 'config-file')
    srv_control.start_srv('DHCP', 'started')

    srv_control.use_dns_set_number('1')
    srv_control.start_srv('DNS', 'started')

    misc.test_procedure()
    srv_msg.dns_question_record('client1.six.example.com', 'AAAA', 'IN')
    srv_msg.client_send_dns_query()

    misc.pass_criteria()
    srv_msg.send_wait_for_query('MUST', None)
    srv_msg.dns_option(None, 'ANSWER')

    misc.test_procedure()
    srv_msg.dns_question_record('client2.six.example.com', 'AAAA', 'IN')
    srv_msg.client_send_dns_query()

    misc.pass_criteria()
    srv_msg.send_wait_for_query('MUST', None)
    srv_msg.dns_option(None, 'ANSWER')

    #  Client 1 add
    misc.test_procedure()
    srv_msg.client_sets_value('Client', 'DUID', '00:03:00:01:ff:ff:ff:ff:ff:01')
    srv_msg.client_does_include('Client', None, 'client-id')
    srv_msg.client_does_include('Client', None, 'IA-NA')
    srv_msg.client_send_msg('SOLICIT')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', None, 'ADVERTISE')
    srv_msg.response_check_include_option('Response', None, '1')
    srv_msg.response_check_include_option('Response', None, '2')

    misc.test_procedure()
    srv_msg.client_sets_value('Client', 'DUID', '00:03:00:01:ff:ff:ff:ff:ff:01')
    srv_msg.client_save_option_count('1', 'IA_NA')
    srv_msg.client_add_saved_option_count('1', 'DONT ')
    srv_msg.client_copy_option('server-id')
    srv_msg.client_sets_value('Client', 'FQDN_domain_name', 'client1.six.example.com.')
    srv_msg.client_sets_value('Client', 'FQDN_flags', 'S')
    srv_msg.client_does_include('Client', None, 'fqdn')
    srv_msg.client_does_include('Client', None, 'client-id')
    srv_msg.client_send_msg('REQUEST')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', None, 'REPLY')
    srv_msg.response_check_include_option('Response', None, '1')
    srv_msg.response_check_include_option('Response', None, '2')
    srv_msg.response_check_include_option('Response', None, '39')
    srv_msg.response_check_option_content('Response', '39', None, 'flags', 'S')
    srv_msg.response_check_option_content('Response',
                                          '39',
                                          None,
                                          'fqdn',
                                          'client1.six.example.com.')

    misc.test_procedure()
    srv_msg.dns_question_record('client1.six.example.com', 'AAAA', 'IN')
    srv_msg.client_send_dns_query()

    misc.pass_criteria()
    srv_msg.send_wait_for_query('MUST', None)
    srv_msg.dns_option('NOT ', 'ANSWER')
    srv_msg.dns_option_content('ANSWER', None, 'rdata', '2001:db8:1::51')
    srv_msg.dns_option_content('ANSWER', None, 'rrname', 'client1.six.example.com.')

    #  Client 2 add
    misc.test_procedure()
    srv_msg.client_sets_value('Client', 'DUID', '00:03:00:01:ff:ff:ff:ff:ff:02')
    srv_msg.client_does_include('Client', None, 'client-id')
    srv_msg.client_does_include('Client', None, 'IA-NA')
    srv_msg.client_send_msg('SOLICIT')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', None, 'ADVERTISE')
    srv_msg.response_check_include_option('Response', None, '1')
    srv_msg.response_check_include_option('Response', None, '2')

    misc.test_procedure()
    srv_msg.client_sets_value('Client', 'DUID', '00:03:00:01:ff:ff:ff:ff:ff:02')
    srv_msg.client_save_option_count('2', 'IA_NA')
    srv_msg.client_add_saved_option_count('2', 'DONT ')
    srv_msg.client_copy_option('server-id')
    srv_msg.client_sets_value('Client', 'FQDN_domain_name', 'client2.six.example.com.')
    srv_msg.client_sets_value('Client', 'FQDN_flags', 'S')
    srv_msg.client_does_include('Client', None, 'fqdn')
    srv_msg.client_does_include('Client', None, 'client-id')
    srv_msg.client_send_msg('REQUEST')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', None, 'REPLY')
    srv_msg.response_check_include_option('Response', None, '1')
    srv_msg.response_check_include_option('Response', None, '2')
    srv_msg.response_check_include_option('Response', None, '39')
    srv_msg.response_check_option_content('Response', '39', None, 'flags', 'S')
    srv_msg.response_check_option_content('Response',
                                          '39',
                                          None,
                                          'fqdn',
                                          'client2.six.example.com.')

    misc.test_procedure()
    srv_msg.dns_question_record('client2.six.example.com', 'AAAA', 'IN')
    srv_msg.client_send_dns_query()

    misc.pass_criteria()
    srv_msg.send_wait_for_query('MUST', None)
    srv_msg.dns_option('NOT ', 'ANSWER')
    srv_msg.dns_option_content('ANSWER', None, 'rdata', '2001:db8:1::52')
    srv_msg.dns_option_content('ANSWER', None, 'rrname', 'client2.six.example.com.')


@pytest.mark.v6
@pytest.mark.ddns
@pytest.mark.kea_only
@pytest.mark.notsig
@pytest.mark.forward_reverse_add
def test_ddns6_notsig_forw_and_rev_dhci_conflicts_Sflag():

    misc.test_setup()
    srv_control.config_srv_subnet('2001:db8:1::/64', '2001:db8:1::51-2001:db8:1::52')
    srv_control.add_ddns_server('127.0.0.1', '53001')
    srv_control.add_ddns_server_options('enable-updates', 'true')
    srv_control.add_ddns_server_options('generated-prefix', 'six')
    srv_control.add_ddns_server_options('qualifying-suffix', 'example.com')
    srv_control.add_forward_ddns('six.example.com.', 'EMPTY_KEY')
    srv_control.add_reverse_ddns('1.0.0.0.8.b.d.0.1.0.0.2.ip6.arpa.', 'EMPTY_KEY')
    srv_control.build_and_send_config_files('SSH', 'config-file')
    srv_control.start_srv('DHCP', 'started')

    srv_control.use_dns_set_number('1')
    srv_control.start_srv('DNS', 'started')

    misc.test_procedure()
    srv_msg.dns_question_record('client1.six.example.com', 'AAAA', 'IN')
    srv_msg.client_send_dns_query()

    misc.pass_criteria()
    srv_msg.send_wait_for_query('MUST', None)
    srv_msg.dns_option(None, 'ANSWER')

    misc.test_procedure()
    srv_msg.dns_question_record('client2.six.example.com', 'AAAA', 'IN')
    srv_msg.client_send_dns_query()

    misc.pass_criteria()
    srv_msg.send_wait_for_query('MUST', None)
    srv_msg.dns_option(None, 'ANSWER')

    #  Client 1 add
    misc.test_procedure()
    srv_msg.client_sets_value('Client', 'DUID', '00:03:00:01:ff:ff:ff:ff:ff:01')
    srv_msg.client_does_include('Client', None, 'client-id')
    srv_msg.client_does_include('Client', None, 'IA-NA')
    srv_msg.client_send_msg('SOLICIT')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', None, 'ADVERTISE')
    srv_msg.response_check_include_option('Response', None, '1')
    srv_msg.response_check_include_option('Response', None, '2')

    misc.test_procedure()
    srv_msg.client_sets_value('Client', 'DUID', '00:03:00:01:ff:ff:ff:ff:ff:01')
    srv_msg.client_save_option_count('1', 'IA_NA')
    srv_msg.client_add_saved_option_count('1', 'DONT ')
    srv_msg.client_copy_option('server-id')
    srv_msg.client_sets_value('Client', 'FQDN_domain_name', 'client1.six.example.com.')
    srv_msg.client_sets_value('Client', 'FQDN_flags', 'S')
    srv_msg.client_does_include('Client', None, 'fqdn')
    srv_msg.client_does_include('Client', None, 'client-id')
    srv_msg.client_send_msg('REQUEST')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', None, 'REPLY')
    srv_msg.response_check_include_option('Response', None, '1')
    srv_msg.response_check_include_option('Response', None, '2')
    srv_msg.response_check_include_option('Response', None, '39')
    srv_msg.response_check_option_content('Response', '39', None, 'flags', 'S')
    srv_msg.response_check_option_content('Response',
                                          '39',
                                          None,
                                          'fqdn',
                                          'client1.six.example.com.')

    misc.test_procedure()
    srv_msg.dns_question_record('client1.six.example.com', 'AAAA', 'IN')
    srv_msg.client_send_dns_query()

    misc.pass_criteria()
    srv_msg.send_wait_for_query('MUST', None)
    srv_msg.dns_option('NOT ', 'ANSWER')
    srv_msg.dns_option_content('ANSWER', None, 'rdata', '2001:db8:1::51')
    srv_msg.dns_option_content('ANSWER', None, 'rrname', 'client1.six.example.com.')

    #  Client 2 add
    misc.test_procedure()
    srv_msg.client_sets_value('Client', 'DUID', '00:03:00:01:ff:ff:ff:ff:ff:02')
    srv_msg.client_does_include('Client', None, 'client-id')
    srv_msg.client_does_include('Client', None, 'IA-NA')
    srv_msg.client_send_msg('SOLICIT')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', None, 'ADVERTISE')
    srv_msg.response_check_include_option('Response', None, '1')
    srv_msg.response_check_include_option('Response', None, '2')

    misc.test_procedure()
    srv_msg.client_sets_value('Client', 'DUID', '00:03:00:01:ff:ff:ff:ff:ff:02')
    srv_msg.client_save_option_count('2', 'IA_NA')
    srv_msg.client_save_option_count('2', 'server-id')
    srv_msg.client_add_saved_option_count('2', 'DONT ')
    srv_msg.client_sets_value('Client', 'FQDN_domain_name', 'client1.six.example.com.')
    srv_msg.client_sets_value('Client', 'FQDN_flags', 'S')
    srv_msg.client_does_include('Client', None, 'fqdn')
    srv_msg.client_does_include('Client', None, 'client-id')
    srv_msg.client_send_msg('REQUEST')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', None, 'REPLY')
    srv_msg.response_check_include_option('Response', None, '1')
    srv_msg.response_check_include_option('Response', None, '2')
    srv_msg.response_check_include_option('Response', None, '39')
    srv_msg.response_check_option_content('Response', '39', None, 'flags', 'S')
    srv_msg.response_check_option_content('Response',
                                          '39',
                                          None,
                                          'fqdn',
                                          'client1.six.example.com.')

    misc.test_procedure()
    srv_msg.dns_question_record('client1.six.example.com', 'AAAA', 'IN')
    srv_msg.client_send_dns_query()

    misc.pass_criteria()
    srv_msg.send_wait_for_query('MUST', None)
    srv_msg.dns_option('NOT ', 'ANSWER')
    srv_msg.dns_option_content('ANSWER', None, 'rdata', '2001:db8:1::51')
    srv_msg.dns_option_content('ANSWER', None, 'rrname', 'client1.six.example.com.')

    misc.test_procedure()
    srv_msg.dns_question_record('client2.six.example.com', 'AAAA', 'IN')
    srv_msg.client_send_dns_query()

    misc.pass_criteria()
    srv_msg.send_wait_for_query('MUST', None)
    srv_msg.dns_option(None, 'ANSWER')

    misc.test_procedure()
    srv_msg.client_sets_value('Client', 'DUID', '00:03:00:01:ff:ff:ff:ff:ff:02')
    srv_msg.client_add_saved_option_count('2', 'DONT ')
    srv_msg.client_sets_value('Client', 'FQDN_domain_name', 'client2.six.example.com.')
    srv_msg.client_sets_value('Client', 'FQDN_flags', 'S')
    srv_msg.client_does_include('Client', None, 'fqdn')
    srv_msg.client_does_include('Client', None, 'client-id')
    srv_msg.client_send_msg('REQUEST')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', None, 'REPLY')
    srv_msg.response_check_include_option('Response', None, '1')
    srv_msg.response_check_include_option('Response', None, '2')
    srv_msg.response_check_include_option('Response', None, '39')
    srv_msg.response_check_option_content('Response', '39', None, 'flags', 'S')
    srv_msg.response_check_option_content('Response',
                                          '39',
                                          None,
                                          'fqdn',
                                          'client2.six.example.com.')

    misc.test_procedure()
    srv_msg.dns_question_record('client2.six.example.com', 'AAAA', 'IN')
    srv_msg.client_send_dns_query()

    misc.pass_criteria()
    srv_msg.send_wait_for_query('MUST', None)
    srv_msg.dns_option('NOT ', 'ANSWER')
    srv_msg.dns_option_content('ANSWER', None, 'rdata', '2001:db8:1::52')
    srv_msg.dns_option_content('ANSWER', None, 'rrname', 'client2.six.example.com.')

    misc.test_procedure()
    srv_msg.dns_question_record('1.5.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.1.0.0.0.8.b.d.0.1.0.0.2.ip6.arpa.',
                                'PTR',
                                'IN')
    srv_msg.client_send_dns_query()

    misc.pass_criteria()
    srv_msg.send_wait_for_query('MUST', None)
    srv_msg.dns_option('NOT ', 'ANSWER')
    srv_msg.dns_option_content('ANSWER', None, 'rdata', 'client1.six.example.com.')
    srv_msg.dns_option_content('ANSWER',
                               None,
                               'rrname',
                               '1.5.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.1.0.0.0.8.b.d.0.1.0.0.2.ip6.arpa.')

    misc.test_procedure()
    srv_msg.dns_question_record('2.5.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.1.0.0.0.8.b.d.0.1.0.0.2.ip6.arpa.',
                                'PTR',
                                'IN')
    srv_msg.client_send_dns_query()

    misc.pass_criteria()
    srv_msg.send_wait_for_query('MUST', None)
    srv_msg.dns_option('NOT ', 'ANSWER')
    srv_msg.dns_option_content('ANSWER', None, 'rdata', 'client2.six.example.com.')
    srv_msg.dns_option_content('ANSWER',
                               None,
                               'rrname',
                               '2.5.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.1.0.0.0.8.b.d.0.1.0.0.2.ip6.arpa.')


@pytest.mark.v6
@pytest.mark.ddns
@pytest.mark.kea_only
@pytest.mark.notsig
@pytest.mark.forward_reverse_add
def test_ddns6_notsig_forw_and_rev_dhci_conflicts_remove_Sflag():

    misc.test_setup()
    srv_control.config_srv_subnet('2001:db8:1::/64', '2001:db8:1::51-2001:db8:1::52')
    srv_control.add_ddns_server('127.0.0.1', '53001')
    srv_control.add_ddns_server_options('enable-updates', 'true')
    srv_control.add_ddns_server_options('generated-prefix', 'six')
    srv_control.add_ddns_server_options('qualifying-suffix', 'example.com')
    srv_control.add_forward_ddns('six.example.com.', 'EMPTY_KEY')
    srv_control.add_reverse_ddns('1.0.0.0.8.b.d.0.1.0.0.2.ip6.arpa.', 'EMPTY_KEY')
    srv_control.build_and_send_config_files('SSH', 'config-file')
    srv_control.start_srv('DHCP', 'started')

    srv_control.use_dns_set_number('1')
    srv_control.start_srv('DNS', 'started')

    misc.test_procedure()
    srv_msg.dns_question_record('client1.six.example.com', 'AAAA', 'IN')
    srv_msg.client_send_dns_query()

    misc.pass_criteria()
    srv_msg.send_wait_for_query('MUST', None)
    srv_msg.dns_option(None, 'ANSWER')

    misc.test_procedure()
    srv_msg.dns_question_record('client2.six.example.com', 'AAAA', 'IN')
    srv_msg.client_send_dns_query()

    misc.pass_criteria()
    srv_msg.send_wait_for_query('MUST', None)
    srv_msg.dns_option(None, 'ANSWER')

    #  Client 1 add
    misc.test_procedure()
    srv_msg.client_sets_value('Client', 'DUID', '00:03:00:01:ff:ff:ff:ff:ff:01')
    srv_msg.client_does_include('Client', None, 'client-id')
    srv_msg.client_does_include('Client', None, 'IA-NA')
    srv_msg.client_send_msg('SOLICIT')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', None, 'ADVERTISE')
    srv_msg.response_check_include_option('Response', None, '1')
    srv_msg.response_check_include_option('Response', None, '2')

    misc.test_procedure()
    srv_msg.client_sets_value('Client', 'DUID', '00:03:00:01:ff:ff:ff:ff:ff:01')
    srv_msg.client_save_option_count('1', 'IA_NA')
    srv_msg.client_add_saved_option_count('1', 'DONT ')
    srv_msg.client_copy_option('server-id')
    srv_msg.client_sets_value('Client', 'FQDN_domain_name', 'client1.six.example.com.')
    srv_msg.client_sets_value('Client', 'FQDN_flags', 'S')
    srv_msg.client_does_include('Client', None, 'fqdn')
    srv_msg.client_does_include('Client', None, 'client-id')
    srv_msg.client_send_msg('REQUEST')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', None, 'REPLY')
    srv_msg.response_check_include_option('Response', None, '1')
    srv_msg.response_check_include_option('Response', None, '2')
    srv_msg.response_check_include_option('Response', None, '39')
    srv_msg.response_check_option_content('Response', '39', None, 'flags', 'S')
    srv_msg.response_check_option_content('Response',
                                          '39',
                                          None,
                                          'fqdn',
                                          'client1.six.example.com.')

    misc.test_procedure()
    srv_msg.dns_question_record('client1.six.example.com', 'AAAA', 'IN')
    srv_msg.client_send_dns_query()

    misc.pass_criteria()
    srv_msg.send_wait_for_query('MUST', None)
    srv_msg.dns_option('NOT ', 'ANSWER')
    srv_msg.dns_option_content('ANSWER', None, 'rdata', '2001:db8:1::51')
    srv_msg.dns_option_content('ANSWER', None, 'rrname', 'client1.six.example.com.')

    #  Client 2 add
    misc.test_procedure()
    srv_msg.client_sets_value('Client', 'DUID', '00:03:00:01:ff:ff:ff:ff:ff:02')
    srv_msg.client_does_include('Client', None, 'client-id')
    srv_msg.client_does_include('Client', None, 'IA-NA')
    srv_msg.client_send_msg('SOLICIT')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', None, 'ADVERTISE')
    srv_msg.response_check_include_option('Response', None, '1')
    srv_msg.response_check_include_option('Response', None, '2')

    misc.test_procedure()
    srv_msg.client_sets_value('Client', 'DUID', '00:03:00:01:ff:ff:ff:ff:ff:02')
    srv_msg.client_save_option_count('2', 'IA_NA')
    srv_msg.client_save_option_count('2', 'server-id')
    srv_msg.client_add_saved_option_count('2', 'DONT ')
    srv_msg.client_sets_value('Client', 'FQDN_domain_name', 'client2.six.example.com.')
    srv_msg.client_sets_value('Client', 'FQDN_flags', 'S')
    srv_msg.client_does_include('Client', None, 'fqdn')
    srv_msg.client_does_include('Client', None, 'client-id')
    srv_msg.client_send_msg('REQUEST')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', None, 'REPLY')
    srv_msg.response_check_include_option('Response', None, '1')
    srv_msg.response_check_include_option('Response', None, '2')
    srv_msg.response_check_include_option('Response', None, '39')
    srv_msg.response_check_option_content('Response', '39', None, 'flags', 'S')
    srv_msg.response_check_option_content('Response',
                                          '39',
                                          None,
                                          'fqdn',
                                          'client2.six.example.com.')

    misc.test_procedure()
    srv_msg.dns_question_record('client1.six.example.com', 'AAAA', 'IN')
    srv_msg.client_send_dns_query()

    misc.pass_criteria()
    srv_msg.send_wait_for_query('MUST', None)
    srv_msg.dns_option('NOT ', 'ANSWER')
    srv_msg.dns_option_content('ANSWER', None, 'rdata', '2001:db8:1::51')
    srv_msg.dns_option_content('ANSWER', None, 'rrname', 'client1.six.example.com.')

    misc.test_procedure()
    srv_msg.dns_question_record('client2.six.example.com', 'AAAA', 'IN')
    srv_msg.client_send_dns_query()

    misc.pass_criteria()
    srv_msg.send_wait_for_query('MUST', None)
    srv_msg.dns_option('NOT ', 'ANSWER')
    srv_msg.dns_option_content('ANSWER', None, 'rdata', '2001:db8:1::52')
    srv_msg.dns_option_content('ANSWER', None, 'rrname', 'client2.six.example.com.')

    misc.test_procedure()
    srv_msg.client_sets_value('Client', 'DUID', '00:03:00:01:ff:ff:ff:ff:ff:02')
    srv_msg.client_add_saved_option_count('2', 'DONT ')
    srv_msg.client_sets_value('Client', 'FQDN_domain_name', 'client1.six.example.com.')
    srv_msg.client_sets_value('Client', 'FQDN_flags', 'S')
    srv_msg.client_does_include('Client', None, 'fqdn')
    srv_msg.client_does_include('Client', None, 'client-id')
    srv_msg.client_send_msg('REQUEST')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', None, 'REPLY')
    srv_msg.response_check_include_option('Response', None, '1')
    srv_msg.response_check_include_option('Response', None, '2')
    srv_msg.response_check_include_option('Response', None, '39')
    srv_msg.response_check_option_content('Response', '39', None, 'flags', 'S')
    srv_msg.response_check_option_content('Response',
                                          '39',
                                          None,
                                          'fqdn',
                                          'client1.six.example.com.')

    misc.test_procedure()
    srv_msg.dns_question_record('client2.six.example.com', 'AAAA', 'IN')
    srv_msg.client_send_dns_query()

    misc.pass_criteria()
    srv_msg.send_wait_for_query('MUST', None)
    srv_msg.dns_option(None, 'ANSWER')

    misc.test_procedure()
    srv_msg.dns_question_record('1.5.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.1.0.0.0.8.b.d.0.1.0.0.2.ip6.arpa.',
                                'PTR',
                                'IN')
    srv_msg.client_send_dns_query()

    misc.pass_criteria()
    srv_msg.send_wait_for_query('MUST', None)
    srv_msg.dns_option('NOT ', 'ANSWER')
    srv_msg.dns_option_content('ANSWER', None, 'rdata', 'client1.six.example.com.')
    srv_msg.dns_option_content('ANSWER',
                               None,
                               'rrname',
                               '1.5.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.1.0.0.0.8.b.d.0.1.0.0.2.ip6.arpa.')

    misc.test_procedure()
    srv_msg.dns_question_record('2.5.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.1.0.0.0.8.b.d.0.1.0.0.2.ip6.arpa.',
                                'PTR',
                                'IN')
    srv_msg.client_send_dns_query()

    misc.pass_criteria()
    srv_msg.send_wait_for_query('MUST', None)
    srv_msg.dns_option(None, 'ANSWER')


@pytest.mark.v6
@pytest.mark.ddns
@pytest.mark.kea_only
@pytest.mark.notsig
@pytest.mark.forward_reverse_add
def test_ddns6_notsig_forw_and_rev_add_success_withoutflag_override_client():

    misc.test_setup()
    srv_control.config_srv_subnet('2001:db8:1::/64', '2001:db8:1::50-2001:db8:1::50')
    srv_control.add_ddns_server('127.0.0.1', '53001')
    srv_control.add_ddns_server_options('enable-updates', 'true')
    srv_control.add_ddns_server_options('override-client-update', 'true')
    srv_control.add_ddns_server_options('generated-prefix', 'six')
    srv_control.add_ddns_server_options('qualifying-suffix', 'example.com')
    srv_control.add_forward_ddns('six.example.com.', 'EMPTY_KEY')
    srv_control.add_reverse_ddns('1.0.0.0.8.b.d.0.1.0.0.2.ip6.arpa.', 'EMPTY_KEY')
    srv_control.build_and_send_config_files('SSH', 'config-file')
    srv_control.start_srv('DHCP', 'started')

    srv_control.use_dns_set_number('1')
    srv_control.start_srv('DNS', 'started')

    misc.test_procedure()
    srv_msg.dns_question_record('sth6.six.example.com', 'AAAA', 'IN')
    srv_msg.client_send_dns_query()

    misc.pass_criteria()
    srv_msg.send_wait_for_query('MUST', None)
    srv_msg.dns_option(None, 'ANSWER')

    misc.test_procedure()
    srv_msg.dns_question_record('0.5.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.1.0.0.0.8.b.d.0.1.0.0.2.ip6.arpa.',
                                'PTR',
                                'IN')
    srv_msg.client_send_dns_query()

    misc.pass_criteria()
    srv_msg.send_wait_for_query('MUST', None)
    srv_msg.dns_option(None, 'ANSWER')

    misc.test_procedure()
    srv_msg.client_sets_value('Client', 'DUID', '00:03:00:01:ff:ff:ff:ff:ff:01')
    srv_msg.client_does_include('Client', None, 'client-id')
    srv_msg.client_does_include('Client', None, 'IA-NA')
    srv_msg.client_send_msg('SOLICIT')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', None, 'ADVERTISE')
    srv_msg.response_check_include_option('Response', None, '1')
    srv_msg.response_check_include_option('Response', None, '2')

    misc.test_procedure()
    srv_msg.client_sets_value('Client', 'DUID', '00:03:00:01:ff:ff:ff:ff:ff:01')
    srv_msg.client_copy_option('IA_NA')
    srv_msg.client_copy_option('server-id')
    srv_msg.client_sets_value('Client', 'FQDN_domain_name', 'sth6.six.example.com.')
    srv_msg.client_does_include('Client', None, 'fqdn')
    srv_msg.client_does_include('Client', None, 'client-id')
    srv_msg.client_send_msg('REQUEST')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', None, 'REPLY')
    srv_msg.response_check_include_option('Response', None, '1')
    srv_msg.response_check_include_option('Response', None, '2')
    srv_msg.response_check_include_option('Response', None, '39')
    srv_msg.response_check_option_content('Response', '39', None, 'flags', 'SO')
    srv_msg.response_check_option_content('Response', '39', None, 'fqdn', 'sth6.six.example.com.')

    misc.test_procedure()
    srv_msg.dns_question_record('sth6.six.example.com', 'AAAA', 'IN')
    srv_msg.client_send_dns_query()

    misc.pass_criteria()
    srv_msg.send_wait_for_query('MUST', None)
    srv_msg.dns_option('NOT ', 'ANSWER')
    srv_msg.dns_option_content('ANSWER', None, 'rdata', '2001:db8:1::50')

    misc.test_procedure()
    srv_msg.dns_question_record('0.5.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.1.0.0.0.8.b.d.0.1.0.0.2.ip6.arpa.',
                                'PTR',
                                'IN')
    srv_msg.client_send_dns_query()

    misc.pass_criteria()
    srv_msg.send_wait_for_query('MUST', None)
    srv_msg.dns_option('NOT ', 'ANSWER')
    srv_msg.dns_option_content('ANSWER', None, 'rdata', 'sth6.six.example.com.')
    srv_msg.dns_option_content('ANSWER',
                               None,
                               'rrname',
                               '0.5.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.1.0.0.0.8.b.d.0.1.0.0.2.ip6.arpa.')


@pytest.mark.v6
@pytest.mark.ddns
@pytest.mark.kea_only
@pytest.mark.notsig
@pytest.mark.reverse_add
def test_ddns6_notsig_rev_success_withoutflag():

    misc.test_setup()
    srv_control.config_srv_subnet('2001:db8:1::/64', '2001:db8:1::50-2001:db8:1::50')
    srv_control.add_ddns_server('127.0.0.1', '53001')
    srv_control.add_ddns_server_options('enable-updates', 'true')
    srv_control.add_ddns_server_options('generated-prefix', 'six')
    srv_control.add_ddns_server_options('qualifying-suffix', 'example.com')
    srv_control.add_forward_ddns('six.example.com.', 'EMPTY_KEY')
    srv_control.add_reverse_ddns('1.0.0.0.8.b.d.0.1.0.0.2.ip6.arpa.', 'EMPTY_KEY')
    srv_control.build_and_send_config_files('SSH', 'config-file')
    srv_control.start_srv('DHCP', 'started')

    srv_control.use_dns_set_number('1')
    srv_control.start_srv('DNS', 'started')

    misc.test_procedure()
    srv_msg.dns_question_record('sth6.six.example.com', 'AAAA', 'IN')
    srv_msg.client_send_dns_query()

    misc.pass_criteria()
    srv_msg.send_wait_for_query('MUST', None)
    srv_msg.dns_option(None, 'ANSWER')

    misc.test_procedure()
    srv_msg.dns_question_record('0.5.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.1.0.0.0.8.b.d.0.1.0.0.2.ip6.arpa.',
                                'PTR',
                                'IN')
    srv_msg.client_send_dns_query()

    misc.pass_criteria()
    srv_msg.send_wait_for_query('MUST', None)
    srv_msg.dns_option(None, 'ANSWER')

    misc.test_procedure()
    srv_msg.client_sets_value('Client', 'DUID', '00:03:00:01:ff:ff:ff:ff:ff:01')
    srv_msg.client_does_include('Client', None, 'client-id')
    srv_msg.client_does_include('Client', None, 'IA-NA')
    srv_msg.client_send_msg('SOLICIT')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', None, 'ADVERTISE')
    srv_msg.response_check_include_option('Response', None, '1')
    srv_msg.response_check_include_option('Response', None, '2')

    misc.test_procedure()
    srv_msg.client_sets_value('Client', 'DUID', '00:03:00:01:ff:ff:ff:ff:ff:01')
    srv_msg.client_copy_option('IA_NA')
    srv_msg.client_copy_option('server-id')
    srv_msg.client_sets_value('Client', 'FQDN_domain_name', 'sth6.six.example.com.')
    srv_msg.client_does_include('Client', None, 'fqdn')
    srv_msg.client_does_include('Client', None, 'client-id')
    srv_msg.client_send_msg('REQUEST')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', None, 'REPLY')
    srv_msg.response_check_include_option('Response', None, '1')
    srv_msg.response_check_include_option('Response', None, '2')
    srv_msg.response_check_include_option('Response', None, '39')
    srv_msg.response_check_option_content('Response', '39', "NOT", 'flags', 'S')
    srv_msg.response_check_option_content('Response', '39', "NOT", 'flags', 'N')
    srv_msg.response_check_option_content('Response', '39', "NOT", 'flags', 'O')
    srv_msg.response_check_option_content('Response', '39', None, 'fqdn', 'sth6.six.example.com.')
    srv_msg.dns_log_contains(None,
                             'adding an RR at \'0.5.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.1.0.0.0.8.b.d.0.1.0.0.2.ip6.arpa\' PTR sth6.six.example.com.')

    misc.test_procedure()
    srv_msg.dns_question_record('sth6.six.example.com', 'AAAA', 'IN')
    srv_msg.client_send_dns_query()

    misc.pass_criteria()
    srv_msg.send_wait_for_query('MUST', None)
    srv_msg.dns_option(None, 'ANSWER')

    misc.test_procedure()
    srv_msg.dns_question_record('0.5.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.1.0.0.0.8.b.d.0.1.0.0.2.ip6.arpa.',
                                'PTR',
                                'IN')
    srv_msg.client_send_dns_query()

    misc.pass_criteria()
    srv_msg.send_wait_for_query('MUST', None)
    srv_msg.dns_option('NOT ', 'ANSWER')
    srv_msg.dns_option_content('ANSWER', None, 'rdata', 'sth6.six.example.com.')
    srv_msg.dns_option_content('ANSWER',
                               None,
                               'rrname',
                               '0.5.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.1.0.0.0.8.b.d.0.1.0.0.2.ip6.arpa.')


@pytest.mark.v6
@pytest.mark.ddns
@pytest.mark.kea_only
@pytest.mark.notsig
@pytest.mark.reverse_add
def test_ddns6_notsig_rev_withoutflag_notenabled():

    misc.test_setup()
    srv_control.config_srv_subnet('2001:db8:1::/64', '2001:db8:1::50-2001:db8:1::50')
    srv_control.add_ddns_server('127.0.0.1', '53001')
    srv_control.add_ddns_server_options('enable-updates', 'false')
    srv_control.add_ddns_server_options('generated-prefix', 'six')
    srv_control.add_ddns_server_options('qualifying-suffix', 'example.com')
    srv_control.add_forward_ddns('six.example.com.', 'EMPTY_KEY')
    srv_control.add_reverse_ddns('1.0.0.0.8.b.d.0.1.0.0.2.ip6.arpa.', 'EMPTY_KEY')
    srv_control.build_and_send_config_files('SSH', 'config-file')
    srv_control.start_srv('DHCP', 'started')

    srv_control.use_dns_set_number('1')
    srv_control.start_srv('DNS', 'started')

    misc.test_procedure()
    srv_msg.dns_question_record('sth6.six.example.com', 'AAAA', 'IN')
    srv_msg.client_send_dns_query()

    misc.pass_criteria()
    srv_msg.send_wait_for_query('MUST', None)
    srv_msg.dns_option(None, 'ANSWER')

    misc.test_procedure()
    srv_msg.client_sets_value('Client', 'DUID', '00:03:00:01:ff:ff:ff:ff:ff:01')
    srv_msg.client_does_include('Client', None, 'client-id')
    srv_msg.client_does_include('Client', None, 'IA-NA')
    srv_msg.client_send_msg('SOLICIT')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', None, 'ADVERTISE')
    srv_msg.response_check_include_option('Response', None, '1')
    srv_msg.response_check_include_option('Response', None, '2')

    misc.test_procedure()
    srv_msg.client_sets_value('Client', 'DUID', '00:03:00:01:ff:ff:ff:ff:ff:01')
    srv_msg.client_copy_option('IA_NA')
    srv_msg.client_copy_option('server-id')
    srv_msg.client_sets_value('Client', 'FQDN_domain_name', 'sth6.six.example.com.')
    srv_msg.client_does_include('Client', None, 'fqdn')
    srv_msg.client_does_include('Client', None, 'client-id')
    srv_msg.client_send_msg('REQUEST')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', None, 'REPLY')
    srv_msg.response_check_include_option('Response', None, '1')
    srv_msg.response_check_include_option('Response', None, '2')
    srv_msg.response_check_include_option('Response', None, '39')
    srv_msg.response_check_option_content('Response', '39', None, 'flags', 'N')
    srv_msg.response_check_option_content('Response', '39', None, 'fqdn', 'sth6.six.example.com.')
    srv_msg.dns_log_contains('NOT ',
                             'adding an RR at \'0.5.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.1.0.0.0.8.b.d.0.1.0.0.2.ip6.arpa\' PTR sth6.six.example.com.')

    misc.test_procedure()
    srv_msg.dns_question_record('sth6.six.example.com', 'AAAA', 'IN')
    srv_msg.client_send_dns_query()

    misc.pass_criteria()
    srv_msg.send_wait_for_query('MUST', None)
    srv_msg.dns_option(None, 'ANSWER')

    misc.test_procedure()
    srv_msg.dns_question_record('0.5.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.1.0.0.0.8.b.d.0.1.0.0.2.ip6.arpa.',
                                'PTR',
                                'IN')
    srv_msg.client_send_dns_query()

    misc.pass_criteria()
    srv_msg.send_wait_for_query('MUST', None)
    srv_msg.dns_option(None, 'ANSWER')


@pytest.mark.v6
@pytest.mark.ddns
@pytest.mark.kea_only
@pytest.mark.notsig
@pytest.mark.reverse_add
def test_ddns6_notsig_rev_Nflag_override_no_update():

    misc.test_setup()
    srv_control.config_srv_subnet('2001:db8:1::/64', '2001:db8:1::50-2001:db8:1::50')
    srv_control.add_ddns_server('127.0.0.1', '53001')
    srv_control.add_ddns_server_options('enable-updates', 'true')
    srv_control.add_ddns_server_options('override-no-update', 'true')
    srv_control.add_ddns_server_options('generated-prefix', 'six')
    srv_control.add_ddns_server_options('qualifying-suffix', 'example.com')
    srv_control.add_forward_ddns('six.example.com.', 'EMPTY_KEY')
    srv_control.add_reverse_ddns('1.0.0.0.8.b.d.0.1.0.0.2.ip6.arpa.', 'EMPTY_KEY')
    srv_control.build_and_send_config_files('SSH', 'config-file')
    srv_control.start_srv('DHCP', 'started')

    srv_control.use_dns_set_number('1')
    srv_control.start_srv('DNS', 'started')

    misc.test_procedure()
    srv_msg.dns_question_record('sth6.six.example.com', 'AAAA', 'IN')
    srv_msg.client_send_dns_query()

    misc.pass_criteria()
    srv_msg.send_wait_for_query('MUST', None)
    srv_msg.dns_option(None, 'ANSWER')

    misc.test_procedure()
    srv_msg.client_sets_value('Client', 'DUID', '00:03:00:01:ff:ff:ff:ff:ff:01')
    srv_msg.client_does_include('Client', None, 'client-id')
    srv_msg.client_does_include('Client', None, 'IA-NA')
    srv_msg.client_send_msg('SOLICIT')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', None, 'ADVERTISE')
    srv_msg.response_check_include_option('Response', None, '1')
    srv_msg.response_check_include_option('Response', None, '2')

    misc.test_procedure()
    srv_msg.client_sets_value('Client', 'DUID', '00:03:00:01:ff:ff:ff:ff:ff:01')
    srv_msg.client_copy_option('IA_NA')
    srv_msg.client_copy_option('server-id')
    srv_msg.client_sets_value('Client', 'FQDN_domain_name', 'sth6.six.example.com.')
    srv_msg.client_sets_value('Client', 'FQDN_flags', 'N')
    srv_msg.client_does_include('Client', None, 'fqdn')
    srv_msg.client_does_include('Client', None, 'client-id')
    srv_msg.client_send_msg('REQUEST')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', None, 'REPLY')
    srv_msg.response_check_include_option('Response', None, '1')
    srv_msg.response_check_include_option('Response', None, '2')
    srv_msg.response_check_include_option('Response', None, '39')
    srv_msg.response_check_option_content('Response', '39', None, 'flags', 'SO')
    srv_msg.response_check_option_content('Response', '39', None, 'fqdn', 'sth6.six.example.com.')
    srv_msg.dns_log_contains(None,
                             'adding an RR at \'0.5.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.1.0.0.0.8.b.d.0.1.0.0.2.ip6.arpa\' PTR sth6.six.example.com.')

    misc.test_procedure()
    srv_msg.dns_question_record('sth6.six.example.com', 'AAAA', 'IN')
    srv_msg.client_send_dns_query()

    misc.pass_criteria()
    srv_msg.send_wait_for_query('MUST', None)
    srv_msg.dns_option('NOT ', 'ANSWER')
    srv_msg.dns_option_content('ANSWER', None, 'rdata', '2001:db8:1::50')
    srv_msg.dns_option_content('ANSWER', None, 'rrname', 'sth6.six.example.com.')

    misc.test_procedure()
    srv_msg.dns_question_record('0.5.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.1.0.0.0.8.b.d.0.1.0.0.2.ip6.arpa.',
                                'PTR',
                                'IN')
    srv_msg.client_send_dns_query()

    misc.pass_criteria()
    srv_msg.send_wait_for_query('MUST', None)
    srv_msg.dns_option('NOT ', 'ANSWER')
    srv_msg.dns_option_content('ANSWER', None, 'rdata', 'sth6.six.example.com.')
    srv_msg.dns_option_content('ANSWER',
                               None,
                               'rrname',
                               '0.5.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.1.0.0.0.8.b.d.0.1.0.0.2.ip6.arpa.')
