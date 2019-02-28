Feature: Kea leases manipulation commands with legal logging hook

@v4 @kea_only @controlchannel @hook @lease_cmds @legal_logging
  Scenario: hook.v4.lease.cmds.legal.logging.update
  Test Procedure:
  Client removes file from server located in: $(SOFTWARE_INSTALL_DIR)/var/kea/kea-legal*.txt.

  Test Setup:
  Server is configured with 192.168.50.0/24 subnet with 192.168.50.1-192.168.50.1 pool.
  Server is configured with another subnet: 10.0.0.0/24 with 10.0.0.5-10.0.0.5 pool.
  Server has control channel on unix socket with name $(SOFTWARE_INSTALL_DIR)/var/kea/control_socket.
  Add hooks library located $(SOFTWARE_INSTALL_DIR)/lib/kea/hooks/libdhcp_legal_log.so.
  Add hooks library located $(SOFTWARE_INSTALL_DIR)/lib/kea/hooks/libdhcp_lease_cmds.so.
  Send server configuration using SSH and config-file.

  DHCP server is started.

  Test Procedure:
  Client requests option 1.
  Client sets chaddr value to ff:01:02:03:ff:04.
  Client sends DISCOVER message.

  Pass Criteria:
  Server MUST respond with OFFER message.
  Response MUST include option 1.
  Response MUST contain yiaddr 192.168.50.1.
  Response option 1 MUST contain value 255.255.255.0.

  Test Procedure:
  Client copies server_id option from received message.
  Client adds to the message requested_addr with value 192.168.50.1.
  Client requests option 1.
  Client sets chaddr value to ff:01:02:03:ff:04.
  Client sends REQUEST message.

  Pass Criteria:
  Server MUST respond with ACK message.
  Response MUST contain yiaddr 192.168.50.1.
  Response MUST include option 1.
  Response option 1 MUST contain value 255.255.255.0.

  File stored in $(SOFTWARE_INSTALL_DIR)/var/kea/kea-leases4.csv MUST contain line or phrase: 192.168.50.1,ff:01:02:03:ff:04,,
  File stored in $(SOFTWARE_INSTALL_DIR)/var/kea/kea-leases4.csv MUST contain line or phrase: ,1,0,0,,0

  Using UNIX socket on server in path $(SOFTWARE_INSTALL_DIR)/var/kea/control_socket send {"command":"lease4-update","arguments":{"ip-address": "192.168.50.1","hostname": "newhostname.example.org","hw-address": "1a:1b:1c:1d:1e:1f","subnet-id":1,"valid-lft":500000}}

  Client download file from server stored in: $(SOFTWARE_INSTALL_DIR)/var/kea/kea-legal*.txt.
  File stored in $(SOFTWARE_INSTALL_DIR)/var/kea/kea-legal*.txt MUST contain line or phrase:  Administrator updated information on the lease of address: 192.168.50.1 to a device with hardware address: 1a:1b:1c:1d:1e:1f for 5 days 18 hrs 53 mins 20 secs

@v4 @kea_only @controlchannel @hook @lease_cmds
  Scenario: hook.v4.lease.cmds.legal.logging.add
  Test Procedure:
  Client removes file from server located in: $(SOFTWARE_INSTALL_DIR)/var/kea/kea-legal*.txt.

  Test Setup:
  Server is configured with 192.168.50.0/24 subnet with 192.168.50.5-192.168.50.5 pool.
  Server has control channel on unix socket with name $(SOFTWARE_INSTALL_DIR)/var/kea/control_socket.
  Add hooks library located $(SOFTWARE_INSTALL_DIR)/lib/kea/hooks/libdhcp_legal_log.so.
  Add hooks library located $(SOFTWARE_INSTALL_DIR)/lib/kea/hooks/libdhcp_lease_cmds.so.
  Send server configuration using SSH and config-file.

  DHCP server is started.

  Using UNIX socket on server in path $(SOFTWARE_INSTALL_DIR)/var/kea/control_socket send {"command": "lease4-add","arguments": {"subnet-id": 1,"ip-address": "192.168.50.5","hw-address": "1a:1b:1c:1d:1e:1f","valid-lft":7777,"expire":123456789,"hostname":"my.host.some.name","client-id":"aa:bb:cc:dd:11:22"}}

  #Now we have to check if lease 192.168.50.50 was actually added -- check leases file
  File stored in $(SOFTWARE_INSTALL_DIR)/var/kea/kea-leases4.csv MUST contain line or phrase: 1a:1b:1c:1d:1e:1f
  File stored in $(SOFTWARE_INSTALL_DIR)/var/kea/kea-leases4.csv MUST contain line or phrase: aa:bb:cc:dd:11:22
  File stored in $(SOFTWARE_INSTALL_DIR)/var/kea/kea-leases4.csv MUST contain line or phrase: 7777
  File stored in $(SOFTWARE_INSTALL_DIR)/var/kea/kea-leases4.csv MUST contain line or phrase: 123456789
  File stored in $(SOFTWARE_INSTALL_DIR)/var/kea/kea-leases4.csv MUST contain line or phrase: my.host.some.name

  Client download file from server stored in: $(SOFTWARE_INSTALL_DIR)/var/kea/kea-legal*.txt.
  File stored in $(SOFTWARE_INSTALL_DIR)/var/kea/kea-legal*.txt MUST contain line or phrase:  Administrator added a lease of address: 192.168.50.5 to a device with hardware address: 1a:1b:1c:1d:1e:1f, client-id: aa:bb:cc:dd:11:22 for 2 hrs 9 mins 37 secs

@v4 @kea_only @controlchannel @hook @lease_cmds
  Scenario: hook.v4.lease.cmds.legal.logging.del-using-address
  Test Procedure:
  Client removes file from server located in: $(SOFTWARE_INSTALL_DIR)/var/kea/kea-legal*.txt.

  Test Setup:
  Server is configured with 192.168.50.0/24 subnet with 192.168.50.1-192.168.50.1 pool.
  Server has control channel on unix socket with name $(SOFTWARE_INSTALL_DIR)/var/kea/control_socket.
  Add hooks library located $(SOFTWARE_INSTALL_DIR)/lib/kea/hooks/libdhcp_legal_log.so.
  Add hooks library located $(SOFTWARE_INSTALL_DIR)/lib/kea/hooks/libdhcp_lease_cmds.so.
  Send server configuration using SSH and config-file.

  DHCP server is started.

  Test Procedure:
  Client requests option 1.
  Client sets chaddr value to ff:01:02:03:ff:04.
  Client sends DISCOVER message.

  Pass Criteria:
  Server MUST respond with OFFER message.
  Response MUST include option 1.
  Response MUST contain yiaddr 192.168.50.1.
  Response option 1 MUST contain value 255.255.255.0.

  Test Procedure:
  Client copies server_id option from received message.
  Client adds to the message requested_addr with value 192.168.50.1.
  Client requests option 1.
  Client sets chaddr value to ff:01:02:03:ff:04.
  Client sends REQUEST message.

  Pass Criteria:
  Server MUST respond with ACK message.
  Response MUST contain yiaddr 192.168.50.1.
  Response MUST include option 1.
  Response option 1 MUST contain value 255.255.255.0.

  Test Procedure:
  Client requests option 1.
  Client sets chaddr value to aa:bb:cc:dd:ee:11.
  Client sends DISCOVER message.

  Pass Criteria:
  Server MUST NOT respond.

  Using UNIX socket on server in path $(SOFTWARE_INSTALL_DIR)/var/kea/control_socket send {"command": "lease4-del","arguments": {"ip-address": "192.168.50.1"}}

  Test Procedure:
  Client requests option 1.
  Client sets chaddr value to aa:bb:cc:dd:ee:11.
  Client sends DISCOVER message.

  Pass Criteria:
  Server MUST respond with OFFER message.
  Response MUST include option 1.
  Response MUST contain yiaddr 192.168.50.1.
  Response option 1 MUST contain value 255.255.255.0.

  Client download file from server stored in: $(SOFTWARE_INSTALL_DIR)/var/kea/kea-legal*.txt.
  File stored in $(SOFTWARE_INSTALL_DIR)/var/kea/kea-legal*.txt MUST contain line or phrase: Administrator deleted the lease for address: 192.168.50.1

@v4 @kea_only @controlchannel @hook @lease_cmds
  Scenario: hook.v4.lease.cmds.legal.logging.del-using-hw-address
  Test Procedure:
  Client removes file from server located in: $(SOFTWARE_INSTALL_DIR)/var/kea/kea-legal*.txt.

  Test Setup:
  Server is configured with 192.168.50.0/24 subnet with 192.168.50.1-192.168.50.1 pool.
  Server has control channel on unix socket with name $(SOFTWARE_INSTALL_DIR)/var/kea/control_socket.
  Add hooks library located $(SOFTWARE_INSTALL_DIR)/lib/kea/hooks/libdhcp_legal_log.so.
  Add hooks library located $(SOFTWARE_INSTALL_DIR)/lib/kea/hooks/libdhcp_lease_cmds.so.
  Send server configuration using SSH and config-file.

  DHCP server is started.

  Test Procedure:
  Client requests option 1.
  Client sets chaddr value to ff:01:02:03:ff:04.
  Client sends DISCOVER message.

  Pass Criteria:
  Server MUST respond with OFFER message.
  Response MUST include option 1.
  Response MUST contain yiaddr 192.168.50.1.
  Response option 1 MUST contain value 255.255.255.0.

  Test Procedure:
  Client copies server_id option from received message.
  Client adds to the message requested_addr with value 192.168.50.1.
  Client requests option 1.
  Client sets chaddr value to ff:01:02:03:ff:04.
  Client sends REQUEST message.

  Pass Criteria:
  Server MUST respond with ACK message.
  Response MUST contain yiaddr 192.168.50.1.
  Response MUST include option 1.
  Response option 1 MUST contain value 255.255.255.0.

  Test Procedure:
  Client requests option 1.
  Client sets chaddr value to aa:bb:cc:dd:ee:11.
  Client sends DISCOVER message.

  Pass Criteria:
  Server MUST NOT respond.

  Using UNIX socket on server in path $(SOFTWARE_INSTALL_DIR)/var/kea/control_socket send {"command": "lease4-del","arguments": {"identifier": "ff:01:02:03:ff:04","identifier-type":"hw-address","subnet-id":1}}

  Test Procedure:
  Client requests option 1.
  Client sets chaddr value to aa:bb:cc:dd:ee:11.
  Client sends DISCOVER message.

  Pass Criteria:
  Server MUST respond with OFFER message.
  Response MUST include option 1.
  Response MUST contain yiaddr 192.168.50.1.
  Response option 1 MUST contain value 255.255.255.0.

  Client download file from server stored in: $(SOFTWARE_INSTALL_DIR)/var/kea/kea-legal*.txt.
  File stored in $(SOFTWARE_INSTALL_DIR)/var/kea/kea-legal*.txt MUST contain line or phrase: Administrator deleted a lease for a device identified by: hw-address of ff:01:02:03:ff:04

@v4 @kea_only @controlchannel @hook @lease_cmds @disabled
  Scenario: hook.v4.lease.cmds.legal.logging.wipe
  Test Procedure:
  Client removes file from server located in: $(SOFTWARE_INSTALL_DIR)/var/kea/kea-legal*.txt.

  Test Setup:
  Server is configured with 192.168.50.0/24 subnet with 192.168.50.1-192.168.50.2 pool.
  Server has control channel on unix socket with name $(SOFTWARE_INSTALL_DIR)/var/kea/control_socket.
  Add hooks library located $(SOFTWARE_INSTALL_DIR)/lib/kea/hooks/libdhcp_legal_log.so.
  Add hooks library located $(SOFTWARE_INSTALL_DIR)/lib/kea/hooks/libdhcp_lease_cmds.so.
  Send server configuration using SSH and config-file.

  DHCP server is started.

  Test Procedure:
  Client requests option 1.
  Client sets chaddr value to ff:01:02:03:ff:04.
  Client sends DISCOVER message.

  Pass Criteria:
  Server MUST respond with OFFER message.
  Response MUST include option 1.
  Response MUST contain yiaddr 192.168.50.1.
  Response option 1 MUST contain value 255.255.255.0.

  Test Procedure:
  Client copies server_id option from received message.
  Client adds to the message requested_addr with value 192.168.50.1.
  Client requests option 1.
  Client sets chaddr value to ff:01:02:03:ff:04.
  Client sends REQUEST message.

  Pass Criteria:
  Server MUST respond with ACK message.
  Response MUST contain yiaddr 192.168.50.1.
  Response MUST include option 1.
  Response option 1 MUST contain value 255.255.255.0.

  Test Procedure:
  Client requests option 1.
  Client sets chaddr value to ff:01:02:03:ff:05.
  Client sends DISCOVER message.

  Pass Criteria:
  Server MUST respond with OFFER message.
  Response MUST include option 1.
  Response MUST contain yiaddr 192.168.50.2.
  Response option 1 MUST contain value 255.255.255.0.

  Test Procedure:
  Client copies server_id option from received message.
  Client adds to the message requested_addr with value 192.168.50.2.
  Client requests option 1.
  Client sets chaddr value to ff:01:02:03:ff:05.
  Client sends REQUEST message.

  Pass Criteria:
  Server MUST respond with ACK message.
  Response MUST contain yiaddr 192.168.50.2.
  Response MUST include option 1.
  Response option 1 MUST contain value 255.255.255.0.

  Test Procedure:
  Client requests option 1.
  Client sets chaddr value to aa:bb:cc:dd:ee:11.
  Client sends DISCOVER message.

  Pass Criteria:
  Server MUST NOT respond.

  Using UNIX socket on server in path $(SOFTWARE_INSTALL_DIR)/var/kea/control_socket send {"command": "lease4-wipe","arguments": {"subnet-id":1}}

  Test Procedure:
  Client requests option 1.
  Client sets chaddr value to aa:bb:cc:dd:ee:11.
  Client sends DISCOVER message.

  Pass Criteria:
  Server MUST respond with OFFER message.
  Response MUST include option 1.
  Response MUST contain yiaddr 192.168.50.1.
  Response option 1 MUST contain value 255.255.255.0.

  Client download file from server stored in: $(SOFTWARE_INSTALL_DIR)/var/kea/kea-legal*.txt.
  Fail test.
  #File stored in $(SOFTWARE_INSTALL_DIR)/var/kea/kea-legal*.txt MUST contain line or phrase: