"""DDNS control channel basic commands"""

# pylint: disable=invalid-name,line-too-long

import pytest

import misc
import srv_msg
import srv_control
from forge_cfg import world


def _send_through_ddns_socket(cmd, socket_name=world.f_cfg.run_join('ddns_control_socket'),
                              exp_result=0, exp_failed=False):
    return srv_msg.send_ctrl_cmd_via_socket(command=cmd, socket_name=socket_name, exp_result=exp_result,
                                            exp_failed=exp_failed)


def _check_if_ddns_is_working_correctly():
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
@pytest.mark.control_channel
def test_ddns6_control_channel_list():
    misc.test_setup()
    srv_control.config_srv_subnet('2001:db8:1::/64', '2001:db8:1::50-2001:db8:1::50')
    srv_control.add_ddns_server('127.0.0.1', '53001')
    srv_control.ddns_open_control_channel()
    srv_control.build_and_send_config_files('SSH', 'config-file')
    srv_control.start_srv('DHCP', 'started')

    cmd = dict(command="list-commands", arguments={})

    response = _send_through_ddns_socket(cmd)

    for cmd in ["build-report",
                "config-get",
                "config-reload",
                "config-set",
                "config-test",
                "config-write",
                "list-commands",
                "shutdown",
                "version-get"]:
        assert cmd in response['arguments']


@pytest.mark.v6
@pytest.mark.ddns
@pytest.mark.kea_only
@pytest.mark.control_channel
def test_ddns6_control_channel_config_set():
    misc.test_setup()
    srv_control.config_srv_subnet('2001:db8:1::/64', '2001:db8:1::50-2001:db8:1::50')
    srv_control.add_ddns_server('127.0.0.1', '53001')
    srv_control.ddns_open_control_channel()
    srv_control.build_and_send_config_files('SSH', 'config-file')
    srv_control.start_srv('DHCP', 'started')

    cmd = dict(command='config-get', arguments={})

    response = _send_through_ddns_socket(cmd)

    cfg = response["arguments"]

    # let's ignore logging, it's added in Dhcp part and for now common,
    # that will have to be fixed in 1.7
    del cfg["DhcpDdns"]["loggers"]
    assert cfg["DhcpDdns"] == world.ddns_main

    # now let's try to set configuration we received
    cmd = dict(command='config-set', arguments=cfg)
    _send_through_ddns_socket(cmd)


@pytest.mark.v6
@pytest.mark.ddns
@pytest.mark.kea_only
@pytest.mark.control_channel
def test_ddns6_control_channel_config_set_all_values():
    misc.test_setup()
    srv_control.config_srv_subnet('2001:db8:1::/64', '2001:db8:1::50-2001:db8:1::50')
    srv_control.add_ddns_server('127.0.0.1', '53001')
    srv_control.add_ddns_server_options('enable-updates', True)
    srv_control.add_ddns_server_options('generated-prefix', 'six')
    srv_control.add_ddns_server_options('qualifying-suffix', 'example.com')
    srv_control.add_forward_ddns('six.example.com.', 'forge.sha1.key')
    srv_control.add_reverse_ddns('1.0.0.0.8.b.d.0.1.0.0.2.ip6.arpa.', 'forge.sha1.key')
    srv_control.add_keys('forge.sha1.key', 'HMAC-SHA1', 'PN4xKZ/jDobCMlo4rpr70w==')
    srv_control.ddns_open_control_channel()
    srv_control.build_and_send_config_files('SSH', 'config-file')
    srv_control.start_srv('DHCP', 'started')

    cmd = dict(command='config-get', arguments={})

    response = _send_through_ddns_socket(cmd)

    cfg = response["arguments"]

    # let's ignore logging, it's added in Dhcp part and for now common,
    # that will have to be fixed in 1.7
    del cfg["DhcpDdns"]["loggers"]
    assert cfg["DhcpDdns"] == world.ddns_main

    # now let's try to set configuration we received
    # first let's stop everything and start empty DDNS server with just control channel:
    # (DHCP and DDNS are combined for now)
    srv_control.start_srv('DHCP', 'stopped')

    misc.test_setup()
    srv_control.config_srv_subnet('2001:db8:1::/64', '2001:db8:1::50-2001:db8:1::50')
    srv_control.add_ddns_server('127.0.0.1', '53001')
    srv_control.add_ddns_server_options('enable-updates', True)
    srv_control.add_ddns_server_options('generated-prefix', 'six')
    srv_control.add_ddns_server_options('qualifying-suffix', 'example.com')
    srv_control.ddns_open_control_channel()
    srv_control.build_and_send_config_files('SSH', 'config-file')
    srv_control.start_srv('DHCP', 'started')

    cmd = dict(command='config-set', arguments=cfg)
    _send_through_ddns_socket(cmd)

    srv_control.use_dns_set_number('3')
    srv_control.start_srv('DNS', 'started')

    _check_if_ddns_is_working_correctly()


@pytest.mark.v6
@pytest.mark.ddns
@pytest.mark.kea_only
@pytest.mark.control_channel
def test_ddns6_control_channel_config_test():
    misc.test_setup()
    srv_control.config_srv_subnet('2001:db8:1::/64', '2001:db8:1::50-2001:db8:1::50')
    srv_control.add_ddns_server('127.0.0.1', '53001')
    srv_control.add_ddns_server_options('enable-updates', True)
    srv_control.add_ddns_server_options('generated-prefix', 'six')
    srv_control.add_ddns_server_options('qualifying-suffix', 'example.com')
    srv_control.add_forward_ddns('six.example.com.', 'forge.sha1.key')
    srv_control.add_reverse_ddns('1.0.0.0.8.b.d.0.1.0.0.2.ip6.arpa.', 'forge.sha1.key')
    srv_control.add_keys('forge.sha1.key', 'HMAC-SHA1', 'PN4xKZ/jDobCMlo4rpr70w==')
    srv_control.ddns_open_control_channel()
    srv_control.build_and_send_config_files('SSH', 'config-file')
    srv_control.start_srv('DHCP', 'started')

    cmd = dict(command='config-get', arguments={})

    response = _send_through_ddns_socket(cmd)

    cfg = response["arguments"]

    cmd = dict(command='config-test', arguments=cfg)

    _send_through_ddns_socket(cmd)

    cmd = dict(command='config-test', arguments=cfg)

    _send_through_ddns_socket(cmd, exp_result=1)


@pytest.mark.v6
@pytest.mark.ddns
@pytest.mark.kea_only
@pytest.mark.control_channel
def test_ddns6_control_channel_config_reload():
    misc.test_setup()
    srv_control.config_srv_subnet('2001:db8:1::/64', '2001:db8:1::50-2001:db8:1::50')
    srv_control.add_ddns_server_options('enable-updates', True)
    srv_control.add_ddns_server_options('generated-prefix', 'six')
    srv_control.add_ddns_server_options('qualifying-suffix', 'example.com')
    # minimal ddns
    srv_control.add_ddns_server('127.0.0.1', '53001')
    srv_control.ddns_open_control_channel()
    srv_control.build_and_send_config_files('SSH', 'config-file')
    srv_control.start_srv('DHCP', 'started')

    misc.test_setup()
    srv_control.config_srv_subnet('2001:db8:1::/64', '2001:db8:1::50-2001:db8:1::50')
    srv_control.add_ddns_server('127.0.0.1', '53001')
    srv_control.add_ddns_server_options('enable-updates', True)
    srv_control.add_ddns_server_options('generated-prefix', 'six')
    srv_control.add_ddns_server_options('qualifying-suffix', 'example.com')
    srv_control.add_forward_ddns('six.example.com.', 'forge.sha1.key')
    srv_control.add_reverse_ddns('1.0.0.0.8.b.d.0.1.0.0.2.ip6.arpa.', 'forge.sha1.key')
    srv_control.add_keys('forge.sha1.key', 'HMAC-SHA1', 'PN4xKZ/jDobCMlo4rpr70w==')
    srv_control.build_and_send_config_files('SSH', 'config-file')

    cmd = dict(command='config-reload', arguments={})

    _send_through_ddns_socket(cmd)

    srv_control.use_dns_set_number('3')
    srv_control.start_srv('DNS', 'started')

    _check_if_ddns_is_working_correctly()


@pytest.mark.v6
@pytest.mark.ddns
@pytest.mark.kea_only
@pytest.mark.control_channel
def test_ddns6_control_channel_build_report():
    misc.test_setup()
    srv_control.config_srv_subnet('2001:db8:1::/64', '2001:db8:1::50-2001:db8:1::50')
    srv_control.add_ddns_server('127.0.0.1', '53001')
    srv_control.ddns_open_control_channel()
    srv_control.build_and_send_config_files('SSH', 'config-file')
    srv_control.start_srv('DHCP', 'started')

    cmd = dict(command='build-report', arguments={})

    response = _send_through_ddns_socket(cmd)

    # there is no good way to check specific values, so let's just check that there is there
    assert "Valgrind" in response["text"]
    assert "CXX_VERSION" in response["text"]
    assert "MYSQL_VERSION" in response["text"]
    assert "Included Hooks" in response["text"]


@pytest.mark.v6
@pytest.mark.ddns
@pytest.mark.kea_only
@pytest.mark.control_channel
def test_ddns6_control_channel_config_write():
    misc.test_setup()
    srv_control.config_srv_subnet('2001:db8:1::/64', '2001:db8:1::50-2001:db8:1::50')
    srv_control.add_ddns_server('127.0.0.1', '53001')
    srv_control.ddns_open_control_channel()
    srv_control.build_and_send_config_files('SSH', 'config-file')
    srv_control.start_srv('DHCP', 'started')

    cmd = dict(command='config-write', arguments={})

    response = _send_through_ddns_socket(cmd)


@pytest.mark.v6
@pytest.mark.ddns
@pytest.mark.kea_only
@pytest.mark.control_channel
def test_ddns6_control_channel_shutdown():
    misc.test_setup()
    srv_control.config_srv_subnet('2001:db8:1::/64', '2001:db8:1::50-2001:db8:1::50')
    srv_control.add_ddns_server('127.0.0.1', '53001')
    srv_control.ddns_open_control_channel()
    srv_control.build_and_send_config_files('SSH', 'config-file')
    srv_control.start_srv('DHCP', 'started')

    cmd = dict(command='shutdown', arguments={})

    _send_through_ddns_socket(cmd)
    # TODO this command return "text": "Shutdown initiated, type is: normal" there is no documentation about
    # normal or not normal type of shutdown, investigate this

    cmd = dict(command='config-write', arguments={})

    _send_through_ddns_socket(cmd, exp_failed=True)
    # TODO we might need a step with checking status of the process, for now it's sufficient


@pytest.mark.v6
@pytest.mark.ddns
@pytest.mark.kea_only
@pytest.mark.control_channel
def test_ddns6_control_channel_version_get():
    misc.test_setup()
    srv_control.config_srv_subnet('2001:db8:1::/64', '2001:db8:1::50-2001:db8:1::50')
    srv_control.add_ddns_server('127.0.0.1', '53001')
    srv_control.ddns_open_control_channel()
    srv_control.build_and_send_config_files('SSH', 'config-file')
    srv_control.start_srv('DHCP', 'started')

    cmd = dict(command='version-get', arguments={})

    _send_through_ddns_socket(cmd)
    assert response["arguments"]["extended"]
    # TODO at least version of kea could be held in forge
