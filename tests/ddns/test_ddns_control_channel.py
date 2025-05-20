# Copyright (C) 2022 Internet Systems Consortium, Inc. ("ISC")
#
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

"""DDNS control channel basic commands"""

import os
import json
import pytest

from src import misc
from src import srv_msg
from src import srv_control
from src.forge_cfg import world
from src.protosupport.multi_protocol_functions import sort_container
from src.protosupport.multi_protocol_functions import remove_file_from_server, copy_file_from_server
from src.softwaresupport.multi_server_functions import verify_file_permissions


def _send_through_ddns_socket(cmd, socket_name=world.f_cfg.run_join('ddns_control_socket'),
                              exp_result=0, exp_failed=False):
    return srv_msg.send_ctrl_cmd_via_socket(command=cmd, socket_name=socket_name, exp_result=exp_result,
                                            exp_failed=exp_failed)


def _check_if_ddns_is_working_correctly():
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


@pytest.mark.v6
@pytest.mark.ddns
@pytest.mark.controlchannel
def test_ddns6_control_channel_list():
    misc.test_setup()
    srv_control.config_srv_subnet('2001:db8:1::/64', '2001:db8:1::50-2001:db8:1::50')
    srv_control.add_ddns_server('127.0.0.1', '53001')
    srv_control.ddns_add_unix_socket()
    srv_control.build_and_send_config_files()
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
@pytest.mark.controlchannel
def test_ddns6_control_channel_config_set():
    misc.test_setup()
    srv_control.config_srv_subnet('2001:db8:1::/64', '2001:db8:1::50-2001:db8:1::50')
    srv_control.add_ddns_server('127.0.0.1', '53001')
    srv_control.ddns_add_unix_socket()
    srv_control.build_and_send_config_files()
    srv_control.start_srv('DHCP', 'started')

    cmd = dict(command='config-get', arguments={})

    response = _send_through_ddns_socket(cmd)

    cfg = response["arguments"]

    # let's ignore logging, it's added in Dhcp part and for now common,
    # that will have to be fixed in 1.7
    del cfg["hash"]
    del cfg["DhcpDdns"]["loggers"]
    del world.ddns_cfg["DhcpDdns"]["loggers"]
    assert cfg == world.ddns_cfg

    # now let's try to set configuration we received
    cmd = dict(command='config-set', arguments=cfg)
    _send_through_ddns_socket(cmd)


@pytest.mark.v6
@pytest.mark.ddns
@pytest.mark.controlchannel
def test_ddns6_control_channel_config_set_all_values():
    misc.test_setup()
    srv_control.config_srv_subnet('2001:db8:1::/64', '2001:db8:1::50-2001:db8:1::50')
    srv_control.add_ddns_server('127.0.0.1', '53001')
    srv_control.add_ddns_server_connectivity_options('enable-updates', True)
    srv_control.add_ddns_server_behavioral_options('ddns-send-updates', True)
    srv_control.add_ddns_server_behavioral_options('ddns-generated-prefix', 'six')
    srv_control.add_ddns_server_behavioral_options('ddns-qualifying-suffix', 'example.com')
    srv_control.add_forward_ddns('six.example.com.', 'forge.sha1.key')
    srv_control.add_reverse_ddns('1.0.0.0.8.b.d.0.1.0.0.2.ip6.arpa.', 'forge.sha1.key')
    srv_control.add_keys('forge.sha1.key', 'HMAC-SHA1', 'PN4xKZ/jDobCMlo4rpr70w==')
    srv_control.ddns_add_unix_socket()
    srv_control.build_and_send_config_files()
    srv_control.start_srv('DHCP', 'started')

    cmd = dict(command='config-get', arguments={})

    response = _send_through_ddns_socket(cmd)

    cfg = response["arguments"]
    del cfg['hash']

    tmp_cfg = world.ddns_cfg

    # let's ignore logging, it's added in Dhcp part and for now common,
    # that will have to be fixed in 1.7
    del cfg["DhcpDdns"]["loggers"]
    del world.ddns_cfg["DhcpDdns"]["loggers"]
    assert cfg == world.ddns_cfg

    # now let's try to set configuration we received
    # first let's stop everything and start empty DDNS server with just control channel:
    # (DHCP and DDNS are combined for now)
    srv_control.start_srv('DHCP', 'stopped')

    misc.test_setup()
    srv_control.config_srv_subnet('2001:db8:1::/64', '2001:db8:1::50-2001:db8:1::50')
    srv_control.add_ddns_server('127.0.0.1', '53001')
    srv_control.add_ddns_server_connectivity_options('enable-updates', True)
    srv_control.add_ddns_server_behavioral_options('ddns-send-updates', True)
    srv_control.add_ddns_server_behavioral_options('ddns-generated-prefix', 'six')
    srv_control.add_ddns_server_behavioral_options('ddns-qualifying-suffix', 'example.com')
    # new socket name
    srv_control.ddns_add_unix_socket(socket_name="different_ddns_control_socket")
    srv_control.build_and_send_config_files()
    srv_control.start_srv('DHCP', 'started')

    cmd = dict(command='config-set', arguments=cfg)
    # send to the new socket, config will change this socket to ddns_control_socket
    _send_through_ddns_socket(cmd, socket_name="different_ddns_control_socket")

    srv_control.use_dns_set_number(3)
    srv_control.start_srv('DNS', 'started')

    _check_if_ddns_is_working_correctly()

    # send to old socket, it should fail:
    cmd = dict(command='config-get', arguments={})
    _send_through_ddns_socket(cmd, socket_name="different_ddns_control_socket", exp_failed=True)

    # send to the new socket, should work, and it should be the same configuration as previously
    # previously we removed logging from config, so new ddns configuration is without logging section
    cmd = dict(command='config-get', arguments={})
    response = _send_through_ddns_socket(cmd)
    cfg = response["arguments"]
    del cfg['hash']

    assert cfg == tmp_cfg


@pytest.mark.v6
@pytest.mark.ddns
@pytest.mark.controlchannel
def test_ddns6_control_channel_config_test():
    # let's check minimal configuration
    misc.test_setup()
    srv_control.config_srv_subnet('2001:db8:1::/64', '2001:db8:1::50-2001:db8:1::50')
    # minimal ddns
    srv_control.add_ddns_server('127.0.0.1', '53001')
    srv_control.add_ddns_server_connectivity_options('enable-updates', True)
    srv_control.add_ddns_server_behavioral_options('ddns-send-updates', True)
    srv_control.add_ddns_server_behavioral_options('ddns-generated-prefix', 'six')
    srv_control.add_ddns_server_behavioral_options('ddns-qualifying-suffix', 'example.com')
    srv_control.ddns_add_unix_socket()
    srv_control.build_and_send_config_files()
    srv_control.start_srv('DHCP', 'started')

    cmd = dict(command='config-get', arguments={})
    response = _send_through_ddns_socket(cmd)
    cfg = response["arguments"]
    del cfg['hash']
    cmd = dict(command='config-test', arguments=cfg)
    _send_through_ddns_socket(cmd)

    srv_control.start_srv('DHCP', 'stopped')

    # let's check if returned configuration is correct
    misc.test_setup()
    srv_control.config_srv_subnet('2001:db8:1::/64', '2001:db8:1::50-2001:db8:1::50')
    srv_control.add_ddns_server('127.0.0.1', '53001')
    srv_control.add_ddns_server_connectivity_options('enable-updates', True)
    srv_control.add_ddns_server_behavioral_options('ddns-send-updates', True)
    srv_control.add_ddns_server_behavioral_options('ddns-generated-prefix', 'six')
    srv_control.add_ddns_server_behavioral_options('ddns-qualifying-suffix', 'example.com')
    srv_control.ddns_add_unix_socket()
    srv_control.add_forward_ddns('six.example.com.', 'forge.sha1.key')
    srv_control.add_reverse_ddns('1.0.0.0.8.b.d.0.1.0.0.2.ip6.arpa.', 'forge.sha1.key')
    srv_control.add_keys('forge.sha1.key', 'HMAC-SHA1', 'PN4xKZ/jDobCMlo4rpr70w==')
    srv_control.build_and_send_config_files()
    srv_control.start_srv('DHCP', 'started')

    cmd = dict(command='config-get', arguments={})
    response = _send_through_ddns_socket(cmd)
    cfg = response["arguments"]
    del cfg['hash']
    cmd = dict(command='config-test', arguments=cfg)
    _send_through_ddns_socket(cmd)

    # and now let's make couple incorrect configs
    cfg = {
        "DhcpDdns": {
            "dns-server-timeout": 100,
            "forward-ddns": {
                "ddns-domains": [
                    {
                        "dns-servers": [
                            {
                                "hostname": "",
                                "ip-address": "2001:db8:1::1000",
                                "port": "an"
                            }
                        ],
                        "key-name": "forge.sha1.key",
                        "name": "six.example.com."
                    }
                ]
            },
            "ip-address": "127.0.0.1",
            "ncr-format": "JSON",
            "ncr-protocol": "UDP",
            "port": 53001,
            "reverse-ddns": {
                "ddns-domains": [
                    {
                        "dns-servers": [
                            {
                                "hostname": "",
                                "ip-address": "2001:db8:1::1000",
                                "port": 53
                            }
                        ],
                        "key-name": "forge.sha1.key",
                        "name": "1.0.0.0.8.b.d.0.1.0.0.2.ip6.arpa."
                    }
                ]
            },
            "tsig-keys": [
                {
                    "algorithm": "HMAC-SHA1",
                    "digest-bits": 0,
                    "name": "forge.sha1.key",
                    "secret": "PN4xKZ/jDobCMlo4rpr70w=="
                }
            ]
        }
    }
    cmd = dict(command='config-test', arguments=cfg)
    _send_through_ddns_socket(cmd, exp_result=1)

    cfg = {
        "DhcpDdns": {
            "dns-server-timeout": 100,
            "forward-ddns": {
                "ddns-domains": [
                    {
                        "dns-servers": [],
                        "key-name": "forge.sha1.key",
                        "name": "six.example.com."
                    }
                ]
            },
            "ip-address": "127.0.0.1",
            "ncr-protocol": "UDP",
            "port": 53001,
        }
    }
    cmd = dict(command='config-test', arguments=cfg)
    _send_through_ddns_socket(cmd, exp_result=1)

    cfg = {
        "DhcpDdns": {
            "dns-server-timeout": 100,
            "forward-ddns": {},
            "ip-address": "127.0.0.1",
            "ncr-format": "ABC",
            "ncr-protocol": "UDP",
            "port": 53001,
            "reverse-ddns": {}
        }
    }
    cmd = dict(command='config-test', arguments=cfg)
    _send_through_ddns_socket(cmd, exp_result=1)

    # and now check if all those tests didn't change kea running configuration
    srv_control.use_dns_set_number(3)
    srv_control.start_srv('DNS', 'started')

    _check_if_ddns_is_working_correctly()


@pytest.mark.v6
@pytest.mark.ddns
@pytest.mark.controlchannel
def test_ddns6_control_channel_config_reload():
    misc.test_setup()
    srv_control.config_srv_subnet('2001:db8:1::/64', '2001:db8:1::50-2001:db8:1::50')
    # minimal ddns
    srv_control.add_ddns_server('127.0.0.1', '53001')
    srv_control.add_ddns_server_connectivity_options('enable-updates', True)
    srv_control.add_ddns_server_behavioral_options('ddns-send-updates', True)
    srv_control.add_ddns_server_behavioral_options('ddns-generated-prefix', 'six')
    srv_control.add_ddns_server_behavioral_options('ddns-qualifying-suffix', 'example.com')
    srv_control.ddns_add_unix_socket()
    srv_control.build_and_send_config_files()
    srv_control.start_srv('DHCP', 'started')

    cmd = dict(command='config-get', arguments={})
    cfg = _send_through_ddns_socket(cmd)
    del cfg['arguments']['hash']
    del cfg["arguments"]["DhcpDdns"]["loggers"]
    del world.ddns_cfg["DhcpDdns"]["loggers"]
    assert cfg["arguments"] == world.ddns_cfg

    misc.test_setup()
    srv_control.config_srv_subnet('2001:db8:1::/64', '2001:db8:1::50-2001:db8:1::50')
    srv_control.add_ddns_server('127.0.0.1', '53001')
    srv_control.add_ddns_server_connectivity_options('enable-updates', True)
    srv_control.add_ddns_server_behavioral_options('ddns-send-updates', True)
    srv_control.add_ddns_server_behavioral_options('ddns-generated-prefix', 'six')
    srv_control.add_ddns_server_behavioral_options('ddns-qualifying-suffix', 'example.com')
    srv_control.ddns_add_unix_socket()
    srv_control.add_forward_ddns('six.example.com.', 'forge.sha1.key')
    srv_control.add_reverse_ddns('1.0.0.0.8.b.d.0.1.0.0.2.ip6.arpa.', 'forge.sha1.key')
    srv_control.add_keys('forge.sha1.key', 'HMAC-SHA1', 'PN4xKZ/jDobCMlo4rpr70w==')
    srv_control.build_and_send_config_files()

    cmd = dict(command='config-reload', arguments={})
    _send_through_ddns_socket(cmd)

    cmd = dict(command='config-get', arguments={})
    cfg = _send_through_ddns_socket(cmd)
    del cfg['arguments']['hash']
    del cfg["arguments"]["DhcpDdns"]["loggers"]
    del world.ddns_cfg["DhcpDdns"]["loggers"]
    assert cfg["arguments"] == world.ddns_cfg

    srv_control.use_dns_set_number(3)
    srv_control.start_srv('DNS', 'started')

    _check_if_ddns_is_working_correctly()


@pytest.mark.v6
@pytest.mark.ddns
@pytest.mark.controlchannel
def test_ddns6_control_channel_build_report():
    misc.test_setup()
    srv_control.config_srv_subnet('2001:db8:1::/64', '2001:db8:1::50-2001:db8:1::50')
    srv_control.add_ddns_server('127.0.0.1', '53001')
    srv_control.ddns_add_unix_socket()
    srv_control.build_and_send_config_files()
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
@pytest.mark.controlchannel
def test_ddns6_control_channel_config_write():
    misc.test_setup()
    srv_control.config_srv_subnet('2001:db8:1::/64', '2001:db8:1::50-2001:db8:1::50')
    srv_control.add_ddns_server('127.0.0.1', '53001')
    srv_control.add_ddns_server_connectivity_options('enable-updates', True)
    srv_control.add_ddns_server_behavioral_options('ddns-send-updates', True)
    srv_control.add_ddns_server_behavioral_options('ddns-generated-prefix', 'six')
    srv_control.add_ddns_server_behavioral_options('ddns-qualifying-suffix', 'example.com')
    srv_control.add_forward_ddns('six.example.com.', 'forge.sha1.key')
    srv_control.add_reverse_ddns('1.0.0.0.8.b.d.0.1.0.0.2.ip6.arpa.', 'forge.sha1.key')
    srv_control.add_keys('forge.sha1.key', 'HMAC-SHA1', 'PN4xKZ/jDobCMlo4rpr70w==')
    srv_control.ddns_add_unix_socket()
    srv_control.build_and_send_config_files()
    srv_control.start_srv('DHCP', 'started')

    cmd = dict(command='config-write', arguments={"filename": world.f_cfg.data_join("new_kea_config_file")})

    response = _send_through_ddns_socket(cmd)
    verify_file_permissions(response['arguments']['filename'])

    srv_msg.copy_remote(world.f_cfg.data_join("new_kea_config_file"))

    # let's load json from downloaded file and check if it is the same what we configured kea with
    with open(os.path.join(world.cfg["test_result_dir"], 'downloaded_file'), 'r', encoding='utf-8') as f:
        downloaded_config = json.load(f)
    del downloaded_config["DhcpDdns"]["loggers"]
    del world.ddns_cfg["DhcpDdns"]["loggers"]
    assert downloaded_config == world.ddns_cfg


@pytest.mark.v6
@pytest.mark.ddns
@pytest.mark.controlchannel
def test_ddns6_control_channel_shutdown():
    misc.test_setup()
    srv_control.config_srv_subnet('2001:db8:1::/64', '2001:db8:1::50-2001:db8:1::50')
    srv_control.add_ddns_server('127.0.0.1', '53001')
    srv_control.ddns_add_unix_socket()
    srv_control.build_and_send_config_files()
    srv_control.start_srv('DHCP', 'started')

    cmd = dict(command='shutdown', arguments={"type": "now"})
    _send_through_ddns_socket(cmd)
    cmd = dict(command='config-write', arguments={})
    _send_through_ddns_socket(cmd, exp_failed=True)

    srv_control.start_srv('DHCP', 'started')
    cmd = dict(command='shutdown', arguments={"type": "normal"})
    _send_through_ddns_socket(cmd)
    cmd = dict(command='config-write', arguments={})
    _send_through_ddns_socket(cmd, exp_failed=True)

    srv_control.start_srv('DHCP', 'started')
    cmd = dict(command='shutdown', arguments={"type": "drain_first"})
    _send_through_ddns_socket(cmd)
    cmd = dict(command='config-write', arguments={})
    _send_through_ddns_socket(cmd, exp_failed=True)


@pytest.mark.v6
@pytest.mark.ddns
@pytest.mark.controlchannel
def test_ddns6_control_channel_version_get():
    misc.test_setup()
    srv_control.config_srv_subnet('2001:db8:1::/64', '2001:db8:1::50-2001:db8:1::50')
    srv_control.add_ddns_server('127.0.0.1', '53001')
    srv_control.ddns_add_unix_socket()
    srv_control.build_and_send_config_files()
    srv_control.start_srv('DHCP', 'started')

    cmd = dict(command='version-get', arguments={})

    response = _send_through_ddns_socket(cmd)
    assert response["arguments"]["extended"]
    # TODO at least version of kea could be held in forge


@pytest.mark.v6
@pytest.mark.ddns
@pytest.mark.controlchannel
def test_ddns6_control_channel_usercontext():
    misc.test_setup()
    srv_control.config_srv_subnet('2001:db8:1::/64', '2001:db8:1::50-2001:db8:1::50')
    srv_control.add_ddns_server('127.0.0.1', '53001')
    srv_control.add_ddns_server_connectivity_options('enable-updates', True)
    srv_control.add_ddns_server_behavioral_options('ddns-send-updates', True)
    srv_control.add_ddns_server_behavioral_options('ddns-generated-prefix', 'six')
    srv_control.add_ddns_server_behavioral_options('ddns-qualifying-suffix', 'example.com')
    srv_control.add_forward_ddns('six.example.com.', 'forge.sha1.key')
    srv_control.add_reverse_ddns('1.0.0.0.8.b.d.0.1.0.0.2.ip6.arpa.', 'forge.sha1.key')
    srv_control.add_keys('forge.sha1.key', 'HMAC-SHA1', 'PN4xKZ/jDobCMlo4rpr70w==')
    srv_control.ddns_add_unix_socket()
    srv_control.build_and_send_config_files()
    srv_control.start_srv('DHCP', 'started')

    #  Get current config
    cmd = dict(command='config-get', arguments={})
    response = _send_through_ddns_socket(cmd)
    config_set = response['arguments']
    hash1 = config_set['hash']
    del config_set['hash']

    # Modify configuration
    config_set['DhcpDdns']['user-context'] = {"version": [{"number": 1, "rev": 2}, {"id": 1, "no": 2}]}
    config_set['DhcpDdns']['forward-ddns']['ddns-domains'][0]['user-context'] = {
        "tre,e": {"bra,nch1": {"treehouse": 1}, "bra,nch2": 2,
                  "bra,nch3": {"leaf1": 1,
                               "leaf2": ["vein1", "vein2"]}}}
    config_set['DhcpDdns']['forward-ddns']['ddns-domains'][0]['dns-servers'][0]['user-context'] = {
        "password": {"id": 2, "name_": "bestpassword"}}

    config_set['DhcpDdns']['loggers'][0]['user-context'] = {"version": [{"number": 2, "rev": 4}, {"id": 6, "no": 8}]}

    config_set['DhcpDdns']['reverse-ddns']['ddns-domains'][0]['user-context'] = {
        "tr,ee": {"Branch1": {"treeHouse": 1}, "Brnch2": 2,
                  "Brnch3": {"leaf_1": 1,
                             "leaf_2": ["Vein1", "Vein2"]}}}
    config_set['DhcpDdns']['reverse-ddns']['ddns-domains'][0]['dns-servers'][0]['user-context'] = {
        "login": {"iD": 5, "name2": "123456"}}

    config_set['DhcpDdns']['tsig-keys'][0]['user-context'] = {"owner": {"id": 1, "name": "John Doe"}}

    # Sort config for easier comparison
    config_set = sort_container(config_set)

    # Send modified config to server
    cmd = dict(command='config-set', arguments=config_set)
    response = _send_through_ddns_socket(cmd)

    # Get new config from server
    cmd = dict(command='config-get', arguments={})
    response = _send_through_ddns_socket(cmd)
    config_get = response['arguments']
    hash2 = config_get['hash']
    del config_get['hash']
    config_get = sort_container(config_get)

    # Compare what we send and what Kea returned.
    assert config_set == config_get, "Send and received configurations are different"

    # After changes in config two hashes from config get should be different
    assert hash1 != hash2, "After changes hash is the same!"

    # Write config to file and download it
    remote_path = world.f_cfg.etc_join('config-export.json')
    remove_file_from_server(remote_path)
    cmd = dict(command='config-write', arguments={"filename": remote_path})
    response = _send_through_ddns_socket(cmd)
    verify_file_permissions(response['arguments']['filename'])
    local_path = copy_file_from_server(remote_path, 'config-export.json')

    # Open downloaded file and sort it for easier comparison
    with open(local_path, 'r', encoding="utf-8") as config_file:
        config_write = json.load(config_file)
    config_write = sort_container(config_write)

    # Compare downloaded file with send config.
    assert config_set == config_write, "Send and downloaded file configurations are different"


@pytest.mark.v6
@pytest.mark.ddns
@pytest.mark.controlchannel
def test_ddns6_config_hash_get():
    misc.test_setup()
    srv_control.config_srv_subnet('2001:db8:1::/64', '2001:db8:1::50-2001:db8:1::50')
    srv_control.add_ddns_server('127.0.0.1', '53001')
    srv_control.ddns_add_unix_socket()
    srv_control.build_and_send_config_files()
    srv_control.start_srv('DHCP', 'started')

    # Get current config
    cmd = {"command": "config-hash-get", "arguments": {}}
    hash1 = _send_through_ddns_socket(cmd)["arguments"]["hash"]
    hash2 = _send_through_ddns_socket(cmd)["arguments"]["hash"]
    assert hash1 == hash2, "Got two different hashes without config change"

    cmd = {"command": "config-get", "arguments": {}}
    cfg_get = _send_through_ddns_socket(cmd)["arguments"]
    hash3 = cfg_get['hash']
    assert hash2 == hash3, "Got two different hashes without config change"
    del cfg_get['hash']

    # let's set something different as a config and check if has changed
    cfg_get["DhcpDdns"]["dns-server-timeout"] = 20000

    cmd = {"command": "config-set", "arguments": cfg_get}
    cfg_set = _send_through_ddns_socket(cmd)["arguments"]
    hash4 = cfg_set['hash']
    assert hash4 != hash1, "Config has changed but hash not!"

    cmd = {"command": "config-hash-get", "arguments": {}}
    hash5 = _send_through_ddns_socket(cmd)["arguments"]["hash"]
    assert hash4 == hash5, "hash returned in config-get-hash and config-set are different!"

    # let's set config from the beginning
    cfg_get["DhcpDdns"]["dns-server-timeout"] = 2000

    cmd = {"command": "config-set", "arguments": cfg_get}
    cfg_set = _send_through_ddns_socket(cmd)["arguments"]
    hash6 = cfg_set['hash']

    assert hash1 == hash2 == hash3 == hash6 != hash4, "Kea reconfigured with the same config, hash shouldn't change"
    cmd = {"command": "config-hash-get", "arguments": {}}
    hash7 = _send_through_ddns_socket(cmd)["arguments"]["hash"]
    assert hash6 == hash7, "hash returned in config-get-hash and config-set are different!"
