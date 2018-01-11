Feature: Kea Control Channel - socket
  Tests for Kea Command Control Channel using unix socket to pass commands.

@v6 @controlchannel @kea_only
  Scenario: control.channel.socket.config-get
  Test Setup:
  Server is configured with 3000::/64 subnet with 3000::1-3000::f pool.
  Server has control channel on unix socket with name $(SOFTWARE_INSTALL_DIR)var/kea/control_socket.

  Send server configuration using SSH and config-file.

  DHCP server is started.

  Using UNIX socket on server in path $(SOFTWARE_INSTALL_DIR)var/kea/control_socket send {"command": "config-get","arguments": {}}
  #Using UNIX socket on server in path $(SOFTWARE_INSTALL_DIR)var/kea/control_socket send {"command": "list-commands","arguments": {}}
  #compare json result with config file

@v6 @controlchannel @kea_only
  Scenario: control.channel.socket.config-test
  Test Setup:
  Server is configured with 3000::/64 subnet with 3000::1-3000::f pool.
  Server has control channel on unix socket with name $(SOFTWARE_INSTALL_DIR)var/kea/control_socket.
    #To global section of the config add file line: "expired-leases-processing":{"flush-reclaimed-timer-wait-time": 0,"hold-reclaimed-time": 0,"max-reclaim-leases": 100,"max-reclaim-time": 0,"reclaim-timer-wait-time": 0,"unwarned-reclaim-cycles": 5}
    #To global section of the config add file line: "expired-leases-processing":{"flush-reclaimed-timer-wait-time": 0,"hold-reclaimed-time": 0,"max-reclaim-leases": 100,"max-reclaim-time": 0,"reclaim-timer-wait-time": 0,"unwarned-reclaim-cycles": 5}


  Send server configuration using SSH and config-file.

  DHCP server is started.

  Test Setup:
  Server is configured with 3000::/64 subnet with 3000::1-3000::f pool.
  Server is configured with 2001:db8:1:: prefix in subnet 0 with 90 prefix length and 96 delegated prefix length.
  Server has control channel on unix socket with name $(SOFTWARE_INSTALL_DIR)var/kea/control_socket_ANOTHER_ONE.
  Server-id configured with type LLT value 00:01:00:02:52:7b:a8:f0:08:00:27:58:f1:e8.
  Server is configured with sip-server-addr option with value 2001:db8::1,2001:db8::2.
  Server is configured with new-posix-timezone option with value EST5EDT4\\,M3.2.0/02:00\\,M11.1.0/02:00.
  Reserve address 3000::1 in subnet 0 for host uniquely identified by duid 00:03:00:01:f6:f5:f4:f3:f2:01.
  Generate server configuration file.

  #Sleep for 10 seconds.
  Using UNIX socket on server in path $(SOFTWARE_INSTALL_DIR)var/kea/control_socket send {"command": "config-test","arguments": $(SERVER_CONFIG) }
  #should be ok

  Test Setup:
  Server is configured with 3000::/64 subnet with 3000::1-3000::f pool.
  Server is configured with 2001:db8:1:: prefix in subnet 0 with 90 prefix length and 96 delegated prefix length.
  Server has control channel on unix socket with name $(SOFTWARE_INSTALL_DIR)var/kea/control_socket_ANOTHER_ONE.
  Server-id configured with type LLT value 00:01:00:02:52:7b:a8:f0:08:00:27:58:f1:e8.
  Server is configured with sip-server-addr option with value 2001:db8::1,2001:db8::2.
  Server is configured with new-posix-timezone option with value EST5EDT4\\,M3.2.0/02:00\\,M11.1.0/02:00.
  # WRONG ADDRESS RESERVATION
  Reserve address 192.168.0.5 in subnet 0 for host uniquely identified by duid 00:03:00:01:f6:f5:f4:f3:f2:01.
  Generate server configuration file.
#
  Using UNIX socket on server in path $(SOFTWARE_INSTALL_DIR)var/kea/control_socket send {"command": "config-test","arguments": $(SERVER_CONFIG) }
#  #should NOT be ok

@v6 @controlchannel @kea_only
Scenario: control.channel.socket.config-write

  Test Setup:
  Server is configured with 3000::/64 subnet with 3000::1-3000::f pool.
  Server has control channel on unix socket with name $(SOFTWARE_INSTALL_DIR)var/kea/control_socket.
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
  Server has control channel on unix socket with name $(SOFTWARE_INSTALL_DIR)var/kea/control_socket.
  Generate server configuration file.

  Using UNIX socket on server in path $(SOFTWARE_INSTALL_DIR)var/kea/control_socket send {"command": "config-set","arguments":  $(SERVER_CONFIG) }
  Using UNIX socket on server in path $(SOFTWARE_INSTALL_DIR)var/kea/control_socket send {"command": "config-write","arguments":  { "filename": "$(SOFTWARE_INSTALL_DIR)etc/kea/kea.conf"} }

  Test Procedure:
  Client sets DUID value to 00:03:00:01:66:55:44:33:22:22.
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

  #Using UNIX socket on server in path $(SOFTWARE_INSTALL_DIR)var/kea/control_socket send {"command": "list-commands","arguments": {}}
  #Using UNIX socket on server in path $(SOFTWARE_INSTALL_DIR)var/kea/control_socket send {"command": "config-write","parameters":  { "filename": "abc"} }
  #Using UNIX socket on server in path $(SOFTWARE_INSTALL_DIR)var/kea/control_socket send {"command": "config-write","arguments":  { "filename": "whatever"} }
#Using UNIX socket on server in path $(SOFTWARE_INSTALL_DIR)var/kea/control_socket send {"command": "config-write","arguments":  { "filename": "installed/git/etc/kea/kea.conf"} }
 # Pause the Test.
  Restart DHCP server.

  Test Procedure:
  Client sets DUID value to 00:03:00:01:66:55:44:33:22:33.
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

@v6 @controlchannel @kea_only
Scenario: control.channel.socket.config-reload

  Test Setup:
  Server is configured with 3000::/64 subnet with 3000::1-3000::f pool.
  Server has control channel on unix socket with name $(SOFTWARE_INSTALL_DIR)var/kea/control_socket.
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

  Using UNIX socket on server in path $(SOFTWARE_INSTALL_DIR)var/kea/control_socket send {"command": "list-commands","arguments": {}}

  Test Setup:
  Server is configured with 2001:db8:1::/64 subnet with 2001:db8:1::1-2001:db8:1::1 pool.
  Server has control channel on unix socket with name $(SOFTWARE_INSTALL_DIR)var/kea/control_socket.
  #Generate server configuration file.
  Send server configuration using SSH and config-file.

  Using UNIX socket on server in path $(SOFTWARE_INSTALL_DIR)var/kea/control_socket send {"command": "config-reload","arguments":  {} }

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
  Response MUST include option 3.w
  Response option 3 MUST contain sub-option 5.
  Response sub-option 5 from option 3 MUST contain address 2001:db8:1::1.