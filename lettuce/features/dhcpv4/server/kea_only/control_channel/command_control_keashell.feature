Feature: Kea Control Channel Script
  Tests for kea-shell. Script that handle command control channel commands using HTTP connection.

@v4 @controlchannel @kea_only
  Scenario: control.channel.keashell.set-config-basic
  Test Setup:
  Server is configured with 192.168.50.0/24 subnet with 192.168.50.1-192.168.50.1 pool.
  Server has control channel on unix socket with name $(SOFTWARE_INSTALL_DIR)var/kea/control_socket.
  Server has control agent configured on HTTP connection with address 127.0.0.1:8000 and socket unix path: $(SOFTWARE_INSTALL_DIR)var/kea/control_socket.
  Send server configuration using SSH and config-file.

  DHCP server is started.

  Test Procedure:
  Client requests option 1.
  Client sends DISCOVER message.

  Pass Criteria:
  Server MUST respond with OFFER message.
  Response MUST include option 1.
  Response MUST contain yiaddr 192.168.50.1.
  Response option 1 MUST contain value 255.255.255.0.

  #this command is with new configuration
  Execute python script in path: $(SOFTWARE_INSTALL_DIR)sbin/kea-shell with arguments: --host 127.0.0.1 --port 8000 --service dhcp4 config-set <<<' "Dhcp4": { "control-socket": { "socket-name": "/home/test/installed/git/var/kea/control_socket", "socket-type": "unix" }, "decline-probation-period": 86400, "dhcp-ddns": { "always-include-fqdn": false, "enable-updates": false, "generated-prefix": "myhost", "max-queue-size": 1024, "ncr-format": "JSON", "ncr-protocol": "UDP", "override-client-update": false, "override-no-update": false, "qualifying-suffix": "", "replace-client-name": "never", "sender-ip": "0.0.0.0", "sender-port": 0, "server-ip": "127.0.0.1", "server-port": 53001 }, "dhcp4o6-port": 0, "echo-client-id": true, "expired-leases-processing": { "flush-reclaimed-timer-wait-time": 25, "hold-reclaimed-time": 3600, "max-reclaim-leases": 100, "max-reclaim-time": 250, "reclaim-timer-wait-time": 10, "unwarned-reclaim-cycles": 5 }, "hooks-libraries": [  ], "host-reservation-identifiers": [ "hw-address", "duid", "circuit-id", "client-id" ], "interfaces-config": { "interfaces": [ "eth2" ], "re-detect": true }, "lease-database": { "type": "memfile" }, "option-data": [  ], "option-def": [  ], "shared-networks": [  ], "subnet4": [ { "4o6-interface": "", "4o6-interface-id": "", "4o6-subnet": "", "boot-file-name": "", "id": 1, "interface": "eth2", "match-client-id": true, "next-server": "0.0.0.0", "option-data": [  ], "pools": [ { "option-data": [  ], "pool": "192.168.51.1/32" } ], "rebind-timer": 2000, "relay": { "ip-address": "0.0.0.0" }, "renew-timer": 1000, "reservation-mode": "all", "reservations": [  ], "server-hostname": "", "subnet": "192.168.51.0/24", "valid-lifetime": 4000 } ] }'

  Sleep for $(SLEEP_TIME_2) seconds.

  Test Procedure:
  Client requests option 1.
  Client sends DISCOVER message.

  Pass Criteria:
  Server MUST respond with OFFER message.
  Response MUST include option 1.
  Response MUST contain yiaddr 192.168.51.1.
  Response option 1 MUST contain value 255.255.255.0.


@v4 @controlchannel @kea_only
Scenario: control.channel.keashell.after-restart-load-config-file

  Test Setup:
  Server is configured with 192.168.50.0/24 subnet with 192.168.50.1-192.168.50.1 pool.
  Server has control channel on unix socket with name $(SOFTWARE_INSTALL_DIR)var/kea/control_socket.
  Server has control agent configured on HTTP connection with address 127.0.0.1:8000 and socket unix path: $(SOFTWARE_INSTALL_DIR)var/kea/control_socket.
  Send server configuration using SSH and config-file.
  DHCP server is started.

  Test Procedure:
  Client requests option 1.
  Client sends DISCOVER message.

  Pass Criteria:
  Server MUST respond with OFFER message.
  Response MUST include option 1.
  Response MUST contain yiaddr 192.168.50.1.
  Response option 1 MUST contain value 255.255.255.0.

  Execute python script in path: $(SOFTWARE_INSTALL_DIR)sbin/kea-shell with arguments: --host 127.0.0.1 --port 8000 --service dhcp4 config-set <<<' "Dhcp4": { "control-socket": { "socket-name": "/home/test/installed/git/var/kea/control_socket", "socket-type": "unix" }, "decline-probation-period": 86400, "dhcp-ddns": { "always-include-fqdn": false, "enable-updates": false, "generated-prefix": "myhost", "max-queue-size": 1024, "ncr-format": "JSON", "ncr-protocol": "UDP", "override-client-update": false, "override-no-update": false, "qualifying-suffix": "", "replace-client-name": "never", "sender-ip": "0.0.0.0", "sender-port": 0, "server-ip": "127.0.0.1", "server-port": 53001 }, "dhcp4o6-port": 0, "echo-client-id": true, "expired-leases-processing": { "flush-reclaimed-timer-wait-time": 25, "hold-reclaimed-time": 3600, "max-reclaim-leases": 100, "max-reclaim-time": 250, "reclaim-timer-wait-time": 10, "unwarned-reclaim-cycles": 5 }, "hooks-libraries": [  ], "host-reservation-identifiers": [ "hw-address", "duid", "circuit-id", "client-id" ], "interfaces-config": { "interfaces": [ "eth2" ], "re-detect": true }, "lease-database": { "type": "memfile" }, "option-data": [  ], "option-def": [  ], "shared-networks": [  ], "subnet4": [ { "4o6-interface": "", "4o6-interface-id": "", "4o6-subnet": "", "boot-file-name": "", "id": 1, "interface": "eth2", "match-client-id": true, "next-server": "0.0.0.0", "option-data": [  ], "pools": [ { "option-data": [  ], "pool": "192.168.51.1/32" } ], "rebind-timer": 2000, "relay": { "ip-address": "0.0.0.0" }, "renew-timer": 1000, "reservation-mode": "all", "reservations": [  ], "server-hostname": "", "subnet": "192.168.51.0/24", "valid-lifetime": 4000 } ] }'
  Sleep for $(SLEEP_TIME_2) seconds.

  Test Procedure:
  Client requests option 1.
  Client sends DISCOVER message.

  Pass Criteria:
  Server MUST respond with OFFER message.
  Response MUST include option 1.
  Response MUST contain yiaddr 192.168.51.1.
  Response option 1 MUST contain value 255.255.255.0.

  Restart DHCP server.

  Test Procedure:
  Client requests option 1.
  Client sends DISCOVER message.

  Pass Criteria:
  Server MUST respond with OFFER message.
  Response MUST include option 1.
  Response MUST contain yiaddr 192.168.50.1.
  Response option 1 MUST contain value 255.255.255.0.

  
@v4 @controlchannel @kea_only
  Scenario: control.channel.keashell.get-config
  Test Setup:
  Server is configured with 192.168.50.0/24 subnet with 192.168.50.1-192.168.50.1 pool.
  Server has control channel on unix socket with name $(SOFTWARE_INSTALL_DIR)var/kea/control_socket.
  Server has control agent configured on HTTP connection with address 127.0.0.1:8000 and socket unix path: $(SOFTWARE_INSTALL_DIR)var/kea/control_socket.
  Send server configuration using SSH and config-file.

  DHCP server is started.

  Execute python script in path: $(SOFTWARE_INSTALL_DIR)sbin/kea-shell with arguments: --host 127.0.0.1 --port 8000 --service dhcp4 config-get <<<''


@v4 @controlchannel @kea_only @disabled
  Scenario: control.channel.keashell.test-config
  Test Setup:
  Server is configured with 192.168.50.0/24 subnet with 192.168.50.1-192.168.50.1 pool.
  Server has control channel on unix socket with name $(SOFTWARE_INSTALL_DIR)var/kea/control_socket.
  Server has control agent configured on HTTP connection with address 127.0.0.1:8000 and socket unix path: $(SOFTWARE_INSTALL_DIR)var/kea/control_socket.
  Send server configuration using SSH and config-file.

  DHCP server is started.

  Test Procedure:
  Client requests option 1.
  Client sends DISCOVER message.

  Pass Criteria:
  Server MUST respond with OFFER message.
  Response MUST include option 1.
  Response MUST contain yiaddr 192.168.50.1.
  Response option 1 MUST contain value 255.255.255.0.

  Test Setup:
  Server is configured with 192.168.51.0/24 subnet with 192.168.51.1-192.168.51.1 pool.
  Server has control agent configured on HTTP connection with address $(SRV4_ADDR):8000 and socket unix path: $(SOFTWARE_INSTALL_DIR)var/kea/control_socket_ANOTHER_ONE.
  DDNS server is configured on 127.0.0.1 address and 53001 port.
  DDNS server is configured with enable-updates option set to true.
  DDNS server is configured with qualifying-suffix option set to my.domain.com.
  Reserve hostname reserved-name in subnet 0 for host uniquely identified by hw-address ff:01:02:03:ff:04.
  For host reservation entry no. 0 in subnet 0 add address with value 192.168.50.5.
  Generate server configuration file.

  Execute python script in path: $(SOFTWARE_INSTALL_DIR)sbin/kea-shell with arguments: --host 127.0.0.1 --port 8000 --service dhcp4 config-test <<<'$(SERVER_CONFIG)'

  Test Procedure:
  Client requests option 1.
  Client sends DISCOVER message.

  Pass Criteria:
  Server MUST respond with OFFER message.
  Response MUST include option 1.
  Response MUST contain yiaddr 192.168.50.1.
  Response option 1 MUST contain value 255.255.255.0.

  Test Setup:
  Server is configured with 192.168.51.0/24 subnet with 192.168.51.1-192.168.51.1 pool.
  Server has control agent configured on HTTP connection with address $(SRV4_ADDR):8000 and socket unix path: $(SOFTWARE_INSTALL_DIR)var/kea/control_socket_ANOTHER_ONE.
  DDNS server is configured on 127.0.0.1 address and 53001 port.
  DDNS server is configured with enable-updates option set to true.
  DDNS server is configured with qualifying-suffix option set to my.domain.com.
  Reserve hostname reserved-name in subnet 0 for host uniquely identified by hw-address ff:01:02:03:ff:04.
  For host reservation entry no. 0 in subnet 0 add address with value 3000::1.
  Generate server configuration file.

  Execute python script in path: $(SOFTWARE_INSTALL_DIR)sbin/kea-shell with arguments: --host 127.0.0.1 --port 8000 --service dhcp4 config-set <<<'$(SERVER_CONFIG)'
  Sleep for $(SLEEP_TIME_2) seconds.

  Test Procedure:
  Client requests option 1.
  Client sends DISCOVER message.

  Pass Criteria:
  Server MUST respond with OFFER message.
  Response MUST include option 1.
  Response MUST contain yiaddr 192.168.50.1.
  Response option 1 MUST contain value 255.255.255.0.


@v4 @controlchannel @kea_only
Scenario: control.channel.keashell.write-config

  Test Setup:
  Server is configured with 192.168.50.0/24 subnet with 192.168.50.1-192.168.50.1 pool.
  Server has control channel on unix socket with name $(SOFTWARE_INSTALL_DIR)var/kea/control_socket.
  Server has control agent configured on HTTP connection with address 127.0.0.1:8000 and socket unix path: $(SOFTWARE_INSTALL_DIR)var/kea/control_socket.
  Send server configuration using SSH and config-file.
  DHCP server is started.

  Test Procedure:
  Client requests option 1.
  Client sends DISCOVER message.

  Pass Criteria:
  Server MUST respond with OFFER message.
  Response MUST include option 1.
  Response MUST contain yiaddr 192.168.50.1.
  Response option 1 MUST contain value 255.255.255.0.

  Test Setup:
  Server is configured with 192.168.51.0/24 subnet with 192.168.51.1-192.168.51.1 pool.
  Server has control agent configured on HTTP connection with address localhost:8000 and socket UNIX path: $(SOFTWARE_INSTALL_DIR)var/kea/control_socket.
  Generate server configuration file.

  Execute python script in path: $(SOFTWARE_INSTALL_DIR)sbin/kea-shell with arguments: --host 127.0.0.1 --port 8000 --service dhcp4 config-set <<<' "Dhcp4": { "control-socket": { "socket-name": "/home/test/installed/git/var/kea/control_socket", "socket-type": "unix" }, "decline-probation-period": 86400, "dhcp-ddns": { "always-include-fqdn": false, "enable-updates": false, "generated-prefix": "myhost", "max-queue-size": 1024, "ncr-format": "JSON", "ncr-protocol": "UDP", "override-client-update": false, "override-no-update": false, "qualifying-suffix": "", "replace-client-name": "never", "sender-ip": "0.0.0.0", "sender-port": 0, "server-ip": "127.0.0.1", "server-port": 53001 }, "dhcp4o6-port": 0, "echo-client-id": true, "expired-leases-processing": { "flush-reclaimed-timer-wait-time": 25, "hold-reclaimed-time": 3600, "max-reclaim-leases": 100, "max-reclaim-time": 250, "reclaim-timer-wait-time": 10, "unwarned-reclaim-cycles": 5 }, "hooks-libraries": [  ], "host-reservation-identifiers": [ "hw-address", "duid", "circuit-id", "client-id" ], "interfaces-config": { "interfaces": [ "eth2" ], "re-detect": true }, "lease-database": { "type": "memfile" }, "option-data": [  ], "option-def": [  ], "shared-networks": [  ], "subnet4": [ { "4o6-interface": "", "4o6-interface-id": "", "4o6-subnet": "", "boot-file-name": "", "id": 1, "interface": "eth2", "match-client-id": true, "next-server": "0.0.0.0", "option-data": [  ], "pools": [ { "option-data": [  ], "pool": "192.168.51.1/32" } ], "rebind-timer": 2000, "relay": { "ip-address": "0.0.0.0" }, "renew-timer": 1000, "reservation-mode": "all", "reservations": [  ], "server-hostname": "", "subnet": "192.168.51.0/24", "valid-lifetime": 4000 } ] }'
  Sleep for $(SLEEP_TIME_2) seconds.

  Test Procedure:
  Client requests option 1.
  Client sends DISCOVER message.

  Pass Criteria:
  Server MUST respond with OFFER message.
  Response MUST include option 1.
  Response MUST contain yiaddr 192.168.51.1.
  Response option 1 MUST contain value 255.255.255.0.

  Execute python script in path: $(SOFTWARE_INSTALL_DIR)sbin/kea-shell with arguments: --host 127.0.0.1 --port 8000 --service dhcp4 config-write <<<''

  #TODO tests needed for not valid/not permitted paths

  Restart DHCP server.

  Test Procedure:
  Client requests option 1.
  Client sends DISCOVER message.

  Pass Criteria:
  Server MUST respond with OFFER message.
  Response MUST include option 1.
  Response MUST contain yiaddr 192.168.51.1.
  Response option 1 MUST contain value 255.255.255.0.
  
@v4 @controlchannel @kea_only
Scenario: control.channel.socket.reload-config

  Test Setup:
  Server is configured with 192.168.50.0/24 subnet with 192.168.50.1-192.168.50.1 pool.
  Server has control channel on unix socket with name $(SOFTWARE_INSTALL_DIR)var/kea/control_socket.
  Server has control agent configured on HTTP connection with address 127.0.0.1:8000 and socket unix path: $(SOFTWARE_INSTALL_DIR)var/kea/control_socket.
  Send server configuration using SSH and config-file.
  DHCP server is started.

  Test Procedure:
  Client requests option 1.
  Client sends DISCOVER message.

  Pass Criteria:
  Server MUST respond with OFFER message.
  Response MUST include option 1.
  Response MUST contain yiaddr 192.168.50.1.
  Response option 1 MUST contain value 255.255.255.0.

  Test Setup:
  Server is configured with 192.168.51.0/24 subnet with 192.168.51.1-192.168.51.1 pool.
  Server has control channel on unix socket with name $(SOFTWARE_INSTALL_DIR)var/kea/control_socket.
  Server has control agent configured on HTTP connection with address 127.0.0.1:8000 and socket unix path: $(SOFTWARE_INSTALL_DIR)var/kea/control_socket.
  Send server configuration using SSH and config-file.

  Execute python script in path: $(SOFTWARE_INSTALL_DIR)sbin/kea-shell with arguments: --host 127.0.0.1 --port 8000 --service dhcp4 config-reload <<<''

  Test Procedure:
  Client requests option 1.
  Client sends DISCOVER message.

  Pass Criteria:
  Server MUST respond with OFFER message.
  Response MUST include option 1.
  Response MUST contain yiaddr 192.168.51.1.
  Response option 1 MUST contain value 255.255.255.0.

  Restart DHCP server.

  Test Procedure:
  Client requests option 1.
  Client sends DISCOVER message.

  Pass Criteria:
  Server MUST respond with OFFER message.
  Response MUST include option 1.
  Response MUST contain yiaddr 192.168.51.1.
  Response option 1 MUST contain value 255.255.255.0.