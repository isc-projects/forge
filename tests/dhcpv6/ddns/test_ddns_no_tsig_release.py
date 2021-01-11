"""DDNS without TSIG"""

# pylint: disable=invalid-name,line-too-long

import pytest

import misc
import srv_msg
import srv_control


@pytest.mark.v6
@pytest.mark.ddns
@pytest.mark.kea_only
@pytest.mark.notsig
@pytest.mark.forward_reverse_remove
def test_ddns6_notsig_forw_and_rev_release():

    misc.test_setup()
    srv_control.config_srv_subnet('2001:db8:1::/64', '2001:db8:1::50-2001:db8:1::50')
    srv_control.add_ddns_server('127.0.0.1', '53001')
    srv_control.add_ddns_server_options('enable-updates', True)
    srv_control.add_ddns_server_options('generated-prefix', 'six')
    srv_control.add_ddns_server_options('qualifying-suffix', 'example.com')
    srv_control.add_forward_ddns('six.example.com.', 'EMPTY_KEY')
    srv_control.add_reverse_ddns('1.0.0.0.8.b.d.0.1.0.0.2.ip6.arpa.', 'EMPTY_KEY')
    srv_control.build_and_send_config_files()
    srv_control.start_srv('DHCP', 'started')

    srv_control.use_dns_set_number(1)
    srv_control.start_srv('DNS', 'started')

    misc.test_procedure()
    srv_msg.dns_question_record('sth6.six.example.com', 'AAAA', 'IN')
    srv_msg.client_send_dns_query()

    misc.pass_criteria()
    srv_msg.send_wait_for_query('MUST')
    srv_msg.dns_option('ANSWER', expect_include=False)

    misc.test_procedure()
    srv_msg.client_sets_value('Client', 'DUID', '00:03:00:01:ff:ff:ff:ff:ff:01')
    srv_msg.client_does_include('Client', 'client-id')
    srv_msg.client_does_include('Client', 'IA-NA')
    srv_msg.client_send_msg('SOLICIT')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', 'ADVERTISE')
    srv_msg.response_check_include_option(1)
    srv_msg.response_check_include_option(2)

    misc.test_procedure()
    srv_msg.client_sets_value('Client', 'DUID', '00:03:00:01:ff:ff:ff:ff:ff:01')
    srv_msg.client_save_option_count(1, 'IA_NA')
    srv_msg.client_save_option_count(1, 'server-id')
    srv_msg.client_add_saved_option_count(1, 'DONT ')
    srv_msg.client_sets_value('Client', 'FQDN_domain_name', 'sth6.six.example.com.')
    srv_msg.client_sets_value('Client', 'FQDN_flags', 'S')
    srv_msg.client_does_include('Client', 'fqdn')
    srv_msg.client_does_include('Client', 'client-id')
    srv_msg.client_send_msg('REQUEST')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', 'REPLY')
    srv_msg.response_check_include_option(1)
    srv_msg.response_check_include_option(2)
    srv_msg.response_check_include_option(39)
    srv_msg.response_check_option_content(39, 'flags', 'S')
    srv_msg.response_check_option_content(39, 'fqdn', 'sth6.six.example.com.')

    misc.test_procedure()
    srv_msg.dns_question_record('sth6.six.example.com', 'AAAA', 'IN')
    srv_msg.client_send_dns_query()

    misc.pass_criteria()
    srv_msg.send_wait_for_query('MUST')
    srv_msg.dns_option('ANSWER')
    srv_msg.dns_option_content('ANSWER', 'rdata', '2001:db8:1::50')

    misc.test_procedure()
    srv_msg.dns_question_record('0.5.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.1.0.0.0.8.b.d.0.1.0.0.2.ip6.arpa.',
                                'PTR',
                                'IN')
    srv_msg.client_send_dns_query()

    misc.pass_criteria()
    srv_msg.send_wait_for_query('MUST')
    srv_msg.dns_option('ANSWER')
    srv_msg.dns_option_content('ANSWER', 'rdata', 'sth6.six.example.com.')
    srv_msg.dns_option_content('ANSWER', 'rrname',
                               '0.5.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.1.0.0.0.8.b.d.0.1.0.0.2.ip6.arpa.')

    misc.test_procedure()
    srv_msg.client_sets_value('Client', 'DUID', '00:03:00:01:ff:ff:ff:ff:ff:01')
    srv_msg.client_add_saved_option_count(1, 'DONT ')
    srv_msg.client_does_include('Client', 'client-id')
    srv_msg.client_send_msg('RELEASE')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', 'REPLY')
    srv_msg.response_check_include_option(1)
    srv_msg.response_check_include_option(2)

    misc.test_procedure()
    srv_msg.dns_question_record('sth6.six.example.com', 'AAAA', 'IN')
    srv_msg.client_send_dns_query()

    misc.pass_criteria()
    srv_msg.send_wait_for_query('MUST')
    srv_msg.dns_option('ANSWER', expect_include=False)

    misc.test_procedure()
    srv_msg.dns_question_record('0.5.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.1.0.0.0.8.b.d.0.1.0.0.2.ip6.arpa.',
                                'PTR',
                                'IN')
    srv_msg.client_send_dns_query()

    misc.pass_criteria()
    srv_msg.send_wait_for_query('MUST')
    srv_msg.dns_option('ANSWER', expect_include=False)

#
# @pytest.mark.v6
# @pytest.mark.ddns
# @pytest.mark.kea_only
# @pytest.mark.notsig
# @pytest.mark.forward_reverse_remove
# def test_ddns6_notsig_forw_and_rev_release_notenabled():
#
#     misc.test_setup()
#     srv_control.config_srv_subnet('2001:db8:1::/64', '2001:db8:1::50-2001:db8:1::50')
#     srv_control.add_ddns_server('127.0.0.1', '53001')
#     srv_control.add_ddns_server_options('enable-updates', True)
#     srv_control.add_ddns_server_options('generated-prefix', 'six')
#     srv_control.add_ddns_server_options('qualifying-suffix', 'example.com')
#     srv_control.add_forward_ddns('six.example.com.', 'EMPTY_KEY')
#     srv_control.add_reverse_ddns('1.0.0.0.8.b.d.0.1.0.0.2.ip6.arpa.', 'EMPTY_KEY')
#     srv_control.build_and_send_config_files()
#     srv_control.start_srv('DHCP', 'started')
#
#     srv_control.use_dns_set_number(1)
#     srv_control.start_srv('DNS', 'started')
#
#     misc.test_procedure()
#     srv_msg.dns_question_record('sth6.six.example.com', 'AAAA', 'IN')
#     srv_msg.client_send_dns_query()
#
#     misc.pass_criteria()
#     srv_msg.send_wait_for_query('MUST')
#     srv_msg.dns_option('ANSWER', expect_include=False)
#
#     misc.test_procedure()
#     srv_msg.client_sets_value('Client', 'DUID', '00:03:00:01:ff:ff:ff:ff:ff:01')
#     srv_msg.client_does_include('Client', 'client-id')
#     srv_msg.client_does_include('Client', 'IA-NA')
#     srv_msg.client_send_msg('SOLICIT')
#
#     misc.pass_criteria()
#     srv_msg.send_wait_for_message('MUST', 'ADVERTISE')
#     srv_msg.response_check_include_option(1)
#     srv_msg.response_check_include_option(2)
#
#     misc.test_procedure()
#     srv_msg.client_sets_value('Client', 'DUID', '00:03:00:01:ff:ff:ff:ff:ff:01')
#     srv_msg.client_save_option_count(1, 'IA_NA')
#     srv_msg.client_save_option_count(1, 'server-id')
#     srv_msg.client_add_saved_option_count(1, 'DONT ')
#     srv_msg.client_sets_value('Client', 'FQDN_domain_name', 'sth6.six.example.com.')
#     srv_msg.client_sets_value('Client', 'FQDN_flags', 'S')
#     srv_msg.client_does_include('Client', 'fqdn')
#     srv_msg.client_does_include('Client', 'client-id')
#     srv_msg.client_send_msg('REQUEST')
#
#     misc.pass_criteria()
#     srv_msg.send_wait_for_message('MUST', 'REPLY')
#     srv_msg.response_check_include_option(1)
#     srv_msg.response_check_include_option(2)
#     srv_msg.response_check_include_option(39)
#     srv_msg.response_check_option_content(39, 'flags', 'S')
#     srv_msg.response_check_option_content(39, 'fqdn', 'sth6.six.example.com.')
#
#     misc.test_procedure()
#     srv_msg.dns_question_record('sth6.six.example.com', 'AAAA', 'IN')
#     srv_msg.client_send_dns_query()
#
#     misc.pass_criteria()
#     srv_msg.send_wait_for_query('MUST')
#     srv_msg.dns_option('ANSWER')
#     srv_msg.dns_option_content('ANSWER', 'rdata', '2001:db8:1::50')
#
#     misc.test_procedure()
#     srv_msg.dns_question_record('0.5.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.1.0.0.0.8.b.d.0.1.0.0.2.ip6.arpa.',
#                                 'PTR',
#                                 'IN')
#     srv_msg.client_send_dns_query()
#
#     misc.pass_criteria()
#     srv_msg.send_wait_for_query('MUST')
#     srv_msg.dns_option('ANSWER')
#     srv_msg.dns_option_content('ANSWER', 'rdata', 'sth6.six.example.com.')
#     srv_msg.dns_option_content('ANSWER', 'rrname',
#                                '0.5.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.1.0.0.0.8.b.d.0.1.0.0.2.ip6.arpa.')
#
#     misc.test_procedure()
#     srv_control.start_srv('DHCP', 'stopped')
#
#     misc.test_setup()
#     srv_control.config_srv_subnet('2001:db8:1::/64', '2001:db8:1::50-2001:db8:1::50')
#     srv_control.add_ddns_server('127.0.0.1', '53001')
#     srv_control.add_ddns_server_options('enable-updates', False)
#     srv_control.add_ddns_server_options('generated-prefix', 'six')
#     srv_control.add_ddns_server_options('qualifying-suffix', 'example.com')
#     srv_control.add_forward_ddns('six.example.com.', 'EMPTY_KEY')
#     srv_control.add_reverse_ddns('1.0.0.0.8.b.d.0.1.0.0.2.ip6.arpa.', 'EMPTY_KEY')
#     srv_control.build_and_send_config_files()
#     srv_control.start_srv('DHCP', 'started')
#
#     misc.test_procedure()
#     srv_msg.client_sets_value('Client', 'DUID', '00:03:00:01:ff:ff:ff:ff:ff:01')
#     srv_msg.client_add_saved_option_count(1, 'DONT ')
#     srv_msg.client_does_include('Client', 'client-id')
#     srv_msg.client_send_msg('RELEASE')
#
#     misc.pass_criteria()
#     srv_msg.send_wait_for_message('MUST', 'REPLY')
#     srv_msg.response_check_include_option(1)
#     srv_msg.response_check_include_option(2)
#
#     misc.test_procedure()
#     srv_msg.dns_question_record('sth6.six.example.com', 'AAAA', 'IN')
#     srv_msg.client_send_dns_query()
#
#     misc.pass_criteria()
#     srv_msg.send_wait_for_query('MUST')
#     srv_msg.dns_option('ANSWER')
#     srv_msg.dns_option_content('ANSWER', 'rdata', '2001:db8:1::50')
#
#     misc.test_procedure()
#     srv_msg.dns_question_record('0.5.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.1.0.0.0.8.b.d.0.1.0.0.2.ip6.arpa.',
#                                 'PTR',
#                                 'IN')
#     srv_msg.client_send_dns_query()
#
#     misc.pass_criteria()
#     srv_msg.send_wait_for_query('MUST')
#     srv_msg.dns_option('ANSWER')
#     srv_msg.dns_option_content('ANSWER', 'rdata', 'sth6.six.example.com.')
#     srv_msg.dns_option_content('ANSWER', 'rrname',
#                                '0.5.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.1.0.0.0.8.b.d.0.1.0.0.2.ip6.arpa.')
#
#
# @pytest.mark.v6
# @pytest.mark.ddns
# @pytest.mark.kea_only
# @pytest.mark.notsig
# @pytest.mark.reverse_remove
# def test_ddns6_notsig_rev_release():
#
#     misc.test_setup()
#     srv_control.config_srv_subnet('2001:db8:1::/64', '2001:db8:1::50-2001:db8:1::50')
#     srv_control.add_ddns_server('127.0.0.1', '53001')
#     srv_control.add_ddns_server_options('enable-updates', True)
#     srv_control.add_ddns_server_options('generated-prefix', 'six')
#     srv_control.add_ddns_server_options('qualifying-suffix', 'example.com')
#     srv_control.add_forward_ddns('six.example.com.', 'EMPTY_KEY')
#     srv_control.add_reverse_ddns('1.0.0.0.8.b.d.0.1.0.0.2.ip6.arpa.', 'EMPTY_KEY')
#     srv_control.build_and_send_config_files()
#     srv_control.start_srv('DHCP', 'started')
#
#     srv_control.use_dns_set_number(1)
#     srv_control.start_srv('DNS', 'started')
#
#     misc.test_procedure()
#     srv_msg.dns_question_record('sth6.six.example.com', 'AAAA', 'IN')
#     srv_msg.client_send_dns_query()
#
#     misc.pass_criteria()
#     srv_msg.send_wait_for_query('MUST')
#     srv_msg.dns_option('ANSWER', expect_include=False)
#
#     misc.test_procedure()
#     srv_msg.dns_question_record('0.5.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.1.0.0.0.8.b.d.0.1.0.0.2.ip6.arpa.',
#                                 'PTR',
#                                 'IN')
#     srv_msg.client_send_dns_query()
#
#     misc.pass_criteria()
#     srv_msg.send_wait_for_query('MUST')
#     srv_msg.dns_option('ANSWER', expect_include=False)
#
#     misc.test_procedure()
#     srv_msg.client_sets_value('Client', 'DUID', '00:03:00:01:ff:ff:ff:ff:ff:01')
#     srv_msg.client_does_include('Client', 'client-id')
#     srv_msg.client_does_include('Client', 'IA-NA')
#     srv_msg.client_send_msg('SOLICIT')
#
#     misc.pass_criteria()
#     srv_msg.send_wait_for_message('MUST', 'ADVERTISE')
#     srv_msg.response_check_include_option(1)
#     srv_msg.response_check_include_option(2)
#
#     misc.test_procedure()
#     srv_msg.client_sets_value('Client', 'DUID', '00:03:00:01:ff:ff:ff:ff:ff:01')
#     srv_msg.client_save_option_count(1, 'IA_NA')
#     srv_msg.client_save_option_count(1, 'server-id')
#     srv_msg.client_add_saved_option_count(1, 'DONT ')
#     srv_msg.client_sets_value('Client', 'FQDN_domain_name', 'sth6.six.example.com.')
#     srv_msg.client_does_include('Client', 'fqdn')
#     srv_msg.client_does_include('Client', 'client-id')
#     srv_msg.client_send_msg('REQUEST')
#
#     misc.pass_criteria()
#     srv_msg.send_wait_for_message('MUST', 'REPLY')
#     srv_msg.response_check_include_option(1)
#     srv_msg.response_check_include_option(2)
#     srv_msg.response_check_include_option(39)
#     srv_msg.response_check_option_content(39, 'flags', 'S', expect_include=False)
#     srv_msg.response_check_option_content(39, 'flags', 'N', expect_include=False)
#     srv_msg.response_check_option_content(39, 'flags', 'O', expect_include=False)
#     srv_msg.response_check_option_content(39, 'fqdn', 'sth6.six.example.com.')
#
#     misc.test_procedure()
#     srv_msg.dns_question_record('sth6.six.example.com', 'AAAA', 'IN')
#     srv_msg.client_send_dns_query()
#
#     misc.pass_criteria()
#     srv_msg.send_wait_for_query('MUST')
#     srv_msg.dns_option('ANSWER', expect_include=False)
#
#     misc.test_procedure()
#     srv_msg.dns_question_record('0.5.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.1.0.0.0.8.b.d.0.1.0.0.2.ip6.arpa.',
#                                 'PTR',
#                                 'IN')
#     srv_msg.client_send_dns_query()
#
#     misc.pass_criteria()
#     srv_msg.send_wait_for_query('MUST')
#     srv_msg.dns_option('ANSWER')
#     srv_msg.dns_option_content('ANSWER', 'rdata', 'sth6.six.example.com.')
#     srv_msg.dns_option_content('ANSWER', 'rrname',
#                                '0.5.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.1.0.0.0.8.b.d.0.1.0.0.2.ip6.arpa.')
#
#     misc.test_procedure()
#     srv_msg.client_sets_value('Client', 'DUID', '00:03:00:01:ff:ff:ff:ff:ff:01')
#     srv_msg.client_add_saved_option_count(1, 'DONT ')
#     srv_msg.client_does_include('Client', 'client-id')
#     srv_msg.client_send_msg('RELEASE')
#
#     misc.pass_criteria()
#     srv_msg.send_wait_for_message('MUST', 'REPLY')
#     srv_msg.response_check_include_option(1)
#     srv_msg.response_check_include_option(2)
#
#     misc.test_procedure()
#     srv_msg.dns_question_record('sth6.six.example.com', 'AAAA', 'IN')
#     srv_msg.client_send_dns_query()
#
#     misc.pass_criteria()
#     srv_msg.send_wait_for_query('MUST')
#     srv_msg.dns_option('ANSWER', expect_include=False)
#
#     misc.test_procedure()
#     srv_msg.dns_question_record('0.5.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.1.0.0.0.8.b.d.0.1.0.0.2.ip6.arpa.',
#                                 'PTR',
#                                 'IN')
#     srv_msg.client_send_dns_query()
#
#     misc.pass_criteria()
#     srv_msg.send_wait_for_query('MUST')
#     srv_msg.dns_option('ANSWER', expect_include=False)
#
#
# @pytest.mark.v6
# @pytest.mark.ddns
# @pytest.mark.kea_only
# @pytest.mark.notsig
# @pytest.mark.ddns_expired
# def test_ddns6_notsig_expired():
#
#     misc.test_setup()
#     srv_control.set_time('renew-timer', 1)
#     srv_control.set_time('rebind-timer', 2)
#     srv_control.set_time('preferred-lifetime', 3)
#     srv_control.set_time('valid-lifetime', 4)
#     srv_control.config_srv_subnet('2001:db8:1::/64', '2001:db8:1::50-2001:db8:1::50')
#     srv_control.add_ddns_server('127.0.0.1', '53001')
#     srv_control.add_ddns_server_options('enable-updates', True)
#     srv_control.add_ddns_server_options('generated-prefix', 'six')
#     srv_control.add_ddns_server_options('qualifying-suffix', 'example.com')
#     srv_control.add_forward_ddns('six.example.com.', 'EMPTY_KEY')
#     srv_control.add_reverse_ddns('1.0.0.0.8.b.d.0.1.0.0.2.ip6.arpa.', 'EMPTY_KEY')
#     srv_control.build_and_send_config_files()
#     srv_control.start_srv('DHCP', 'started')
#
#     srv_control.use_dns_set_number(1)
#     srv_control.start_srv('DNS', 'started')
#
#     misc.test_procedure()
#     srv_msg.dns_question_record('sth6.six.example.com', 'AAAA', 'IN')
#     srv_msg.client_send_dns_query()
#
#     misc.pass_criteria()
#     srv_msg.send_wait_for_query('MUST')
#     srv_msg.dns_option('ANSWER', expect_include=False)
#
#     misc.test_procedure()
#     srv_msg.client_sets_value('Client', 'DUID', '00:03:00:01:ff:ff:ff:ff:ff:01')
#     srv_msg.client_does_include('Client', 'client-id')
#     srv_msg.client_does_include('Client', 'IA-NA')
#     srv_msg.client_send_msg('SOLICIT')
#
#     misc.pass_criteria()
#     srv_msg.send_wait_for_message('MUST', 'ADVERTISE')
#     srv_msg.response_check_include_option(1)
#     srv_msg.response_check_include_option(2)
#
#     misc.test_procedure()
#     srv_msg.client_sets_value('Client', 'DUID', '00:03:00:01:ff:ff:ff:ff:ff:01')
#     srv_msg.client_copy_option('IA_NA')
#     srv_msg.client_copy_option('server-id')
#     srv_msg.client_sets_value('Client', 'FQDN_domain_name', 'sth6.six.example.com.')
#     srv_msg.client_sets_value('Client', 'FQDN_flags', 'S')
#     srv_msg.client_does_include('Client', 'fqdn')
#     srv_msg.client_does_include('Client', 'client-id')
#     srv_msg.client_send_msg('REQUEST')
#
#     misc.pass_criteria()
#     srv_msg.send_wait_for_message('MUST', 'REPLY')
#     srv_msg.response_check_include_option(1)
#     srv_msg.response_check_include_option(2)
#     srv_msg.response_check_include_option(39)
#     srv_msg.response_check_option_content(39, 'flags', 'S')
#     srv_msg.response_check_option_content(39, 'fqdn', 'sth6.six.example.com.')
#
#     misc.test_procedure()
#     srv_msg.dns_question_record('sth6.six.example.com', 'AAAA', 'IN')
#     srv_msg.client_send_dns_query()
#
#     misc.pass_criteria()
#     srv_msg.send_wait_for_query('MUST')
#     srv_msg.dns_option('ANSWER')
#     srv_msg.dns_option_content('ANSWER', 'rdata', '2001:db8:1::50')
#
#     misc.test_procedure()
#     srv_msg.dns_question_record('0.5.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.1.0.0.0.8.b.d.0.1.0.0.2.ip6.arpa.',
#                                 'PTR',
#                                 'IN')
#     srv_msg.client_send_dns_query()
#
#     misc.pass_criteria()
#     srv_msg.send_wait_for_query('MUST')
#     srv_msg.dns_option('ANSWER')
#     srv_msg.dns_option_content('ANSWER', 'rdata', 'sth6.six.example.com.')
#     srv_msg.dns_option_content('ANSWER',
#                                None,
#                                'rrname',
#                                '0.5.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.1.0.0.0.8.b.d.0.1.0.0.2.ip6.arpa.')
#
#     srv_msg.forge_sleep(15, 'seconds')
#
#     misc.test_procedure()
#     srv_msg.dns_question_record('sth6.six.example.com', 'AAAA', 'IN')
#     srv_msg.client_send_dns_query()
#
#     misc.pass_criteria()
#     srv_msg.send_wait_for_query('MUST')
#     srv_msg.dns_option('ANSWER', expect_include=False)
#
#     misc.test_procedure()
#     srv_msg.dns_question_record('0.5.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.1.0.0.0.8.b.d.0.1.0.0.2.ip6.arpa.',
#                                 'PTR',
#                                 'IN')
#     srv_msg.client_send_dns_query()
#
#     misc.pass_criteria()
#     srv_msg.send_wait_for_query('MUST')
#     srv_msg.dns_option('ANSWER', expect_include=False)
