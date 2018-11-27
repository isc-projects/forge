Feature: Kea Control Channel Script
  Tests for kea-shell. Script that handle command control channel commands using HTTP connection.

@v6 @controlchannel @kea_onlyn
  Scenario: control.channel.keashell.dhcp-disable-timer
  Test Setup:
  Server is configured with 3000::/64 subnet with 3000::1-3000::f pool.
  Server has control channel on unix socket with name $(SOFTWARE_INSTALL_DIR)/var/kea/control_socket.
  Server has control agent configured on HTTP connection with address 127.0.0.1:8000 and socket unix path: $(SOFTWARE_INSTALL_DIR)/var/kea/control_socket.
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

  Execute python script in path: $(SOFTWARE_INSTALL_DIR)/sbin/kea-shell with arguments: --host 127.0.0.1 --port 8000 --service dhcp6 dhcp-disable <<<'"max-period": 5'

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
  Scenario: control.channel.keashell.dhcp-disable
  Test Setup:
  Server is configured with 3000::/64 subnet with 3000::1-3000::f pool.
  Server has control channel on unix socket with name $(SOFTWARE_INSTALL_DIR)/var/kea/control_socket.
  Server has control agent configured on HTTP connection with address 127.0.0.1:8000 and socket unix path: $(SOFTWARE_INSTALL_DIR)/var/kea/control_socket.
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

  Execute python script in path: $(SOFTWARE_INSTALL_DIR)/sbin/kea-shell with arguments: --host 127.0.0.1 --port 8000 --service dhcp6 dhcp-disable <<<''

  Test Procedure:
  Client sets DUID value to 00:03:00:01:66:55:44:33:22:11.
  Client does include client-id.
  Client does include IA_Address.
  Client does include IA-NA.
  Client sends SOLICIT message.

  Pass Criteria:
  Server MUST NOT respond.

@v6 @controlchannel @kea_only
  Scenario: control.channel.keashell.dhcp-disable-and-enable
  Test Setup:
  Server is configured with 3000::/64 subnet with 3000::1-3000::f pool.
  Server has control channel on unix socket with name $(SOFTWARE_INSTALL_DIR)/var/kea/control_socket.
  Server has control agent configured on HTTP connection with address 127.0.0.1:8000 and socket unix path: $(SOFTWARE_INSTALL_DIR)/var/kea/control_socket.
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

  Execute python script in path: $(SOFTWARE_INSTALL_DIR)/sbin/kea-shell with arguments: --host 127.0.0.1 --port 8000 --service dhcp6 dhcp-disable <<<''

  Test Procedure:
  Client sets DUID value to 00:03:00:01:66:55:44:33:22:11.
  Client does include client-id.
  Client does include IA_Address.
  Client does include IA-NA.
  Client sends SOLICIT message.

  Pass Criteria:
  Server MUST NOT respond.
  Execute python script in path: $(SOFTWARE_INSTALL_DIR)/sbin/kea-shell with arguments: --host 127.0.0.1 --port 8000 --service dhcp6 dhcp-enable <<<''

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
  Scenario: control.channel.keashell.set-config-basic
  Test Setup:
  Server is configured with 3000::/64 subnet with 3000::1-3000::f pool.
  Server has control channel on unix socket with name $(SOFTWARE_INSTALL_DIR)/var/kea/control_socket.
  Server has control agent configured on HTTP connection with address 127.0.0.1:8000 and socket unix path: $(SOFTWARE_INSTALL_DIR)/var/kea/control_socket.
  Send server configuration using SSH and config-file.

  DHCP server is started.
  Sleep for 2 seconds.

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

  #this command is with new configuration
  Execute python script in path: $(SOFTWARE_INSTALL_DIR)/sbin/kea-shell with arguments: --host 127.0.0.1 --port 8000 --service dhcp6 config-set <<<'"Dhcp6": { "control-socket": { "socket-name": "$(SOFTWARE_INSTALL_DIR)/var/kea/control_socket", "socket-type": "unix" }, "decline-probation-period": 86400, "dhcp-ddns": { "always-include-fqdn": false, "enable-updates": false, "generated-prefix": "myhost", "max-queue-size": 1024, "ncr-format": "JSON", "ncr-protocol": "UDP", "override-client-update": false, "override-no-update": false, "qualifying-suffix": "", "replace-client-name": "never", "sender-ip": "0.0.0.0", "sender-port": 0, "server-ip": "127.0.0.1", "server-port": 53001 }, "dhcp4o6-port": 0, "expired-leases-processing": { "flush-reclaimed-timer-wait-time": 25, "hold-reclaimed-time": 3600, "max-reclaim-leases": 100, "max-reclaim-time": 250, "reclaim-timer-wait-time": 10, "unwarned-reclaim-cycles": 5 }, "hooks-libraries": [  ], "host-reservation-identifiers": [ "hw-address", "duid" ], "interfaces-config": { "interfaces": [ "$(SERVER_IFACE)" ], "re-detect": true }, "lease-database": { "type": "memfile" }, "mac-sources": [ "any" ], "option-data": [  ], "option-def": [  ], "relay-supplied-options": [ "65" ], "server-id": { "enterprise-id": 0, "htype": 0, "identifier": "", "persist": true, "time": 0, "type": "LLT" }, "shared-networks": [  ], "subnet6": [ { "id": 1, "interface": "$(SERVER_IFACE)", "option-data": [  ], "pd-pools": [  ], "pools": [ { "option-data": [  ], "pool": "2001:db8:1::1-2001:db8:1::1" } ], "preferred-lifetime": 3000, "rapid-commit": false, "rebind-timer": 2000, "relay": { "ip-address": "::" }, "renew-timer": 1000, "reservation-mode": "all", "reservations": [  ], "subnet": "2001:db8:1::/64", "valid-lifetime": 4000 } ] }'

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
Scenario: control.channel.keashell.after-restart-load-config-file

  Test Setup:
  Server is configured with 3000::/64 subnet with 3000::1-3000::f pool.
  Server has control channel on unix socket with name $(SOFTWARE_INSTALL_DIR)/var/kea/control_socket.
  Server has control agent configured on HTTP connection with address 127.0.0.1:8000 and socket unix path: $(SOFTWARE_INSTALL_DIR)/var/kea/control_socket.
  Send server configuration using SSH and config-file.
  DHCP server is started.
  Sleep for 2 seconds.

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

  Execute python script in path: $(SOFTWARE_INSTALL_DIR)/sbin/kea-shell with arguments: --host 127.0.0.1 --port 8000 --service dhcp6 config-set <<<'"Dhcp6": { "control-socket": { "socket-name": "$(SOFTWARE_INSTALL_DIR)/var/kea/control_socket", "socket-type": "unix" }, "decline-probation-period": 86400, "dhcp-ddns": { "always-include-fqdn": false, "enable-updates": false, "generated-prefix": "myhost", "max-queue-size": 1024, "ncr-format": "JSON", "ncr-protocol": "UDP", "override-client-update": false, "override-no-update": false, "qualifying-suffix": "", "replace-client-name": "never", "sender-ip": "0.0.0.0", "sender-port": 0, "server-ip": "127.0.0.1", "server-port": 53001 }, "dhcp4o6-port": 0, "expired-leases-processing": { "flush-reclaimed-timer-wait-time": 25, "hold-reclaimed-time": 3600, "max-reclaim-leases": 100, "max-reclaim-time": 250, "reclaim-timer-wait-time": 10, "unwarned-reclaim-cycles": 5 }, "hooks-libraries": [  ], "host-reservation-identifiers": [ "hw-address", "duid" ], "interfaces-config": { "interfaces": [ "$(SERVER_IFACE)" ], "re-detect": true }, "lease-database": { "type": "memfile" }, "mac-sources": [ "any" ], "option-data": [  ], "option-def": [  ], "relay-supplied-options": [ "65" ], "server-id": { "enterprise-id": 0, "htype": 0, "identifier": "", "persist": true, "time": 0, "type": "LLT" }, "shared-networks": [  ], "subnet6": [ { "id": 1, "interface": "$(SERVER_IFACE)", "option-data": [  ], "pd-pools": [  ], "pools": [ { "option-data": [  ], "pool": "2001:db8:1::1-2001:db8:1::1" } ], "preferred-lifetime": 3000, "rapid-commit": false, "rebind-timer": 2000, "relay": { "ip-address": "::" }, "renew-timer": 1000, "reservation-mode": "all", "reservations": [  ], "subnet": "2001:db8:1::/64", "valid-lifetime": 4000 } ] }'

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
  Scenario: control.channel.keashell.get-config
  Test Setup:
  Server is configured with 3000::/64 subnet with 3000::1-3000::f pool.
  Server has control channel on unix socket with name $(SOFTWARE_INSTALL_DIR)/var/kea/control_socket.
  Server has control agent configured on HTTP connection with address 127.0.0.1:8000 and socket unix path: $(SOFTWARE_INSTALL_DIR)/var/kea/control_socket.
  Send server configuration using SSH and config-file.

  DHCP server is started.

  Execute python script in path: $(SOFTWARE_INSTALL_DIR)/sbin/kea-shell with arguments: --host 127.0.0.1 --port 8000 --service dhcp6 config-get <<<''


@v6 @controlchannel @kea_only @disabled
  Scenario: control.channel.keashell.test-config
  Test Setup:
  Server is configured with 3000::/64 subnet with 3000::1-3000::1 pool.
  Server has control channel on unix socket with name $(SOFTWARE_INSTALL_DIR)/var/kea/control_socket.
  Server has control agent configured on HTTP connection with address 127.0.0.1:8000 and socket unix path: $(SOFTWARE_INSTALL_DIR)/var/kea/control_socket.
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
  Server has control agent configured on HTTP connection with address $(SRV4_ADDR):8000 and socket unix path: $(SOFTWARE_INSTALL_DIR)/var/kea/control_socket_ANOTHER_ONE.
  Server-id configured with type LLT value 00:01:00:02:52:7b:a8:f0:08:00:27:58:f1:e8.
  Server is configured with sip-server-addr option with value 2001:db8::1,2001:db8::2.
  Server is configured with new-posix-timezone option with value EST5EDT4\\,M3.2.0/02:00\\,M11.1.0/02:00.
  Reserve address 3000::1 in subnet 0 for host uniquely identified by duid 00:03:00:01:f6:f5:f4:f3:f2:01.
  Generate server configuration file.

  Execute python script in path: $(SOFTWARE_INSTALL_DIR)/sbin/kea-shell with arguments: --host 127.0.0.1 --port 8000 --service dhcp6 config-test <<<'$(SERVER_CONFIG)'

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
  Server has control agent configured on HTTP connection with address $(SRV4_ADDR):8000 and socket unix path: $(SOFTWARE_INSTALL_DIR)/var/kea/control_socket_ANOTHER_ONE.
  Server-id configured with type LLT value 00:01:00:02:52:7b:a8:f0:08:00:27:58:f1:e8.
  Server is configured with sip-server-addr option with value 2001:db8::1,2001:db8::2.
  Server is configured with new-posix-timezone option with value EST5EDT4\\,M3.2.0/02:00\\,M11.1.0/02:00.
  # WRONG ADDRESS RESERVATION
  Reserve address 192.168.0.5 in subnet 0 for host uniquely identified by duid 00:03:00:01:f6:f5:f4:f3:f2:01.
  Generate server configuration file.

  Execute python script in path: $(SOFTWARE_INSTALL_DIR)/sbin/kea-shell with arguments: --host 127.0.0.1 --port 8000 --service dhcp6 config-test <<<'$(SERVER_CONFIG)'
  Sleep for 5 seconds.

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
Scenario: control.channel.keashell.write-config

  Test Setup:
  Server is configured with 3000::/64 subnet with 3000::1-3000::1 pool.
  Server has control channel on unix socket with name $(SOFTWARE_INSTALL_DIR)/var/kea/control_socket.
  Server has control agent configured on HTTP connection with address 127.0.0.1:8000 and socket unix path: $(SOFTWARE_INSTALL_DIR)/var/kea/control_socket.
  Send server configuration using SSH and config-file.
  DHCP server is started.
  Sleep for 2 seconds.

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
  Server has control agent configured on HTTP connection with address localhost:8000 and socket UNIX path: $(SOFTWARE_INSTALL_DIR)/var/kea/control_socket.
  Generate server configuration file.

  Execute python script in path: $(SOFTWARE_INSTALL_DIR)/sbin/kea-shell with arguments: --host 127.0.0.1 --port 8000 --service dhcp6 config-set <<<'"Dhcp6": { "control-socket": { "socket-name": "$(SOFTWARE_INSTALL_DIR)/var/kea/control_socket", "socket-type": "unix" }, "decline-probation-period": 86400, "dhcp-ddns": { "always-include-fqdn": false, "enable-updates": false, "generated-prefix": "myhost", "max-queue-size": 1024, "ncr-format": "JSON", "ncr-protocol": "UDP", "override-client-update": false, "override-no-update": false, "qualifying-suffix": "", "replace-client-name": "never", "sender-ip": "0.0.0.0", "sender-port": 0, "server-ip": "127.0.0.1", "server-port": 53001 }, "dhcp4o6-port": 0, "expired-leases-processing": { "flush-reclaimed-timer-wait-time": 25, "hold-reclaimed-time": 3600, "max-reclaim-leases": 100, "max-reclaim-time": 250, "reclaim-timer-wait-time": 10, "unwarned-reclaim-cycles": 5 }, "hooks-libraries": [  ], "host-reservation-identifiers": [ "hw-address", "duid" ], "interfaces-config": { "interfaces": [ "$(SERVER_IFACE)" ], "re-detect": true }, "lease-database": { "type": "memfile" }, "mac-sources": [ "any" ], "option-data": [  ], "option-def": [  ], "relay-supplied-options": [ "65" ], "server-id": { "enterprise-id": 0, "htype": 0, "identifier": "", "persist": true, "time": 0, "type": "LLT" }, "shared-networks": [  ], "subnet6": [ { "id": 1, "interface": "$(SERVER_IFACE)", "option-data": [  ], "pd-pools": [  ], "pools": [ { "option-data": [  ], "pool": "2001:db8:1::1-2001:db8:1::1" } ], "preferred-lifetime": 3000, "rapid-commit": false, "rebind-timer": 2000, "relay": { "ip-address": "::" }, "renew-timer": 1000, "reservation-mode": "all", "reservations": [  ], "subnet": "2001:db8:1::/64", "valid-lifetime": 4000 } ] }'
  Sleep for 5 seconds.

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

  Execute python script in path: $(SOFTWARE_INSTALL_DIR)/sbin/kea-shell with arguments: --host 127.0.0.1 --port 8000 --service dhcp6 config-write <<<''
  Sleep for 5 seconds.
  #TODO tests needed for not valid/not permitted paths

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

@v6 @controlchannel @kea_only
Scenario: control.channel.socket.reload-config

  Test Setup:
  Server is configured with 3000::/64 subnet with 3000::1-3000::1 pool.
  Server has control channel on unix socket with name $(SOFTWARE_INSTALL_DIR)/var/kea/control_socket.
  Server has control agent configured on HTTP connection with address 127.0.0.1:8000 and socket unix path: $(SOFTWARE_INSTALL_DIR)/var/kea/control_socket.
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
  Server has control channel on unix socket with name $(SOFTWARE_INSTALL_DIR)/var/kea/control_socket.
  Server has control agent configured on HTTP connection with address 127.0.0.1:8000 and socket unix path: $(SOFTWARE_INSTALL_DIR)/var/kea/control_socket.
  Send server configuration using SSH and config-file.

  Execute python script in path: $(SOFTWARE_INSTALL_DIR)/sbin/kea-shell with arguments: --host 127.0.0.1 --port 8000 --service dhcp6 config-reload <<<''
  Sleep for 5 seconds.

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