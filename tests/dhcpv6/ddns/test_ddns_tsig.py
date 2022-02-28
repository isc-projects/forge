"""DDNS without TSIG"""

# pylint: disable=invalid-name,line-too-long

import pytest

import srv_control
import misc
import srv_msg

# to reduce size of the tests


def _get_lease(fqdn='sth6.six.example.com.'):
    # we don't need multiple options here
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
    srv_msg.client_sets_value('Client', 'FQDN_domain_name', fqdn)
    srv_msg.client_sets_value('Client', 'FQDN_flags', 'S')
    srv_msg.client_does_include('Client', 'fqdn')
    srv_msg.client_does_include('Client', 'client-id')
    srv_msg.client_send_msg('REQUEST')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', 'REPLY')
    # if _get_lease used twice during test it will save multiple options are release will fail
    srv_msg.client_save_option_count(1, 'IA_NA')  # save for release
    srv_msg.client_save_option_count(1, 'server-id')  # save for release
    srv_msg.response_check_include_option(1)
    srv_msg.response_check_include_option(2)
    srv_msg.response_check_include_option(39)
    srv_msg.response_check_option_content(39, 'flags', 'S')
    # we always expect this one fqdn back
    srv_msg.response_check_option_content(39, 'fqdn', 'sth6.six.example.com.')
    srv_msg.response_check_include_option(3)
    srv_msg.response_check_option_content(3, 'sub-option', 5)
    srv_msg.response_check_suboption_content(5, 3, 'addr', '2001:db8:1::50')


def _release():
    misc.test_procedure()
    srv_msg.client_sets_value('Client', 'DUID', '00:03:00:01:ff:ff:ff:ff:ff:01')
    srv_msg.client_add_saved_option_count(1)
    srv_msg.client_does_include('Client', 'client-id')
    srv_msg.client_send_msg('RELEASE')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', 'REPLY')
    srv_msg.response_check_include_option(1)
    srv_msg.response_check_include_option(2)


def _check_dns_record(expect_dns_record=True):
    misc.test_procedure()
    srv_msg.dns_question_record('sth6.six.example.com', 'AAAA', 'IN')
    srv_msg.client_send_dns_query()

    misc.pass_criteria()
    srv_msg.send_wait_for_query('MUST')
    if expect_dns_record:
        srv_msg.dns_option('ANSWER')
        srv_msg.dns_option_content('ANSWER', 'rdata', '2001:db8:1::50')
    else:
        srv_msg.dns_option('ANSWER', expect_include=False)

    misc.test_procedure()
    srv_msg.dns_question_record('0.5.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.1.0.0.0.8.b.d.0.1.0.0.2.ip6.arpa.',
                                'PTR',
                                'IN')
    srv_msg.client_send_dns_query()

    misc.pass_criteria()
    srv_msg.send_wait_for_query('MUST')
    if expect_dns_record:
        srv_msg.dns_option('ANSWER')
        srv_msg.dns_option_content('ANSWER', 'rdata', 'sth6.six.example.com.')
        srv_msg.dns_option_content('ANSWER', 'rrname',
                                   '0.5.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.1.0.0.0.8.b.d.0.1.0.0.2.ip6.arpa.')
    else:
        srv_msg.dns_option('ANSWER', expect_include=False)

    misc.test_procedure()
    srv_msg.dns_question_record('sth6.six.example.com', 'AAAA', 'IN')
    srv_msg.client_send_dns_query()

    misc.pass_criteria()
    srv_msg.send_wait_for_query('MUST')


@pytest.mark.v6
@pytest.mark.ddns
@pytest.mark.kea_only
@pytest.mark.tsig
@pytest.mark.forward_reverse_add
def test_ddns6_tsig_sha1_forw_and_rev_hostname_reservation():
    misc.test_setup()
    srv_control.config_srv_subnet('2001:db8:1::/64', '2001:db8:1::50-2001:db8:1::50')
    srv_control.add_ddns_server('127.0.0.1', '53001')
    srv_control.add_ddns_server_options('enable-updates', True)
    srv_control.add_ddns_server_options('generated-prefix', 'six')
    srv_control.add_ddns_server_options('qualifying-suffix', 'example.com')
    srv_control.add_forward_ddns('six.example.com.', 'forge.sha1.key')
    srv_control.add_reverse_ddns('1.0.0.0.8.b.d.0.1.0.0.2.ip6.arpa.', 'forge.sha1.key')
    srv_control.add_keys('forge.sha1.key', 'HMAC-SHA1', 'PN4xKZ/jDobCMlo4rpr70w==')
    srv_control.host_reservation_in_subnet('hostname',
                                           'sth6.six',
                                           0,
                                           'duid',
                                           '00:03:00:01:ff:ff:ff:ff:ff:01')

    srv_control.build_and_send_config_files()
    srv_control.start_srv('DHCP', 'started')

    srv_control.use_dns_set_number(3)
    srv_control.start_srv('DNS', 'started')

    _check_dns_record(expect_dns_record=False)
    _get_lease(fqdn='something-we-don-want-back')
    _check_dns_record()


@pytest.mark.v6
@pytest.mark.ddns
@pytest.mark.kea_only
@pytest.mark.tsig
@pytest.mark.forward_reverse_add
def test_ddns6_tsig_sha1_forw_and_rev_rapid_commit():
    misc.test_setup()
    srv_control.config_srv_subnet('2001:db8:1::/64', '2001:db8:1::50-2001:db8:1::50')
    srv_control.add_ddns_server('127.0.0.1', '53001')
    srv_control.add_ddns_server_options('enable-updates', True)
    srv_control.add_ddns_server_options('generated-prefix', 'six')
    srv_control.add_ddns_server_options('qualifying-suffix', 'example.com')
    srv_control.add_forward_ddns('six.example.com.', 'forge.sha1.key')
    srv_control.add_reverse_ddns('1.0.0.0.8.b.d.0.1.0.0.2.ip6.arpa.', 'forge.sha1.key')
    srv_control.add_keys('forge.sha1.key', 'HMAC-SHA1', 'PN4xKZ/jDobCMlo4rpr70w==')
    srv_control.set_conf_parameter_subnet('rapid-commit', True, 0)
    srv_control.build_and_send_config_files()
    srv_control.start_srv('DHCP', 'started')

    srv_control.use_dns_set_number(3)
    srv_control.start_srv('DNS', 'started')

    # make sure DNS record is missing
    _check_dns_record(expect_dns_record=False)

    misc.test_procedure()
    srv_msg.client_does_include('Client', 'rapid-commit')
    srv_msg.client_sets_value('Client', 'DUID', '00:03:00:01:ff:ff:ff:ff:ff:01')
    srv_msg.client_does_include('Client', 'IA-NA')
    srv_msg.client_sets_value('Client', 'FQDN_domain_name', 'sth6.six.example.com.')
    srv_msg.client_sets_value('Client', 'FQDN_flags', 'S')
    srv_msg.client_does_include('Client', 'fqdn')
    srv_msg.client_does_include('Client', 'client-id')
    srv_msg.client_send_msg('SOLICIT')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', 'REPLY')
    srv_msg.response_check_include_option(1)
    srv_msg.response_check_include_option(2)
    srv_msg.response_check_include_option(3)
    srv_msg.response_check_option_content(3, 'sub-option', 5)
    srv_msg.response_check_include_option(14)

    # now we want an DNS record
    _check_dns_record()


@pytest.mark.v6
@pytest.mark.ddns
@pytest.mark.kea_only
@pytest.mark.tsig
@pytest.mark.forward_reverse_add
@pytest.mark.parametrize('key_type', ['sha1', 'sha224', 'sha256', 'sha384', 'sha512', 'md5', 'multiple'])
@pytest.mark.parametrize('exchange', ['request', 'release'])
def test_ddns6_tsig_forw_rev_with_key(key_type, exchange):
    misc.test_setup()
    srv_control.config_srv_subnet('2001:db8:1::/64', '2001:db8:1::50-2001:db8:1::50')
    srv_control.add_ddns_server('127.0.0.1', '53001')
    srv_control.add_ddns_server_options('enable-updates', True)
    srv_control.add_ddns_server_options('generated-prefix', 'six')
    srv_control.add_ddns_server_options('qualifying-suffix', 'example.com')
    if key_type != 'multiple':
        srv_control.add_forward_ddns('six.example.com.', f'forge.{key_type}.key')
        srv_control.add_reverse_ddns('1.0.0.0.8.b.d.0.1.0.0.2.ip6.arpa.', f'forge.{key_type}.key')

    if key_type == 'sha1':
        srv_control.add_keys('forge.sha1.key', 'HMAC-SHA1', 'PN4xKZ/jDobCMlo4rpr70w==')
        srv_control.use_dns_set_number(3)
    elif key_type == 'sha224':
        srv_control.add_keys('forge.sha224.key', 'HMAC-SHA224', 'TxAiO5TRKkFyHSCa4erQZQ==')
        srv_control.use_dns_set_number(4)
    elif key_type == 'sha256':
        srv_control.add_keys('forge.sha256.key', 'HMAC-SHA256', '5AYMijv0rhZJyQqK/caV7g==')
        srv_control.use_dns_set_number(5)
    elif key_type == 'sha384':
        srv_control.add_keys('forge.sha384.key', 'HMAC-SHA384', '21upyvp7zcG0S2PB4+kuQQ==')
        srv_control.use_dns_set_number(6)
    elif key_type == 'sha512':
        srv_control.add_keys('forge.sha512.key', 'HMAC-SHA512', 'jBng5D6QL4f8cfLUUwE7OQ==')
        srv_control.use_dns_set_number(7)
    elif key_type == 'md5':
        srv_control.add_keys('forge.md5.key', 'HMAC-MD5', 'bX3Hs+fG/tThidQPuhK1mA==')
        srv_control.use_dns_set_number(8)
    elif key_type == 'multiple':
        srv_control.add_forward_ddns('six.example.com.', 'forge.md5.key')
        srv_control.add_reverse_ddns('1.0.0.0.8.b.d.0.1.0.0.2.ip6.arpa.', 'forge.sha512.key')
        srv_control.add_keys('forge.sha512.key', 'HMAC-SHA512', 'jBng5D6QL4f8cfLUUwE7OQ==')
        srv_control.add_keys('forge.md5.key', 'HMAC-MD5', 'bX3Hs+fG/tThidQPuhK1mA==')
        srv_control.use_dns_set_number(9)
    srv_control.build_and_send_config_files()

    srv_control.start_srv('DHCP', 'started')
    srv_control.start_srv('DNS', 'started')

    # we are always checking address 2001:db8:1::50 and sth6.six fqdn
    _check_dns_record(expect_dns_record=False)
    _get_lease()
    _check_dns_record()
    if exchange == 'release':
        # dividing this test for additional exchange may looks like an overkill
        # but it's updating DNS on release is big enough subject to have it's own test
        _release()
        # make sure DNS record is removed
        _check_dns_record(expect_dns_record=False)


@pytest.mark.v6
@pytest.mark.ddns
@pytest.mark.kea_only
@pytest.mark.tsig
@pytest.mark.forward_reverse_remove
def test_ddns6_tsig_forw_and_rev_release_notenabled():

    misc.test_setup()
    srv_control.config_srv_subnet('2001:db8:1::/64', '2001:db8:1::50-2001:db8:1::50')
    srv_control.add_ddns_server('127.0.0.1', '53001')
    srv_control.add_ddns_server_options('enable-updates', True)
    srv_control.add_ddns_server_options('generated-prefix', 'six')
    srv_control.add_ddns_server_options('qualifying-suffix', 'example.com')
    srv_control.add_forward_ddns('six.example.com.', 'forge.sha1.key')
    srv_control.add_reverse_ddns('1.0.0.0.8.b.d.0.1.0.0.2.ip6.arpa.', 'forge.sha1.key')
    srv_control.add_keys('forge.sha1.key', 'HMAC-SHA1', 'PN4xKZ/jDobCMlo4rpr70w==')
    srv_control.build_and_send_config_files()
    srv_control.start_srv('DHCP', 'started')

    srv_control.use_dns_set_number(3)
    srv_control.start_srv('DNS', 'started')

    _check_dns_record(expect_dns_record=False)
    _get_lease()
    _check_dns_record()

    misc.test_procedure()
    srv_control.start_srv('DHCP', 'stopped')

    misc.test_setup()
    srv_control.config_srv_subnet('2001:db8:1::/64', '2001:db8:1::50-2001:db8:1::50')
    srv_control.add_ddns_server('127.0.0.1', '53001')
    srv_control.add_ddns_server_options('enable-updates', False)
    srv_control.add_ddns_server_options('generated-prefix', 'six')
    srv_control.add_ddns_server_options('qualifying-suffix', 'example.com')
    srv_control.add_forward_ddns('six.example.com.', 'forge.sha1.key')
    srv_control.add_reverse_ddns('1.0.0.0.8.b.d.0.1.0.0.2.ip6.arpa.', 'forge.sha1.key')
    srv_control.add_keys('forge.sha1.key', 'HMAC-SHA1', 'PN4xKZ/jDobCMlo4rpr70w==')
    srv_control.build_and_send_config_files()
    srv_control.start_srv('DHCP', 'started')

    _release()
    _check_dns_record()
