"""DDNS without TSIG"""

import pytest
import misc
import srv_control
import srv_msg

# importing directly from server definitions is not usual way we do, but I don't want to change kea related code
from softwaresupport.isc_dhcp6_server.functions_ddns import add_forward_ddns, add_reverse_ddns


@pytest.mark.v6
@pytest.mark.ddns
@pytest.mark.dhcpd
def test_ddns6_tsig_sha1_forw_and_rev():
    """new-ddns6.tsig-sha1-forw_and_rev"""
    misc.test_setup()
    srv_control.config_srv_subnet('2001:db8:1::/64', '2001:db8:1::50-2001:db8:1::50')
    srv_control.add_ddns_server('127.0.0.1', '53001')
    srv_control.add_ddns_server_options('ddns-update-style', 'interim')
    # DDNS server is configured with generated-prefix option set to six.
    # DDNS server is configured with qualifying-suffix option set to example.com.
    add_forward_ddns('six.example.com.', 'forge.sha1.key', '2001:db8:1::1000')
    add_reverse_ddns('1.0.0.0.8.b.d.0.1.0.0.2.ip6.arpa.', 'forge.sha1.key', '2001:db8:1::1000')
    srv_control.add_keys('forge.sha1.key', 'HMAC-SHA1', 'PN4xKZ/jDobCMlo4rpr70w==')
    srv_control.build_and_send_config_files()
    srv_control.start_srv('DHCP', 'started')

    srv_control.use_dns_set_number(3)
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
    srv_msg.client_copy_option('IA_NA')
    srv_msg.client_copy_option('server-id')
    srv_msg.client_sets_value('Client', 'FQDN_domain_name', 'sth6.six.example.com.')
    srv_msg.client_sets_value('Client', 'FQDN_flags', 'S')
    srv_msg.client_does_include('Client', 'fqdn')
    srv_msg.client_does_include('Client', 'client-id')
    srv_msg.client_send_msg('REQUEST')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', 'REPLY')
    srv_msg.response_check_include_option(1)
    srv_msg.response_check_include_option(2)
    # Response MUST include option 39.
    # Response option 39 MUST contain flags 1. #later make it 's' 'n' and 'o'
    # Response option 39 MUST contain fqdn sth6.six.example.com.

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


@pytest.mark.v6
@pytest.mark.ddns
@pytest.mark.dhcpd
def test_ddns6_tsig_sha224_forw_and_rev():
    """new-ddns6.tsig-sha224-forw_and_rev"""

    misc.test_setup()
    srv_control.config_srv_subnet('2001:db8:1::/64', '2001:db8:1::50-2001:db8:1::50')
    srv_control.add_ddns_server('127.0.0.1', '53001')
    srv_control.add_ddns_server_options('ddns-update-style', 'interim')
    # DDNS server is configured with generated-prefix option set to six.
    # DDNS server is configured with qualifying-suffix option set to example.com.
    add_forward_ddns('six.example.com.',
                     'forge.sha224.key',
                     '2001:db8:1::1000')
    add_reverse_ddns('1.0.0.0.8.b.d.0.1.0.0.2.ip6.arpa.',
                     'forge.sha224.key',
                     '2001:db8:1::1000')
    srv_control.add_keys('forge.sha224.key', 'HMAC-SHA224', 'TxAiO5TRKkFyHSCa4erQZQ==')
    srv_control.build_and_send_config_files()
    srv_control.start_srv('DHCP', 'started')

    srv_control.use_dns_set_number(4)
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
    srv_msg.client_copy_option('IA_NA')
    srv_msg.client_copy_option('server-id')
    srv_msg.client_sets_value('Client', 'FQDN_domain_name', 'sth6.six.example.com.')
    srv_msg.client_sets_value('Client', 'FQDN_flags', 'S')
    srv_msg.client_does_include('Client', 'fqdn')
    srv_msg.client_does_include('Client', 'client-id')
    srv_msg.client_send_msg('REQUEST')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', 'REPLY')
    srv_msg.response_check_include_option(1)
    srv_msg.response_check_include_option(2)
    # Response MUST include option 39.
    # Response option 39 MUST contain flags 1. #later make it 's' 'n' and 'o'
    # Response option 39 MUST contain fqdn sth6.six.example.com.

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


@pytest.mark.v6
@pytest.mark.ddns
@pytest.mark.dhcpd
def test_ddns6_tsig_sha256_forw_and_rev():
    """new-ddns6.tsig-sha256-forw_and_rev"""

    misc.test_setup()
    srv_control.config_srv_subnet('2001:db8:1::/64', '2001:db8:1::50-2001:db8:1::50')
    srv_control.add_ddns_server('127.0.0.1', '53001')
    srv_control.add_ddns_server_options('ddns-update-style', 'interim')
    # DDNS server is configured with generated-prefix option set to six.
    # DDNS server is configured with qualifying-suffix option set to example.com.
    add_forward_ddns('six.example.com.',
                     'forge.sha256.key',
                     '2001:db8:1::1000')
    add_reverse_ddns('1.0.0.0.8.b.d.0.1.0.0.2.ip6.arpa.',
                     'forge.sha256.key',
                     '2001:db8:1::1000')
    srv_control.add_keys('forge.sha256.key', 'HMAC-SHA256', '5AYMijv0rhZJyQqK/caV7g==')
    srv_control.build_and_send_config_files()
    srv_control.start_srv('DHCP', 'started')

    srv_control.use_dns_set_number(5)
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
    srv_msg.client_copy_option('IA_NA')
    srv_msg.client_copy_option('server-id')
    srv_msg.client_sets_value('Client', 'FQDN_domain_name', 'sth6.six.example.com.')
    srv_msg.client_sets_value('Client', 'FQDN_flags', 'S')
    srv_msg.client_does_include('Client', 'fqdn')
    srv_msg.client_does_include('Client', 'client-id')
    srv_msg.client_send_msg('REQUEST')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', 'REPLY')
    srv_msg.response_check_include_option(1)
    srv_msg.response_check_include_option(2)
    # Response MUST include option 39.
    # Response option 39 MUST contain flags 1. #later make it 's' 'n' and 'o'
    # Response option 39 MUST contain fqdn sth6.six.example.com.

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


@pytest.mark.v6
@pytest.mark.ddns
@pytest.mark.dhcpd
def test_ddns6_tsig_sha384_forw_and_rev():
    """new-ddns6.tsig-sha384-forw_and_rev"""

    misc.test_setup()
    srv_control.config_srv_subnet('2001:db8:1::/64', '2001:db8:1::50-2001:db8:1::50')
    srv_control.add_ddns_server('127.0.0.1', '53001')
    srv_control.add_ddns_server_options('ddns-update-style', 'interim')
    # DDNS server is configured with generated-prefix option set to six.
    # DDNS server is configured with qualifying-suffix option set to example.com.
    add_forward_ddns('six.example.com.',
                     'forge.sha384.key',
                     '2001:db8:1::1000')
    add_reverse_ddns('1.0.0.0.8.b.d.0.1.0.0.2.ip6.arpa.',
                     'forge.sha384.key',
                     '2001:db8:1::1000')
    srv_control.add_keys('forge.sha384.key', 'HMAC-SHA384', '21upyvp7zcG0S2PB4+kuQQ==')
    srv_control.build_and_send_config_files()
    srv_control.start_srv('DHCP', 'started')

    srv_control.use_dns_set_number(6)
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
    srv_msg.client_copy_option('IA_NA')
    srv_msg.client_copy_option('server-id')
    srv_msg.client_sets_value('Client', 'FQDN_domain_name', 'sth6.six.example.com.')
    srv_msg.client_sets_value('Client', 'FQDN_flags', 'S')
    srv_msg.client_does_include('Client', 'fqdn')
    srv_msg.client_does_include('Client', 'client-id')
    srv_msg.client_send_msg('REQUEST')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', 'REPLY')
    srv_msg.response_check_include_option(1)
    srv_msg.response_check_include_option(2)
    # Response MUST include option 39.
    # Response option 39 MUST contain flags 1. #later make it 's' 'n' and 'o'
    # Response option 39 MUST contain fqdn sth6.six.example.com.

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


@pytest.mark.v6
@pytest.mark.ddns
@pytest.mark.dhcpd
def test_ddns6_tsig_sha512_forw_and_rev():
    """new-ddns6.tsig-sha512-forw_and_rev"""

    misc.test_setup()
    srv_control.config_srv_subnet('2001:db8:1::/64', '2001:db8:1::50-2001:db8:1::50')
    srv_control.add_ddns_server('127.0.0.1', '53001')
    srv_control.add_ddns_server_options('ddns-update-style', 'interim')
    # DDNS server is configured with generated-prefix option set to six.
    # DDNS server is configured with qualifying-suffix option set to example.com.
    add_forward_ddns('six.example.com.',
                     'forge.sha512.key',
                     '2001:db8:1::1000')
    add_reverse_ddns('1.0.0.0.8.b.d.0.1.0.0.2.ip6.arpa.',
                     'forge.sha512.key',
                     '2001:db8:1::1000')
    srv_control.add_keys('forge.sha512.key', 'HMAC-SHA512', 'jBng5D6QL4f8cfLUUwE7OQ==')
    srv_control.build_and_send_config_files()
    srv_control.start_srv('DHCP', 'started')

    srv_control.use_dns_set_number(7)
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
    srv_msg.client_copy_option('IA_NA')
    srv_msg.client_copy_option('server-id')
    srv_msg.client_sets_value('Client', 'FQDN_domain_name', 'sth6.six.example.com.')
    srv_msg.client_sets_value('Client', 'FQDN_flags', 'S')
    srv_msg.client_does_include('Client', 'fqdn')
    srv_msg.client_does_include('Client', 'client-id')
    srv_msg.client_send_msg('REQUEST')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', 'REPLY')
    srv_msg.response_check_include_option(1)
    srv_msg.response_check_include_option(2)
    # Response MUST include option 39.
    # Response option 39 MUST contain flags 1. #later make it 's' 'n' and 'o'
    # Response option 39 MUST contain fqdn sth6.six.example.com.

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


@pytest.mark.v6
@pytest.mark.ddns
@pytest.mark.dhcpd
def test_ddns6_tsig_md5_forw_and_rev():
    """new-ddns6.tsig-md5-forw_and_rev"""

    misc.test_setup()
    srv_control.config_srv_subnet('2001:db8:1::/64', '2001:db8:1::50-2001:db8:1::50')
    srv_control.add_ddns_server('127.0.0.1', '53001')
    srv_control.add_ddns_server_options('ddns-update-style', 'interim')
    # DDNS server is configured with generated-prefix option set to six.
    # DDNS server is configured with qualifying-suffix option set to example.com.
    add_forward_ddns('six.example.com.',
                     'forge.md5.key',
                     '2001:db8:1::1000')
    add_reverse_ddns('1.0.0.0.8.b.d.0.1.0.0.2.ip6.arpa.',
                     'forge.md5.key',
                     '2001:db8:1::1000')
    srv_control.add_keys('forge.md5.key', 'HMAC-MD5', 'bX3Hs+fG/tThidQPuhK1mA==')
    srv_control.build_and_send_config_files()
    srv_control.start_srv('DHCP', 'started')

    srv_control.use_dns_set_number(8)
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
    srv_msg.client_copy_option('IA_NA')
    srv_msg.client_copy_option('server-id')
    srv_msg.client_sets_value('Client', 'FQDN_domain_name', 'sth6.six.example.com.')
    srv_msg.client_sets_value('Client', 'FQDN_flags', 'S')
    srv_msg.client_does_include('Client', 'fqdn')
    srv_msg.client_does_include('Client', 'client-id')
    srv_msg.client_send_msg('REQUEST')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', 'REPLY')
    srv_msg.response_check_include_option(1)
    srv_msg.response_check_include_option(2)
    # Response MUST include option 39.
    # Response option 39 MUST contain flags 1. #later make it 's' 'n' and 'o'
    # Response option 39 MUST contain fqdn sth6.six.example.com.

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


@pytest.mark.v6
@pytest.mark.ddns
@pytest.mark.dhcpd
def test_ddns6_tsig_multi_key_forw_and_rev():
    """new-ddns6.tsig-multi-key-forw_and_rev"""

    misc.test_setup()
    srv_control.config_srv_subnet('2001:db8:1::/64', '2001:db8:1::50-2001:db8:1::50')
    srv_control.add_ddns_server('127.0.0.1', '53001')
    srv_control.add_ddns_server_options('ddns-update-style', 'interim')
    # DDNS server is configured with generated-prefix option set to six.
    # DDNS server is configured with qualifying-suffix option set to example.com.
    add_forward_ddns('six.example.com.',
                     'forge.md5.key',
                     '2001:db8:1::1000')
    add_reverse_ddns('1.0.0.0.8.b.d.0.1.0.0.2.ip6.arpa.',
                     'forge.sha512.key',
                     '2001:db8:1::1000')
    srv_control.add_keys('forge.sha512.key', 'HMAC-SHA512', 'jBng5D6QL4f8cfLUUwE7OQ==')
    srv_control.add_keys('forge.md5.key', 'HMAC-MD5', 'bX3Hs+fG/tThidQPuhK1mA==')
    srv_control.build_and_send_config_files()
    srv_control.start_srv('DHCP', 'started')

    srv_control.use_dns_set_number(9)
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
    srv_msg.client_copy_option('IA_NA')
    srv_msg.client_copy_option('server-id')
    srv_msg.client_sets_value('Client', 'FQDN_domain_name', 'sth6.six.example.com.')
    srv_msg.client_sets_value('Client', 'FQDN_flags', 'S')
    srv_msg.client_does_include('Client', 'fqdn')
    srv_msg.client_does_include('Client', 'client-id')
    srv_msg.client_send_msg('REQUEST')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', 'REPLY')
    srv_msg.response_check_include_option(1)
    srv_msg.response_check_include_option(2)
    # Response MUST include option 39.
    # Response option 39 MUST contain flags 1. #later make it 's' 'n' and 'o'
    # Response option 39 MUST contain fqdn sth6.six.example.com.

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
