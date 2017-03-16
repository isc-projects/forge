Feature: Kea Control Channel Script
  Tests for kea-shell. Script that handle command control channel commands using HTTP connection.

@v6 @controlchannel
  Scenario: control.channel.keashell.set-config-basic
  Test Setup:
  Server is configured with 3000::/64 subnet with 3000::1-3000::f pool.
  Server has control agent configred on HTTP connection with address localhost:8000 and socket UNIX path: $(SOFTWARE_INSTALL_DIR)var/kea/control_socket.
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
  Response sub-option 5 from option 3 MUST contain address 3000::1.

  Test Setup:
  Server is configured with 2001:db8:1::/64 subnet with 2001:db8:1::1-2001:db8:1::1 pool.
  Server has control agent configred on HTTP connection with address localhost:8000 and socket UNIX path: $(SOFTWARE_INSTALL_DIR)var/kea/control_socket.
  Generate server configuration file.

  Execute python script in path: $(SOFTWARE_INSTALL_DIR)sbin/kea-shell with arguments: --host localhost --port 8000 set-config < $(SERVER_CONFIG)

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

@v6 @controlchannel
  Scenario: control.channel.keashell.change-socket-during-reconfigure
  #change address test needed also
  Test Setup:
  Server is configured with 3000::/64 subnet with 3000::1-3000::f pool.
  Server has control agent configred on HTTP connection with address localhost:8000 and socket UNIX path: $(SOFTWARE_INSTALL_DIR)var/kea/control_socket.
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
  Response sub-option 5 from option 3 MUST contain address 3000::1.

  Test Setup:
  Server is configured with 2001:db8:1::/64 subnet with 2001:db8:1::1-2001:db8:1::1 pool.
  Server has control agent configred on HTTP connection with address localhost:8000 and socket UNIX path: $(SOFTWARE_INSTALL_DIR)var/kea/control_socket2.
  Generate server configuration file.

  Execute python script in path: $(SOFTWARE_INSTALL_DIR)sbin/kea-shell with arguments: --host localhost --port 8000 set-config < $(SERVER_CONFIG)

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
  Using existing HTTP localhost:8000 connection send: {"command":"list-commands","arguments": {} }

@v6 @controlchannel
Scenario: control.channel.keashell.after-restart-load-config-file

  Test Setup:
  Server is configured with 3000::/64 subnet with 3000::1-3000::f pool.
  Server has control agent configred on HTTP connection with address localhost:8000 and socket UNIX path: $(SOFTWARE_INSTALL_DIR)var/kea/control_socket.
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
  Response sub-option 5 from option 3 MUST contain address 3000::1.

  Test Setup:
  Server is configured with 2001:db8:1::/64 subnet with 2001:db8:1::1-2001:db8:1::1 pool.
  Server has control agent configred on HTTP connection with address localhost:8000 and socket UNIX path: $(SOFTWARE_INSTALL_DIR)var/kea/control_socket.
  Generate server configuration file.

  Execute python script in path: $(SOFTWARE_INSTALL_DIR)sbin/kea-shell with arguments: --host localhost --port 8000 set-config < $(SERVER_CONFIG)

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

  Restart DHCP server.

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
  Response sub-option 5 from option 3 MUST contain address 3000::1.

  
@v6 @controlchannel
  Scenario: control.channel.keashell.get-config
  Test Setup:
  Server is configured with 3000::/64 subnet with 3000::1-3000::f pool.
  Server has control agent configred on HTTP connection with address 192.168.0.1:8000 and socket UNIX path: $(SOFTWARE_INSTALL_DIR)var/kea/control_socket.
  Send server configuration using SSH and config-file.

  DHCP server is started.

  Using existing HTTP localhost:8000 connection send: {"command": "get-config","arguments": {} }


@v6 @controlchannel
  Scenario: control.channel.keashell.test-config
  Test Setup:
  Server is configured with 3000::/64 subnet with 3000::1-3000::f pool.
  Server has control agent configred on HTTP connection with address localhost:8000 and socket UNIX path: $(SOFTWARE_INSTALL_DIR)var/kea/control_socket.
  Send server configuration using SSH and config-file.

  DHCP server is started.

  Test Setup:
  Server is configured with 3000::/64 subnet with 3000::1-3000::f pool.
  Server is configured with 2001:db8:1:: prefix in subnet 0 with 90 prefix length and 96 delegated prefix length.
  Server has control agent configred on HTTP connection with address localhost:8000 and socket UNIX path: $(SOFTWARE_INSTALL_DIR)var/kea/control_socket_ANOTHER_ONE.
  Server-id configured with type LLT value 00:01:00:02:52:7b:a8:f0:08:00:27:58:f1:e8.
  Server is configured with sip-server-addr option with value 2001:db8::1,2001:db8::2.
  Server is configured with new-posix-timezone option with value EST5EDT4\\,M3.2.0/02:00\\,M11.1.0/02:00.
  Reserve address 3000::1 in subnet 0 for host uniquely identified by duid 00:03:00:01:f6:f5:f4:f3:f2:01.
  Generate server configuration file.

  Execute python script in path: $(SOFTWARE_INSTALL_DIR)sbin/kea-shell with arguments: --host localhost --port 8000 test-config < $(SERVER_CONFIG)
  #should be ok

  Test Setup:
  Server is configured with 3000::/64 subnet with 3000::1-3000::f pool.
  Server is configured with 2001:db8:1:: prefix in subnet 0 with 90 prefix length and 96 delegated prefix length.
  Server has control agent configred on HTTP connection with address localhost:8000 and socket UNIX path: $(SOFTWARE_INSTALL_DIR)var/kea/control_socket_ANOTHER_ONE.
  Server-id configured with type LLT value 00:01:00:02:52:7b:a8:f0:08:00:27:58:f1:e8.
  Server is configured with sip-server-addr option with value 2001:db8::1,2001:db8::2.
  Server is configured with new-posix-timezone option with value EST5EDT4\\,M3.2.0/02:00\\,M11.1.0/02:00.
  # WRONG ADDRESS RESERVATION
  Reserve address 192.168.0.5 in subnet 0 for host uniquely identified by duid 00:03:00:01:f6:f5:f4:f3:f2:01.
  Generate server configuration file.

  Execute python script in path: $(SOFTWARE_INSTALL_DIR)sbin/kea-shell with arguments: --host localhost --port 8000 test-config < $(SERVER_CONFIG)
  #should NOT be ok

@v6 @controlchannel
Scenario: control.channel.keashell.write-config

  Test Setup:
  Server is configured with 3000::/64 subnet with 3000::1-3000::f pool.
  Server has control agent configred on HTTP connection with address localhost:8000 and socket UNIX path: $(SOFTWARE_INSTALL_DIR)var/kea/control_socket.
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
  Response option 3 MUST contain sub-option 5.
  Response sub-option 5 from option 3 MUST contain address 3000::1.

  Test Setup:
  Server is configured with 2001:db8:1::/64 subnet with 2001:db8:1::1-2001:db8:1::1 pool.
  Server has control agent configred on HTTP connection with address localhost:8000 and socket UNIX path: $(SOFTWARE_INSTALL_DIR)var/kea/control_socket.
  Generate server configuration file.

  Execute python script in path: $(SOFTWARE_INSTALL_DIR)sbin/kea-shell with arguments: --host localhost --port 8000 set-config < $(SERVER_CONFIG)

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

  Execute python script in path: $(SOFTWARE_INSTALL_DIR)sbin/kea-shell with arguments: --host localhost --port 8000 write-config

  #tests needed for not valid/not permited paths

  Restart DHCP server.

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