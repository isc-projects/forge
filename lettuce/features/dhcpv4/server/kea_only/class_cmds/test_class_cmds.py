# Copyright (C) 2018-2019 Internet Systems Consortium, Inc. ("ISC")
#
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.


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
