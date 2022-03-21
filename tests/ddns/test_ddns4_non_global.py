"""DDNS configured non global level"""

# pylint: disable=invalid-name,line-too-long

import pytest

import misc
import srv_control
import srv_msg
from forge_cfg import world


def _resend_ddns(address, exp_result=0):
    cmd = dict(command="lease4-resend-ddns", arguments={"ip-address": address})
    return srv_msg.send_ctrl_cmd(cmd, exp_result=exp_result, channel='socket')


def _check_fqdn_record(fqdn, address='', expect='notempty'):
    # check new DNS entry
    misc.test_procedure()
    srv_msg.dns_question_record(fqdn, 'A', 'IN')
    srv_msg.client_send_dns_query()
    if expect == 'empty':
        misc.pass_criteria()
        srv_msg.send_wait_for_query('MUST')
        srv_msg.dns_option('ANSWER', expect_include=False)
    else:
        misc.pass_criteria()
        srv_msg.send_wait_for_query('MUST')
        srv_msg.dns_option('ANSWER')
        srv_msg.dns_option_content('ANSWER', 'rdata', address)
        srv_msg.dns_option_content('ANSWER', 'rrname', fqdn)


def _check_address_record(fqdn, arpa):
    misc.test_procedure()
    srv_msg.dns_question_record(arpa, 'PTR', 'IN')
    srv_msg.client_send_dns_query()

    misc.pass_criteria()
    srv_msg.send_wait_for_query('MUST')
    srv_msg.dns_option('ANSWER')
    srv_msg.dns_option_content('ANSWER', 'rdata', fqdn)
    srv_msg.dns_option_content('ANSWER', 'rrname', arpa)


def _get_address(mac, fqdn, address):
    misc.test_procedure()
    srv_msg.client_sets_value('Client', 'chaddr', mac)
    srv_msg.client_send_msg('DISCOVER')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', 'OFFER')
    srv_msg.response_check_content('yiaddr', address)

    misc.test_procedure()
    srv_msg.client_copy_option('server_id')
    srv_msg.client_does_include_with_value('requested_addr', address)
    srv_msg.client_sets_value('Client', 'FQDN_domain_name', fqdn)
    srv_msg.client_sets_value('Client', 'FQDN_flags', 'S')
    srv_msg.client_does_include('Client', 'fqdn')
    srv_msg.client_send_msg('REQUEST')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', 'ACK')
    srv_msg.response_check_content('yiaddr', address)
    srv_msg.response_check_include_option(81)
    srv_msg.response_check_option_content(81, 'flags', 1)
    srv_msg.response_check_option_content(81, 'fqdn', fqdn)


def _get_address_and_update_ddns(mac=None, fqdn=None, address=None, arpa=None):
    # checking if record is indeed empty on start
    _check_fqdn_record(fqdn, expect='empty')
    # getting new address that should also generate DDNS entry
    _get_address(mac, fqdn, address)
    # checking both forward and reverse DNS entries
    _check_fqdn_record(fqdn, address=address)
    _check_address_record(fqdn, arpa)


@pytest.mark.v4
@pytest.mark.ddns
def test_ddns4_subnet():
    misc.test_setup()
    # simple case, ddns configuration in subnet - get and addres and dns entry
    srv_control.config_srv_subnet('192.168.50.0/24', '192.168.50.10-192.168.50.10')

    world.dhcp_cfg["subnet4"][0].update({"ddns-send-updates": True,
                                         "ddns-generated-prefix": "abc",
                                         "ddns-qualifying-suffix": "example.com"})

    srv_control.shared_subnet('192.168.50.0/24', 0)
    srv_control.set_conf_parameter_shared_subnet('name', '"name-abc"', 0)
    srv_control.set_conf_parameter_shared_subnet('interface', '"$(SERVER_IFACE)"', 0)

    srv_control.add_ddns_server('127.0.0.1', '53001')
    srv_control.add_ddns_server_options('enable-updates', True)
    srv_control.add_forward_ddns('four.example.com.', 'EMPTY_KEY')
    srv_control.add_reverse_ddns('50.168.192.in-addr.arpa.', 'EMPTY_KEY')

    srv_control.build_and_send_config_files()
    srv_control.start_srv('DHCP', 'started')

    srv_control.start_srv('DNS', 'started', config_set=32)

    _get_address_and_update_ddns(mac='00:00:00:00:00:01', fqdn='aa.four.example.com.',
                                 address='192.168.50.10', arpa='10.50.168.192.in-addr.arpa.')


@pytest.mark.v4
@pytest.mark.ddns
def test_ddns4_shared_network():
    misc.test_setup()
    # simple case, ddns configuration in shared network - get and addres and dns entry
    srv_control.config_srv_subnet('192.168.50.0/24', '192.168.50.10-192.168.50.10')

    srv_control.shared_subnet('192.168.50.0/24', 0)
    srv_control.set_conf_parameter_shared_subnet('name', '"name-abc"', 0)
    srv_control.set_conf_parameter_shared_subnet('interface', '"$(SERVER_IFACE)"', 0)

    world.dhcp_cfg["shared-networks"][0].update({"ddns-send-updates": True,
                                                 "ddns-generated-prefix": "abc",
                                                 "ddns-qualifying-suffix": "example.com"})

    srv_control.add_ddns_server('127.0.0.1', '53001')
    srv_control.add_ddns_server_options('enable-updates', True)
    srv_control.add_forward_ddns('four.example.com.', 'EMPTY_KEY')
    srv_control.add_reverse_ddns('50.168.192.in-addr.arpa.', 'EMPTY_KEY')

    srv_control.build_and_send_config_files()
    srv_control.start_srv('DHCP', 'started')

    srv_control.start_srv('DNS', 'started', config_set=32)

    _get_address_and_update_ddns(mac='00:00:00:00:00:01', fqdn='aa.four.example.com.',
                                 address='192.168.50.10', arpa='10.50.168.192.in-addr.arpa.')


@pytest.mark.v4
@pytest.mark.ddns
def test_ddns4_gloabl():
    misc.test_setup()
    # simple case, ddns configuration in global - get and addres and dns entry
    srv_control.config_srv_subnet('192.168.50.0/24', '192.168.50.10-192.168.50.10')

    srv_control.shared_subnet('192.168.50.0/24', 0)
    srv_control.set_conf_parameter_shared_subnet('name', '"name-abc"', 0)
    srv_control.set_conf_parameter_shared_subnet('interface', '"$(SERVER_IFACE)"', 0)

    world.dhcp_cfg.update({"ddns-send-updates": True,
                           "ddns-generated-prefix": "abc",
                           "ddns-qualifying-suffix": "example.com"})

    srv_control.add_ddns_server('127.0.0.1', '53001')
    srv_control.add_ddns_server_options('enable-updates', True)
    srv_control.add_forward_ddns('four.example.com.', 'EMPTY_KEY')
    srv_control.add_reverse_ddns('50.168.192.in-addr.arpa.', 'EMPTY_KEY')

    srv_control.build_and_send_config_files()
    srv_control.start_srv('DHCP', 'started')

    srv_control.start_srv('DNS', 'started', config_set=32)

    _get_address_and_update_ddns(mac='00:00:00:00:00:01', fqdn='aa.four.example.com.',
                                 address='192.168.50.10', arpa='10.50.168.192.in-addr.arpa.')


@pytest.mark.v4
@pytest.mark.ddns
def test_ddns4_all_levels_resend_command():
    misc.test_setup()
    srv_control.open_control_channel()
    srv_control.add_hooks('libdhcp_lease_cmds.so')
    srv_control.config_srv_subnet('192.168.50.0/24', '192.168.50.10-192.168.50.10')
    srv_control.config_srv_another_subnet_no_interface('192.168.51.0/24',
                                                       '192.168.51.10-192.168.51.10')
    srv_control.config_srv_another_subnet_no_interface('192.168.52.0/24',
                                                       '192.168.52.10-192.168.52.10')

    # let's get 3 different ddns settings, global, shared-network and subnet.
    world.dhcp_cfg.update({"ddns-send-updates": True,
                           "ddns-generated-prefix": "six",
                           "ddns-qualifying-suffix": "example.com"})

    world.dhcp_cfg["subnet4"][1].update({"ddns-send-updates": True,
                                         "ddns-generated-prefix": "abc",
                                         "ddns-qualifying-suffix": "example.com"})

    srv_control.shared_subnet('192.168.50.0/24', 0)
    srv_control.shared_subnet('192.168.51.0/24', 0)
    srv_control.shared_subnet('192.168.52.0/24', 0)
    srv_control.set_conf_parameter_shared_subnet('name', '"name-abc"', 0)
    srv_control.set_conf_parameter_shared_subnet('interface', '"$(SERVER_IFACE)"', 0)

    world.dhcp_cfg["shared-networks"][0].update({"ddns-send-updates": True,
                                                 "ddns-generated-prefix": "xyz",
                                                 "ddns-qualifying-suffix": "example.com"})

    srv_control.add_ddns_server('127.0.0.1', '53001')
    srv_control.add_ddns_server_options('enable-updates', True)
    srv_control.add_forward_ddns('four.example.com.', 'EMPTY_KEY')
    srv_control.add_forward_ddns('five.example.com.', 'EMPTY_KEY')
    srv_control.add_forward_ddns('three.example.com.', 'EMPTY_KEY')
    srv_control.add_reverse_ddns('50.168.192.in-addr.arpa.', 'EMPTY_KEY')
    srv_control.add_reverse_ddns('51.168.192.in-addr.arpa.', 'EMPTY_KEY')
    srv_control.add_reverse_ddns('52.168.192.in-addr.arpa.', 'EMPTY_KEY')

    srv_control.print_cfg()
    srv_control.print_cfg(service='DDNS')
    srv_control.build_and_send_config_files()
    srv_control.start_srv('DHCP', 'started')

    srv_control.start_srv('DNS', 'started', config_set=32)

    _get_address_and_update_ddns(mac='ff:ff:ff:ff:ff:01', fqdn='sth4.four.example.com.',
                                 address='192.168.50.10', arpa='10.50.168.192.in-addr.arpa.')

    _get_address_and_update_ddns(mac='ff:ff:ff:ff:ff:02', fqdn='some.five.example.com.',
                                 address='192.168.51.10', arpa='10.51.168.192.in-addr.arpa.')

    _get_address_and_update_ddns(mac='ff:ff:ff:ff:ff:03', fqdn='record.three.example.com.',
                                 address='192.168.52.10', arpa='10.52.168.192.in-addr.arpa.')

    # stop bind, remove data files, start bind with empty zones
    srv_control.start_srv('DNS', 'stopped')
    srv_control.clear_some_data('all', service='DNS')
    srv_control.start_srv('DNS', 'started', config_set=32)
    # check is all records were removed
    _check_fqdn_record("sth4.four.example.com.", expect='empty')
    _check_fqdn_record("some.five.example.com.", expect='empty')
    _check_fqdn_record("record.three.example.com.", expect='empty')

    response = _resend_ddns('192.168.50.100', exp_result=3)
    assert response["text"] == "No lease found for: 192.168.50.100"
    response = _resend_ddns('192.168.50.10', exp_result=0)
    assert response["text"] == "NCR generated for: 192.168.50.10, hostname: sth4.four.example.com."
    response = _resend_ddns('192.168.51.10', exp_result=0)
    assert response["text"] == "NCR generated for: 192.168.51.10, hostname: some.five.example.com."
    response = _resend_ddns('192.168.52.10', exp_result=0)
    assert response["text"] == "NCR generated for: 192.168.52.10, hostname: record.three.example.com."

    _check_fqdn_record("sth4.four.example.com.", address='192.168.50.10')
    _check_fqdn_record("some.five.example.com.", address='192.168.51.10')
    _check_fqdn_record("record.three.example.com.", address='192.168.52.10')

    _check_address_record("sth4.four.example.com.",
                          '10.50.168.192.in-addr.arpa.')
    _check_address_record("some.five.example.com.",
                          '10.51.168.192.in-addr.arpa.')
    _check_address_record("record.three.example.com.",
                          '10.52.168.192.in-addr.arpa.')


@pytest.mark.v4
@pytest.mark.ddns
def test_ddns4_all_levels_resend_without_ddns():
    misc.test_setup()
    srv_control.open_control_channel()
    srv_control.add_hooks('libdhcp_lease_cmds.so')
    srv_control.config_srv_subnet('192.168.50.0/24', '192.168.50.10-192.168.50.10')
    srv_control.config_srv_another_subnet_no_interface('192.168.51.0/24',
                                                       '192.168.51.10-192.168.51.10')

    world.dhcp_cfg["subnet4"][0].update({"ddns-send-updates": True,
                                         "ddns-generated-prefix": "six",
                                         "ddns-qualifying-suffix": "example.com"})

    srv_control.shared_subnet('192.168.50.0/24', 0)
    srv_control.shared_subnet('192.168.51.0/24', 0)
    srv_control.set_conf_parameter_shared_subnet('name', '"name-abc"', 0)
    srv_control.set_conf_parameter_shared_subnet('interface', '"$(SERVER_IFACE)"', 0)

    srv_control.add_ddns_server('127.0.0.1', '53001')
    srv_control.add_ddns_server_options('enable-updates', True)
    srv_control.add_forward_ddns('four.example.com.', 'EMPTY_KEY')
    srv_control.add_reverse_ddns('50.168.192.in-addr.arpa.', 'EMPTY_KEY')

    srv_control.build_and_send_config_files()
    srv_control.start_srv('DHCP', 'started')
    srv_control.start_srv('DNS', 'started', config_set=32)

    _get_address_and_update_ddns(mac='ff:ff:ff:ff:ff:01', fqdn='sth4.four.example.com.',
                                 address='192.168.50.10',
                                 arpa='10.50.168.192.in-addr.arpa.')

    _get_address(mac='ff:ff:ff:ff:ff:02', fqdn='sth4.four.example.com.', address='192.168.51.10')

    _check_fqdn_record("some.five.example.com.", expect='empty')

    # stop bind, remove data files, start bind with empty zones
    srv_control.start_srv('DNS', 'stopped')
    srv_control.clear_some_data('all', service='DNS')
    srv_control.start_srv('DNS', 'started', config_set=32)
    # check is all records were removed
    _check_fqdn_record("sth4.four.example.com.", expect='empty')
    _check_fqdn_record("some.five.example.com.", expect='empty')
    _check_fqdn_record("record.three.example.com.", expect='empty')

    response = _resend_ddns('192.168.51.100', exp_result=3)
    assert response["text"] == "No lease found for: 192.168.51.100"
    response = _resend_ddns('192.168.50.10', exp_result=0)
    assert response["text"] == "NCR generated for: 192.168.50.10, hostname: sth4.four.example.com."

    _check_fqdn_record("sth4.four.example.com.", address='192.168.50.10')

    _check_address_record("sth4.four.example.com.",
                          '10.50.168.192.in-addr.arpa.')
    _check_fqdn_record("some.five.example.com.", expect='empty')
