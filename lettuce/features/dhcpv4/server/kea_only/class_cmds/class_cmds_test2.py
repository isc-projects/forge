# Feature: Kea Class manipulation commands
#
# @v4 @kea_only @controlchannel @hook @subnet_cmds
#   Scenario: hook.v4.class.cmds.list-commands
#   Test Setup:
#   Server is configured with 192.168.50.0/24 subnet with 192.168.50.5-192.168.50.5 pool.
#   Server has control channel on unix socket with name $(SOFTWARE_INSTALL_DIR)/var/kea/control_socket.
#   Add hooks library located $(SOFTWARE_INSTALL_DIR)/lib/hooks/libdhcp_class_cmds.so.
#   Send server configuration using SSH and config-file.
#
#   DHCP server is started.
#
#   Test Procedure:
#   Using UNIX socket on server in path $(SOFTWARE_INSTALL_DIR)/var/kea/control_socket send {"command":"list-commands","arguments":{}}
#
#   Pass Criteria:
#   Command response arguments contain class-add, class-del, class-get, class-list, class-update.

# def test_class_cmds_availability():
#     cmd = dict(command='list-commands')
#     response = send_request(cmd)
#     for cmd in ['class-list', 'class-add', 'class-update', 'class-get', 'class-del']:
#         assert cmd in response['arguments']


import sys
if 'features' not in sys.path:
    sys.path.append('features')

import misc
import srv_control
import srv_msg

FEATURE = "Kea Class manipulation commands"


def test_hook_v4_class_cmds_list_commands(step):
    """new-hook.v4.class.cmds.list-commands"""
    misc.set_world()
    srv_control.config_srv_subnet(step, '192.168.50.0/24', '192.168.50.5-192.168.50.5')
    srv_control.open_control_channel(step, 'unix', '$(SOFTWARE_INSTALL_DIR)/var/kea/control_socket')
    srv_control.add_hooks(step, '$(SOFTWARE_INSTALL_DIR)/lib/hooks/libdhcp_class_cmds.so')
    srv_control.build_and_send_config_files(step, 'SSH', 'config-file')

    srv_control.start_srv(step, 'DHCP', 'started')

    misc.test_procedure(step)
    srv_msg.send_through_socket_server_site(step, '$(SOFTWARE_INSTALL_DIR)/var/kea/control_socket', '{"command":"list-commands","arguments":{}}')

    srv_msg.cmd_resp_field_contains(step, 'arguments', 'class-add, class-del, class-get, class-list, class-update')
