"""Kea Control Channel Script"""

# pylint: disable=invalid-name,line-too-long

import pytest

from features import srv_control
from features import srv_msg
from features import misc


@pytest.mark.v6
@pytest.mark.controlchannel
@pytest.mark.kea_onlyn
def test_control_channel_keashell_dhcp_disable_timer(step):
    misc.test_setup(step)
    srv_control.config_srv_subnet(step, '3000::/64', '3000::1-3000::f')
    srv_control.open_control_channel(step,
                                     'unix',
                                     '$(SOFTWARE_INSTALL_DIR)/var/kea/control_socket')
    srv_control.agent_control_channel(step,
                                      '127.0.0.1',
                                      '8000',
                                      'unix',
                                      '$(SOFTWARE_INSTALL_DIR)/var/kea/control_socket')
    srv_control.build_and_send_config_files(step, 'SSH', 'config-file')

    srv_control.start_srv(step, 'DHCP', 'started')

    misc.test_procedure(step)
    srv_msg.client_sets_value(step, 'Client', 'DUID', '00:03:00:01:66:55:44:33:22:11')
    srv_msg.client_does_include(step, 'Client', None, 'client-id')
    srv_msg.client_does_include(step, 'Client', None, 'IA_Address')
    srv_msg.client_does_include(step, 'Client', None, 'IA-NA')
    srv_msg.client_send_msg(step, 'SOLICIT')

    misc.pass_criteria(step)
    srv_msg.send_wait_for_message(step, 'MUST', None, 'ADVERTISE')
    srv_msg.response_check_include_option(step, 'Response', None, '1')
    srv_msg.response_check_include_option(step, 'Response', None, '2')
    srv_msg.response_check_include_option(step, 'Response', None, '3')
    srv_msg.response_check_option_content(step, 'Response', '3', None, 'sub-option', '5')
    srv_msg.response_check_suboption_content(step,
                                             'Response',
                                             '5',
                                             '3',
                                             None,
                                             'address',
                                             '3000::1')

    srv_msg.execute_shell_with_args(step,
                                    'python',
                                    '$(SOFTWARE_INSTALL_DIR)/sbin/kea-shell',
                                    '--host 127.0.0.1 --port 8000 --service dhcp6 dhcp-disable <<<\'"max-period": 5\'')

    misc.test_procedure(step)
    srv_msg.client_sets_value(step, 'Client', 'DUID', '00:03:00:01:66:55:44:33:22:11')
    srv_msg.client_does_include(step, 'Client', None, 'client-id')
    srv_msg.client_does_include(step, 'Client', None, 'IA_Address')
    srv_msg.client_does_include(step, 'Client', None, 'IA-NA')
    srv_msg.client_send_msg(step, 'SOLICIT')

    misc.pass_criteria(step)
    srv_msg.send_dont_wait_for_message(step)

    srv_msg.forge_sleep(step, '7', 'seconds')

    misc.test_procedure(step)
    srv_msg.client_sets_value(step, 'Client', 'DUID', '00:03:00:01:66:55:44:33:22:11')
    srv_msg.client_does_include(step, 'Client', None, 'client-id')
    srv_msg.client_does_include(step, 'Client', None, 'IA_Address')
    srv_msg.client_does_include(step, 'Client', None, 'IA-NA')
    srv_msg.client_send_msg(step, 'SOLICIT')

    misc.pass_criteria(step)
    srv_msg.send_wait_for_message(step, 'MUST', None, 'ADVERTISE')
    srv_msg.response_check_include_option(step, 'Response', None, '1')
    srv_msg.response_check_include_option(step, 'Response', None, '2')
    srv_msg.response_check_include_option(step, 'Response', None, '3')
    srv_msg.response_check_option_content(step, 'Response', '3', None, 'sub-option', '5')


@pytest.mark.v6
@pytest.mark.controlchannel
@pytest.mark.kea_only
def test_control_channel_keashell_dhcp_disable(step):
    misc.test_setup(step)
    srv_control.config_srv_subnet(step, '3000::/64', '3000::1-3000::f')
    srv_control.open_control_channel(step,
                                     'unix',
                                     '$(SOFTWARE_INSTALL_DIR)/var/kea/control_socket')
    srv_control.agent_control_channel(step,
                                      '127.0.0.1',
                                      '8000',
                                      'unix',
                                      '$(SOFTWARE_INSTALL_DIR)/var/kea/control_socket')
    srv_control.build_and_send_config_files(step, 'SSH', 'config-file')

    srv_control.start_srv(step, 'DHCP', 'started')

    misc.test_procedure(step)
    srv_msg.client_sets_value(step, 'Client', 'DUID', '00:03:00:01:66:55:44:33:22:11')
    srv_msg.client_does_include(step, 'Client', None, 'client-id')
    srv_msg.client_does_include(step, 'Client', None, 'IA_Address')
    srv_msg.client_does_include(step, 'Client', None, 'IA-NA')
    srv_msg.client_send_msg(step, 'SOLICIT')

    misc.pass_criteria(step)
    srv_msg.send_wait_for_message(step, 'MUST', None, 'ADVERTISE')
    srv_msg.response_check_include_option(step, 'Response', None, '1')
    srv_msg.response_check_include_option(step, 'Response', None, '2')
    srv_msg.response_check_include_option(step, 'Response', None, '3')
    srv_msg.response_check_option_content(step, 'Response', '3', None, 'sub-option', '5')
    srv_msg.response_check_suboption_content(step,
                                             'Response',
                                             '5',
                                             '3',
                                             None,
                                             'address',
                                             '3000::1')

    srv_msg.execute_shell_with_args(step,
                                    'python',
                                    '$(SOFTWARE_INSTALL_DIR)/sbin/kea-shell',
                                    '--host 127.0.0.1 --port 8000 --service dhcp6 dhcp-disable <<<\'\'')

    misc.test_procedure(step)
    srv_msg.client_sets_value(step, 'Client', 'DUID', '00:03:00:01:66:55:44:33:22:11')
    srv_msg.client_does_include(step, 'Client', None, 'client-id')
    srv_msg.client_does_include(step, 'Client', None, 'IA_Address')
    srv_msg.client_does_include(step, 'Client', None, 'IA-NA')
    srv_msg.client_send_msg(step, 'SOLICIT')

    misc.pass_criteria(step)
    srv_msg.send_dont_wait_for_message(step)


@pytest.mark.v6
@pytest.mark.controlchannel
@pytest.mark.kea_only
def test_control_channel_keashell_dhcp_disable_and_enable(step):
    misc.test_setup(step)
    srv_control.config_srv_subnet(step, '3000::/64', '3000::1-3000::f')
    srv_control.open_control_channel(step,
                                     'unix',
                                     '$(SOFTWARE_INSTALL_DIR)/var/kea/control_socket')
    srv_control.agent_control_channel(step,
                                      '127.0.0.1',
                                      '8000',
                                      'unix',
                                      '$(SOFTWARE_INSTALL_DIR)/var/kea/control_socket')
    srv_control.build_and_send_config_files(step, 'SSH', 'config-file')

    srv_control.start_srv(step, 'DHCP', 'started')

    misc.test_procedure(step)
    srv_msg.client_sets_value(step, 'Client', 'DUID', '00:03:00:01:66:55:44:33:22:11')
    srv_msg.client_does_include(step, 'Client', None, 'client-id')
    srv_msg.client_does_include(step, 'Client', None, 'IA_Address')
    srv_msg.client_does_include(step, 'Client', None, 'IA-NA')
    srv_msg.client_send_msg(step, 'SOLICIT')

    misc.pass_criteria(step)
    srv_msg.send_wait_for_message(step, 'MUST', None, 'ADVERTISE')
    srv_msg.response_check_include_option(step, 'Response', None, '1')
    srv_msg.response_check_include_option(step, 'Response', None, '2')
    srv_msg.response_check_include_option(step, 'Response', None, '3')
    srv_msg.response_check_option_content(step, 'Response', '3', None, 'sub-option', '5')
    srv_msg.response_check_suboption_content(step,
                                             'Response',
                                             '5',
                                             '3',
                                             None,
                                             'address',
                                             '3000::1')

    srv_msg.execute_shell_with_args(step,
                                    'python',
                                    '$(SOFTWARE_INSTALL_DIR)/sbin/kea-shell',
                                    '--host 127.0.0.1 --port 8000 --service dhcp6 dhcp-disable <<<\'\'')

    misc.test_procedure(step)
    srv_msg.client_sets_value(step, 'Client', 'DUID', '00:03:00:01:66:55:44:33:22:11')
    srv_msg.client_does_include(step, 'Client', None, 'client-id')
    srv_msg.client_does_include(step, 'Client', None, 'IA_Address')
    srv_msg.client_does_include(step, 'Client', None, 'IA-NA')
    srv_msg.client_send_msg(step, 'SOLICIT')

    misc.pass_criteria(step)
    srv_msg.send_dont_wait_for_message(step)
    srv_msg.execute_shell_with_args(step,
                                    'python',
                                    '$(SOFTWARE_INSTALL_DIR)/sbin/kea-shell',
                                    '--host 127.0.0.1 --port 8000 --service dhcp6 dhcp-enable <<<\'\'')

    misc.test_procedure(step)
    srv_msg.client_sets_value(step, 'Client', 'DUID', '00:03:00:01:66:55:44:33:22:11')
    srv_msg.client_does_include(step, 'Client', None, 'client-id')
    srv_msg.client_does_include(step, 'Client', None, 'IA_Address')
    srv_msg.client_does_include(step, 'Client', None, 'IA-NA')
    srv_msg.client_send_msg(step, 'SOLICIT')

    misc.pass_criteria(step)
    srv_msg.send_wait_for_message(step, 'MUST', None, 'ADVERTISE')
    srv_msg.response_check_include_option(step, 'Response', None, '1')
    srv_msg.response_check_include_option(step, 'Response', None, '2')
    srv_msg.response_check_include_option(step, 'Response', None, '3')
    srv_msg.response_check_option_content(step, 'Response', '3', None, 'sub-option', '5')


@pytest.mark.v6
@pytest.mark.controlchannel
@pytest.mark.kea_only
def test_control_channel_keashell_set_config_basic(step):
    misc.test_setup(step)
    srv_control.config_srv_subnet(step, '3000::/64', '3000::1-3000::f')
    srv_control.open_control_channel(step,
                                     'unix',
                                     '$(SOFTWARE_INSTALL_DIR)/var/kea/control_socket')
    srv_control.agent_control_channel(step,
                                      '127.0.0.1',
                                      '8000',
                                      'unix',
                                      '$(SOFTWARE_INSTALL_DIR)/var/kea/control_socket')
    srv_control.build_and_send_config_files(step, 'SSH', 'config-file')

    srv_control.start_srv(step, 'DHCP', 'started')
    srv_msg.forge_sleep(step, '2', 'seconds')

    misc.test_procedure(step)
    srv_msg.client_sets_value(step, 'Client', 'DUID', '00:03:00:01:66:55:44:33:22:11')
    srv_msg.client_does_include(step, 'Client', None, 'client-id')
    srv_msg.client_does_include(step, 'Client', None, 'IA_Address')
    srv_msg.client_does_include(step, 'Client', None, 'IA-NA')
    srv_msg.client_send_msg(step, 'SOLICIT')

    misc.pass_criteria(step)
    srv_msg.send_wait_for_message(step, 'MUST', None, 'ADVERTISE')
    srv_msg.response_check_include_option(step, 'Response', None, '1')
    srv_msg.response_check_include_option(step, 'Response', None, '2')
    srv_msg.response_check_include_option(step, 'Response', None, '3')
    srv_msg.response_check_option_content(step, 'Response', '3', None, 'sub-option', '5')
    srv_msg.response_check_suboption_content(step,
                                             'Response',
                                             '5',
                                             '3',
                                             None,
                                             'address',
                                             '3000::1')

    # this command is with new configuration
    srv_msg.execute_shell_with_args(step,
                                    'python',
                                    '$(SOFTWARE_INSTALL_DIR)/sbin/kea-shell',
                                    '--host 127.0.0.1 --port 8000 --service dhcp6 config-set <<<\'"Dhcp6": { "control-socket": { "socket-name": "$(SOFTWARE_INSTALL_DIR)/var/kea/control_socket", "socket-type": "unix" }, "decline-probation-period": 86400, "dhcp-ddns": { "always-include-fqdn": false, "enable-updates": false, "generated-prefix": "myhost", "max-queue-size": 1024, "ncr-format": "JSON", "ncr-protocol": "UDP", "override-client-update": false, "override-no-update": false, "qualifying-suffix": "", "replace-client-name": "never", "sender-ip": "0.0.0.0", "sender-port": 0, "server-ip": "127.0.0.1", "server-port": 53001 }, "dhcp4o6-port": 0, "expired-leases-processing": { "flush-reclaimed-timer-wait-time": 25, "hold-reclaimed-time": 3600, "max-reclaim-leases": 100, "max-reclaim-time": 250, "reclaim-timer-wait-time": 10, "unwarned-reclaim-cycles": 5 }, "hooks-libraries": [  ], "host-reservation-identifiers": [ "hw-address", "duid" ], "interfaces-config": { "interfaces": [ "$(SERVER_IFACE)" ], "re-detect": true }, "lease-database": { "type": "memfile" }, "mac-sources": [ "any" ], "option-data": [  ], "option-def": [  ], "relay-supplied-options": [ "65" ], "server-id": { "enterprise-id": 0, "htype": 0, "identifier": "", "persist": true, "time": 0, "type": "LLT" }, "shared-networks": [  ], "subnet6": [ { "id": 1, "interface": "$(SERVER_IFACE)", "option-data": [  ], "pd-pools": [  ], "pools": [ { "option-data": [  ], "pool": "2001:db8:1::1-2001:db8:1::1" } ], "preferred-lifetime": 3000, "rapid-commit": false, "rebind-timer": 2000, "relay": { "ip-address": "::" }, "renew-timer": 1000, "reservation-mode": "all", "reservations": [  ], "subnet": "2001:db8:1::/64", "valid-lifetime": 4000 } ] }\'')

    misc.test_procedure(step)
    srv_msg.client_sets_value(step, 'Client', 'DUID', '00:03:00:01:66:55:44:33:22:11')
    srv_msg.client_does_include(step, 'Client', None, 'client-id')
    srv_msg.client_does_include(step, 'Client', None, 'IA_Address')
    srv_msg.client_does_include(step, 'Client', None, 'IA-NA')
    srv_msg.client_send_msg(step, 'SOLICIT')

    misc.pass_criteria(step)
    srv_msg.send_wait_for_message(step, 'MUST', None, 'ADVERTISE')
    srv_msg.response_check_include_option(step, 'Response', None, '1')
    srv_msg.response_check_include_option(step, 'Response', None, '2')
    srv_msg.response_check_include_option(step, 'Response', None, '3')
    srv_msg.response_check_option_content(step, 'Response', '3', None, 'sub-option', '5')
    srv_msg.response_check_suboption_content(step,
                                             'Response',
                                             '5',
                                             '3',
                                             None,
                                             'address',
                                             '2001:db8:1::1')


@pytest.mark.v6
@pytest.mark.controlchannel
@pytest.mark.kea_only
def test_control_channel_keashell_after_restart_load_config_file(step):

    misc.test_setup(step)
    srv_control.config_srv_subnet(step, '3000::/64', '3000::1-3000::f')
    srv_control.open_control_channel(step,
                                     'unix',
                                     '$(SOFTWARE_INSTALL_DIR)/var/kea/control_socket')
    srv_control.agent_control_channel(step,
                                      '127.0.0.1',
                                      '8000',
                                      'unix',
                                      '$(SOFTWARE_INSTALL_DIR)/var/kea/control_socket')
    srv_control.build_and_send_config_files(step, 'SSH', 'config-file')
    srv_control.start_srv(step, 'DHCP', 'started')
    srv_msg.forge_sleep(step, '2', 'seconds')

    misc.test_procedure(step)
    srv_msg.client_sets_value(step, 'Client', 'DUID', '00:03:00:01:66:55:44:33:22:11')
    srv_msg.client_does_include(step, 'Client', None, 'client-id')
    srv_msg.client_does_include(step, 'Client', None, 'IA_Address')
    srv_msg.client_does_include(step, 'Client', None, 'IA-NA')
    srv_msg.client_send_msg(step, 'SOLICIT')

    misc.pass_criteria(step)
    srv_msg.send_wait_for_message(step, 'MUST', None, 'ADVERTISE')
    srv_msg.response_check_include_option(step, 'Response', None, '1')
    srv_msg.response_check_include_option(step, 'Response', None, '2')
    srv_msg.response_check_include_option(step, 'Response', None, '3')
    srv_msg.response_check_option_content(step, 'Response', '3', None, 'sub-option', '5')
    srv_msg.response_check_suboption_content(step,
                                             'Response',
                                             '5',
                                             '3',
                                             None,
                                             'address',
                                             '3000::1')

    srv_msg.execute_shell_with_args(step,
                                    'python',
                                    '$(SOFTWARE_INSTALL_DIR)/sbin/kea-shell',
                                    '--host 127.0.0.1 --port 8000 --service dhcp6 config-set <<<\'"Dhcp6": { "control-socket": { "socket-name": "$(SOFTWARE_INSTALL_DIR)/var/kea/control_socket", "socket-type": "unix" }, "decline-probation-period": 86400, "dhcp-ddns": { "always-include-fqdn": false, "enable-updates": false, "generated-prefix": "myhost", "max-queue-size": 1024, "ncr-format": "JSON", "ncr-protocol": "UDP", "override-client-update": false, "override-no-update": false, "qualifying-suffix": "", "replace-client-name": "never", "sender-ip": "0.0.0.0", "sender-port": 0, "server-ip": "127.0.0.1", "server-port": 53001 }, "dhcp4o6-port": 0, "expired-leases-processing": { "flush-reclaimed-timer-wait-time": 25, "hold-reclaimed-time": 3600, "max-reclaim-leases": 100, "max-reclaim-time": 250, "reclaim-timer-wait-time": 10, "unwarned-reclaim-cycles": 5 }, "hooks-libraries": [  ], "host-reservation-identifiers": [ "hw-address", "duid" ], "interfaces-config": { "interfaces": [ "$(SERVER_IFACE)" ], "re-detect": true }, "lease-database": { "type": "memfile" }, "mac-sources": [ "any" ], "option-data": [  ], "option-def": [  ], "relay-supplied-options": [ "65" ], "server-id": { "enterprise-id": 0, "htype": 0, "identifier": "", "persist": true, "time": 0, "type": "LLT" }, "shared-networks": [  ], "subnet6": [ { "id": 1, "interface": "$(SERVER_IFACE)", "option-data": [  ], "pd-pools": [  ], "pools": [ { "option-data": [  ], "pool": "2001:db8:1::1-2001:db8:1::1" } ], "preferred-lifetime": 3000, "rapid-commit": false, "rebind-timer": 2000, "relay": { "ip-address": "::" }, "renew-timer": 1000, "reservation-mode": "all", "reservations": [  ], "subnet": "2001:db8:1::/64", "valid-lifetime": 4000 } ] }\'')

    misc.test_procedure(step)
    srv_msg.client_sets_value(step, 'Client', 'DUID', '00:03:00:01:66:55:44:33:22:11')
    srv_msg.client_does_include(step, 'Client', None, 'client-id')
    srv_msg.client_does_include(step, 'Client', None, 'IA_Address')
    srv_msg.client_does_include(step, 'Client', None, 'IA-NA')
    srv_msg.client_send_msg(step, 'SOLICIT')

    misc.pass_criteria(step)
    srv_msg.send_wait_for_message(step, 'MUST', None, 'ADVERTISE')
    srv_msg.response_check_include_option(step, 'Response', None, '1')
    srv_msg.response_check_include_option(step, 'Response', None, '2')
    srv_msg.response_check_include_option(step, 'Response', None, '3')
    srv_msg.response_check_option_content(step, 'Response', '3', None, 'sub-option', '5')
    srv_msg.response_check_suboption_content(step,
                                             'Response',
                                             '5',
                                             '3',
                                             None,
                                             'address',
                                             '2001:db8:1::1')

    srv_control.start_srv(step, 'DHCP', 'restarted')

    misc.test_procedure(step)
    srv_msg.client_sets_value(step, 'Client', 'DUID', '00:03:00:01:66:55:44:33:22:11')
    srv_msg.client_does_include(step, 'Client', None, 'client-id')
    srv_msg.client_does_include(step, 'Client', None, 'IA_Address')
    srv_msg.client_does_include(step, 'Client', None, 'IA-NA')
    srv_msg.client_send_msg(step, 'SOLICIT')

    misc.pass_criteria(step)
    srv_msg.send_wait_for_message(step, 'MUST', None, 'ADVERTISE')
    srv_msg.response_check_include_option(step, 'Response', None, '1')
    srv_msg.response_check_include_option(step, 'Response', None, '2')
    srv_msg.response_check_include_option(step, 'Response', None, '3')
    srv_msg.response_check_option_content(step, 'Response', '3', None, 'sub-option', '5')
    srv_msg.response_check_suboption_content(step,
                                             'Response',
                                             '5',
                                             '3',
                                             None,
                                             'address',
                                             '3000::1')


@pytest.mark.v6
@pytest.mark.controlchannel
@pytest.mark.kea_only
def test_control_channel_keashell_get_config(step):
    misc.test_setup(step)
    srv_control.config_srv_subnet(step, '3000::/64', '3000::1-3000::f')
    srv_control.open_control_channel(step,
                                     'unix',
                                     '$(SOFTWARE_INSTALL_DIR)/var/kea/control_socket')
    srv_control.agent_control_channel(step,
                                      '127.0.0.1',
                                      '8000',
                                      'unix',
                                      '$(SOFTWARE_INSTALL_DIR)/var/kea/control_socket')
    srv_control.build_and_send_config_files(step, 'SSH', 'config-file')

    srv_control.start_srv(step, 'DHCP', 'started')

    srv_msg.execute_shell_with_args(step,
                                    'python',
                                    '$(SOFTWARE_INSTALL_DIR)/sbin/kea-shell',
                                    '--host 127.0.0.1 --port 8000 --service dhcp6 config-get <<<\'\'')


@pytest.mark.v6
@pytest.mark.controlchannel
@pytest.mark.kea_only
@pytest.mark.disabled
def test_control_channel_keashell_test_config(step):
    misc.test_setup(step)
    srv_control.config_srv_subnet(step, '3000::/64', '3000::1-3000::1')
    srv_control.open_control_channel(step,
                                     'unix',
                                     '$(SOFTWARE_INSTALL_DIR)/var/kea/control_socket')
    srv_control.agent_control_channel(step,
                                      '127.0.0.1',
                                      '8000',
                                      'unix',
                                      '$(SOFTWARE_INSTALL_DIR)/var/kea/control_socket')
    srv_control.build_and_send_config_files(step, 'SSH', 'config-file')

    srv_control.start_srv(step, 'DHCP', 'started')

    misc.test_procedure(step)
    srv_msg.client_sets_value(step, 'Client', 'DUID', '00:03:00:01:66:55:44:33:22:11')
    srv_msg.client_does_include(step, 'Client', None, 'client-id')
    srv_msg.client_does_include(step, 'Client', None, 'IA_Address')
    srv_msg.client_does_include(step, 'Client', None, 'IA-NA')
    srv_msg.client_send_msg(step, 'SOLICIT')

    misc.pass_criteria(step)
    srv_msg.send_wait_for_message(step, 'MUST', None, 'ADVERTISE')
    srv_msg.response_check_include_option(step, 'Response', None, '1')
    srv_msg.response_check_include_option(step, 'Response', None, '2')
    srv_msg.response_check_include_option(step, 'Response', None, '3')
    srv_msg.response_check_option_content(step, 'Response', '3', None, 'sub-option', '5')
    srv_msg.response_check_suboption_content(step,
                                             'Response',
                                             '5',
                                             '3',
                                             None,
                                             'address',
                                             '3000::1')

    misc.test_setup(step)
    srv_control.config_srv_subnet(step, '2001:db8:a::/64', '2001:db8:a::1-2001:db8:a::1')
    srv_control.config_srv_prefix(step, '2001:db8:1::', '0', '90', '96')
    srv_control.agent_control_channel(step,
                                      '$(SRV4_ADDR)',
                                      '8000',
                                      'unix',
                                      '$(SOFTWARE_INSTALL_DIR)/var/kea/control_socket_ANOTHER_ONE')
    srv_control.config_srv_id(step, 'LLT', '00:01:00:02:52:7b:a8:f0:08:00:27:58:f1:e8')
    srv_control.config_srv_opt(step, 'sip-server-addr', '2001:db8::1,2001:db8::2')
    srv_control.config_srv_opt(step,
                               'new-posix-timezone',
                               'EST5EDT4\\,M3.2.0/02:00\\,M11.1.0/02:00')
    srv_control.host_reservation_in_subnet(step,
                                           'address',
                                           '3000::1',
                                           '0',
                                           'duid',
                                           '00:03:00:01:f6:f5:f4:f3:f2:01')
    srv_control.generate_config_files(step)

    srv_msg.execute_shell_with_args(step,
                                    'python',
                                    '$(SOFTWARE_INSTALL_DIR)/sbin/kea-shell',
                                    '--host 127.0.0.1 --port 8000 --service dhcp6 config-test <<<\'$(SERVER_CONFIG)\'')

    misc.test_procedure(step)
    srv_msg.client_sets_value(step, 'Client', 'DUID', '00:03:00:01:66:55:44:33:22:11')
    srv_msg.client_does_include(step, 'Client', None, 'client-id')
    srv_msg.client_does_include(step, 'Client', None, 'IA_Address')
    srv_msg.client_does_include(step, 'Client', None, 'IA-NA')
    srv_msg.client_send_msg(step, 'SOLICIT')

    misc.pass_criteria(step)
    srv_msg.send_wait_for_message(step, 'MUST', None, 'ADVERTISE')
    srv_msg.response_check_include_option(step, 'Response', None, '1')
    srv_msg.response_check_include_option(step, 'Response', None, '2')
    srv_msg.response_check_include_option(step, 'Response', None, '3')
    srv_msg.response_check_option_content(step, 'Response', '3', None, 'sub-option', '5')
    srv_msg.response_check_suboption_content(step,
                                             'Response',
                                             '5',
                                             '3',
                                             None,
                                             'address',
                                             '3000::1')

    misc.test_setup(step)
    srv_control.config_srv_subnet(step, '2001:db8:a::/64', '2001:db8:a::1-2001:db8:a::1')
    srv_control.config_srv_prefix(step, '2001:db8:1::', '0', '90', '96')
    srv_control.agent_control_channel(step,
                                      '$(SRV4_ADDR)',
                                      '8000',
                                      'unix',
                                      '$(SOFTWARE_INSTALL_DIR)/var/kea/control_socket_ANOTHER_ONE')
    srv_control.config_srv_id(step, 'LLT', '00:01:00:02:52:7b:a8:f0:08:00:27:58:f1:e8')
    srv_control.config_srv_opt(step, 'sip-server-addr', '2001:db8::1,2001:db8::2')
    srv_control.config_srv_opt(step,
                               'new-posix-timezone',
                               'EST5EDT4\\,M3.2.0/02:00\\,M11.1.0/02:00')
    # WRONG ADDRESS RESERVATION
    srv_control.host_reservation_in_subnet(step,
                                           'address',
                                           '192.168.0.5',
                                           '0',
                                           'duid',
                                           '00:03:00:01:f6:f5:f4:f3:f2:01')
    srv_control.generate_config_files(step)

    srv_msg.execute_shell_with_args(step,
                                    'python',
                                    '$(SOFTWARE_INSTALL_DIR)/sbin/kea-shell',
                                    '--host 127.0.0.1 --port 8000 --service dhcp6 config-test <<<\'$(SERVER_CONFIG)\'')
    srv_msg.forge_sleep(step, '5', 'seconds')

    misc.test_procedure(step)
    srv_msg.client_sets_value(step, 'Client', 'DUID', '00:03:00:01:66:55:44:33:22:11')
    srv_msg.client_does_include(step, 'Client', None, 'client-id')
    srv_msg.client_does_include(step, 'Client', None, 'IA_Address')
    srv_msg.client_does_include(step, 'Client', None, 'IA-NA')
    srv_msg.client_send_msg(step, 'SOLICIT')

    misc.pass_criteria(step)
    srv_msg.send_wait_for_message(step, 'MUST', None, 'ADVERTISE')
    srv_msg.response_check_include_option(step, 'Response', None, '1')
    srv_msg.response_check_include_option(step, 'Response', None, '2')
    srv_msg.response_check_include_option(step, 'Response', None, '3')
    srv_msg.response_check_option_content(step, 'Response', '3', None, 'sub-option', '5')
    srv_msg.response_check_suboption_content(step,
                                             'Response',
                                             '5',
                                             '3',
                                             None,
                                             'address',
                                             '3000::1')


@pytest.mark.v6
@pytest.mark.controlchannel
@pytest.mark.kea_only
def test_control_channel_keashell_write_config(step):

    misc.test_setup(step)
    srv_control.config_srv_subnet(step, '3000::/64', '3000::1-3000::1')
    srv_control.open_control_channel(step,
                                     'unix',
                                     '$(SOFTWARE_INSTALL_DIR)/var/kea/control_socket')
    srv_control.agent_control_channel(step,
                                      '127.0.0.1',
                                      '8000',
                                      'unix',
                                      '$(SOFTWARE_INSTALL_DIR)/var/kea/control_socket')
    srv_control.build_and_send_config_files(step, 'SSH', 'config-file')
    srv_control.start_srv(step, 'DHCP', 'started')
    srv_msg.forge_sleep(step, '2', 'seconds')

    misc.test_procedure(step)
    srv_msg.client_sets_value(step, 'Client', 'DUID', '00:03:00:01:66:55:44:33:22:11')
    srv_msg.client_does_include(step, 'Client', None, 'client-id')
    srv_msg.client_does_include(step, 'Client', None, 'IA_Address')
    srv_msg.client_does_include(step, 'Client', None, 'IA-NA')
    srv_msg.client_send_msg(step, 'SOLICIT')

    misc.pass_criteria(step)
    srv_msg.send_wait_for_message(step, 'MUST', None, 'ADVERTISE')
    srv_msg.response_check_include_option(step, 'Response', None, '1')
    srv_msg.response_check_include_option(step, 'Response', None, '2')
    srv_msg.response_check_option_content(step, 'Response', '3', None, 'sub-option', '5')
    srv_msg.response_check_suboption_content(step,
                                             'Response',
                                             '5',
                                             '3',
                                             None,
                                             'address',
                                             '3000::1')

    misc.test_setup(step)
    srv_control.config_srv_subnet(step, '2001:db8:1::/64', '2001:db8:1::1-2001:db8:1::1')
    srv_control.agent_control_channel(step,
                                      'localhost',
                                      '8000',
                                      'UNIX',
                                      '$(SOFTWARE_INSTALL_DIR)/var/kea/control_socket')
    srv_control.generate_config_files(step)

    srv_msg.execute_shell_with_args(step,
                                    'python',
                                    '$(SOFTWARE_INSTALL_DIR)/sbin/kea-shell',
                                    '--host 127.0.0.1 --port 8000 --service dhcp6 config-set <<<\'"Dhcp6": { "control-socket": { "socket-name": "$(SOFTWARE_INSTALL_DIR)/var/kea/control_socket", "socket-type": "unix" }, "decline-probation-period": 86400, "dhcp-ddns": { "always-include-fqdn": false, "enable-updates": false, "generated-prefix": "myhost", "max-queue-size": 1024, "ncr-format": "JSON", "ncr-protocol": "UDP", "override-client-update": false, "override-no-update": false, "qualifying-suffix": "", "replace-client-name": "never", "sender-ip": "0.0.0.0", "sender-port": 0, "server-ip": "127.0.0.1", "server-port": 53001 }, "dhcp4o6-port": 0, "expired-leases-processing": { "flush-reclaimed-timer-wait-time": 25, "hold-reclaimed-time": 3600, "max-reclaim-leases": 100, "max-reclaim-time": 250, "reclaim-timer-wait-time": 10, "unwarned-reclaim-cycles": 5 }, "hooks-libraries": [  ], "host-reservation-identifiers": [ "hw-address", "duid" ], "interfaces-config": { "interfaces": [ "$(SERVER_IFACE)" ], "re-detect": true }, "lease-database": { "type": "memfile" }, "mac-sources": [ "any" ], "option-data": [  ], "option-def": [  ], "relay-supplied-options": [ "65" ], "server-id": { "enterprise-id": 0, "htype": 0, "identifier": "", "persist": true, "time": 0, "type": "LLT" }, "shared-networks": [  ], "subnet6": [ { "id": 1, "interface": "$(SERVER_IFACE)", "option-data": [  ], "pd-pools": [  ], "pools": [ { "option-data": [  ], "pool": "2001:db8:1::1-2001:db8:1::1" } ], "preferred-lifetime": 3000, "rapid-commit": false, "rebind-timer": 2000, "relay": { "ip-address": "::" }, "renew-timer": 1000, "reservation-mode": "all", "reservations": [  ], "subnet": "2001:db8:1::/64", "valid-lifetime": 4000 } ] }\'')
    srv_msg.forge_sleep(step, '5', 'seconds')

    misc.test_procedure(step)
    srv_msg.client_sets_value(step, 'Client', 'DUID', '00:03:00:01:66:55:44:33:22:11')
    srv_msg.client_does_include(step, 'Client', None, 'client-id')
    srv_msg.client_does_include(step, 'Client', None, 'IA_Address')
    srv_msg.client_does_include(step, 'Client', None, 'IA-NA')
    srv_msg.client_send_msg(step, 'SOLICIT')

    misc.pass_criteria(step)
    srv_msg.send_wait_for_message(step, 'MUST', None, 'ADVERTISE')
    srv_msg.response_check_include_option(step, 'Response', None, '1')
    srv_msg.response_check_include_option(step, 'Response', None, '2')
    srv_msg.response_check_include_option(step, 'Response', None, '3')
    srv_msg.response_check_option_content(step, 'Response', '3', None, 'sub-option', '5')
    srv_msg.response_check_suboption_content(step,
                                             'Response',
                                             '5',
                                             '3',
                                             None,
                                             'address',
                                             '2001:db8:1::1')

    srv_msg.execute_shell_with_args(step,
                                    'python',
                                    '$(SOFTWARE_INSTALL_DIR)/sbin/kea-shell',
                                    '--host 127.0.0.1 --port 8000 --service dhcp6 config-write <<<\'\'')
    srv_msg.forge_sleep(step, '5', 'seconds')
    # TODO tests needed for not valid/not permitted paths

    srv_control.start_srv(step, 'DHCP', 'restarted')

    misc.test_procedure(step)
    srv_msg.client_sets_value(step, 'Client', 'DUID', '00:03:00:01:66:55:44:33:22:11')
    srv_msg.client_does_include(step, 'Client', None, 'client-id')
    srv_msg.client_does_include(step, 'Client', None, 'IA_Address')
    srv_msg.client_does_include(step, 'Client', None, 'IA-NA')
    srv_msg.client_send_msg(step, 'SOLICIT')

    misc.pass_criteria(step)
    srv_msg.send_wait_for_message(step, 'MUST', None, 'ADVERTISE')
    srv_msg.response_check_include_option(step, 'Response', None, '1')
    srv_msg.response_check_include_option(step, 'Response', None, '2')
    srv_msg.response_check_include_option(step, 'Response', None, '3')
    srv_msg.response_check_option_content(step, 'Response', '3', None, 'sub-option', '5')
    srv_msg.response_check_suboption_content(step,
                                             'Response',
                                             '5',
                                             '3',
                                             None,
                                             'address',
                                             '2001:db8:1::1')


@pytest.mark.v6
@pytest.mark.controlchannel
@pytest.mark.kea_only
def test_control_channel_socket_reload_config(step):

    misc.test_setup(step)
    srv_control.config_srv_subnet(step, '3000::/64', '3000::1-3000::1')
    srv_control.open_control_channel(step,
                                     'unix',
                                     '$(SOFTWARE_INSTALL_DIR)/var/kea/control_socket')
    srv_control.agent_control_channel(step,
                                      '127.0.0.1',
                                      '8000',
                                      'unix',
                                      '$(SOFTWARE_INSTALL_DIR)/var/kea/control_socket')
    srv_control.build_and_send_config_files(step, 'SSH', 'config-file')
    srv_control.start_srv(step, 'DHCP', 'started')

    misc.test_procedure(step)
    srv_msg.client_sets_value(step, 'Client', 'DUID', '00:03:00:01:66:55:44:33:22:11')
    srv_msg.client_does_include(step, 'Client', None, 'client-id')
    srv_msg.client_does_include(step, 'Client', None, 'IA_Address')
    srv_msg.client_does_include(step, 'Client', None, 'IA-NA')
    srv_msg.client_send_msg(step, 'SOLICIT')

    misc.pass_criteria(step)
    srv_msg.send_wait_for_message(step, 'MUST', None, 'ADVERTISE')
    srv_msg.response_check_include_option(step, 'Response', None, '1')
    srv_msg.response_check_include_option(step, 'Response', None, '2')
    srv_msg.response_check_include_option(step, 'Response', None, '3')
    srv_msg.response_check_option_content(step, 'Response', '3', None, 'sub-option', '5')
    srv_msg.response_check_suboption_content(step,
                                             'Response',
                                             '5',
                                             '3',
                                             None,
                                             'address',
                                             '3000::1')

    misc.test_setup(step)
    srv_control.config_srv_subnet(step, '2001:db8:1::/64', '2001:db8:1::1-2001:db8:1::1')
    srv_control.open_control_channel(step,
                                     'unix',
                                     '$(SOFTWARE_INSTALL_DIR)/var/kea/control_socket')
    srv_control.agent_control_channel(step,
                                      '127.0.0.1',
                                      '8000',
                                      'unix',
                                      '$(SOFTWARE_INSTALL_DIR)/var/kea/control_socket')
    srv_control.build_and_send_config_files(step, 'SSH', 'config-file')

    srv_msg.execute_shell_with_args(step,
                                    'python',
                                    '$(SOFTWARE_INSTALL_DIR)/sbin/kea-shell',
                                    '--host 127.0.0.1 --port 8000 --service dhcp6 config-reload <<<\'\'')
    srv_msg.forge_sleep(step, '5', 'seconds')

    misc.test_procedure(step)
    srv_msg.client_sets_value(step, 'Client', 'DUID', '00:03:00:01:66:55:44:33:22:11')
    srv_msg.client_does_include(step, 'Client', None, 'client-id')
    srv_msg.client_does_include(step, 'Client', None, 'IA_Address')
    srv_msg.client_does_include(step, 'Client', None, 'IA-NA')
    srv_msg.client_send_msg(step, 'SOLICIT')

    misc.pass_criteria(step)
    srv_msg.send_wait_for_message(step, 'MUST', None, 'ADVERTISE')
    srv_msg.response_check_include_option(step, 'Response', None, '1')
    srv_msg.response_check_include_option(step, 'Response', None, '2')
    srv_msg.response_check_include_option(step, 'Response', None, '3')
    srv_msg.response_check_option_content(step, 'Response', '3', None, 'sub-option', '5')
    srv_msg.response_check_suboption_content(step,
                                             'Response',
                                             '5',
                                             '3',
                                             None,
                                             'address',
                                             '2001:db8:1::1')

    srv_control.start_srv(step, 'DHCP', 'restarted')

    misc.test_procedure(step)
    srv_msg.client_sets_value(step, 'Client', 'DUID', '00:03:00:01:66:55:44:33:22:11')
    srv_msg.client_does_include(step, 'Client', None, 'client-id')
    srv_msg.client_does_include(step, 'Client', None, 'IA_Address')
    srv_msg.client_does_include(step, 'Client', None, 'IA-NA')
    srv_msg.client_send_msg(step, 'SOLICIT')

    misc.pass_criteria(step)
    srv_msg.send_wait_for_message(step, 'MUST', None, 'ADVERTISE')
    srv_msg.response_check_include_option(step, 'Response', None, '1')
    srv_msg.response_check_include_option(step, 'Response', None, '2')
    srv_msg.response_check_include_option(step, 'Response', None, '3')
    srv_msg.response_check_option_content(step, 'Response', '3', None, 'sub-option', '5')
    srv_msg.response_check_suboption_content(step,
                                             'Response',
                                             '5',
                                             '3',
                                             None,
                                             'address',
                                             '2001:db8:1::1')
