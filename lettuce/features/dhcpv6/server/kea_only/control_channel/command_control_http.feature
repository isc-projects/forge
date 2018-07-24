Feature: Kea Control Channel Agent - HTTP
  Tests for Kea Command Control Channel Agent using unix socket to pass commands and HTTP based connection.

@v6 @controlchannel @kea_only
  Scenario: control.channel.http.dhcp-disable-timer
  Test Setup:
  Server is configured with 3000::/64 subnet with 3000::1-3000::f pool.
  Server has control channel on unix socket with name $(SOFTWARE_INSTALL_DIR)var/kea/control_socket.
  Server has control agent configured on HTTP connection with address $(SRV4_ADDR):8000 and socket unix path: $(SOFTWARE_INSTALL_DIR)var/kea/control_socket.
  Send server configuration using SSH and config-file.

  DHCP server is started.

  Test Procedure:
  Client sets DUID value to 00:03:00:01:66:55:44:33:22:11.
  Client does include client-id.
  Client does include IA_Address.
  Client does include IA-NA.
  Client sends SOLICIT message.

  Pass Criteria:
  Server MUST respond with ADVERTISE message.
  Response MUST include option 1.
  Response MUST include option 2.
  Response MUST include option 3.
  Response option 3 MUST contain sub-option 5.
  Response sub-option 5 from option 3 MUST contain address 3000::1.

  Using existing HTTP $(SRV4_ADDR):8000 connection send: {"command": "dhcp-disable","service": ["dhcp6"], "arguments": {"max-period": 5}}

  Test Procedure:
  Client sets DUID value to 00:03:00:01:66:55:44:33:22:11.
  Client does include client-id.
  Client does include IA_Address.
  Client does include IA-NA.
  Client sends SOLICIT message.

  Pass Criteria:
  Server MUST NOT respond.

  Sleep for 7 seconds.

  Test Procedure:
  Client sets DUID value to 00:03:00:01:66:55:44:33:22:11.
  Client does include client-id.
  Client does include IA_Address.
  Client does include IA-NA.
  Client sends SOLICIT message.

  Pass Criteria:
  Server MUST respond with ADVERTISE message.
  Response MUST include option 1.
  Response MUST include option 2.
  Response MUST include option 3.
  Response option 3 MUST contain sub-option 5.

@v6 @controlchannel @kea_only
  Scenario: control.channel.http.dhcp-disable
  Test Setup:
  Server is configured with 3000::/64 subnet with 3000::1-3000::f pool.
  Server has control channel on unix socket with name $(SOFTWARE_INSTALL_DIR)var/kea/control_socket.
  Server has control agent configured on HTTP connection with address $(SRV4_ADDR):8000 and socket unix path: $(SOFTWARE_INSTALL_DIR)var/kea/control_socket.
  Send server configuration using SSH and config-file.

  DHCP server is started.

  Test Procedure:
  Client sets DUID value to 00:03:00:01:66:55:44:33:22:11.
  Client does include client-id.
  Client does include IA_Address.
  Client does include IA-NA.
  Client sends SOLICIT message.

  Pass Criteria:
  Server MUST respond with ADVERTISE message.
  Response MUST include option 1.
  Response MUST include option 2.
  Response MUST include option 3.
  Response option 3 MUST contain sub-option 5.
  Response sub-option 5 from option 3 MUST contain address 3000::1.

  Using existing HTTP $(SRV4_ADDR):8000 connection send: {"command": "dhcp-disable","service": ["dhcp6"]}

  Test Procedure:
  Client sets DUID value to 00:03:00:01:66:55:44:33:22:11.
  Client does include client-id.
  Client does include IA_Address.
  Client does include IA-NA.
  Client sends SOLICIT message.

  Pass Criteria:
  Server MUST NOT respond.

@v6 @controlchannel @kea_only
  Scenario: control.channel.http.dhcp-disable-and-enable
  Test Setup:
  Server is configured with 3000::/64 subnet with 3000::1-3000::f pool.
  Server has control channel on unix socket with name $(SOFTWARE_INSTALL_DIR)var/kea/control_socket.
  Server has control agent configured on HTTP connection with address $(SRV4_ADDR):8000 and socket unix path: $(SOFTWARE_INSTALL_DIR)var/kea/control_socket.
  Send server configuration using SSH and config-file.

  DHCP server is started.

  Test Procedure:
  Client sets DUID value to 00:03:00:01:66:55:44:33:22:11.
  Client does include client-id.
  Client does include IA_Address.
  Client does include IA-NA.
  Client sends SOLICIT message.

  Pass Criteria:
  Server MUST respond with ADVERTISE message.
  Response MUST include option 1.
  Response MUST include option 2.
  Response MUST include option 3.
  Response option 3 MUST contain sub-option 5.
  Response sub-option 5 from option 3 MUST contain address 3000::1.

  Using existing HTTP $(SRV4_ADDR):8000 connection send: {"command": "dhcp-disable","service": ["dhcp6"]}

  Test Procedure:
  Client sets DUID value to 00:03:00:01:66:55:44:33:22:11.
  Client does include client-id.
  Client does include IA_Address.
  Client does include IA-NA.
  Client sends SOLICIT message.

  Pass Criteria:
  Server MUST NOT respond.

  Using existing HTTP $(SRV4_ADDR):8000 connection send: {"command": "dhcp-enable","service": ["dhcp6"]}

  Test Procedure:
  Client sets DUID value to 00:03:00:01:66:55:44:33:22:11.
  Client does include client-id.
  Client does include IA_Address.
  Client does include IA-NA.
  Client sends SOLICIT message.

  Pass Criteria:
  Server MUST respond with ADVERTISE message.
  Response MUST include option 1.
  Response MUST include option 2.
  Response MUST include option 3.
  Response option 3 MUST contain sub-option 5.

@v6 @controlchannel @kea_only
  Scenario: control.channel.http.config-set-basic
  Test Setup:
  Server is configured with 3000::/64 subnet with 3000::1-3000::f pool.
  Server has control channel on unix socket with name $(SOFTWARE_INSTALL_DIR)var/kea/control_socket.
  Server has control agent configured on HTTP connection with address $(SRV4_ADDR):8000 and socket unix path: $(SOFTWARE_INSTALL_DIR)var/kea/control_socket.
  Send server configuration using SSH and config-file.

  DHCP server is started.

  Test Procedure:
  Client sets DUID value to 00:03:00:01:66:55:44:33:22:11.
  Client does include client-id.
  Client does include IA_Address.
  Client does include IA-NA.
  Client sends SOLICIT message.

  Pass Criteria:
  Server MUST respond with ADVERTISE message.
  Response MUST include option 1.
  Response MUST include option 2.
  Response MUST include option 3.
  Response option 3 MUST contain sub-option 5.
  Response sub-option 5 from option 3 MUST contain address 3000::1.

  Test Setup:
  Server is configured with 2001:db8:1::/64 subnet with 2001:db8:1::1-2001:db8:1::1 pool.
  #Server has control agent configured on HTTP connection with address $(SRV4_ADDR):8000 and socket unix path: $(SOFTWARE_INSTALL_DIR)var/kea/control_socket.
  Generate server configuration file.

  Using existing HTTP $(SRV4_ADDR):8000 connection send: {"command": "config-set", "service": ["dhcp6"], "arguments":  $(SERVER_CONFIG) }
  
  Sleep for $(SLEEP_TIME_2) seconds.
  Test Procedure:
  Client sets DUID value to 00:03:00:01:66:55:44:33:22:11.
  Client does include client-id.
  Client does include IA_Address.
  Client does include IA-NA.
  Client sends SOLICIT message.

  Pass Criteria:
  Server MUST respond with ADVERTISE message.
  Response MUST include option 1.
  Response MUST include option 2.
  Response MUST include option 3.
  Response option 3 MUST contain sub-option 5.
  Response sub-option 5 from option 3 MUST contain address 2001:db8:1::1.

@v6 @controlchannel @kea_only
  Scenario: control.channel.http.change-socket-during-reconfigure
  #change address test needed also
  Test Setup:
  Server is configured with 3000::/64 subnet with 3000::1-3000::f pool.
  Add hooks library located $(SOFTWARE_INSTALL_DIR)lib/hooks/libdhcp_host_cmds.so.
  Server has control channel on unix socket with name $(SOFTWARE_INSTALL_DIR)var/kea/control_socket.
  Server has control agent configured on HTTP connection with address $(SRV4_ADDR):8000 and socket unix path: $(SOFTWARE_INSTALL_DIR)var/kea/control_socket.
  Send server configuration using SSH and config-file.
  DHCP server is started.

  Test Procedure:
  Client sets DUID value to 00:03:00:01:66:55:44:33:22:11.
  Client does include client-id.
  Client does include IA_Address.
  Client does include IA-NA.
  Client sends SOLICIT message.

  Pass Criteria:
  Server MUST respond with ADVERTISE message.
  Response MUST include option 1.
  Response MUST include option 2.
  Response MUST include option 3.
  Response option 3 MUST contain sub-option 5.
  Response sub-option 5 from option 3 MUST contain address 3000::1.

  Test Setup:
  Server is configured with 2001:db8:1::/64 subnet with 2001:db8:1::1-2001:db8:1::1 pool.
  Server has control channel on unix socket with name $(SOFTWARE_INSTALL_DIR)var/kea/control_socket.
  Server has control agent configured on HTTP connection with address $(SRV4_ADDR):8000 and socket unix path: $(SOFTWARE_INSTALL_DIR)var/kea/control_socket2.
  Generate server configuration file.

  Using existing HTTP $(SRV4_ADDR):8000 connection send: {"command": "config-set", "service": ["dhcp6"],"arguments":  $(SERVER_CONFIG) }
  Sleep for $(SLEEP_TIME_2) seconds.

  Test Procedure:
  Client sets DUID value to 00:03:00:01:66:55:44:33:22:11.
  Client does include client-id.
  Client does include IA_Address.
  Client does include IA-NA.
  Client sends SOLICIT message.

  Pass Criteria:
  Server MUST respond with ADVERTISE message.
  Response MUST include option 1.
  Response MUST include option 2.
  Response MUST include option 3.
  Response option 3 MUST contain sub-option 5.
  Response sub-option 5 from option 3 MUST contain address 2001:db8:1::1.
  Using existing HTTP $(SRV4_ADDR):8000 connection send: {"command":"list-commands","arguments": {} }

@v6 @controlchannel @kea_only
Scenario: control.channel.http.after-restart-load-config-file

  Test Setup:
  Server is configured with 3000::/64 subnet with 3000::1-3000::f pool.
  Server has control channel on unix socket with name $(SOFTWARE_INSTALL_DIR)var/kea/control_socket.
  Server has control agent configured on HTTP connection with address $(SRV4_ADDR):8000 and socket unix path: $(SOFTWARE_INSTALL_DIR)var/kea/control_socket.
  Send server configuration using SSH and config-file.
  DHCP server is started.

  Test Procedure:
  Client sets DUID value to 00:03:00:01:66:55:44:33:22:11.
  Client does include client-id.
  Client does include IA_Address.
  Client does include IA-NA.
  Client sends SOLICIT message.

  Pass Criteria:
  Server MUST respond with ADVERTISE message.
  Response MUST include option 1.
  Response MUST include option 2.
  Response MUST include option 3.
  Response option 3 MUST contain sub-option 5.
  Response sub-option 5 from option 3 MUST contain address 3000::1.

  Test Setup:
  Server is configured with 2001:db8:1::/64 subnet with 2001:db8:1::1-2001:db8:1::1 pool.
  Server has control agent configured on HTTP connection with address $(SRV4_ADDR):8000 and socket unix path: $(SOFTWARE_INSTALL_DIR)var/kea/control_socket.
  Generate server configuration file.

  Using existing HTTP $(SRV4_ADDR):8000 connection send: {"command": "config-set", "service": ["dhcp6"],"arguments":  $(SERVER_CONFIG) }

  Sleep for $(SLEEP_TIME_2) seconds.

  Test Procedure:
  Client sets DUID value to 00:03:00:01:66:55:44:33:22:11.
  Client does include client-id.
  Client does include IA_Address.
  Client does include IA-NA.
  Client sends SOLICIT message.

  Pass Criteria:
  Server MUST respond with ADVERTISE message.
  Response MUST include option 1.
  Response MUST include option 2.
  Response MUST include option 3.
  Response option 3 MUST contain sub-option 5.
  Response sub-option 5 from option 3 MUST contain address 2001:db8:1::1.

  DHCP server is restarted.

  Test Procedure:
  Client sets DUID value to 00:03:00:01:66:55:44:33:22:11.
  Client does include client-id.
  Client does include IA_Address.
  Client does include IA-NA.
  Client sends SOLICIT message.

  Pass Criteria:
  Server MUST respond with ADVERTISE message.
  Response MUST include option 1.
  Response MUST include option 2.
  Response MUST include option 3.
  Response option 3 MUST contain sub-option 5.
  Response sub-option 5 from option 3 MUST contain address 3000::1.

  
@v6 @controlchannel @kea_only
  Scenario: control.channel.http.get-config
  Test Setup:
  Server is configured with 3000::/64 subnet with 3000::1-3000::f pool.
  Server has control channel on unix socket with name $(SOFTWARE_INSTALL_DIR)var/kea/control_socket.
  Server has control agent configured on HTTP connection with address $(SRV4_ADDR):8000 and socket unix path: $(SOFTWARE_INSTALL_DIR)var/kea/control_socket.
  Send server configuration using SSH and config-file.

  DHCP server is started.

  Using existing HTTP $(SRV4_ADDR):8000 connection send: {"command": "config-get","service":["dhcp6"],"arguments": {} }


@v6 @controlchannel @kea_only
  Scenario: control.channel.http.test-config
  Test Setup:
  Server is configured with 3000::/64 subnet with 3000::1-3000::1 pool.
  Server has control channel on unix socket with name $(SOFTWARE_INSTALL_DIR)var/kea/control_socket.
  Server has control agent configured on HTTP connection with address $(SRV4_ADDR):8000 and socket unix path: $(SOFTWARE_INSTALL_DIR)var/kea/control_socket.
  Send server configuration using SSH and config-file.

  DHCP server is started.

  Test Procedure:
  Client sets DUID value to 00:03:00:01:66:55:44:33:22:11.
  Client does include client-id.
  Client does include IA_Address.
  Client does include IA-NA.
  Client sends SOLICIT message.

  Pass Criteria:
  Server MUST respond with ADVERTISE message.
  Response MUST include option 1.
  Response MUST include option 2.
  Response MUST include option 3.
  Response option 3 MUST contain sub-option 5.
  Response sub-option 5 from option 3 MUST contain address 3000::1.

  Test Setup:
  Server is configured with 2001:db8:a::/64 subnet with 2001:db8:a::1-2001:db8:a::1 pool.
  Server is configured with 2001:db8:1:: prefix in subnet 0 with 90 prefix length and 96 delegated prefix length.
  Server has control agent configured on HTTP connection with address $(SRV4_ADDR):8000 and socket unix path: $(SOFTWARE_INSTALL_DIR)var/kea/control_socket_ANOTHER_ONE.
  Server-id configured with type LLT value 00:01:00:02:52:7b:a8:f0:08:00:27:58:f1:e8.
  Server is configured with sip-server-addr option with value 2001:db8::1,2001:db8::2.
  Server is configured with new-posix-timezone option with value EST5EDT4\\,M3.2.0/02:00\\,M11.1.0/02:00.
  Reserve address 3000::1 in subnet 0 for host uniquely identified by duid 00:03:00:01:f6:f5:f4:f3:f2:01.
  Generate server configuration file.

  Using existing HTTP $(SRV4_ADDR):8000 connection send: {"command": "config-test","service": ["dhcp6"], "arguments":  $(SERVER_CONFIG) }

  Test Procedure:
  Client sets DUID value to 00:03:00:01:66:55:44:33:22:11.
  Client does include client-id.
  Client does include IA_Address.
  Client does include IA-NA.
  Client sends SOLICIT message.

  Pass Criteria:
  Server MUST respond with ADVERTISE message.
  Response MUST include option 1.
  Response MUST include option 2.
  Response MUST include option 3.
  Response option 3 MUST contain sub-option 5.
  Response sub-option 5 from option 3 MUST contain address 3000::1.

  Test Setup:
  Server is configured with 2001:db8:a::/64 subnet with 2001:db8:a::1-2001:db8:a::1 pool.
  Server is configured with 2001:db8:1:: prefix in subnet 0 with 90 prefix length and 96 delegated prefix length.
  Server has control agent configured on HTTP connection with address $(SRV4_ADDR):8000 and socket unix path: $(SOFTWARE_INSTALL_DIR)var/kea/control_socket_ANOTHER_ONE.
  Server-id configured with type LLT value 00:01:00:02:52:7b:a8:f0:08:00:27:58:f1:e8.
  Server is configured with sip-server-addr option with value 2001:db8::1,2001:db8::2.
  Server is configured with new-posix-timezone option with value EST5EDT4\\,M3.2.0/02:00\\,M11.1.0/02:00.
  # WRONG ADDRESS RESERVATION
  Reserve address 192.168.0.5 in subnet 0 for host uniquely identified by duid 00:03:00:01:f6:f5:f4:f3:f2:01.
  Generate server configuration file.

  Using existing HTTP $(SRV4_ADDR):8000 connection send: {"command": "config-test","service": ["dhcp6"], "arguments":  $(SERVER_CONFIG) }

  Test Procedure:
  Client sets DUID value to 00:03:00:01:66:55:44:33:22:11.
  Client does include client-id.
  Client does include IA_Address.
  Client does include IA-NA.
  Client sends SOLICIT message.

  Pass Criteria:
  Server MUST respond with ADVERTISE message.
  Response MUST include option 1.
  Response MUST include option 2.
  Response MUST include option 3.
  Response option 3 MUST contain sub-option 5.
  Response sub-option 5 from option 3 MUST contain address 3000::1.

@v6 @controlchannel @kea_only
Scenario: control.channel.http.config-write

  Test Setup:
  Server is configured with 3000::/64 subnet with 3000::1-3000::f pool.
  Server has control channel on unix socket with name $(SOFTWARE_INSTALL_DIR)var/kea/control_socket.
  Server has control agent configured on HTTP connection with address $(SRV4_ADDR):8000 and socket unix path: $(SOFTWARE_INSTALL_DIR)var/kea/control_socket.
  Send server configuration using SSH and config-file.
  DHCP server is started.

  Using existing HTTP $(SRV4_ADDR):8000 connection send: {"command": "list-commands", "service": ["dhcp6"],"arguments": {} }
  Using existing HTTP $(SRV4_ADDR):8000 connection send: {"command": "config-write", "service": ["dhcp6"],"arguments": {"filename": "config-modified-2017-03-15.json"} } #TODO probably confing file location/name

  Test Procedure:
  Client sets DUID value to 00:03:00:01:66:55:44:33:22:11.
  Client does include client-id.
  Client does include IA_Address.
  Client does include IA-NA.
  Client sends SOLICIT message.

  Pass Criteria:
  Server MUST respond with ADVERTISE message.
  Response MUST include option 1.
  Response MUST include option 2.
  Response option 3 MUST contain sub-option 5.
  Response sub-option 5 from option 3 MUST contain address 3000::1.

  Test Setup:
  Server is configured with 2001:db8:1::/64 subnet with 2001:db8:1::1-2001:db8:1::1 pool.
  Server has control agent configured on HTTP connection with address $(SRV4_ADDR):8000 and socket unix path: $(SOFTWARE_INSTALL_DIR)var/kea/control_socket.
  Generate server configuration file.

  Using unix socket on server in path $(SOFTWARE_INSTALL_DIR)var/kea/control_socket send {"command": "config-set", "service": ["dhcp6"],"arguments":  $(SERVER_CONFIG) }

  Sleep for $(SLEEP_TIME_2) seconds.

  Test Procedure:
  Client sets DUID value to 00:03:00:01:66:55:44:33:22:11.
  Client does include client-id.
  Client does include IA_Address.
  Client does include IA-NA.
  Client sends SOLICIT message.

  Pass Criteria:
  Server MUST respond with ADVERTISE message.
  Response MUST include option 1.
  Response MUST include option 2.
  Response MUST include option 3.
  Response option 3 MUST contain sub-option 5.
  Response sub-option 5 from option 3 MUST contain address 2001:db8:1::1.

  DHCP server is restarted.

  Test Procedure:
  Client sets DUID value to 00:03:00:01:66:55:44:33:22:11.
  Client does include client-id.
  Client does include IA_Address.
  Client does include IA-NA.
  Client sends SOLICIT message.

  Pass Criteria:
  Server MUST respond with ADVERTISE message.
  Response MUST include option 1.
  Response MUST include option 2.
  Response MUST include option 3.
  Response option 3 MUST contain sub-option 5.
  Response sub-option 5 from option 3 MUST contain address 3000::1.

@v6 @controlchannel @kea_only
Scenario: control.channel.http.reload-config

  Test Setup:
  Server is configured with 3000::/64 subnet with 3000::1-3000::f pool.
  Server has control channel on unix socket with name $(SOFTWARE_INSTALL_DIR)var/kea/control_socket.
  Server has control agent configured on HTTP connection with address $(SRV4_ADDR):8000 and socket unix path: $(SOFTWARE_INSTALL_DIR)var/kea/control_socket.
  Send server configuration using SSH and config-file.
  DHCP server is started.

  Test Procedure:
  Client sets DUID value to 00:03:00:01:66:55:44:33:22:11.
  Client does include client-id.
  Client does include IA_Address.
  Client does include IA-NA.
  Client sends SOLICIT message.

  Pass Criteria:
  Server MUST respond with ADVERTISE message.
  Response MUST include option 1.
  Response MUST include option 2.
  Response MUST include option 3.
  Response option 3 MUST contain sub-option 5.
  Response sub-option 5 from option 3 MUST contain address 3000::1.

  Test Setup:
  Server is configured with 2001:db8:1::/64 subnet with 2001:db8:1::1-2001:db8:1::1 pool.
  Server has control channel on unix socket with name $(SOFTWARE_INSTALL_DIR)var/kea/control_socket.
  Server has control agent configured on HTTP connection with address $(SRV4_ADDR):8000 and socket unix path: $(SOFTWARE_INSTALL_DIR)var/kea/control_socket.
  Send server configuration using SSH and config-file.

  Using existing HTTP $(SRV4_ADDR):8000 connection send: {"command":"config-reload","service":["dhcp6"],"arguments":{}}

  Test Procedure:
  Client sets DUID value to 00:03:00:01:66:55:44:33:22:11.
  Client does include client-id.
  Client does include IA_Address.
  Client does include IA-NA.
  Client sends SOLICIT message.

  Pass Criteria:
  Server MUST respond with ADVERTISE message.
  Response MUST include option 1.
  Response MUST include option 2.
  Response MUST include option 3.
  Response option 3 MUST contain sub-option 5.
  Response sub-option 5 from option 3 MUST contain address 2001:db8:1::1.

  DHCP server is restarted.

  Test Procedure:
  Client sets DUID value to 00:03:00:01:66:55:44:33:22:11.
  Client does include client-id.
  Client does include IA_Address.
  Client does include IA-NA.
  Client sends SOLICIT message.

  Pass Criteria:
  Server MUST respond with ADVERTISE message.
  Response MUST include option 1.
  Response MUST include option 2.
  Response MUST include option 3.
  Response option 3 MUST contain sub-option 5.
  Response sub-option 5 from option 3 MUST contain address 2001:db8:1::1.