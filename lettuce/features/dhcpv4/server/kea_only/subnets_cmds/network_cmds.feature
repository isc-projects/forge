Feature: Kea Subnet manipulation commands

@v4 @kea_only @controlchannel @hook @network_cmds
  Scenario: hook.v4.network.cmds.list
  Test Setup:
  Server is configured with 192.168.50.0/24 subnet with 192.168.50.1-192.168.50.1 pool.
  Server is configured with another subnet: 192.168.51.0/24 with 192.168.51.1-192.168.51.1 pool.
  Server is configured with another subnet: 192.168.52.0/24 with 192.168.52.1-192.168.52.1 pool.
  Server is configured with another subnet: 192.168.53.0/24 with 192.168.53.1-192.168.53.1 pool.
  #first shared subnet
  Add subnet 0 to shared-subnet set 0.
  Add subnet 1 to shared-subnet set 0.
  Add configuration parameter name with value "name-abc" to shared-subnet 0 configuration.
  Add configuration parameter interface with value "$(SERVER_IFACE)" to shared-subnet 0 configuration.
  #second shared-subnet
  Add subnet 2 to shared-subnet set 1.
  Add subnet 3 to shared-subnet set 1.
  Add configuration parameter name with value "name-xyz" to shared-subnet 1 configuration.
  Add configuration parameter relay with value {"ip-address":"$(GIADDR4)"} to shared-subnet 1 configuration.

  Server is configured with time-servers option in subnet 0 with value 199.199.199.10.
  Server is configured with time-servers option in subnet 2 with value 199.199.199.100.
  Server is configured with time-servers option in subnet 3 with value 199.199.199.200.
  Add hooks library located $(SOFTWARE_INSTALL_DIR)/lib/kea/hooks/libdhcp_subnet_cmds.so.

  Server has control channel on unix socket with name $(SOFTWARE_INSTALL_DIR)/var/kea/control_socket.
  Send server configuration using SSH and config-file.

  DHCP server is started.

  Using UNIX socket on server in path $(SOFTWARE_INSTALL_DIR)/var/kea/control_socket send {"command":"network4-list","arguments":{}}

@v4 @kea_only @controlchannel @hook @network_cmds
  Scenario: hook.v4.network.cmds.get-by-name
  Test Setup:
  Server is configured with 192.168.50.0/24 subnet with 192.168.50.1-192.168.50.1 pool.
  Server is configured with another subnet: 192.168.51.0/24 with 192.168.51.1-192.168.51.1 pool.
  Server is configured with another subnet: 192.168.52.0/24 with 192.168.52.1-192.168.52.1 pool.
  Server is configured with another subnet: 192.168.53.0/24 with 192.168.53.1-192.168.53.1 pool.
  #first shared subnet
  Add subnet 0 to shared-subnet set 0.
  Add subnet 1 to shared-subnet set 0.
  Add configuration parameter name with value "name-abc" to shared-subnet 0 configuration.
  Add configuration parameter interface with value "$(SERVER_IFACE)" to shared-subnet 0 configuration.
  #second shared-subnet
  Add subnet 2 to shared-subnet set 1.
  Add subnet 3 to shared-subnet set 1.
  Add configuration parameter name with value "name-xyz" to shared-subnet 1 configuration.
  Add configuration parameter relay with value {"ip-address":"$(GIADDR4)"} to shared-subnet 1 configuration.

  Server is configured with time-servers option in subnet 0 with value 199.199.199.10.
  Server is configured with time-servers option in subnet 2 with value 199.199.199.100.
  Server is configured with time-servers option in subnet 3 with value 199.199.199.200.
  Add hooks library located $(SOFTWARE_INSTALL_DIR)/lib/kea/hooks/libdhcp_subnet_cmds.so.

  Server has control channel on unix socket with name $(SOFTWARE_INSTALL_DIR)/var/kea/control_socket.
  Send server configuration using SSH and config-file.
  DHCP server is started.

  Using UNIX socket on server in path $(SOFTWARE_INSTALL_DIR)/var/kea/control_socket send {"command":"network4-get","arguments":{"name":"name-xyz"}}

@v4 @kea_only @controlchannel @hook @network_cmds
  Scenario: hook.v4.network.cmds.add
  Test Setup:
  Server is configured with $(EMPTY) subnet with $(EMPTY) pool.
  Server is configured with domain-name-servers option with value 199.199.199.1,100.100.100.1.
  Server has control channel on unix socket with name $(SOFTWARE_INSTALL_DIR)/var/kea/control_socket.
  Add hooks library located $(SOFTWARE_INSTALL_DIR)/lib/kea/hooks/libdhcp_subnet_cmds.so.
  Send server configuration using SSH and config-file.

  DHCP server is started.

  Test Procedure:
  Client requests option 1.
  Client sets chaddr value to ff:01:02:03:ff:04.
  Client sends DISCOVER message.

  Pass Criteria:
  Server MUST NOT respond.

  Using UNIX socket on server in path $(SOFTWARE_INSTALL_DIR)/var/kea/control_socket send {"command":"network4-list","arguments":{}}
  Using UNIX socket on server in path $(SOFTWARE_INSTALL_DIR)/var/kea/control_socket send {"command":"network4-add","arguments":{"shared-networks": [{"name": "name-xyz","rebind-timer": 100,"renew-timer": 100,"valid-lifetime": 400,"subnet4": [{"interface": "$(SERVER_IFACE)", "pools": [{"pool": "192.168.50.1/32"}],"rebind-timer": 2000,"renew-timer": 1000,"subnet": "192.168.50.0/24","valid-lifetime": 4000}]}]}}
  Using UNIX socket on server in path $(SOFTWARE_INSTALL_DIR)/var/kea/control_socket send {"command":"network4-get","arguments":{"name": "name-xyz"}}

  Sleep for 3 seconds.

  Test Procedure:
  Client requests option 1.
  Client requests option 6.
  Client sets chaddr value to ff:01:02:03:ff:04.
  Client sends DISCOVER message.

  Pass Criteria:
  Server MUST respond with OFFER message.

@v4 @kea_only @controlchannel @hook @network_cmds
  Scenario: hook.v4.network.cmds.add-conflict
  Test Setup:
  Server is configured with 192.168.50.0/24 subnet with 192.168.50.1-192.168.50.1 pool.
  Server is configured with another subnet: 192.168.51.0/24 with 192.168.51.1-192.168.51.1 pool.
  Server is configured with another subnet: 192.168.52.0/24 with 192.168.52.1-192.168.52.1 pool.
  Server is configured with another subnet: 192.168.53.0/24 with 192.168.53.1-192.168.53.1 pool.
  #first shared subnet
  Add subnet 0 to shared-subnet set 0.
  Add subnet 1 to shared-subnet set 0.
  Add configuration parameter name with value "name-abc" to shared-subnet 0 configuration.
  Add configuration parameter interface with value "$(SERVER_IFACE)" to shared-subnet 0 configuration.
  #second shared-subnet
  Add subnet 2 to shared-subnet set 1.
  Add subnet 3 to shared-subnet set 1.
  Add configuration parameter name with value "name-xyz" to shared-subnet 1 configuration.
  Add configuration parameter relay with value {"ip-address":"$(GIADDR4)"} to shared-subnet 1 configuration.

  Server is configured with time-servers option in subnet 0 with value 199.199.199.10.
  Server is configured with time-servers option in subnet 2 with value 199.199.199.100.
  Server is configured with time-servers option in subnet 3 with value 199.199.199.200.
  Add hooks library located $(SOFTWARE_INSTALL_DIR)/lib/kea/hooks/libdhcp_subnet_cmds.so.

  Server has control channel on unix socket with name $(SOFTWARE_INSTALL_DIR)/var/kea/control_socket.
  Send server configuration using SSH and config-file.

  DHCP server is started.

  Using UNIX socket on server in path $(SOFTWARE_INSTALL_DIR)/var/kea/control_socket send {"command":"network4-list","arguments":{}}
  Using UNIX socket on server in path $(SOFTWARE_INSTALL_DIR)/var/kea/control_socket send {"command":"network4-add","arguments":{"shared-networks": [{"match-client-id": true,"name": "name-xyz","option-data": [],"rebind-timer": 0,"relay": {"ip-address": "0.0.0.0"},"renew-timer": 0,"reservation-mode": "all","subnet4": [{"4o6-interface": "","4o6-interface-id": "","4o6-subnet": "","boot-file-name": "","id": 3,"match-client-id": true,"next-server": "0.0.0.0","option-data": [{"always-send": false,"code": 4,"csv-format": false,"data": "C7C7C764","name": "time-servers","space": "dhcp4"}],"pools": [{"option-data": [],"pool": "192.168.52.1/32"}],"rebind-timer": 2000,"relay": {"ip-address": "192.168.50.249"},"renew-timer": 1000,"reservation-mode": "all","server-hostname": "","subnet": "192.168.52.0/24","valid-lifetime": 4000},{"4o6-interface": "","4o6-interface-id": "","4o6-subnet": "","boot-file-name": "","id": 4,"match-client-id": true,"next-server": "0.0.0.0","option-data": [{"always-send": false,"code": 4,"csv-format": false,"data": "C7C7C7C8","name": "time-servers","space": "dhcp4"}],"pools": [{"option-data": [],"pool": "192.168.53.1/32"}],"rebind-timer": 2000,"relay": {"ip-address": "192.168.50.249"},"renew-timer": 1000,"reservation-mode": "all","server-hostname": "","subnet": "192.168.53.0/24","valid-lifetime": 4000}],"valid-lifetime": 0}]}}
  Using UNIX socket on server in path $(SOFTWARE_INSTALL_DIR)/var/kea/control_socket send {"command":"network4-get","arguments":{"name": "name-xyz"}}


@v4 @kea_only @controlchannel @hook @network_cmds
  Scenario: hook.v4.network.cmds.del
  Test Setup:
  Server is configured with 192.168.50.0/24 subnet with 192.168.50.1-192.168.50.1 pool.
  Server is configured with another subnet: 192.168.51.0/24 with 192.168.51.1-192.168.51.1 pool.
  Add subnet 0 to shared-subnet set 0.
  Add subnet 1 to shared-subnet set 0.
  Add configuration parameter name with value "name-abc" to shared-subnet 0 configuration.
  Add configuration parameter interface with value "$(SERVER_IFACE)" to shared-subnet 0 configuration.

  Server is configured with time-servers option in subnet 0 with value 199.199.199.10.
  Add hooks library located $(SOFTWARE_INSTALL_DIR)/lib/kea/hooks/libdhcp_subnet_cmds.so.

  Server has control channel on unix socket with name $(SOFTWARE_INSTALL_DIR)/var/kea/control_socket.
  Send server configuration using SSH and config-file.

  DHCP server is started.

  Test Procedure:
  Client requests option 1.
  Client requests option 6.
  Client sets chaddr value to ff:01:02:03:ff:04.
  Client sends DISCOVER message.

  Pass Criteria:
  Server MUST respond with OFFER message.

  Using UNIX socket on server in path $(SOFTWARE_INSTALL_DIR)/var/kea/control_socket send {"command":"network4-list","arguments":{}}
  Using UNIX socket on server in path $(SOFTWARE_INSTALL_DIR)/var/kea/control_socket send {"command":"network4-del","arguments":{"name":"name-abc","subnets-action": "delete"}}

  Test Procedure:
  Client requests option 1.
  Client sets chaddr value to ff:01:02:03:ff:04.
  Client sends DISCOVER message.

  Pass Criteria:
  Server MUST NOT respond.

@v4 @kea_only @controlchannel @hook @network_cmds
  Scenario: hook.v4.network.cmds.del-keep-subnet
  Test Setup:
  Server is configured with 192.168.50.0/24 subnet with 192.168.50.1-192.168.50.1 pool.
  Server is configured with another subnet: 192.168.51.0/24 with 192.168.51.1-192.168.51.1 pool.
  Add subnet 0 to shared-subnet set 0.
  Add subnet 1 to shared-subnet set 0.
  Add configuration parameter name with value "name-abc" to shared-subnet 0 configuration.
  Add configuration parameter interface with value "$(SERVER_IFACE)" to shared-subnet 0 configuration.

  Server is configured with time-servers option in subnet 0 with value 199.199.199.10.
  Add hooks library located $(SOFTWARE_INSTALL_DIR)/lib/kea/hooks/libdhcp_subnet_cmds.so.

  Server has control channel on unix socket with name $(SOFTWARE_INSTALL_DIR)/var/kea/control_socket.
  Send server configuration using SSH and config-file.

  DHCP server is started.

  Test Procedure:
  Client requests option 1.
  Client requests option 6.
  Client sets chaddr value to ff:01:02:03:ff:04.
  Client sends DISCOVER message.

  Pass Criteria:
  Server MUST respond with OFFER message.

  Using UNIX socket on server in path $(SOFTWARE_INSTALL_DIR)/var/kea/control_socket send {"command":"network4-list","arguments":{}}
  Using UNIX socket on server in path $(SOFTWARE_INSTALL_DIR)/var/kea/control_socket send {"command":"network4-del","arguments":{"name":"name-abc","subnets-action": "keep"}}

  Test Procedure:
  Client requests option 1.
  Client requests option 6.
  Client sets chaddr value to ff:01:02:03:ff:04.
  Client sends DISCOVER message.

  Pass Criteria:
  Server MUST respond with OFFER message.

  Using UNIX socket on server in path $(SOFTWARE_INSTALL_DIR)/var/kea/control_socket send {"command":"network4-list","arguments":{}}

@v4 @kea_only @controlchannel @hook @network_cmds
  Scenario: hook.v4.network.cmds.del-non-existing
  Test Setup:
  Server is configured with 192.168.50.0/24 subnet with 192.168.50.1-192.168.50.1 pool.
  Server is configured with another subnet: 192.168.51.0/24 with 192.168.51.1-192.168.51.1 pool.
  Server is configured with another subnet: 192.168.52.0/24 with 192.168.52.1-192.168.52.1 pool.
  Server is configured with another subnet: 192.168.53.0/24 with 192.168.53.1-192.168.53.1 pool.
  #first shared subnet
  Add subnet 0 to shared-subnet set 0.
  Add subnet 1 to shared-subnet set 0.
  Add configuration parameter name with value "name-abc" to shared-subnet 0 configuration.
  Add configuration parameter interface with value "$(SERVER_IFACE)" to shared-subnet 0 configuration.
  #second shared-subnet
  Add subnet 2 to shared-subnet set 1.
  Add subnet 3 to shared-subnet set 1.
  Add configuration parameter name with value "name-xyz" to shared-subnet 1 configuration.
  Add configuration parameter relay with value {"ip-address":"$(GIADDR4)"} to shared-subnet 1 configuration.

  Server is configured with time-servers option in subnet 0 with value 199.199.199.10.
  Server is configured with time-servers option in subnet 2 with value 199.199.199.100.
  Server is configured with time-servers option in subnet 3 with value 199.199.199.200.
  Add hooks library located $(SOFTWARE_INSTALL_DIR)/lib/kea/hooks/libdhcp_subnet_cmds.so.

  Server has control channel on unix socket with name $(SOFTWARE_INSTALL_DIR)/var/kea/control_socket.
  Send server configuration using SSH and config-file.

  DHCP server is started.

  Using UNIX socket on server in path $(SOFTWARE_INSTALL_DIR)/var/kea/control_socket send {"command":"network4-del","arguments":{"name":"name-xxyz,"subnets-action": "delete""}}
  Using UNIX socket on server in path $(SOFTWARE_INSTALL_DIR)/var/kea/control_socket send {"command":"network4-list","arguments":{}}

@v4 @kea_only @controlchannel @hook @network_cmds
  Scenario: hook.v4.network.cmds.del-global-options
  Test Setup:
  Server is configured with domain-name-servers option with value 199.199.199.1,100.100.100.1.
  Server is configured with 192.168.50.0/24 subnet with $(EMPTY) pool.
  Server is configured with another subnet: 192.168.51.0/24 with 192.168.51.1-192.168.51.1 pool.
  #first shared subnet
  Add subnet 1 to shared-subnet set 0.
  Add configuration parameter name with value "name-abc" to shared-subnet 0 configuration.
  Add configuration parameter interface with value "$(SERVER_IFACE)" to shared-subnet 0 configuration.

  Server has control channel on unix socket with name $(SOFTWARE_INSTALL_DIR)/var/kea/control_socket.
  Add hooks library located $(SOFTWARE_INSTALL_DIR)/lib/kea/hooks/libdhcp_subnet_cmds.so.
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

  Using UNIX socket on server in path $(SOFTWARE_INSTALL_DIR)/var/kea/control_socket send {"command": "network4-del","arguments":{"name":"name-abc","subnets-action": "delete"}}

  Test Procedure:
  Client requests option 1.
  Client sets chaddr value to ff:01:02:03:ff:04.
  Client sends DISCOVER message.

  Pass Criteria:
  Server MUST NOT respond.

# That needs subnet with empty pool to work
  Test Procedure:
  Client requests option 6.
  Client sets ciaddr value to $(CIADDR).
  Client sends INFORM message.

  Pass Criteria:
  Server MUST respond with ACK message.
  Response MUST include option 6.
  Response option 6 MUST contain value 199.199.199.1.
  Response option 6 MUST contain value 100.100.100.1.

@v4 @kea_only @controlchannel @hook @network_cmds
  Scenario: hook.v4.network.cmds.add-and-del
  Test Setup:
  Server is configured with $(EMPTY) subnet with $(EMPTY) pool.
  Server is configured with domain-name-servers option with value 199.199.199.1,100.100.100.1.
  Server has control channel on unix socket with name $(SOFTWARE_INSTALL_DIR)/var/kea/control_socket.
  Add hooks library located $(SOFTWARE_INSTALL_DIR)/lib/kea/hooks/libdhcp_subnet_cmds.so.
  Send server configuration using SSH and config-file.

  DHCP server is started.

  Test Procedure:
  Client requests option 1.
  Client sets chaddr value to ff:01:02:03:ff:04.
  Client sends DISCOVER message.

  Pass Criteria:
  Server MUST NOT respond.

  Using UNIX socket on server in path $(SOFTWARE_INSTALL_DIR)/var/kea/control_socket send {"command":"network4-add","arguments":{"shared-networks": [{"name": "name-xyz","rebind-timer": 100,"renew-timer": 100,"valid-lifetime": 400,"subnet4": [{"interface": "$(SERVER_IFACE)", "pools": [{"pool": "192.168.50.1/32"}],"rebind-timer": 2000,"renew-timer": 1000,"subnet": "192.168.50.0/24","valid-lifetime": 4000}]}]}}

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

  Using UNIX socket on server in path $(SOFTWARE_INSTALL_DIR)/var/kea/control_socket send {"command": "network4-del","arguments":{"name":"name-xyz","subnets-action": "delete"}}

  Test Procedure:
  Client requests option 1.
  Client sets chaddr value to ff:01:02:03:ff:04.
  Client sends DISCOVER message.

  Pass Criteria:
  Server MUST NOT respond.