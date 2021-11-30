"""DDNS without TSIG"""

# pylint: disable=invalid-name,line-too-long

import pytest

import misc
import srv_msg
import srv_control


def _check_dns_record(expect_dns_record=True):
    misc.test_procedure()
    srv_msg.dns_question_record('aa.four.example.com', 'A', 'IN')
    srv_msg.client_send_dns_query()

    misc.pass_criteria()
    srv_msg.send_wait_for_query('MUST')
    if expect_dns_record:
        srv_msg.dns_option('ANSWER')
        srv_msg.dns_option_content('ANSWER', 'rdata', '192.168.50.10')
        srv_msg.dns_option_content('ANSWER', 'rrname', 'aa.four.example.com.')
    else:
        srv_msg.dns_option('ANSWER', expect_include=False)

    misc.test_procedure()
    srv_msg.dns_question_record('10.50.168.192.in-addr.arpa.', 'PTR', 'IN')
    srv_msg.client_send_dns_query()

    misc.pass_criteria()
    srv_msg.send_wait_for_query('MUST')
    if expect_dns_record:
        srv_msg.dns_option('ANSWER')
        srv_msg.dns_option_content('ANSWER', 'rdata', 'aa.four.example.com.')
        srv_msg.dns_option_content('ANSWER', 'rrname', '10.50.168.192.in-addr.arpa.')
    else:
        srv_msg.dns_option('ANSWER', expect_include=False)


def _get_lease():
    misc.test_procedure()
    srv_msg.client_sets_value('Client', 'chaddr', 'ff:01:02:03:ff:04')
    srv_msg.client_send_msg('DISCOVER')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', 'OFFER')
    srv_msg.response_check_include_option(1)
    srv_msg.response_check_content('yiaddr', '192.168.50.10')
    srv_msg.response_check_option_content(1, 'value', '255.255.255.0')

    misc.test_procedure()
    srv_msg.client_copy_option('server_id')
    srv_msg.client_sets_value('Client', 'chaddr', 'ff:01:02:03:ff:04')
    srv_msg.client_does_include_with_value('requested_addr', '192.168.50.10')
    srv_msg.client_requests_option(1)
    srv_msg.client_sets_value('Client', 'FQDN_domain_name', 'aa.four.example.com.')
    srv_msg.client_sets_value('Client', 'FQDN_flags', 'S')
    srv_msg.client_does_include('Client', 'fqdn')
    srv_msg.client_send_msg('REQUEST')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', 'ACK')
    srv_msg.response_check_content('yiaddr', '192.168.50.10')
    srv_msg.response_check_include_option(1)
    srv_msg.client_save_option_count(1, 'server_id')
    srv_msg.response_check_option_content(1, 'value', '255.255.255.0')
    srv_msg.response_check_include_option(81)
    srv_msg.response_check_option_content(81, 'flags', 1)
    srv_msg.response_check_option_content(81, 'fqdn', 'aa.four.example.com.')


def _release():
    misc.test_procedure()
    srv_msg.client_add_saved_option_count(1)
    srv_msg.client_sets_value('Client', 'ciaddr', '192.168.50.10')
    srv_msg.client_send_msg('RELEASE')

    misc.pass_criteria()
    srv_msg.send_dont_wait_for_message()


@pytest.mark.v4
@pytest.mark.ddns
@pytest.mark.tsig
@pytest.mark.forward_reverse_add
@pytest.mark.parametrize('key_type', ['sha1', 'sha224', 'sha256', 'sha384', 'sha512', 'md5', 'multiple'])
@pytest.mark.parametrize('exchange', ['request', 'release'])
def test_ddns4_tsig_forw_and_rev(key_type, exchange):
    misc.test_setup()
    srv_control.config_srv_subnet('192.168.50.0/24', '192.168.50.10-192.168.50.10')
    srv_control.add_ddns_server('127.0.0.1', '53001')
    srv_control.add_ddns_server_options('enable-updates', True)
    srv_control.add_ddns_server_options('generated-prefix', 'four')
    srv_control.add_ddns_server_options('qualifying-suffix', 'example.com')

    if key_type != 'multiple':
        srv_control.add_forward_ddns('four.example.com.', f'forge.{key_type}.key')
        srv_control.add_reverse_ddns('50.168.192.in-addr.arpa.', f'forge.{key_type}.key')

    if key_type == 'sha1':
        srv_control.add_keys('forge.sha1.key', 'HMAC-SHA1', 'PN4xKZ/jDobCMlo4rpr70w==')
        srv_control.use_dns_set_number(21)
    elif key_type == 'sha224':
        srv_control.add_keys('forge.sha224.key', 'HMAC-SHA224', 'TxAiO5TRKkFyHSCa4erQZQ==')
        srv_control.use_dns_set_number(22)
    elif key_type == 'sha256':
        srv_control.add_keys('forge.sha256.key', 'HMAC-SHA256', '5AYMijv0rhZJyQqK/caV7g==')
        srv_control.use_dns_set_number(23)
    elif key_type == 'sha384':
        srv_control.add_keys('forge.sha384.key', 'HMAC-SHA384', '21upyvp7zcG0S2PB4+kuQQ==')
        srv_control.use_dns_set_number(24)
    elif key_type == 'sha512':
        srv_control.add_keys('forge.sha512.key', 'HMAC-SHA512', 'jBng5D6QL4f8cfLUUwE7OQ==')
        srv_control.use_dns_set_number(25)
    elif key_type == 'md5':
        srv_control.add_keys('forge.md5.key', 'HMAC-MD5', 'bX3Hs+fG/tThidQPuhK1mA==')
        srv_control.use_dns_set_number(26)
    elif key_type == 'multiple':
        srv_control.add_forward_ddns('four.example.com.', 'forge.md5.key')
        srv_control.add_reverse_ddns('50.168.192.in-addr.arpa.', 'forge.sha512.key')
        srv_control.add_keys('forge.sha512.key', 'HMAC-SHA512', 'jBng5D6QL4f8cfLUUwE7OQ==')
        srv_control.add_keys('forge.md5.key', 'HMAC-MD5', 'bX3Hs+fG/tThidQPuhK1mA==')
        srv_control.use_dns_set_number(27)

    srv_control.build_and_send_config_files()
    srv_control.start_srv('DHCP', 'started')
    srv_control.start_srv('DNS', 'started')

    _check_dns_record(expect_dns_record=False)
    _get_lease()
    _check_dns_record()
    if exchange == 'release':
        _release()
        _check_dns_record(expect_dns_record=False)


@pytest.mark.v4
@pytest.mark.ddns
@pytest.mark.tsig
@pytest.mark.forward_reverse_remove
def test_ddns4_tsig_forw_and_rev_release_notenabled():

    misc.test_setup()
    srv_control.config_srv_subnet('192.168.50.0/24', '192.168.50.10-192.168.50.10')
    srv_control.add_ddns_server('127.0.0.1', '53001')
    srv_control.add_ddns_server_options('enable-updates', True)
    srv_control.add_ddns_server_options('generated-prefix', 'four')
    srv_control.add_ddns_server_options('qualifying-suffix', 'example.com')
    srv_control.add_forward_ddns('four.example.com.', 'forge.sha1.key')
    srv_control.add_reverse_ddns('50.168.192.in-addr.arpa.', 'forge.sha1.key')
    srv_control.add_keys('forge.sha1.key', 'HMAC-SHA1', 'PN4xKZ/jDobCMlo4rpr70w==')
    srv_control.build_and_send_config_files()
    srv_control.start_srv('DHCP', 'started')

    srv_control.use_dns_set_number(21)
    srv_control.start_srv('DNS', 'started')

    _check_dns_record(expect_dns_record=False)
    _get_lease()
    _check_dns_record()

    misc.test_procedure()
    srv_control.start_srv('DHCP', 'stopped')

    misc.test_setup()
    srv_control.config_srv_subnet('192.168.50.0/24', '192.168.50.10-192.168.50.10')
    srv_control.add_ddns_server('127.0.0.1', '53001')
    srv_control.add_ddns_server_options('enable-updates', False)
    srv_control.add_ddns_server_options('generated-prefix', 'four')
    srv_control.add_ddns_server_options('qualifying-suffix', 'example.com')
    srv_control.add_forward_ddns('four.example.com.', 'forge.sha1.key')
    srv_control.add_reverse_ddns('50.168.192.in-addr.arpa.', 'forge.sha1.key')
    srv_control.add_keys('forge.sha1.key', 'HMAC-SHA1', 'PN4xKZ/jDobCMlo4rpr70w==')
    srv_control.build_and_send_config_files()
    srv_control.start_srv('DHCP', 'started')

    # release lease but with DNS updates disabled
    _release()
    # we still should have entry available
    _check_dns_record()


@pytest.mark.v4
@pytest.mark.ddns
@pytest.mark.kea_only
@pytest.mark.tsig
@pytest.mark.forward_reverse_add
def test_ddns4_tsig_sha1_forw_and_rev_hostname_reservation():
    misc.test_setup()
    srv_control.config_srv_subnet('192.168.50.10/24', '192.168.50.10-192.168.50.10')
    srv_control.add_ddns_server('127.0.0.1', '53001')
    srv_control.add_ddns_server_options('enable-updates', True)
    srv_control.add_ddns_server_options('generated-prefix', 'four')
    srv_control.add_ddns_server_options('qualifying-suffix', 'example.com.')
    srv_control.add_forward_ddns('four.example.com.', 'forge.sha1.key')
    srv_control.add_reverse_ddns('50.168.192.in-addr.arpa.', 'forge.sha1.key')
    srv_control.add_keys('forge.sha1.key', 'HMAC-SHA1', 'PN4xKZ/jDobCMlo4rpr70w==')
    srv_control.host_reservation_in_subnet('hostname',
                                           'aa.four',
                                           0,
                                           'hw-address',
                                           'ff:01:02:03:ff:04')

    srv_control.build_and_send_config_files()
    srv_control.start_srv('DHCP', 'started')

    srv_control.use_dns_set_number(21)
    srv_control.start_srv('DNS', 'started')

    _check_dns_record(expect_dns_record=False)

    misc.test_procedure()
    srv_msg.client_sets_value('Client', 'chaddr', 'ff:01:02:03:ff:04')
    srv_msg.client_send_msg('DISCOVER')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', 'OFFER')
    srv_msg.response_check_include_option(1)
    srv_msg.response_check_content('yiaddr', '192.168.50.10')
    srv_msg.response_check_option_content(1, 'value', '255.255.255.0')

    misc.test_procedure()
    srv_msg.client_copy_option('server_id')
    srv_msg.client_sets_value('Client', 'chaddr', 'ff:01:02:03:ff:04')
    srv_msg.client_does_include_with_value('requested_addr', '192.168.50.10')
    srv_msg.client_requests_option(1)
    srv_msg.client_sets_value('Client', 'FQDN_domain_name', 'blabla')
    srv_msg.client_sets_value('Client', 'FQDN_flags', 'S')
    srv_msg.client_does_include('Client', 'fqdn')
    srv_msg.client_send_msg('REQUEST')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', 'ACK')
    srv_msg.response_check_content('yiaddr', '192.168.50.10')
    srv_msg.response_check_include_option(1)
    srv_msg.client_save_option_count(1, 'server_id')
    srv_msg.response_check_option_content(1, 'value', '255.255.255.0')
    srv_msg.response_check_include_option(81)
    srv_msg.response_check_option_content(81, 'flags', 1)
    srv_msg.response_check_option_content(81, 'fqdn', 'aa.four.example.com.')

    _check_dns_record()
