Feature: Kea Subnet manipulation commands

@v4 @kea_only @controlchannel @hook @subnet_cmds
  Scenario: hook.v4.subnet.cmds.list
  Test Setup:
  Server is configured with 192.168.50.0/24 subnet with 192.168.50.5-192.168.50.5 pool.
  Server is configured with another subnet: 10.0.0.0/24 with 10.0.0.5-10.0.0.5 pool.
  Server has control channel on unix socket with name $(SOFTWARE_INSTALL_DIR)var/kea/control_socket.
  Add hooks library located $(SOFTWARE_INSTALL_DIR)lib/hooks/libdhcp_subnet_cmds.so.
  Send server configuration using SSH and config-file.

  DHCP server is started.

  Using UNIX socket on server in path $(SOFTWARE_INSTALL_DIR)var/kea/control_socket send {"command":"subnet4-list","arguments":{}}

@v4 @kea_only @controlchannel @hook @subnet_cmds
  Scenario: hook.v4.subnet.cmds.get-by-id
  Test Setup:
  Server is configured with 192.168.50.0/24 subnet with 192.168.50.5-192.168.50.5 pool.
  Server is configured with another subnet: 10.0.0.0/24 with 10.0.0.5-10.0.0.5 pool.
  Server is configured with another subnet: 150.0.0.0/24 with 150.0.0.5-150.0.0.5 pool.
  Server is configured with streettalk-directory-assistance-server option in subnet 2 with value 199.1.1.1,200.1.1.2.
  Server has control channel on unix socket with name $(SOFTWARE_INSTALL_DIR)var/kea/control_socket.
  Add hooks library located $(SOFTWARE_INSTALL_DIR)lib/hooks/libdhcp_subnet_cmds.so.
  Send server configuration using SSH and config-file.

  DHCP server is started.

  Using UNIX socket on server in path $(SOFTWARE_INSTALL_DIR)var/kea/control_socket send {"command":"subnet4-get","arguments":{"id":3}}

@v4 @kea_only @controlchannel @hook @subnet_cmds
  Scenario: hook.v4.subnet.cmds.get-by-subnet
  Test Setup:
  Server is configured with 192.168.50.0/24 subnet with 192.168.50.5-192.168.50.5 pool.
  Server is configured with another subnet: 10.0.0.0/24 with 10.0.0.5-10.0.0.5 pool.
  Server is configured with domain-name-servers option in subnet 1 with value 199.199.199.1,100.100.100.1.
  Server has control channel on unix socket with name $(SOFTWARE_INSTALL_DIR)var/kea/control_socket.
  Add hooks library located $(SOFTWARE_INSTALL_DIR)lib/hooks/libdhcp_subnet_cmds.so.
  Send server configuration using SSH and config-file.

  DHCP server is started.

  Using UNIX socket on server in path $(SOFTWARE_INSTALL_DIR)var/kea/control_socket send {"command":"subnet4-get","arguments":{"subnet":"10.0.0.0/24"}}

@v4 @kea_only @controlchannel @hook @subnet_cmds
  Scenario: hook.v4.subnet.cmds.add
  Test Setup:
  Server is configured with $(EMPTY) subnet with $(EMPTY) pool.
  Server is configured with domain-name-servers option with value 199.199.199.1,100.100.100.1.
  Server has control channel on unix socket with name $(SOFTWARE_INSTALL_DIR)var/kea/control_socket.
  Add hooks library located $(SOFTWARE_INSTALL_DIR)lib/hooks/libdhcp_subnet_cmds.so.
  Send server configuration using SSH and config-file.

  DHCP server is started.

  Test Procedure:
  Client requests option 1.
  Client sets chaddr value to ff:01:02:03:ff:04.
  Client sends DISCOVER message.

  Pass Criteria:
  Server MUST NOT respond.

#  Using UNIX socket on server in path $(SOFTWARE_INSTALL_DIR)var/kea/control_socket send {"command":"subnet4-list","arguments":{}}
  Using UNIX socket on server in path $(SOFTWARE_INSTALL_DIR)var/kea/control_socket send {"command":"subnet4-add","arguments":{"subnet4":[{"subnet":"192.168.50.0/24","interface":"eth2","id":234,"pools":[{"pool":"192.168.50.1-192.168.50.1"}]}]}}
  Using UNIX socket on server in path $(SOFTWARE_INSTALL_DIR)var/kea/control_socket send {"command":"subnet4-get","arguments":{"id": 234}}

  Test Procedure:
  Client requests option 1.
  Client sends DISCOVER message.

  Pass Criteria:
  Server MUST respond with OFFER message.
  Response MUST include option 1.
  Response MUST contain yiaddr 192.168.50.1.
  Response option 1 MUST contain value 255.255.255.0.

@v4 @kea_only @controlchannel @hook @subnet_cmds
  Scenario: hook.v4.subnet.cmds.add-with-options
  Test Setup:
  Server is configured with 192.168.50.0/24 subnet with $(EMPTY) pool.
  Server is configured with domain-name-servers option with value 199.199.199.1,100.100.100.1.
  Server has control channel on unix socket with name $(SOFTWARE_INSTALL_DIR)var/kea/control_socket.
  Add hooks library located $(SOFTWARE_INSTALL_DIR)lib/hooks/libdhcp_subnet_cmds.so.
  Send server configuration using SSH and config-file.

  DHCP server is started.

  Test Procedure:
  Client requests option 6.
  Client sets ciaddr value to $(CIADDR).
  Client sends INFORM message.

  Pass Criteria:
  Server MUST respond with ACK message.
  Response MUST include option 6.
  Response option 6 MUST contain value 199.199.199.1.
  Response option 6 MUST contain value 100.100.100.1.

  Test Procedure:
  Client requests option 1.
  Client sets chaddr value to ff:01:02:03:ff:04.
  Client sends DISCOVER message.

  Pass Criteria:
  Server MUST NOT respond.

#  Using UNIX socket on server in path $(SOFTWARE_INSTALL_DIR)var/kea/control_socket send {"command":"subnet4-list","arguments":{}}
  Using UNIX socket on server in path $(SOFTWARE_INSTALL_DIR)var/kea/control_socket send {"command": "subnet4-add","arguments": {"subnet4": [{"subnet": "192.168.51.0/24","interface": "eth2","id": 234,"pools": [{"pool": "192.168.51.1-192.168.51.1"}],"option-data": [{"csv-format": true,"code": 6,"data": "19.19.19.1,10.10.10.1","name": "domain-name-servers","space": "dhcp4"}]}]}}
  Using UNIX socket on server in path $(SOFTWARE_INSTALL_DIR)var/kea/control_socket send {"command":"subnet4-get","arguments":{"id": 234}}
  Using UNIX socket on server in path $(SOFTWARE_INSTALL_DIR)var/kea/control_socket send {"command": "subnet4-del","arguments":{"id":1}}

  Test Procedure:
  Client requests option 1.
  Client requests option 6.
  Client sets chaddr value to ff:01:02:03:ff:04.
  Client sends DISCOVER message.

  Pass Criteria:
  Server MUST respond with OFFER message.
  Response MUST include option 1.
  Response MUST contain yiaddr 192.168.51.1.
  Response option 1 MUST contain value 255.255.255.0.
  Response MUST include option 6.
  Response option 6 MUST contain value 19.19.19.1.
  Response option 6 MUST contain value 10.10.10.1.

@v4 @kea_only @controlchannel @hook @subnet_cmds
  Scenario: hook.v4.subnet.cmds.add-conflict
  Test Setup:
  Server is configured with 192.168.51.0/24 subnet with 192.168.51.1-192.168.51.1 pool.
  Server is configured with domain-name-servers option with value 199.199.199.1,100.100.100.1.
  Server has control channel on unix socket with name $(SOFTWARE_INSTALL_DIR)var/kea/control_socket.
  Add hooks library located $(SOFTWARE_INSTALL_DIR)lib/hooks/libdhcp_subnet_cmds.so.
  Send server configuration using SSH and config-file.

  DHCP server is started.

  Test Procedure:
  Client requests option 1.
  Client requests option 6.
  Client sets chaddr value to ff:01:02:03:ff:04.
  Client sends DISCOVER message.

  Pass Criteria:
  Server MUST respond with OFFER message.
  Response MUST include option 1.
  Response MUST contain yiaddr 192.168.51.1.
  Response option 1 MUST contain value 255.255.255.0.

#  Using UNIX socket on server in path $(SOFTWARE_INSTALL_DIR)var/kea/control_socket send {"command":"subnet4-list","arguments":{}}
  Using UNIX socket on server in path $(SOFTWARE_INSTALL_DIR)var/kea/control_socket send {"command": "subnet4-add","arguments": {"subnet4": [{"subnet": "192.168.55.0/24","interface": "eth2","id": 1,"pools": [{"pool": "192.168.55.1-192.168.55.1"}],"option-data": [{"csv-format": true,"code": 6,"data": "19.19.19.1,10.10.10.1","name": "domain-name-servers","space": "dhcp4"}]}]}}
  Using UNIX socket on server in path $(SOFTWARE_INSTALL_DIR)var/kea/control_socket send {"command":"subnet4-get","arguments":{"id": 1}}

  Test Procedure:
  Client requests option 1.
  Client requests option 6.
  Client sets chaddr value to ff:01:02:03:ff:04.
  Client sends DISCOVER message.

  Pass Criteria:
  Server MUST respond with OFFER message.
  Response MUST include option 1.
  Response MUST contain yiaddr 192.168.51.1.
  Response option 1 MUST contain value 255.255.255.0.

@v4 @kea_only @controlchannel @hook @subnet_cmds
  Scenario: hook.v4.subnet.cmds.del
  Test Setup:
  Server is configured with 192.168.51.0/24 subnet with 192.168.51.1-192.168.51.1 pool.
  Server is configured with domain-name-servers option with value 199.199.199.1,100.100.100.1.
  Server has control channel on unix socket with name $(SOFTWARE_INSTALL_DIR)var/kea/control_socket.
  Add hooks library located $(SOFTWARE_INSTALL_DIR)lib/hooks/libdhcp_subnet_cmds.so.
  Send server configuration using SSH and config-file.

  DHCP server is started.

  Test Procedure:
  Client requests option 1.
  Client requests option 6.
  Client sets chaddr value to ff:01:02:03:ff:04.
  Client sends DISCOVER message.

  Pass Criteria:
  Server MUST respond with OFFER message.
  Response MUST include option 1.
  Response MUST contain yiaddr 192.168.51.1.
  Response option 1 MUST contain value 255.255.255.0.

  Using UNIX socket on server in path $(SOFTWARE_INSTALL_DIR)var/kea/control_socket send {"command": "subnet4-del","arguments":{"id":1}}

  Test Procedure:
  Client requests option 1.
  Client sets chaddr value to ff:01:02:03:ff:04.
  Client sends DISCOVER message.

  Pass Criteria:
  Server MUST NOT respond.

@v4 @kea_only @controlchannel @hook @subnet_cmds
  Scenario: hook.v4.subnet.cmds.del-non-existing
  Test Setup:
  Server is configured with 192.168.51.0/24 subnet with 192.168.51.1-192.168.51.1 pool.
  Server is configured with domain-name-servers option with value 199.199.199.1,100.100.100.1.
  Server has control channel on unix socket with name $(SOFTWARE_INSTALL_DIR)var/kea/control_socket.
  Add hooks library located $(SOFTWARE_INSTALL_DIR)lib/hooks/libdhcp_subnet_cmds.so.
  Send server configuration using SSH and config-file.

  DHCP server is started.

  Test Procedure:
  Client requests option 1.
  Client requests option 6.
  Client sets chaddr value to ff:01:02:03:ff:04.
  Client sends DISCOVER message.

  Pass Criteria:
  Server MUST respond with OFFER message.
  Response MUST include option 1.
  Response MUST contain yiaddr 192.168.51.1.
  Response option 1 MUST contain value 255.255.255.0.

  Using UNIX socket on server in path $(SOFTWARE_INSTALL_DIR)var/kea/control_socket send {"command": "subnet4-del","arguments":{"id":2}}

  Test Procedure:
  Client requests option 1.
  Client requests option 6.
  Client sets chaddr value to ff:01:02:03:ff:04.
  Client sends DISCOVER message.

  Pass Criteria:
  Server MUST respond with OFFER message.
  Response MUST include option 1.
  Response MUST contain yiaddr 192.168.51.1.
  Response option 1 MUST contain value 255.255.255.0.

@v4 @kea_only @controlchannel @hook @subnet_cmds
  Scenario: hook.v4.subnet.cmds.del-global-options
  Test Setup:
  Server is configured with 192.168.51.0/24 subnet with 192.168.51.1-192.168.51.1 pool.
  Server is configured with domain-name-servers option with value 199.199.199.1,100.100.100.1.
  Server has control channel on unix socket with name $(SOFTWARE_INSTALL_DIR)var/kea/control_socket.
  Add hooks library located $(SOFTWARE_INSTALL_DIR)lib/hooks/libdhcp_subnet_cmds.so.
  Send server configuration using SSH and config-file.

  DHCP server is started.

  Test Procedure:
  Client requests option 1.
  Client requests option 6.
  Client sets chaddr value to ff:01:02:03:ff:04.
  Client sends DISCOVER message.

  Pass Criteria:
  Server MUST respond with OFFER message.
  Response MUST include option 1.
  Response MUST contain yiaddr 192.168.51.1.
  Response option 1 MUST contain value 255.255.255.0.

  Using UNIX socket on server in path $(SOFTWARE_INSTALL_DIR)var/kea/control_socket send {"command": "subnet4-del","arguments":{"id":1}}

  Test Procedure:
  Client requests option 1.
  Client sets chaddr value to ff:01:02:03:ff:04.
  Client sends DISCOVER message.

  Pass Criteria:
  Server MUST NOT respond.

# That needs subnet with empty pool to work
#  Test Procedure:
#  Client requests option 6.
#  Client sets ciaddr value to $(CIADDR).
#  Client sends INFORM message.
#
#  Pass Criteria:
#  Server MUST respond with ACK message.
#  Response MUST include option 6.
#  Response option 6 MUST contain value 199.199.199.1.
#  Response option 6 MUST contain value 100.100.100.1.

@v4 @kea_only @controlchannel @hook @subnet_cmds
  Scenario: hook.v4.subnet.cmds.add-and-del
  Test Setup:
  Server is configured with $(EMPTY) subnet with $(EMPTY) pool.
  Server is configured with domain-name-servers option with value 199.199.199.1,100.100.100.1.
  Server has control channel on unix socket with name $(SOFTWARE_INSTALL_DIR)var/kea/control_socket.
  Add hooks library located $(SOFTWARE_INSTALL_DIR)lib/hooks/libdhcp_subnet_cmds.so.
  Send server configuration using SSH and config-file.

  DHCP server is started.

  Test Procedure:
  Client requests option 1.
  Client sets chaddr value to ff:01:02:03:ff:04.
  Client sends DISCOVER message.

  Pass Criteria:
  Server MUST NOT respond.

  Using UNIX socket on server in path $(SOFTWARE_INSTALL_DIR)var/kea/control_socket send {"command":"subnet4-add","arguments":{"subnet4":[{"subnet":"192.168.50.0/24","interface":"eth2","id":66,"pools":[{"pool":"192.168.50.1-192.168.50.1"}]}]}}

  Test Procedure:
  Client requests option 1.
  Client requests option 6.
  Client sets chaddr value to ff:01:02:03:ff:04.
  Client sends DISCOVER message.

  Pass Criteria:
  Server MUST respond with OFFER message.
  Response MUST include option 1.
  Response MUST contain yiaddr 192.168.50.1.
  Response option 1 MUST contain value 255.255.255.0.

  Using UNIX socket on server in path $(SOFTWARE_INSTALL_DIR)var/kea/control_socket send {"command": "subnet4-del","arguments":{"id":66}}

  Test Procedure:
  Client requests option 1.
  Client sets chaddr value to ff:01:02:03:ff:04.
  Client sends DISCOVER message.

  Pass Criteria:
  Server MUST NOT respond.