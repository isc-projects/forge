"""Kea Control Channel Script"""

# pylint: disable=invalid-name,line-too-long

import pytest

import srv_msg
import misc
import srv_control
from forge_cfg import world


@pytest.mark.v6
@pytest.mark.controlchannel
@pytest.mark.kea_onlyn
def test_control_channel_keashell_dhcp_disable_timer():
    misc.test_setup()
    srv_control.config_srv_subnet('3000::/64', '3000::1-3000::f')
    srv_control.open_control_channel()
    srv_control.agent_control_channel('127.0.0.1')
    srv_control.build_and_send_config_files('SSH', 'config-file')

    srv_control.start_srv('DHCP', 'started')

    misc.test_procedure()
    srv_msg.client_sets_value('Client', 'DUID', '00:03:00:01:66:55:44:33:22:11')
    srv_msg.client_does_include('Client', None, 'client-id')
    srv_msg.client_does_include('Client', None, 'IA_Address')
    srv_msg.client_does_include('Client', None, 'IA-NA')
    srv_msg.client_send_msg('SOLICIT')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', None, 'ADVERTISE')
    srv_msg.response_check_include_option('Response', None, '1')
    srv_msg.response_check_include_option('Response', None, '2')
    srv_msg.response_check_include_option('Response', None, '3')
    srv_msg.response_check_option_content('Response', '3', None, 'sub-option', '5')
    srv_msg.response_check_suboption_content('Response', '5', '3', None, 'addr', '3000::1')

    srv_msg.execute_kea_shell('--host 127.0.0.1 --port 8000 --service dhcp6 dhcp-disable <<<\'"max-period": 5\'')

    misc.test_procedure()
    srv_msg.client_sets_value('Client', 'DUID', '00:03:00:01:66:55:44:33:22:11')
    srv_msg.client_does_include('Client', None, 'client-id')
    srv_msg.client_does_include('Client', None, 'IA_Address')
    srv_msg.client_does_include('Client', None, 'IA-NA')
    srv_msg.client_send_msg('SOLICIT')

    misc.pass_criteria()
    srv_msg.send_dont_wait_for_message()

    srv_msg.forge_sleep('7', 'seconds')

    misc.test_procedure()
    srv_msg.client_sets_value('Client', 'DUID', '00:03:00:01:66:55:44:33:22:11')
    srv_msg.client_does_include('Client', None, 'client-id')
    srv_msg.client_does_include('Client', None, 'IA_Address')
    srv_msg.client_does_include('Client', None, 'IA-NA')
    srv_msg.client_send_msg('SOLICIT')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', None, 'ADVERTISE')
    srv_msg.response_check_include_option('Response', None, '1')
    srv_msg.response_check_include_option('Response', None, '2')
    srv_msg.response_check_include_option('Response', None, '3')
    srv_msg.response_check_option_content('Response', '3', None, 'sub-option', '5')


@pytest.mark.v6
@pytest.mark.controlchannel
@pytest.mark.kea_only
def test_control_channel_keashell_dhcp_disable():
    misc.test_setup()
    srv_control.config_srv_subnet('3000::/64', '3000::1-3000::f')
    srv_control.open_control_channel()
    srv_control.agent_control_channel('127.0.0.1')
    srv_control.build_and_send_config_files('SSH', 'config-file')

    srv_control.start_srv('DHCP', 'started')

    misc.test_procedure()
    srv_msg.client_sets_value('Client', 'DUID', '00:03:00:01:66:55:44:33:22:11')
    srv_msg.client_does_include('Client', None, 'client-id')
    srv_msg.client_does_include('Client', None, 'IA_Address')
    srv_msg.client_does_include('Client', None, 'IA-NA')
    srv_msg.client_send_msg('SOLICIT')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', None, 'ADVERTISE')
    srv_msg.response_check_include_option('Response', None, '1')
    srv_msg.response_check_include_option('Response', None, '2')
    srv_msg.response_check_include_option('Response', None, '3')
    srv_msg.response_check_option_content('Response', '3', None, 'sub-option', '5')
    srv_msg.response_check_suboption_content('Response', '5', '3', None, 'addr', '3000::1')

    srv_msg.execute_kea_shell('--host 127.0.0.1 --port 8000 --service dhcp6 dhcp-disable <<<\'\'')

    misc.test_procedure()
    srv_msg.client_sets_value('Client', 'DUID', '00:03:00:01:66:55:44:33:22:11')
    srv_msg.client_does_include('Client', None, 'client-id')
    srv_msg.client_does_include('Client', None, 'IA_Address')
    srv_msg.client_does_include('Client', None, 'IA-NA')
    srv_msg.client_send_msg('SOLICIT')

    misc.pass_criteria()
    srv_msg.send_dont_wait_for_message()


@pytest.mark.v6
@pytest.mark.controlchannel
@pytest.mark.kea_only
def test_control_channel_keashell_dhcp_disable_and_enable():
    misc.test_setup()
    srv_control.config_srv_subnet('3000::/64', '3000::1-3000::f')
    srv_control.open_control_channel()
    srv_control.agent_control_channel('127.0.0.1')
    srv_control.build_and_send_config_files('SSH', 'config-file')

    srv_control.start_srv('DHCP', 'started')

    misc.test_procedure()
    srv_msg.client_sets_value('Client', 'DUID', '00:03:00:01:66:55:44:33:22:11')
    srv_msg.client_does_include('Client', None, 'client-id')
    srv_msg.client_does_include('Client', None, 'IA_Address')
    srv_msg.client_does_include('Client', None, 'IA-NA')
    srv_msg.client_send_msg('SOLICIT')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', None, 'ADVERTISE')
    srv_msg.response_check_include_option('Response', None, '1')
    srv_msg.response_check_include_option('Response', None, '2')
    srv_msg.response_check_include_option('Response', None, '3')
    srv_msg.response_check_option_content('Response', '3', None, 'sub-option', '5')
    srv_msg.response_check_suboption_content('Response', '5', '3', None, 'addr', '3000::1')

    srv_msg.execute_kea_shell('--host 127.0.0.1 --port 8000 --service dhcp6 dhcp-disable <<<\'\'')

    misc.test_procedure()
    srv_msg.client_sets_value('Client', 'DUID', '00:03:00:01:66:55:44:33:22:11')
    srv_msg.client_does_include('Client', None, 'client-id')
    srv_msg.client_does_include('Client', None, 'IA_Address')
    srv_msg.client_does_include('Client', None, 'IA-NA')
    srv_msg.client_send_msg('SOLICIT')

    misc.pass_criteria()
    srv_msg.send_dont_wait_for_message()
    srv_msg.execute_kea_shell('--host 127.0.0.1 --port 8000 --service dhcp6 dhcp-enable <<<\'\'')

    misc.test_procedure()
    srv_msg.client_sets_value('Client', 'DUID', '00:03:00:01:66:55:44:33:22:11')
    srv_msg.client_does_include('Client', None, 'client-id')
    srv_msg.client_does_include('Client', None, 'IA_Address')
    srv_msg.client_does_include('Client', None, 'IA-NA')
    srv_msg.client_send_msg('SOLICIT')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', None, 'ADVERTISE')
    srv_msg.response_check_include_option('Response', None, '1')
    srv_msg.response_check_include_option('Response', None, '2')
    srv_msg.response_check_include_option('Response', None, '3')
    srv_msg.response_check_option_content('Response', '3', None, 'sub-option', '5')


@pytest.mark.v6
@pytest.mark.controlchannel
@pytest.mark.kea_only
def test_control_channel_keashell_set_config_basic():
    misc.test_setup()
    srv_control.config_srv_subnet('3000::/64', '3000::1-3000::f')
    srv_control.open_control_channel()
    srv_control.agent_control_channel('127.0.0.1')
    srv_control.build_and_send_config_files('SSH', 'config-file')

    srv_control.start_srv('DHCP', 'started')
    srv_msg.forge_sleep('2', 'seconds')

    misc.test_procedure()
    srv_msg.client_sets_value('Client', 'DUID', '00:03:00:01:66:55:44:33:22:11')
    srv_msg.client_does_include('Client', None, 'client-id')
    srv_msg.client_does_include('Client', None, 'IA_Address')
    srv_msg.client_does_include('Client', None, 'IA-NA')
    srv_msg.client_send_msg('SOLICIT')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', None, 'ADVERTISE')
    srv_msg.response_check_include_option('Response', None, '1')
    srv_msg.response_check_include_option('Response', None, '2')
    srv_msg.response_check_include_option('Response', None, '3')
    srv_msg.response_check_option_content('Response', '3', None, 'sub-option', '5')
    srv_msg.response_check_suboption_content('Response', '5', '3', None, 'addr', '3000::1')

    # this command is with new configuration
    srv_msg.execute_kea_shell('--host 127.0.0.1 --port 8000 --service dhcp6 config-set <<<\'"Dhcp6": { "control-socket": { "socket-name": "%s", "socket-type": "unix" }, "decline-probation-period": 86400, "dhcp-ddns": { "always-include-fqdn": false, "enable-updates": false, "generated-prefix": "myhost", "max-queue-size": 1024, "ncr-format": "JSON", "ncr-protocol": "UDP", "override-client-update": false, "override-no-update": false, "qualifying-suffix": "", "replace-client-name": "never", "sender-ip": "0.0.0.0", "sender-port": 0, "server-ip": "127.0.0.1", "server-port": 53001 }, "dhcp4o6-port": 0, "expired-leases-processing": { "flush-reclaimed-timer-wait-time": 25, "hold-reclaimed-time": 3600, "max-reclaim-leases": 100, "max-reclaim-time": 250, "reclaim-timer-wait-time": 10, "unwarned-reclaim-cycles": 5 }, "hooks-libraries": [  ], "host-reservation-identifiers": [ "hw-address", "duid" ], "interfaces-config": { "interfaces": [ "$(SERVER_IFACE)" ], "re-detect": true }, "lease-database": { "type": "memfile" }, "mac-sources": [ "any" ], "option-data": [  ], "option-def": [  ], "relay-supplied-options": [ "65" ], "server-id": { "enterprise-id": 0, "htype": 0, "identifier": "", "persist": true, "time": 0, "type": "LLT" }, "shared-networks": [  ], "subnet6": [ { "id": 1, "interface": "$(SERVER_IFACE)", "option-data": [  ], "pd-pools": [  ], "pools": [ { "option-data": [  ], "pool": "2001:db8:1::1-2001:db8:1::1" } ], "preferred-lifetime": 3000, "rapid-commit": false, "rebind-timer": 2000, "relay": { "ip-address": "::" }, "renew-timer": 1000, "reservation-mode": "all", "reservations": [  ], "subnet": "2001:db8:1::/64", "valid-lifetime": 4000 } ] }\'' % world.f_cfg.run_join('control_socket'))

    misc.test_procedure()
    srv_msg.client_sets_value('Client', 'DUID', '00:03:00:01:66:55:44:33:22:11')
    srv_msg.client_does_include('Client', None, 'client-id')
    srv_msg.client_does_include('Client', None, 'IA_Address')
    srv_msg.client_does_include('Client', None, 'IA-NA')
    srv_msg.client_send_msg('SOLICIT')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', None, 'ADVERTISE')
    srv_msg.response_check_include_option('Response', None, '1')
    srv_msg.response_check_include_option('Response', None, '2')
    srv_msg.response_check_include_option('Response', None, '3')
    srv_msg.response_check_option_content('Response', '3', None, 'sub-option', '5')
    srv_msg.response_check_suboption_content('Response',
                                             '5',
                                             '3',
                                             None,
                                             'addr',
                                             '2001:db8:1::1')


@pytest.mark.v6
@pytest.mark.controlchannel
@pytest.mark.kea_only
def test_control_channel_keashell_after_restart_load_config_file():

    misc.test_setup()
    srv_control.config_srv_subnet('3000::/64', '3000::1-3000::f')
    srv_control.open_control_channel()
    srv_control.agent_control_channel('127.0.0.1')
    srv_control.build_and_send_config_files('SSH', 'config-file')
    srv_control.start_srv('DHCP', 'started')
    srv_msg.forge_sleep('2', 'seconds')

    misc.test_procedure()
    srv_msg.client_sets_value('Client', 'DUID', '00:03:00:01:66:55:44:33:22:11')
    srv_msg.client_does_include('Client', None, 'client-id')
    srv_msg.client_does_include('Client', None, 'IA_Address')
    srv_msg.client_does_include('Client', None, 'IA-NA')
    srv_msg.client_send_msg('SOLICIT')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', None, 'ADVERTISE')
    srv_msg.response_check_include_option('Response', None, '1')
    srv_msg.response_check_include_option('Response', None, '2')
    srv_msg.response_check_include_option('Response', None, '3')
    srv_msg.response_check_option_content('Response', '3', None, 'sub-option', '5')
    srv_msg.response_check_suboption_content('Response', '5', '3', None, 'addr', '3000::1')

    srv_msg.execute_kea_shell('--host 127.0.0.1 --port 8000 --service dhcp6 config-set <<<\'"Dhcp6": { "control-socket": { "socket-name": "%s", "socket-type": "unix" }, "decline-probation-period": 86400, "dhcp-ddns": { "always-include-fqdn": false, "enable-updates": false, "generated-prefix": "myhost", "max-queue-size": 1024, "ncr-format": "JSON", "ncr-protocol": "UDP", "override-client-update": false, "override-no-update": false, "qualifying-suffix": "", "replace-client-name": "never", "sender-ip": "0.0.0.0", "sender-port": 0, "server-ip": "127.0.0.1", "server-port": 53001 }, "dhcp4o6-port": 0, "expired-leases-processing": { "flush-reclaimed-timer-wait-time": 25, "hold-reclaimed-time": 3600, "max-reclaim-leases": 100, "max-reclaim-time": 250, "reclaim-timer-wait-time": 10, "unwarned-reclaim-cycles": 5 }, "hooks-libraries": [  ], "host-reservation-identifiers": [ "hw-address", "duid" ], "interfaces-config": { "interfaces": [ "$(SERVER_IFACE)" ], "re-detect": true }, "lease-database": { "type": "memfile" }, "mac-sources": [ "any" ], "option-data": [  ], "option-def": [  ], "relay-supplied-options": [ "65" ], "server-id": { "enterprise-id": 0, "htype": 0, "identifier": "", "persist": true, "time": 0, "type": "LLT" }, "shared-networks": [  ], "subnet6": [ { "id": 1, "interface": "$(SERVER_IFACE)", "option-data": [  ], "pd-pools": [  ], "pools": [ { "option-data": [  ], "pool": "2001:db8:1::1-2001:db8:1::1" } ], "preferred-lifetime": 3000, "rapid-commit": false, "rebind-timer": 2000, "relay": { "ip-address": "::" }, "renew-timer": 1000, "reservation-mode": "all", "reservations": [  ], "subnet": "2001:db8:1::/64", "valid-lifetime": 4000 } ] }\'' % world.f_cfg.run_join('control_socket'))

    misc.test_procedure()
    srv_msg.client_sets_value('Client', 'DUID', '00:03:00:01:66:55:44:33:22:11')
    srv_msg.client_does_include('Client', None, 'client-id')
    srv_msg.client_does_include('Client', None, 'IA_Address')
    srv_msg.client_does_include('Client', None, 'IA-NA')
    srv_msg.client_send_msg('SOLICIT')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', None, 'ADVERTISE')
    srv_msg.response_check_include_option('Response', None, '1')
    srv_msg.response_check_include_option('Response', None, '2')
    srv_msg.response_check_include_option('Response', None, '3')
    srv_msg.response_check_option_content('Response', '3', None, 'sub-option', '5')
    srv_msg.response_check_suboption_content('Response',
                                             '5',
                                             '3',
                                             None,
                                             'addr',
                                             '2001:db8:1::1')

    srv_control.start_srv('DHCP', 'restarted')

    misc.test_procedure()
    srv_msg.client_sets_value('Client', 'DUID', '00:03:00:01:66:55:44:33:22:11')
    srv_msg.client_does_include('Client', None, 'client-id')
    srv_msg.client_does_include('Client', None, 'IA_Address')
    srv_msg.client_does_include('Client', None, 'IA-NA')
    srv_msg.client_send_msg('SOLICIT')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', None, 'ADVERTISE')
    srv_msg.response_check_include_option('Response', None, '1')
    srv_msg.response_check_include_option('Response', None, '2')
    srv_msg.response_check_include_option('Response', None, '3')
    srv_msg.response_check_option_content('Response', '3', None, 'sub-option', '5')
    srv_msg.response_check_suboption_content('Response', '5', '3', None, 'addr', '3000::1')


@pytest.mark.v6
@pytest.mark.controlchannel
@pytest.mark.kea_only
def test_control_channel_keashell_get_config():
    misc.test_setup()
    srv_control.config_srv_subnet('3000::/64', '3000::1-3000::f')
    srv_control.open_control_channel()
    srv_control.agent_control_channel('127.0.0.1')
    srv_control.build_and_send_config_files('SSH', 'config-file')

    srv_control.start_srv('DHCP', 'started')

    srv_msg.execute_kea_shell('--host 127.0.0.1 --port 8000 --service dhcp6 config-get <<<\'\'')


@pytest.mark.v6
@pytest.mark.controlchannel
@pytest.mark.kea_only
@pytest.mark.disabled
def test_control_channel_keashell_test_config():
    misc.test_setup()
    srv_control.config_srv_subnet('3000::/64', '3000::1-3000::1')
    srv_control.open_control_channel()
    srv_control.agent_control_channel('127.0.0.1')
    srv_control.build_and_send_config_files('SSH', 'config-file')

    srv_control.start_srv('DHCP', 'started')

    misc.test_procedure()
    srv_msg.client_sets_value('Client', 'DUID', '00:03:00:01:66:55:44:33:22:11')
    srv_msg.client_does_include('Client', None, 'client-id')
    srv_msg.client_does_include('Client', None, 'IA_Address')
    srv_msg.client_does_include('Client', None, 'IA-NA')
    srv_msg.client_send_msg('SOLICIT')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', None, 'ADVERTISE')
    srv_msg.response_check_include_option('Response', None, '1')
    srv_msg.response_check_include_option('Response', None, '2')
    srv_msg.response_check_include_option('Response', None, '3')
    srv_msg.response_check_option_content('Response', '3', None, 'sub-option', '5')
    srv_msg.response_check_suboption_content('Response', '5', '3', None, 'addr', '3000::1')

    misc.test_setup()
    srv_control.config_srv_subnet('2001:db8:a::/64', '2001:db8:a::1-2001:db8:a::1')
    srv_control.config_srv_prefix('2001:db8:1::', '0', '90', '96')
    srv_control.config_srv_id('LLT', '00:01:00:02:52:7b:a8:f0:08:00:27:58:f1:e8')
    srv_control.config_srv_opt('sip-server-addr', '2001:db8::1,2001:db8::2')
    srv_control.config_srv_opt('new-posix-timezone', r'EST5EDT4\\,M3.2.0/02:00\\,M11.1.0/02:00')
    srv_control.host_reservation_in_subnet('address',
                                           '3000::1',
                                           '0',
                                           'duid',
                                           '00:03:00:01:f6:f5:f4:f3:f2:01')
    srv_control.generate_config_files()

    srv_msg.execute_kea_shell('--host 127.0.0.1 --port 8000 --service dhcp6 config-test <<<\'$(SERVER_CONFIG)\'')

    misc.test_procedure()
    srv_msg.client_sets_value('Client', 'DUID', '00:03:00:01:66:55:44:33:22:11')
    srv_msg.client_does_include('Client', None, 'client-id')
    srv_msg.client_does_include('Client', None, 'IA_Address')
    srv_msg.client_does_include('Client', None, 'IA-NA')
    srv_msg.client_send_msg('SOLICIT')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', None, 'ADVERTISE')
    srv_msg.response_check_include_option('Response', None, '1')
    srv_msg.response_check_include_option('Response', None, '2')
    srv_msg.response_check_include_option('Response', None, '3')
    srv_msg.response_check_option_content('Response', '3', None, 'sub-option', '5')
    srv_msg.response_check_suboption_content('Response', '5', '3', None, 'addr', '3000::1')

    misc.test_setup()
    srv_control.config_srv_subnet('2001:db8:a::/64', '2001:db8:a::1-2001:db8:a::1')
    srv_control.config_srv_prefix('2001:db8:1::', '0', '90', '96')
    srv_control.config_srv_id('LLT', '00:01:00:02:52:7b:a8:f0:08:00:27:58:f1:e8')
    srv_control.config_srv_opt('sip-server-addr', '2001:db8::1,2001:db8::2')
    srv_control.config_srv_opt('new-posix-timezone', r'EST5EDT4\\,M3.2.0/02:00\\,M11.1.0/02:00')
    # WRONG ADDRESS RESERVATION
    srv_control.host_reservation_in_subnet('address',
                                           '192.168.0.5',
                                           '0',
                                           'duid',
                                           '00:03:00:01:f6:f5:f4:f3:f2:01')
    srv_control.generate_config_files()

    srv_msg.execute_kea_shell('--host 127.0.0.1 --port 8000 --service dhcp6 config-test <<<\'$(SERVER_CONFIG)\'')
    srv_msg.forge_sleep('5', 'seconds')

    misc.test_procedure()
    srv_msg.client_sets_value('Client', 'DUID', '00:03:00:01:66:55:44:33:22:11')
    srv_msg.client_does_include('Client', None, 'client-id')
    srv_msg.client_does_include('Client', None, 'IA_Address')
    srv_msg.client_does_include('Client', None, 'IA-NA')
    srv_msg.client_send_msg('SOLICIT')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', None, 'ADVERTISE')
    srv_msg.response_check_include_option('Response', None, '1')
    srv_msg.response_check_include_option('Response', None, '2')
    srv_msg.response_check_include_option('Response', None, '3')
    srv_msg.response_check_option_content('Response', '3', None, 'sub-option', '5')
    srv_msg.response_check_suboption_content('Response', '5', '3', None, 'addr', '3000::1')


@pytest.mark.v6
@pytest.mark.controlchannel
@pytest.mark.kea_only
def test_control_channel_keashell_write_config():

    misc.test_setup()
    srv_control.config_srv_subnet('3000::/64', '3000::1-3000::1')
    srv_control.open_control_channel()
    srv_control.agent_control_channel('127.0.0.1')
    srv_control.build_and_send_config_files('SSH', 'config-file')
    srv_control.start_srv('DHCP', 'started')
    srv_msg.forge_sleep('2', 'seconds')

    misc.test_procedure()
    srv_msg.client_sets_value('Client', 'DUID', '00:03:00:01:66:55:44:33:22:11')
    srv_msg.client_does_include('Client', None, 'client-id')
    srv_msg.client_does_include('Client', None, 'IA_Address')
    srv_msg.client_does_include('Client', None, 'IA-NA')
    srv_msg.client_send_msg('SOLICIT')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', None, 'ADVERTISE')
    srv_msg.response_check_include_option('Response', None, '1')
    srv_msg.response_check_include_option('Response', None, '2')
    srv_msg.response_check_option_content('Response', '3', None, 'sub-option', '5')
    srv_msg.response_check_suboption_content('Response', '5', '3', None, 'addr', '3000::1')

    misc.test_setup()
    srv_control.config_srv_subnet('2001:db8:1::/64', '2001:db8:1::1-2001:db8:1::1')
    srv_control.agent_control_channel('localhost')
    srv_control.generate_config_files()

    srv_msg.execute_kea_shell('--host 127.0.0.1 --port 8000 --service dhcp6 config-set <<<\'"Dhcp6": { "control-socket": { "socket-name": "%s", "socket-type": "unix" }, "decline-probation-period": 86400, "dhcp-ddns": { "always-include-fqdn": false, "enable-updates": false, "generated-prefix": "myhost", "max-queue-size": 1024, "ncr-format": "JSON", "ncr-protocol": "UDP", "override-client-update": false, "override-no-update": false, "qualifying-suffix": "", "replace-client-name": "never", "sender-ip": "0.0.0.0", "sender-port": 0, "server-ip": "127.0.0.1", "server-port": 53001 }, "dhcp4o6-port": 0, "expired-leases-processing": { "flush-reclaimed-timer-wait-time": 25, "hold-reclaimed-time": 3600, "max-reclaim-leases": 100, "max-reclaim-time": 250, "reclaim-timer-wait-time": 10, "unwarned-reclaim-cycles": 5 }, "hooks-libraries": [  ], "host-reservation-identifiers": [ "hw-address", "duid" ], "interfaces-config": { "interfaces": [ "$(SERVER_IFACE)" ], "re-detect": true }, "lease-database": { "type": "memfile" }, "mac-sources": [ "any" ], "option-data": [  ], "option-def": [  ], "relay-supplied-options": [ "65" ], "server-id": { "enterprise-id": 0, "htype": 0, "identifier": "", "persist": true, "time": 0, "type": "LLT" }, "shared-networks": [  ], "subnet6": [ { "id": 1, "interface": "$(SERVER_IFACE)", "option-data": [  ], "pd-pools": [  ], "pools": [ { "option-data": [  ], "pool": "2001:db8:1::1-2001:db8:1::1" } ], "preferred-lifetime": 3000, "rapid-commit": false, "rebind-timer": 2000, "relay": { "ip-address": "::" }, "renew-timer": 1000, "reservation-mode": "all", "reservations": [  ], "subnet": "2001:db8:1::/64", "valid-lifetime": 4000 } ] }\'' % world.f_cfg.run_join('control_socket'))  # TODO: why generated config is not taken?
    srv_msg.forge_sleep('5', 'seconds')

    misc.test_procedure()
    srv_msg.client_sets_value('Client', 'DUID', '00:03:00:01:66:55:44:33:22:11')
    srv_msg.client_does_include('Client', None, 'client-id')
    srv_msg.client_does_include('Client', None, 'IA_Address')
    srv_msg.client_does_include('Client', None, 'IA-NA')
    srv_msg.client_send_msg('SOLICIT')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', None, 'ADVERTISE')
    srv_msg.response_check_include_option('Response', None, '1')
    srv_msg.response_check_include_option('Response', None, '2')
    srv_msg.response_check_include_option('Response', None, '3')
    srv_msg.response_check_option_content('Response', '3', None, 'sub-option', '5')
    srv_msg.response_check_suboption_content('Response',
                                             '5',
                                             '3',
                                             None,
                                             'addr',
                                             '2001:db8:1::1')

    srv_msg.execute_kea_shell('--host 127.0.0.1 --port 8000 --service dhcp6 config-write <<<\'\'')
    srv_msg.forge_sleep('5', 'seconds')
    # TODO tests needed for not valid/not permitted paths

    srv_control.start_srv('DHCP', 'restarted')

    misc.test_procedure()
    srv_msg.client_sets_value('Client', 'DUID', '00:03:00:01:66:55:44:33:22:11')
    srv_msg.client_does_include('Client', None, 'client-id')
    srv_msg.client_does_include('Client', None, 'IA_Address')
    srv_msg.client_does_include('Client', None, 'IA-NA')
    srv_msg.client_send_msg('SOLICIT')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', None, 'ADVERTISE')
    srv_msg.response_check_include_option('Response', None, '1')
    srv_msg.response_check_include_option('Response', None, '2')
    srv_msg.response_check_include_option('Response', None, '3')
    srv_msg.response_check_option_content('Response', '3', None, 'sub-option', '5')
    srv_msg.response_check_suboption_content('Response',
                                             '5',
                                             '3',
                                             None,
                                             'addr',
                                             '2001:db8:1::1')


@pytest.mark.v6
@pytest.mark.controlchannel
@pytest.mark.kea_only
def test_control_channel_socket_reload_config():

    misc.test_setup()
    srv_control.config_srv_subnet('3000::/64', '3000::1-3000::1')
    srv_control.open_control_channel()
    srv_control.agent_control_channel('127.0.0.1')
    srv_control.build_and_send_config_files('SSH', 'config-file')
    srv_control.start_srv('DHCP', 'started')

    misc.test_procedure()
    srv_msg.client_sets_value('Client', 'DUID', '00:03:00:01:66:55:44:33:22:11')
    srv_msg.client_does_include('Client', None, 'client-id')
    srv_msg.client_does_include('Client', None, 'IA_Address')
    srv_msg.client_does_include('Client', None, 'IA-NA')
    srv_msg.client_send_msg('SOLICIT')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', None, 'ADVERTISE')
    srv_msg.response_check_include_option('Response', None, '1')
    srv_msg.response_check_include_option('Response', None, '2')
    srv_msg.response_check_include_option('Response', None, '3')
    srv_msg.response_check_option_content('Response', '3', None, 'sub-option', '5')
    srv_msg.response_check_suboption_content('Response', '5', '3', None, 'addr', '3000::1')

    misc.test_setup()
    srv_control.config_srv_subnet('2001:db8:1::/64', '2001:db8:1::1-2001:db8:1::1')
    srv_control.open_control_channel()
    srv_control.agent_control_channel('127.0.0.1')
    srv_control.build_and_send_config_files('SSH', 'config-file')

    srv_msg.execute_kea_shell('--host 127.0.0.1 --port 8000 --service dhcp6 config-reload <<<\'\'')
    srv_msg.forge_sleep('5', 'seconds')

    misc.test_procedure()
    srv_msg.client_sets_value('Client', 'DUID', '00:03:00:01:66:55:44:33:22:11')
    srv_msg.client_does_include('Client', None, 'client-id')
    srv_msg.client_does_include('Client', None, 'IA_Address')
    srv_msg.client_does_include('Client', None, 'IA-NA')
    srv_msg.client_send_msg('SOLICIT')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', None, 'ADVERTISE')
    srv_msg.response_check_include_option('Response', None, '1')
    srv_msg.response_check_include_option('Response', None, '2')
    srv_msg.response_check_include_option('Response', None, '3')
    srv_msg.response_check_option_content('Response', '3', None, 'sub-option', '5')
    srv_msg.response_check_suboption_content('Response',
                                             '5',
                                             '3',
                                             None,
                                             'addr',
                                             '2001:db8:1::1')

    srv_control.start_srv('DHCP', 'restarted')

    misc.test_procedure()
    srv_msg.client_sets_value('Client', 'DUID', '00:03:00:01:66:55:44:33:22:11')
    srv_msg.client_does_include('Client', None, 'client-id')
    srv_msg.client_does_include('Client', None, 'IA_Address')
    srv_msg.client_does_include('Client', None, 'IA-NA')
    srv_msg.client_send_msg('SOLICIT')

    misc.pass_criteria()
    srv_msg.send_wait_for_message('MUST', None, 'ADVERTISE')
    srv_msg.response_check_include_option('Response', None, '1')
    srv_msg.response_check_include_option('Response', None, '2')
    srv_msg.response_check_include_option('Response', None, '3')
    srv_msg.response_check_option_content('Response', '3', None, 'sub-option', '5')
    srv_msg.response_check_suboption_content('Response',
                                             '5',
                                             '3',
                                             None,
                                             'addr',
                                             '2001:db8:1::1')
