Feature: Kea Hook hosts_cmds testing

@v4 @hosts_cmds @kea_only 
  Scenario: v4.hosts.cmds.add-reservation-mysql
  Test Setup:
  Add hooks library located $(SOFTWARE_INSTALL_DIR)lib/hooks/libdhcp_host_cmds.so.
  Server is configured with 192.168.50.0/24 subnet with 192.168.50.50-192.168.50.50 pool.
  Server has control channel on unix socket with name $(SOFTWARE_INSTALL_DIR)var/kea/control_socket.

  Use MySQL reservation system.

  Send server configuration using SSH and config-file.
  DHCP server is started.

  Test Procedure:
  Client sets chaddr value to ff:01:02:03:ff:04.
  Client sends DISCOVER message.

  Pass Criteria:
  Server MUST respond with OFFER message.
  Response MUST contain yiaddr 192.168.50.50.

  Using UNIX socket on server in path $(SOFTWARE_INSTALL_DIR)var/kea/control_socket send {"command":"reservation-add","arguments":{"reservation":{"subnet-id":1,"hw-address":"ff:01:02:03:ff:04","ip-address":"192.168.50.100"}}}

  Test Procedure:
  Client sets chaddr value to ff:01:02:03:ff:04.
  Client sends DISCOVER message.

  Pass Criteria:
  Server MUST respond with OFFER message.
  Response MUST contain yiaddr 192.168.50.100.

  Test Procedure:
  Client copies server_id option from received message.
  Client adds to the message requested_addr with value 192.168.50.100.
  Client sets chaddr value to ff:01:02:03:ff:04.
  Client sends REQUEST message.

  Pass Criteria:
  Server MUST respond with ACK message.
  Response MUST contain yiaddr 192.168.50.100.
  Response MUST include option 1.
  Response option 1 MUST contain value 255.255.255.0.

@v4 @hosts_cmds @kea_only 
  Scenario: v4.hosts.cmds.del-reservation-mysql
  Test Setup:
  Add hooks library located $(SOFTWARE_INSTALL_DIR)lib/hooks/libdhcp_host_cmds.so.
  Server is configured with 192.168.50.0/24 subnet with 192.168.50.50-192.168.50.50 pool.
  Server has control channel on unix socket with name $(SOFTWARE_INSTALL_DIR)var/kea/control_socket.

  Use MySQL reservation system.

  Send server configuration using SSH and config-file.
  DHCP server is started.

  Test Procedure:
  Client sets chaddr value to ff:01:02:03:ff:04.
  Client sends DISCOVER message.

  Pass Criteria:
  Server MUST respond with OFFER message.
  Response MUST contain yiaddr 192.168.50.50.

  Using UNIX socket on server in path $(SOFTWARE_INSTALL_DIR)var/kea/control_socket send {"command":"reservation-add","arguments":{"reservation":{"subnet-id":1,"hw-address":"ff:01:02:03:ff:04","ip-address":"192.168.50.100"}}}

  Test Procedure:
  Client sets chaddr value to ff:01:02:03:ff:04.
  Client sends DISCOVER message.

  Pass Criteria:
  Server MUST respond with OFFER message.
  Response MUST contain yiaddr 192.168.50.100.

  Using UNIX socket on server in path $(SOFTWARE_INSTALL_DIR)var/kea/control_socket send {"command":"reservation-del","arguments":{"subnet-id":1,"ip-address":"192.168.50.100"}}

  Test Procedure:
  Client sets chaddr value to ff:01:02:03:ff:04.
  Client sends DISCOVER message.

  Pass Criteria:
  Server MUST respond with OFFER message.
  Response MUST contain yiaddr 192.168.50.50.

@v4 @hosts_cmds @kea_only 
  Scenario: v4.hosts.cmds.del-reservation-mysql-2
  Test Setup:
  #address reserved without using command
  Add hooks library located $(SOFTWARE_INSTALL_DIR)lib/hooks/libdhcp_host_cmds.so.
  Server is configured with 192.168.50.0/24 subnet with 192.168.50.50-192.168.50.50 pool.
  Server has control channel on unix socket with name $(SOFTWARE_INSTALL_DIR)var/kea/control_socket.

  Use MySQL reservation system.
  Create new MySQL reservation identified by hw-address ff:01:02:03:ff:04.
  Add hostname reserved-hostname to MySQL reservation record id 1.
  Add ipv4_address 192.168.50.100 to MySQL reservation record id 1.
  Add dhcp4_subnet_id 1 to MySQL reservation record id 1.
  Upload hosts reservation to MySQL database.

  Send server configuration using SSH and config-file.
  DHCP server is started.

  Test Procedure:
  Client sets chaddr value to ff:01:02:03:ff:04.
  Client sends DISCOVER message.

  Pass Criteria:
  Server MUST respond with OFFER message.
  Response MUST contain yiaddr 192.168.50.100.

  Using UNIX socket on server in path $(SOFTWARE_INSTALL_DIR)var/kea/control_socket send {"command":"reservation-del","arguments":{"subnet-id":1,"ip-address":"192.168.50.100"}}

  Test Procedure:
  Client sets chaddr value to ff:01:02:03:ff:04.
  Client sends DISCOVER message.

  Pass Criteria:
  Server MUST respond with OFFER message.
  Response MUST contain yiaddr 192.168.50.50.

@v4 @hosts_cmds @kea_only 
  Scenario: v4.hosts.cmds.del-reservation-pgsql
  Test Setup:
  Add hooks library located $(SOFTWARE_INSTALL_DIR)lib/hooks/libdhcp_host_cmds.so.
  Server is configured with 192.168.50.0/24 subnet with 192.168.50.50-192.168.50.50 pool.
  Server has control channel on unix socket with name $(SOFTWARE_INSTALL_DIR)var/kea/control_socket.

  Use PostgreSQL reservation system.

  Send server configuration using SSH and config-file.
  DHCP server is started.

  Test Procedure:
  Client sets chaddr value to ff:01:02:03:ff:04.
  Client sends DISCOVER message.

  Pass Criteria:
  Server MUST respond with OFFER message.
  Response MUST contain yiaddr 192.168.50.50.

  Using UNIX socket on server in path $(SOFTWARE_INSTALL_DIR)var/kea/control_socket send {"command":"reservation-add","arguments":{"reservation":{"subnet-id":1,"hw-address":"ff:01:02:03:ff:04","ip-address":"192.168.50.100"}}}

  Test Procedure:
  Client sets chaddr value to ff:01:02:03:ff:04.
  Client sends DISCOVER message.

  Pass Criteria:
  Server MUST respond with OFFER message.
  Response MUST contain yiaddr 192.168.50.100.

  Using UNIX socket on server in path $(SOFTWARE_INSTALL_DIR)var/kea/control_socket send {"command":"reservation-del","arguments":{"subnet-id":1,"ip-address":"192.168.50.100"}}

  Test Procedure:
  Client sets chaddr value to ff:01:02:03:ff:04.
  Client sends DISCOVER message.

  Pass Criteria:
  Server MUST respond with OFFER message.
  Response MUST contain yiaddr 192.168.50.50.

@v4 @hosts_cmds @kea_only 
  Scenario: v4.hosts.cmds.del-reservation-pgsql-2
  Test Setup:
  Add hooks library located $(SOFTWARE_INSTALL_DIR)lib/hooks/libdhcp_host_cmds.so.
  Server is configured with 192.168.50.0/24 subnet with 192.168.50.50-192.168.50.50 pool.
  Server has control channel on unix socket with name $(SOFTWARE_INSTALL_DIR)var/kea/control_socket.

  Use PostgreSQL reservation system.
  Create new PostgreSQL reservation identified by hw-address ff:01:02:03:ff:04.
  Add hostname reserved-hostname to PostgreSQL reservation record id 1.
  Add ipv4_address 192.168.50.100 to PostgreSQL reservation record id 1.
  Add dhcp4_subnet_id 1 to PostgreSQL reservation record id 1.
  Upload hosts reservation to PostgreSQL database.

  Send server configuration using SSH and config-file.
  DHCP server is started.

  Test Procedure:
  Client sets chaddr value to ff:01:02:03:ff:04.
  Client sends DISCOVER message.

  Pass Criteria:
  Server MUST respond with OFFER message.
  Response MUST contain yiaddr 192.168.50.100.

  Using UNIX socket on server in path $(SOFTWARE_INSTALL_DIR)var/kea/control_socket send {"command":"reservation-del","arguments":{"subnet-id":1,"ip-address":"192.168.50.100"}}

  Test Procedure:
  Client sets chaddr value to ff:01:02:03:ff:04.
  Client sends DISCOVER message.

  Pass Criteria:
  Server MUST respond with OFFER message.
  Response MUST contain yiaddr 192.168.50.50.

  Test Procedure:
  Client copies server_id option from received message.
  Client adds to the message requested_addr with value 192.168.50.50.
  Client sets chaddr value to ff:01:02:03:ff:04.
  Client sends REQUEST message.

  Pass Criteria:
  Server MUST respond with ACK message.
  Response MUST contain yiaddr 192.168.50.50.
  Response MUST include option 1.
  Response option 1 MUST contain value 255.255.255.0.

@v4 @hosts_cmds @kea_only 
  Scenario: v4.hosts.cmds.add-reservation-pgsql
  Test Setup:
  Add hooks library located $(SOFTWARE_INSTALL_DIR)lib/hooks/libdhcp_host_cmds.so.
  Server is configured with 192.168.50.0/24 subnet with 192.168.50.50-192.168.50.50 pool.
  Server has control channel on unix socket with name $(SOFTWARE_INSTALL_DIR)var/kea/control_socket.

  Use PostgreSQL reservation system.

  Send server configuration using SSH and config-file.
  DHCP server is started.

  Test Procedure:
  Client sets chaddr value to ff:01:02:03:ff:04.
  Client sends DISCOVER message.

  Pass Criteria:
  Server MUST respond with OFFER message.
  Response MUST contain yiaddr 192.168.50.50.

  Using UNIX socket on server in path $(SOFTWARE_INSTALL_DIR)var/kea/control_socket send {"command":"reservation-add","arguments":{"reservation":{"subnet-id":1,"hw-address":"ff:01:02:03:ff:04","ip-address":"192.168.50.100"}}}

  Test Procedure:
  Client sets chaddr value to ff:01:02:03:ff:04.
  Client sends DISCOVER message.

  Pass Criteria:
  Server MUST respond with OFFER message.
  Response MUST contain yiaddr 192.168.50.100.

  Test Procedure:
  Client copies server_id option from received message.
  Client adds to the message requested_addr with value 192.168.50.100.
  Client sets chaddr value to ff:01:02:03:ff:04.
  Client sends REQUEST message.

  Pass Criteria:
  Server MUST respond with ACK message.
  Response MUST contain yiaddr 192.168.50.100.
  Response MUST include option 1.
  Response option 1 MUST contain value 255.255.255.0.

@v4 @hosts_cmds @kea_only 
  Scenario: v4.hosts.cmds.get-reservation-mysql
  Test Setup:
  Add hooks library located $(SOFTWARE_INSTALL_DIR)lib/hooks/libdhcp_host_cmds.so.
  Server is configured with 192.168.50.0/24 subnet with 192.168.50.50-192.168.50.50 pool.
  Server has control channel on unix socket with name $(SOFTWARE_INSTALL_DIR)var/kea/control_socket.

  Use MySQL reservation system.

  Send server configuration using SSH and config-file.
  DHCP server is started.

  Test Procedure:
  Client sets chaddr value to ff:01:02:03:ff:04.
  Client sends DISCOVER message.

  Pass Criteria:
  Server MUST respond with OFFER message.
  Response MUST contain yiaddr 192.168.50.50.

  Using UNIX socket on server in path $(SOFTWARE_INSTALL_DIR)var/kea/control_socket send {"command":"reservation-add","arguments":{"reservation":{"subnet-id":1,"hw-address":"ff:01:02:03:ff:04","ip-address":"192.168.50.100"}}}

  Test Procedure:
  Client sets chaddr value to ff:01:02:03:ff:04.
  Client sends DISCOVER message.

  Pass Criteria:
  Server MUST respond with OFFER message.
  Response MUST contain yiaddr 192.168.50.100.

  Using UNIX socket on server in path $(SOFTWARE_INSTALL_DIR)var/kea/control_socket send {"command": "reservation-get","arguments":{"subnet-id":1,"identifier-type": "hw-address","identifier":"ff:01:02:03:ff:04"}}

@v4 @hosts_cmds @kea_only 
  Scenario: v4.hosts.cmds.get-reservation-mysql-2
  Test Setup:
  #address reserved without using command
  Add hooks library located $(SOFTWARE_INSTALL_DIR)lib/hooks/libdhcp_host_cmds.so.
  Server is configured with 192.168.50.0/24 subnet with 192.168.50.50-192.168.50.50 pool.
  Server has control channel on unix socket with name $(SOFTWARE_INSTALL_DIR)var/kea/control_socket.

  Use MySQL reservation system.
  Create new MySQL reservation identified by hw-address ff:01:02:03:ff:04.
  Add hostname reserved-hostname to MySQL reservation record id 1.
  Add ipv4_address 192.168.50.100 to MySQL reservation record id 1.
  Add dhcp4_subnet_id 1 to MySQL reservation record id 1.
  Upload hosts reservation to MySQL database.

  Send server configuration using SSH and config-file.
  DHCP server is started.

  Test Procedure:
  Client sets chaddr value to ff:01:02:03:ff:04.
  Client sends DISCOVER message.

  Pass Criteria:
  Server MUST respond with OFFER message.
  Response MUST contain yiaddr 192.168.50.100.

  Using UNIX socket on server in path $(SOFTWARE_INSTALL_DIR)var/kea/control_socket send {"command": "reservation-get","arguments":{"subnet-id":1,"identifier-type": "hw-address","identifier":"ff:01:02:03:ff:04"}}

@v4 @hosts_cmds @kea_only 
  Scenario: v4.hosts.cmds.get-reservation-pgsql
  Test Setup:
  Add hooks library located $(SOFTWARE_INSTALL_DIR)lib/hooks/libdhcp_host_cmds.so.
  Server is configured with 192.168.50.0/24 subnet with 192.168.50.50-192.168.50.50 pool.
  Server has control channel on unix socket with name $(SOFTWARE_INSTALL_DIR)var/kea/control_socket.

  Use PostgreSQL reservation system.

  Send server configuration using SSH and config-file.
  DHCP server is started.

  Test Procedure:
  Client sets chaddr value to ff:01:02:03:ff:04.
  Client sends DISCOVER message.

  Pass Criteria:
  Server MUST respond with OFFER message.
  Response MUST contain yiaddr 192.168.50.50.

  Using UNIX socket on server in path $(SOFTWARE_INSTALL_DIR)var/kea/control_socket send {"command":"reservation-add","arguments":{"reservation":{"subnet-id":1,"hw-address":"ff:01:02:03:ff:04","ip-address":"192.168.50.100"}}}

  Test Procedure:
  Client sets chaddr value to ff:01:02:03:ff:04.
  Client sends DISCOVER message.

  Pass Criteria:
  Server MUST respond with OFFER message.
  Response MUST contain yiaddr 192.168.50.100.

  Using UNIX socket on server in path $(SOFTWARE_INSTALL_DIR)var/kea/control_socket send {"command": "reservation-get","arguments":{"subnet-id":1,"identifier-type": "hw-address","identifier":"ff:01:02:03:ff:04"}}

@v4 @hosts_cmds @kea_only 
  Scenario: v4.hosts.cmds.get-reservation-pgsql-2
  Test Setup:
  Add hooks library located $(SOFTWARE_INSTALL_DIR)lib/hooks/libdhcp_host_cmds.so.
  Server is configured with 192.168.50.0/24 subnet with 192.168.50.50-192.168.50.50 pool.
  Server has control channel on unix socket with name $(SOFTWARE_INSTALL_DIR)var/kea/control_socket.

  Use PostgreSQL reservation system.
  Create new PostgreSQL reservation identified by hw-address ff:01:02:03:ff:04.
  Add hostname reserved-hostname to PostgreSQL reservation record id 1.
  Add ipv4_address 192.168.50.100 to PostgreSQL reservation record id 1.
  Add dhcp4_subnet_id 1 to PostgreSQL reservation record id 1.
  Upload hosts reservation to PostgreSQL database.

  Send server configuration using SSH and config-file.
  DHCP server is started.

  Test Procedure:
  Client sets chaddr value to ff:01:02:03:ff:04.
  Client sends DISCOVER message.

  Pass Criteria:
  Server MUST respond with OFFER message.
  Response MUST contain yiaddr 192.168.50.100.

  Using UNIX socket on server in path $(SOFTWARE_INSTALL_DIR)var/kea/control_socket send {"command": "reservation-get","arguments":{"subnet-id":1,"identifier-type": "hw-address","identifier":"ff:01:02:03:ff:04"}}

@v4 @hosts_cmds @kea_only 
  Scenario: v4.hosts.cmds.add-reservation-mysql-flex-id
  Test Setup:
  Server is configured with 192.168.50.0/24 subnet with 192.168.50.50-192.168.50.50 pool.
  Server has control channel on unix socket with name $(SOFTWARE_INSTALL_DIR)var/kea/control_socket.

  Add hooks library located $(SOFTWARE_INSTALL_DIR)lib/hooks/libdhcp_host_cmds.so.
  Add hooks library located $(SOFTWARE_INSTALL_DIR)lib/hooks/libdhcp_flex_id.so.
  To hook no. 2 add parameter named identifier-expression with value: option[60].hex
  Add to config file line: "host-reservation-identifiers": [ "flex-id" ]

  Use MySQL reservation system.

  Send server configuration using SSH and config-file.
  DHCP server is started.

  Test Procedure:
  Client adds to the message vendor_class_id with value docsis3.0.
  Client sets chaddr value to ff:01:02:03:ff:04.
  Client sends DISCOVER message.

  Pass Criteria:
  Server MUST respond with OFFER message.
  Response MUST contain yiaddr 192.168.50.50.

  Using UNIX socket on server in path $(SOFTWARE_INSTALL_DIR)var/kea/control_socket send {"command":"reservation-add","arguments":{"reservation":{"subnet-id":1,"flex-id":"'docsis3.0'","ip-address":"192.168.50.100"}}}

  Test Procedure:
  Client adds to the message vendor_class_id with value docsis3.0.
  Client sets chaddr value to ff:01:02:03:ff:04.
  Client sends DISCOVER message.

  Pass Criteria:
  Server MUST respond with OFFER message.
  Response MUST contain yiaddr 192.168.50.100.

  Test Procedure:
  #Client adds to the message vendor_class_id with value docsis3.0.
  Client copies server_id option from received message.
  Client adds to the message requested_addr with value 192.168.50.100.
  Client adds to the message vendor_class_id with value docsis3.0.
  Client sets chaddr value to ff:01:02:03:ff:04.
  Client sends REQUEST message.

  Pass Criteria:
  Server MUST respond with ACK message.
  Response MUST contain yiaddr 192.168.50.100.
  Response MUST include option 1.
  Response option 1 MUST contain value 255.255.255.0.

@v4 @hosts_cmds @kea_only 
  Scenario: v4.hosts.cmds.add-reservation-mysql-flex-id-nak
  Test Setup:
  Server is configured with 192.168.50.0/24 subnet with 192.168.50.50-192.168.50.50 pool.
  Server has control channel on unix socket with name $(SOFTWARE_INSTALL_DIR)var/kea/control_socket.

  Add hooks library located $(SOFTWARE_INSTALL_DIR)lib/hooks/libdhcp_host_cmds.so.
  Add hooks library located $(SOFTWARE_INSTALL_DIR)lib/hooks/libdhcp_flex_id.so.
  To hook no. 2 add parameter named identifier-expression with value: option[60].hex
  Add to config file line: "host-reservation-identifiers": [ "flex-id" ]

  Use MySQL reservation system.

  Send server configuration using SSH and config-file.
  DHCP server is started.

  Test Procedure:
  Client adds to the message vendor_class_id with value docsis3.0.
  Client sets chaddr value to ff:01:02:03:ff:04.
  Client sends DISCOVER message.

  Pass Criteria:
  Server MUST respond with OFFER message.
  Response MUST contain yiaddr 192.168.50.50.

  Using UNIX socket on server in path $(SOFTWARE_INSTALL_DIR)var/kea/control_socket send {"command":"reservation-add","arguments":{"reservation":{"subnet-id":1,"flex-id":"'docsis3.0'","ip-address":"192.168.50.100"}}}

  Test Procedure:
  Client adds to the message vendor_class_id with value docsis3.0.
  Client sets chaddr value to ff:01:02:03:ff:04.
  Client sends DISCOVER message.

  Pass Criteria:
  Server MUST respond with OFFER message.
  Response MUST contain yiaddr 192.168.50.100.

  Test Procedure:
  #Client adds to the message vendor_class_id with value docsis3.0.
  Client copies server_id option from received message.
  Client adds to the message requested_addr with value 192.168.50.10.
  Client adds to the message vendor_class_id with value docsis3.0.
  Client sets chaddr value to ff:01:02:03:ff:04.
  Client sends REQUEST message.

  Pass Criteria:
  Server MUST respond with NAK message.
  
  @v4 @hosts_cmds @kea_only 
  Scenario: v4.hosts.cmds.add-reservation-pgsql-flex-id
  Test Setup:
  Server is configured with 192.168.50.0/24 subnet with 192.168.50.50-192.168.50.50 pool.
  Server has control channel on unix socket with name $(SOFTWARE_INSTALL_DIR)var/kea/control_socket.

  Add hooks library located $(SOFTWARE_INSTALL_DIR)lib/hooks/libdhcp_host_cmds.so.
  Add hooks library located $(SOFTWARE_INSTALL_DIR)lib/hooks/libdhcp_flex_id.so.
  To hook no. 2 add parameter named identifier-expression with value: option[60].hex
  Add to config file line: "host-reservation-identifiers": [ "flex-id" ]

  Use PostgreSQL reservation system.

  Send server configuration using SSH and config-file.
  DHCP server is started.

  Test Procedure:
  Client adds to the message vendor_class_id with value docsis3.0.
  Client sets chaddr value to ff:01:02:03:ff:04.
  Client sends DISCOVER message.

  Pass Criteria:
  Server MUST respond with OFFER message.
  Response MUST contain yiaddr 192.168.50.50.

  Using UNIX socket on server in path $(SOFTWARE_INSTALL_DIR)var/kea/control_socket send {"command":"reservation-add","arguments":{"reservation":{"subnet-id":1,"flex-id":"'docsis3.0'","ip-address":"192.168.50.100"}}}

  Test Procedure:
  Client adds to the message vendor_class_id with value docsis3.0.
  Client sets chaddr value to ff:01:02:03:ff:04.
  Client sends DISCOVER message.

  Pass Criteria:
  Server MUST respond with OFFER message.
  Response MUST contain yiaddr 192.168.50.100.

  Test Procedure:
  #Client adds to the message vendor_class_id with value docsis3.0.
  Client copies server_id option from received message.
  Client adds to the message requested_addr with value 192.168.50.100.
  Client adds to the message vendor_class_id with value docsis3.0.
  Client sets chaddr value to ff:01:02:03:ff:04.
  Client sends REQUEST message.

  Pass Criteria:
  Server MUST respond with ACK message.
  Response MUST contain yiaddr 192.168.50.100.
  Response MUST include option 1.
  Response option 1 MUST contain value 255.255.255.0.

@v4 @hosts_cmds @kea_only 
  Scenario: v4.hosts.cmds.add-reservation-pgsql-flex-id-nak
  Test Setup:
  Server is configured with 192.168.50.0/24 subnet with 192.168.50.50-192.168.50.50 pool.
  Server has control channel on unix socket with name $(SOFTWARE_INSTALL_DIR)var/kea/control_socket.

  Add hooks library located $(SOFTWARE_INSTALL_DIR)lib/hooks/libdhcp_host_cmds.so.
  Add hooks library located $(SOFTWARE_INSTALL_DIR)lib/hooks/libdhcp_flex_id.so.
  To hook no. 2 add parameter named identifier-expression with value: option[60].hex
  Add to config file line: "host-reservation-identifiers": [ "flex-id" ]

  Use PostgreSQL reservation system.

  Send server configuration using SSH and config-file.
  DHCP server is started.

  Test Procedure:
  Client adds to the message vendor_class_id with value docsis3.0.
  Client sets chaddr value to ff:01:02:03:ff:04.
  Client sends DISCOVER message.

  Pass Criteria:
  Server MUST respond with OFFER message.
  Response MUST contain yiaddr 192.168.50.50.

  Using UNIX socket on server in path $(SOFTWARE_INSTALL_DIR)var/kea/control_socket send {"command":"reservation-add","arguments":{"reservation":{"subnet-id":1,"flex-id":"'docsis3.0'","ip-address":"192.168.50.100"}}}

  Test Procedure:
  Client adds to the message vendor_class_id with value docsis3.0.
  Client sets chaddr value to ff:01:02:03:ff:04.
  Client sends DISCOVER message.

  Pass Criteria:
  Server MUST respond with OFFER message.
  Response MUST contain yiaddr 192.168.50.100.

  Test Procedure:
  #Client adds to the message vendor_class_id with value docsis3.0.
  Client copies server_id option from received message.
  Client adds to the message requested_addr with value 192.168.50.10.
  Client adds to the message vendor_class_id with value docsis3.0.
  Client sets chaddr value to ff:01:02:03:ff:04.
  Client sends REQUEST message.

  Pass Criteria:
  Server MUST respond with NAK message.

@v4 @hosts_cmds @kea_only 
  Scenario: v4.hosts.cmds.add-reservation-complex-pgsql
  Test Setup:
  Add hooks library located $(SOFTWARE_INSTALL_DIR)lib/hooks/libdhcp_host_cmds.so.
  Server is configured with 192.168.50.0/24 subnet with 192.168.50.50-192.168.50.50 pool.
  Server has control channel on unix socket with name $(SOFTWARE_INSTALL_DIR)var/kea/control_socket.
  Use PostgreSQL reservation system.
  Send server configuration using SSH and config-file.
  DHCP server is started.

  Test Procedure:
  Client adds to the message client_id with value 01:0a:0b:0c:0d:0e:0f.
  Client sends DISCOVER message.

  Pass Criteria:
  Server MUST respond with OFFER message.
  Response MUST contain yiaddr 192.168.50.50.

  Using UNIX socket on server in path $(SOFTWARE_INSTALL_DIR)var/kea/control_socket send {"command":"reservation-add","arguments":{"reservation":{"subnet-id":1,"client-id":"01:0a:0b:0c:0d:0e:0f","ip-address":"192.0.2.205","next-server":"192.0.2.1","server-hostname":"hal9000","boot-file-name":"/dev/null","option-data":[{"name":"domain-name-servers","data":"10.1.1.202,10.1.1.203"}],"client-classes":["special_snowflake","office"]}}}

  Test Procedure:
  Client adds to the message client_id with value 01:0a:0b:0c:0d:0e:0f.
  Client sends DISCOVER message.

  Pass Criteria:
  Server MUST respond with OFFER message.
  Response MUST contain yiaddr 192.0.2.205.
  Response MUST include option 6.
  Response option 6 MUST contain value 10.1.1.203.
  Response option 6 MUST contain value 10.1.1.202.
  Response MUST contain sname hal9000.
  Response MUST contain file /dev/null.

  Test Procedure:
  Client copies server_id option from received message.
  Client adds to the message requested_addr with value 192.0.2.205.
  Client adds to the message client_id with value 01:0a:0b:0c:0d:0e:0f.
  Client sets chaddr value to 01:0a:0b:0c:0d:0e:0f.
  Client sends REQUEST message.

  Pass Criteria:
  Server MUST respond with ACK message.
  Response MUST contain yiaddr 192.0.2.205.
  Response MUST include option 6.
  Response option 6 MUST contain value 10.1.1.203.
  Response option 6 MUST contain value 10.1.1.202.
  Response MUST contain sname hal9000.
  Response MUST contain file /dev/null.

@v4 @hosts_cmds @kea_only 
  Scenario: v4.hosts.cmds.add-reservation-complex-mysql
  Test Setup:
  Add hooks library located $(SOFTWARE_INSTALL_DIR)lib/hooks/libdhcp_host_cmds.so.
  Server is configured with 192.168.50.0/24 subnet with 192.168.50.50-192.168.50.50 pool.
  Server has control channel on unix socket with name $(SOFTWARE_INSTALL_DIR)var/kea/control_socket.
  Use MySQL reservation system.
  Send server configuration using SSH and config-file.
  DHCP server is started.

  Test Procedure:
  Client adds to the message client_id with value 01:0a:0b:0c:0d:0e:0f.
  Client sends DISCOVER message.

  Pass Criteria:
  Server MUST respond with OFFER message.
  Response MUST contain yiaddr 192.168.50.50.

  Using UNIX socket on server in path $(SOFTWARE_INSTALL_DIR)var/kea/control_socket send {"command":"reservation-add","arguments":{"reservation":{"subnet-id":1,"client-id":"01:0a:0b:0c:0d:0e:0f","ip-address":"192.0.2.205","next-server":"192.0.2.1","server-hostname":"hal9000","boot-file-name":"/dev/null","option-data":[{"name":"domain-name-servers","data":"10.1.1.202,10.1.1.203"}],"client-classes":["special_snowflake","office"]}}}

  Test Procedure:
  Client adds to the message client_id with value 01:0a:0b:0c:0d:0e:0f.
  Client sends DISCOVER message.

  Pass Criteria:
  Server MUST respond with OFFER message.
  Response MUST contain yiaddr 192.0.2.205.
  Response MUST include option 6.
  Response option 6 MUST contain value 10.1.1.203.
  Response option 6 MUST contain value 10.1.1.202.
  Response MUST contain sname hal9000.
  Response MUST contain file /dev/null.

  Test Procedure:
  Client copies server_id option from received message.
  Client adds to the message requested_addr with value 192.0.2.205.
  Client adds to the message client_id with value 01:0a:0b:0c:0d:0e:0f.
  Client sets chaddr value to 01:0a:0b:0c:0d:0e:0f.
  Client sends REQUEST message.

  Pass Criteria:
  Server MUST respond with ACK message.
  Response MUST contain yiaddr 192.0.2.205.
  Response MUST include option 6.
  Response option 6 MUST contain value 10.1.1.203.
  Response option 6 MUST contain value 10.1.1.202.
  Response MUST contain sname hal9000.
  Response MUST contain file /dev/null.