Feature: Kea Class manipulation commands

@v4 @kea_only @controlchannel @hook @subnet_cmds
  Scenario: hook.v4.class.cmds.list-commands
  Test Setup:
  Server is configured with 192.168.50.0/24 subnet with 192.168.50.5-192.168.50.5 pool.
  Server has control channel on unix socket with name $(SOFTWARE_INSTALL_DIR)/var/kea/control_socket.
  Add hooks library located $(SOFTWARE_INSTALL_DIR)/lib/hooks/libdhcp_class_cmds.so.
  Send server configuration using SSH and config-file.

  DHCP server is started.

  Test Procedure:
  Using UNIX socket on server in path $(SOFTWARE_INSTALL_DIR)/var/kea/control_socket send {"command":"list-commands","arguments":{}}

  Pass Criteria:
  Command response arguments contain class-add, class-del, class-get, class-list, class-update.


@v4 @kea_only @controlchannel @hook @subnet_cmds
  Scenario: hook.v4.class.cmds.basic
  Test Setup:
  Server is configured with 192.168.50.0/24 subnet with 192.168.50.5-192.168.50.5 pool.
  Server has control channel on unix socket with name $(SOFTWARE_INSTALL_DIR)/var/kea/control_socket.
  Add hooks library located $(SOFTWARE_INSTALL_DIR)/lib/hooks/libdhcp_class_cmds.so.
  Send server configuration using SSH and config-file.

  DHCP server is started.

  # there is no classes at the beginning
  Test Procedure:
  Using UNIX socket on server in path $(SOFTWARE_INSTALL_DIR)/var/kea/control_socket send {"command":"class-list"}

  Pass Criteria:
  Command response result equals 3.
  Command response text contain 0 classes found.

  # add new class ipxe
  Test Procedure:
  Using UNIX socket on server in path $(SOFTWARE_INSTALL_DIR)/var/kea/control_socket send {"command":"class-add","arguments":{"client-classes":[{"boot-file-name":"/dev/null","name":"ipxe_efi_x64","next-server":"192.0.2.254","option-data":[],"option-def":[],"server-hostname":"hal9000","test":"option[93].hex == 0x0009"}]}}

  Pass Criteria:
  Command response equals {"text": "Class 'ipxe_efi_x64' added", "result": 0}.

  # check what classes are available now
  Test Procedure:
  Using UNIX socket on server in path $(SOFTWARE_INSTALL_DIR)/var/kea/control_socket send {"command":"class-list"}

  Pass Criteria:
  Command response equals {"text": "1 class found", "arguments": {"client-classes": [{"name": "ipxe_efi_x64"}]}, "result": 0}.

  # let's see if it works in real, so send DHCPOFFER and check DHCPOFFER
#   Test Procedure:
#   Client sets chaddr value to ff:01:02:03:ff:04.
#   Client adds to the message client_id with value ff:01:11:11:11:11:11:22.
#   Client sends DISCOVER message.

#   Pass Criteria:
# #  Server MUST NOT respond.
#   Server MUST respond with OFFER message.
#   Response MUST contain yiaddr 192.168.50.5.
#   Response MUST NOT contain siaddr 192.0.2.254.
#   Response MUST NOT contain file /dev/null.
#   Response MUST NOT contain sname hal9000.

  Test Procedure:
  Client sets chaddr value to ff:01:02:03:ff:04.
  Client adds to the message client_id with value ff:01:02:03:ff:04:11:22.
  Client adds to the message pxe_client_architecture with value 9.
  Client adds to the message pxe_client_network_interface with value 320.
  Client adds to the message pxe_client_machine_identifier with value 123456789a.
  Client sends DISCOVER message.

  Pass Criteria:
  Server MUST respond with OFFER message.
  Response MUST contain yiaddr 192.168.50.5.
  Response MUST contain siaddr 192.0.2.254.
  Response MUST contain file /dev/null.
  Response MUST contain sname hal9000.
