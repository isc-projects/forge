Feature: Kea Subnet manipulation commands

@v6 @kea_only @controlchannel @hook @subnet_cmds
  Scenario: hook.v6.subnet.cmds.list
  Test Setup:
  Server is configured with 2001:db8:1::/64 subnet with 2001:db8:1::1-2001:db8:1::1 pool.
  Server is configured with another subnet: 1000::/32 with 1000::5-1000::5 pool.
  Server is configured with another subnet: 3000::/100 with 3000::5-3000::5 pool.
  Server has control channel on unix socket with name $(SOFTWARE_INSTALL_DIR)var/kea/control_socket.
  Add hooks library located $(SOFTWARE_INSTALL_DIR)lib/hooks/libdhcp_subnet_cmds.so.
  Send server configuration using SSH and config-file.

  DHCP server is started.

  Using UNIX socket on server in path $(SOFTWARE_INSTALL_DIR)var/kea/control_socket send {"command":"subnet6-list","arguments":{}}

@v6 @kea_only @controlchannel @hook @subnet_cmds
  Scenario: hook.v6.subnet.cmds.get-by-id
  Test Setup:
  Server is configured with 2001:db8:1::/64 subnet with 2001:db8:1::1-2001:db8:1::1 pool.
  Server is configured with another subnet: 1000::/32 with 1000::5-1000::5 pool.
  Server is configured with another subnet: 3000::/100 with 3000::5-3000::5 pool.
  Server has control channel on unix socket with name $(SOFTWARE_INSTALL_DIR)var/kea/control_socket.
  Add hooks library located $(SOFTWARE_INSTALL_DIR)lib/hooks/libdhcp_subnet_cmds.so.
  Send server configuration using SSH and config-file.

  DHCP server is started.

  Using UNIX socket on server in path $(SOFTWARE_INSTALL_DIR)var/kea/control_socket send {"command":"subnet6-get","arguments":{"id":2}}

@v6 @kea_only @controlchannel @hook @subnet_cmds
  Scenario: hook.v6.subnet.cmds.get-by-subnet
  Test Setup:
  Server is configured with 2001:db8:1::/64 subnet with 2001:db8:1::1-2001:db8:1::1 pool.
  Server is configured with another subnet: 1000::/32 with 1000::5-1000::5 pool.
  Server is configured with another subnet: 3000::/100 with 3000::5-3000::5 pool.
  Server has control channel on unix socket with name $(SOFTWARE_INSTALL_DIR)var/kea/control_socket.
  Add hooks library located $(SOFTWARE_INSTALL_DIR)lib/hooks/libdhcp_subnet_cmds.so.
  Send server configuration using SSH and config-file.

  DHCP server is started.

  Using UNIX socket on server in path $(SOFTWARE_INSTALL_DIR)var/kea/control_socket send {"command":"subnet6-get","arguments":{"subnet":"3000::/100"}}


@v6 @kea_only @controlchannel @hook @subnet_cmds
  Scenario: hook.v6.subnet.cmds.add
  Test Setup:
  Server is configured with $(EMPTY) subnet with $(EMPTY) pool.
  Server is configured with preference option with value 123.
  Server is configured with domain-search option with value domain1.example.com,domain2.isc.org.
  Server has control channel on unix socket with name $(SOFTWARE_INSTALL_DIR)var/kea/control_socket.
  Add hooks library located $(SOFTWARE_INSTALL_DIR)lib/hooks/libdhcp_subnet_cmds.so.
  Send server configuration using SSH and config-file.

  DHCP server is started.

  Test Procedure:
  Client sets DUID value to 00:03:00:01:66:55:44:33:22:11.
  Client does include client-id.
  Client does include IA-NA.
  Client sends SOLICIT message.

  Pass Criteria:
  Server MUST respond with ADVERTISE message.
  Response MUST include option 1.
  Response MUST include option 2.
  Response MUST include option 3.
  Response option 3 MUST contain sub-option 13.
  Response sub-option 13 from option 3 MUST contain statuscode 2.

  Using UNIX socket on server in path $(SOFTWARE_INSTALL_DIR)var/kea/control_socket send {"command":"subnet6-list","arguments":{}}
  Using UNIX socket on server in path $(SOFTWARE_INSTALL_DIR)var/kea/control_socket send {"command":"subnet6-add","arguments":{"subnet6":[{"id": 234,"interface":"$(SERVER_IFACE)","subnet": "2001:db8:1::/64","pools":[{"pool":"2001:db8:1::1-2001:db8:1::2"}]}]}}
  Using UNIX socket on server in path $(SOFTWARE_INSTALL_DIR)var/kea/control_socket send {"command":"subnet6-get","arguments":{"id": 234}}

  Test Procedure:
  Client sets DUID value to 00:03:00:01:66:55:44:33:22:11.
  Client does include client-id.
  Client does include IA-NA.
  Client sends SOLICIT message.

  Pass Criteria:
  Server MUST respond with ADVERTISE message.
  Response MUST include option 1.
  Response MUST include option 2.
  Response MUST include option 3.
  Response option 3 MUST contain sub-option 5.
  Response sub-option 5 from option 3 MUST contain address 2001:db8:1::1.

@v6 @kea_only @controlchannel @hook @subnet_cmds
  Scenario: hook.v6.subnet.cmds.add-with-options
  Test Setup:
  Server is configured with $(EMPTY) subnet with $(EMPTY) pool.
  Server is configured with preference option with value 123.
  Server is configured with domain-search option with value domain1.example.com,domain2.isc.org.
  Server has control channel on unix socket with name $(SOFTWARE_INSTALL_DIR)var/kea/control_socket.
  Add hooks library located $(SOFTWARE_INSTALL_DIR)lib/hooks/libdhcp_subnet_cmds.so.
  Send server configuration using SSH and config-file.

  DHCP server is started.

  Test Procedure:
  Client sets DUID value to 00:03:00:01:66:55:44:33:22:11.
  Client does include client-id.
  Client does include IA-NA.
  Client sends SOLICIT message.

  Pass Criteria:
  Server MUST respond with ADVERTISE message.
  Response MUST include option 1.
  Response MUST include option 2.
  Response MUST include option 3.
  Response option 3 MUST contain sub-option 13.
  Response sub-option 13 from option 3 MUST contain statuscode 2.

  Test Procedure:
  Client requests option 7.
  Client requests option 24.
  Client sends INFOREQUEST message.

  Pass Criteria:
  Server MUST respond with REPLY message.
  Response MUST include option 7.
  Response option 7 MUST contain value 123.
  Response MUST include option 24.
  Response option 24 MUST contain domains domain1.example.com,domain2.isc.org.

  Using UNIX socket on server in path $(SOFTWARE_INSTALL_DIR)var/kea/control_socket send {"command":"subnet6-list","arguments":{}}
  Using UNIX socket on server in path $(SOFTWARE_INSTALL_DIR)var/kea/control_socket send {"command": "subnet6-add","arguments":{"subnet6":[{"id": 234,"interface":"$(SERVER_IFACE)","subnet": "2001:db8:1::/64","pools":[{"pool":"2001:db8:1::1-2001:db8:1::2"}],"option-data":[{"csv-format":true,"code":7,"data":"55","name":"preference","space":"dhcp6"}]}]}}
  Using UNIX socket on server in path $(SOFTWARE_INSTALL_DIR)var/kea/control_socket send {"command":"subnet6-get","arguments":{"id": 234}}

  Test Procedure:
  Client sets DUID value to 00:03:00:01:66:55:44:33:22:11.
  Client does include client-id.
  Client does include IA-NA.
  Client requests option 7.
  Client requests option 24.
  Client sends SOLICIT message.

  Pass Criteria:
  Server MUST respond with ADVERTISE message.
  Response MUST include option 1.
  Response MUST include option 2.
  Response MUST include option 3.
  Response option 3 MUST contain sub-option 5.
  Response sub-option 5 from option 3 MUST contain address 2001:db8:1::1.
  Response MUST include option 7.
  Response option 7 MUST contain value 55.
  Response MUST include option 24.
  Response option 24 MUST contain domains domain1.example.com,domain2.isc.org.

@v6 @kea_only @controlchannel @hook @subnet_cmds
  Scenario: hook.v6.subnet.cmds.add-conflict
  Test Setup:
  Server is configured with 2001:db8:1::/64 subnet with 2001:db8:1::1-2001:db8:1::1 pool.
  Server is configured with preference option with value 123.
  Server is configured with domain-search option with value domain1.example.com,domain2.isc.org.
  Server has control channel on unix socket with name $(SOFTWARE_INSTALL_DIR)var/kea/control_socket.
  Add hooks library located $(SOFTWARE_INSTALL_DIR)lib/hooks/libdhcp_subnet_cmds.so.
  Send server configuration using SSH and config-file.

  DHCP server is started.

  Test Procedure:
  Client sets DUID value to 00:03:00:01:66:55:44:33:22:11.
  Client does include client-id.
  Client does include IA-NA.
  Client sends SOLICIT message.

  Pass Criteria:
  Server MUST respond with ADVERTISE message.
  Response MUST include option 1.
  Response MUST include option 2.
  Response MUST include option 3.
  Response option 3 MUST contain sub-option 5.
  Response sub-option 5 from option 3 MUST contain address 2001:db8:1::1.

  Using UNIX socket on server in path $(SOFTWARE_INSTALL_DIR)var/kea/control_socket send {"command":"subnet6-list","arguments":{}}
  Using UNIX socket on server in path $(SOFTWARE_INSTALL_DIR)var/kea/control_socket send {"command": "subnet6-add","arguments":{"subnet6":[{"id": 1,"interface":"$(SERVER_IFACE)","subnet": "2001:db8:1::/64","pools":[{"pool":"2001:db8:1::10-2001:db8:1::20"}]}]}}
  Using UNIX socket on server in path $(SOFTWARE_INSTALL_DIR)var/kea/control_socket send {"command":"subnet6-get","arguments":{}

  Test Procedure:
  Client sets DUID value to 00:03:00:01:66:55:44:33:22:11.
  Client does include client-id.
  Client does include IA-NA.
  Client sends SOLICIT message.

  Pass Criteria:
  Server MUST respond with ADVERTISE message.
  Response MUST include option 1.
  Response MUST include option 2.
  Response MUST include option 3.
  Response option 3 MUST contain sub-option 5.
  Response sub-option 5 from option 3 MUST contain address 2001:db8:1::1.


@v6 @kea_only @controlchannel @hook @subnet_cmds
  Scenario: hook.v6.subnet.cmds.del
  Test Setup:
  Server is configured with 2001:db8:1::/64 subnet with 2001:db8:1::1-2001:db8:1::1 pool.
  Server has control channel on unix socket with name $(SOFTWARE_INSTALL_DIR)var/kea/control_socket.
  Add hooks library located $(SOFTWARE_INSTALL_DIR)lib/hooks/libdhcp_subnet_cmds.so.
  Send server configuration using SSH and config-file.

  DHCP server is started.

  Test Procedure:
  Client sets DUID value to 00:03:00:01:66:55:44:33:22:11.
  Client does include client-id.
  Client does include IA-NA.
  Client sends SOLICIT message.

  Pass Criteria:
  Server MUST respond with ADVERTISE message.
  Response MUST include option 1.
  Response MUST include option 2.
  Response MUST include option 3.
  Response option 3 MUST contain sub-option 5.
  Response sub-option 5 from option 3 MUST contain address 2001:db8:1::1.

  Using UNIX socket on server in path $(SOFTWARE_INSTALL_DIR)var/kea/control_socket send {"command":"subnet6-list","arguments":{}}
  Using UNIX socket on server in path $(SOFTWARE_INSTALL_DIR)var/kea/control_socket send {"command": "subnet6-del","arguments":{"id":1}}
  #Using UNIX socket on server in path $(SOFTWARE_INSTALL_DIR)var/kea/control_socket send {"command": "subnet6-add","arguments":{"subnet6":[{"id": 234,"interface":"$(SERVER_IFACE)","subnet": "2001:db8:1::/64","pools":[{"pool":"2001:db8:1::1-2001:db8:1::2"}]}]}}
  Using UNIX socket on server in path $(SOFTWARE_INSTALL_DIR)var/kea/control_socket send {"command":"subnet6-get","arguments":{}

  Test Procedure:
  Client sets DUID value to 00:03:00:01:66:55:44:33:22:11.
  Client does include client-id.
  Client does include IA-NA.
  Client sends SOLICIT message.

  Pass Criteria:
  Server MUST respond with ADVERTISE message.
  Response MUST include option 1.
  Response MUST include option 2.
  Response MUST include option 3.
  Response option 3 MUST contain sub-option 13.
  Response sub-option 13 from option 3 MUST contain statuscode 2.

@v6 @kea_only @controlchannel @hook @subnet_cmds
  Scenario: hook.v6.subnet.cmds.del-non-existing
  Test Setup:
  Server is configured with 2001:db8:1::/64 subnet with 2001:db8:1::1-2001:db8:1::1 pool.
  Server has control channel on unix socket with name $(SOFTWARE_INSTALL_DIR)var/kea/control_socket.
  Add hooks library located $(SOFTWARE_INSTALL_DIR)lib/hooks/libdhcp_subnet_cmds.so.
  Send server configuration using SSH and config-file.

  DHCP server is started.

  Test Procedure:
  Client sets DUID value to 00:03:00:01:66:55:44:33:22:11.
  Client does include client-id.
  Client does include IA-NA.
  Client sends SOLICIT message.

  Pass Criteria:
  Server MUST respond with ADVERTISE message.
  Response MUST include option 1.
  Response MUST include option 2.
  Response MUST include option 3.
  Response option 3 MUST contain sub-option 5.
  Response sub-option 5 from option 3 MUST contain address 2001:db8:1::1.

  Using UNIX socket on server in path $(SOFTWARE_INSTALL_DIR)var/kea/control_socket send {"command":"subnet6-list","arguments":{}}
  Using UNIX socket on server in path $(SOFTWARE_INSTALL_DIR)var/kea/control_socket send {"command": "subnet6-del","arguments":{"id":2}}
  #Using UNIX socket on server in path $(SOFTWARE_INSTALL_DIR)var/kea/control_socket send {"command": "subnet6-add","arguments":{"subnet6":[{"id": 234,"interface":"$(SERVER_IFACE)","subnet": "2001:db8:1::/64","pools":[{"pool":"2001:db8:1::1-2001:db8:1::2"}]}]}}
  Using UNIX socket on server in path $(SOFTWARE_INSTALL_DIR)var/kea/control_socket send {"command":"subnet6-get","arguments":{}

  Test Procedure:
  Client sets DUID value to 00:03:00:01:66:55:44:33:22:11.
  Client does include client-id.
  Client does include IA-NA.
  Client sends SOLICIT message.

  Pass Criteria:
  Server MUST respond with ADVERTISE message.
  Response MUST include option 1.
  Response MUST include option 2.
  Response MUST include option 3.
  Response option 3 MUST contain sub-option 5.
  Response sub-option 5 from option 3 MUST contain address 2001:db8:1::1.

@v6 @kea_only @controlchannel @hook @subnet_cmds
  Scenario: hook.v6.subnet.cmds.del-global-options
  Test Setup:
  Server is configured with 2001:db8:1::/64 subnet with 2001:db8:1::1-2001:db8:1::1 pool.
  Server is configured with preference option with value 123.
  Server is configured with domain-search option with value domain1.example.com,domain2.isc.org.
  Server has control channel on unix socket with name $(SOFTWARE_INSTALL_DIR)var/kea/control_socket.
  Add hooks library located $(SOFTWARE_INSTALL_DIR)lib/hooks/libdhcp_subnet_cmds.so.
  Send server configuration using SSH and config-file.

  DHCP server is started.

  Test Procedure:
  Client sets DUID value to 00:03:00:01:66:55:44:33:22:11.
  Client does include client-id.
  Client does include IA-NA.
  Client requests option 7.
  Client sends SOLICIT message.

  Pass Criteria:
  Server MUST respond with ADVERTISE message.
  Response MUST include option 1.
  Response MUST include option 2.
  Response MUST include option 3.
  Response option 3 MUST contain sub-option 5.
  Response sub-option 5 from option 3 MUST contain address 2001:db8:1::1.
  Response MUST include option 7.
  Response option 7 MUST contain value 123.

  Using UNIX socket on server in path $(SOFTWARE_INSTALL_DIR)var/kea/control_socket send {"command":"subnet6-list","arguments":{}}
  Using UNIX socket on server in path $(SOFTWARE_INSTALL_DIR)var/kea/control_socket send {"command": "subnet6-del","arguments":{"id":1}}
  #Using UNIX socket on server in path $(SOFTWARE_INSTALL_DIR)var/kea/control_socket send {"command": "subnet6-add","arguments":{"subnet6":[{"id": 234,"interface":"$(SERVER_IFACE)","subnet": "2001:db8:1::/64","pools":[{"pool":"2001:db8:1::1-2001:db8:1::2"}]}]}}
  Using UNIX socket on server in path $(SOFTWARE_INSTALL_DIR)var/kea/control_socket send {"command":"subnet6-get","arguments":{}

  Test Procedure:
  Client sets DUID value to 00:03:00:01:66:55:44:33:22:11.
  Client does include client-id.
  Client does include IA-NA.
  Client sends SOLICIT message.

  Pass Criteria:
  Server MUST respond with ADVERTISE message.
  Response MUST include option 1.
  Response MUST include option 2.
  Response MUST include option 3.
  Response option 3 MUST contain sub-option 13.
  Response sub-option 13 from option 3 MUST contain statuscode 2.

  Test Procedure:
  Client requests option 7.
  Client sends INFOREQUEST message.

  Pass Criteria:
  Server MUST respond with REPLY message.
  Response MUST include option 7.
  Response option 7 MUST contain value 123.

@v6 @kea_only @controlchannel @hook @subnet_cmds
  Scenario: hook.v6.subnet.cmds.add-and-del
  Test Setup:
  Server is configured with $(EMPTY) subnet with $(EMPTY) pool.
  Server is configured with preference option with value 123.
  Server is configured with domain-search option with value domain1.example.com,domain2.isc.org.
  Server has control channel on unix socket with name $(SOFTWARE_INSTALL_DIR)var/kea/control_socket.
  Add hooks library located $(SOFTWARE_INSTALL_DIR)lib/hooks/libdhcp_subnet_cmds.so.
  Send server configuration using SSH and config-file.

  DHCP server is started.

  Test Procedure:
  Client sets DUID value to 00:03:00:01:66:55:44:33:22:11.
  Client does include client-id.
  Client does include IA-NA.
  Client sends SOLICIT message.

  Pass Criteria:
  Server MUST respond with ADVERTISE message.
  Response MUST include option 1.
  Response MUST include option 2.
  Response MUST include option 3.
  Response option 3 MUST contain sub-option 13.
  Response sub-option 13 from option 3 MUST contain statuscode 2.

  Using UNIX socket on server in path $(SOFTWARE_INSTALL_DIR)var/kea/control_socket send {"command":"subnet6-list","arguments":{}}
  Using UNIX socket on server in path $(SOFTWARE_INSTALL_DIR)var/kea/control_socket send {"command": "subnet6-add","arguments":{"subnet6":[{"id": 234,"interface":"$(SERVER_IFACE)","subnet": "2001:db8:1::/64","pools":[{"pool":"2001:db8:1::1-2001:db8:1::2"}]}]}}
  Using UNIX socket on server in path $(SOFTWARE_INSTALL_DIR)var/kea/control_socket send {"command":"subnet6-get","arguments":{"id": 234}}

  Test Procedure:
  Client sets DUID value to 00:03:00:01:66:55:44:33:22:11.
  Client does include client-id.
  Client does include IA-NA.
  Client sends SOLICIT message.

  Pass Criteria:
  Server MUST respond with ADVERTISE message.
  Response MUST include option 1.
  Response MUST include option 2.
  Response MUST include option 3.
  Response option 3 MUST contain sub-option 5.
  Response sub-option 5 from option 3 MUST contain address 2001:db8:1::1.

  Using UNIX socket on server in path $(SOFTWARE_INSTALL_DIR)var/kea/control_socket send {"command": "subnet6-del","arguments":{"id":234}}
  #Using UNIX socket on server in path $(SOFTWARE_INSTALL_DIR)var/kea/control_socket send {"command": "subnet6-add","arguments":{"subnet6":[{"id": 234,"interface":"$(SERVER_IFACE)","subnet": "2001:db8:1::/64","pools":[{"pool":"2001:db8:1::1-2001:db8:1::2"}]}]}}
  Using UNIX socket on server in path $(SOFTWARE_INSTALL_DIR)var/kea/control_socket send {"command":"subnet6-get","arguments":{}

  Test Procedure:
  Client sets DUID value to 00:03:00:01:66:55:44:33:22:11.
  Client does include client-id.
  Client does include IA-NA.
  Client sends SOLICIT message.

  Pass Criteria:
  Server MUST respond with ADVERTISE message.
  Response MUST include option 1.
  Response MUST include option 2.
  Response MUST include option 3.
  Response option 3 MUST contain sub-option 13.
  Response sub-option 13 from option 3 MUST contain statuscode 2.