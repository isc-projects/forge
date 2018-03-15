Feature: Kea shared networks manipulation commands

@v6 @kea_only @controlchannel @hook @network_cmds
  Scenario: hook.v6.network.cmds.list
  Test Setup:
  Server is configured with 2001:db8:a::/64 subnet with 2001:db8:a::1-2001:db8:a::1 pool.
  Server is configured with another subnet: 2001:db8:b::/64 with 2001:db8:b::1-2001:db8:b::1 pool.
  Server is configured with another subnet: 2001:db8:c::/64 with 2001:db8:c::1-2001:db8:c::1 pool.
  Server is configured with another subnet: 2001:db8:d::/64 with 2001:db8:d::1-2001:db8:d::1 pool.
  Server is configured with another subnet: 2001:db8:e::/64 with 2001:db8:e::1-2001:db8:e::1 pool.
  Server is configured with another subnet: 2001:db8:f::/64 with 2001:db8:f::1-2001:db8:f::1 pool.
  Server is configured with dns-servers option in subnet 1 with value 2001:db8::1,2001:db8::2.
  #first shared subnet
  Add subnet 0 to shared-subnet set 0.
  Add subnet 1 to shared-subnet set 0.
  Add configuration parameter name with value "name-abc" to shared-subnet 0 configuration.
  Add configuration parameter interface-id with value "interface-abc" to shared-subnet 0 configuration.
  #second shared-subnet
  Add subnet 2 to shared-subnet set 1.
  Add subnet 3 to shared-subnet set 1.
  Add configuration parameter name with value "name-xyz" to shared-subnet 1 configuration.
  Add configuration parameter interface with value "$(SERVER_IFACE)" to shared-subnet 1 configuration.
  Add subnet 4 to shared-subnet set 2.
  Add subnet 5 to shared-subnet set 2.
  Add configuration parameter name with value "name-something" to shared-subnet 2 configuration.
  Add configuration parameter relay with value {"ip-address":"2001:db8::1234"} to shared-subnet 2 configuration.
  Add hooks library located $(SOFTWARE_INSTALL_DIR)lib/hooks/libdhcp_subnet_cmds.so.
  Server has control channel on unix socket with name $(SOFTWARE_INSTALL_DIR)var/kea/control_socket.
  Send server configuration using SSH and config-file.

  DHCP server is started.

  Using UNIX socket on server in path $(SOFTWARE_INSTALL_DIR)var/kea/control_socket send {"command":"network6-list","arguments":{}}

@v6 @kea_only @controlchannel @hook @network_cmds
  Scenario: hook.v6.network.cmds.get-by-name
  Test Setup:
  Server is configured with 2001:db8:a::/64 subnet with 2001:db8:a::1-2001:db8:a::1 pool.
  Server is configured with another subnet: 2001:db8:b::/64 with 2001:db8:b::1-2001:db8:b::1 pool.
  Server is configured with another subnet: 2001:db8:c::/64 with 2001:db8:c::1-2001:db8:c::1 pool.
  Server is configured with another subnet: 2001:db8:d::/64 with 2001:db8:d::1-2001:db8:d::1 pool.
  Server is configured with another subnet: 2001:db8:e::/64 with 2001:db8:e::1-2001:db8:e::1 pool.
  Server is configured with another subnet: 2001:db8:f::/64 with 2001:db8:f::1-2001:db8:f::1 pool.
  Server is configured with dns-servers option in subnet 1 with value 2001:db8::1,2001:db8::2.
  #first shared subnet
  Add subnet 0 to shared-subnet set 0.
  Add subnet 1 to shared-subnet set 0.
  Add configuration parameter name with value "name-abc" to shared-subnet 0 configuration.
  Add configuration parameter interface-id with value "interface-abc" to shared-subnet 0 configuration.
  #second shared-subnet
  Add subnet 2 to shared-subnet set 1.
  Add subnet 3 to shared-subnet set 1.
  Add configuration parameter name with value "name-xyz" to shared-subnet 1 configuration.
  Add configuration parameter interface with value "$(SERVER_IFACE)" to shared-subnet 1 configuration.
  Add subnet 4 to shared-subnet set 2.
  Add subnet 5 to shared-subnet set 2.
  Add configuration parameter name with value "name-something" to shared-subnet 2 configuration.
  Add configuration parameter relay with value {"ip-address":"2001:db8::1234"} to shared-subnet 2 configuration.
  Add hooks library located $(SOFTWARE_INSTALL_DIR)lib/hooks/libdhcp_subnet_cmds.so.
  Server has control channel on unix socket with name $(SOFTWARE_INSTALL_DIR)var/kea/control_socket.
  Send server configuration using SSH and config-file.

  DHCP server is started.

  Using UNIX socket on server in path $(SOFTWARE_INSTALL_DIR)var/kea/control_socket send {"command":"network6-get","arguments":{"name":"name-xyz"}}

@v6 @kea_only @controlchannel @hook @network_cmds
  Scenario: hook.v6.network.cmds.add-on-interface
  Test Setup:
  Server is configured with $(EMPTY) subnet with $(EMPTY) pool.
  Server is configured with preference option with value 123.
  #Server is configured with domain-search option with value domain1.example.com,domain2.isc.org.
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

  Using UNIX socket on server in path $(SOFTWARE_INSTALL_DIR)var/kea/control_socket send {"command": "network6-add","arguments": {"shared-networks": [{"name": "name-abc","preferred-lifetime": 3000,"rebind-timer": 2000,"renew-timer": 1000,"valid-lifetime": 4000,"subnet6":[{"subnet":"2001:db8:a::/64","interface": "$(SERVER_IFACE)","pools":[{"pool":"2001:db8:a::1-2001:db8:a::1"}]}]}]}}

  Using UNIX socket on server in path $(SOFTWARE_INSTALL_DIR)var/kea/control_socket send {"command":"network6-get","arguments":{"name": "name-abc"}}
  Sleep for 5 seconds.
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

@v6 @kea_only @controlchannel @hook @network_cmds
  Scenario: hook.v6.network.cmds.add-on-interface-id
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

  Using UNIX socket on server in path $(SOFTWARE_INSTALL_DIR)var/kea/control_socket send {"command":"network6-add","arguments":{"shared-networks":[{"name": "name-abc","interface-id": "interface-abc","preferred-lifetime": 3000,"rebind-timer": 2000,"renew-timer": 1000,"valid-lifetime": 4000,"subnet6":[{"id":1,"pools": [{"pool": "2001:db8:1::1-2001:db8:1::10"}],"preferred-lifetime": 3000,"rebind-timer": 2000,"renew-timer": 1000,"reservation-mode": "all","subnet": "2001:db8:1::/64","valid-lifetime": 4000}]}]}}
  Using UNIX socket on server in path $(SOFTWARE_INSTALL_DIR)var/kea/control_socket send {"command":"network6-get","arguments":{"name": "name-abc"}}
  Sleep for 5 seconds.

  Test Procedure:
  Client sets DUID value to 00:03:00:01:f6:f5:f4:f3:f2:01.
  Client does include client-id.
  Client does include IA-NA.
  Client sends SOLICIT message.

  RelayAgent sets ifaceid value to interface-abc.
  RelayAgent does include interface-id.
  RelayAgent forwards message encapsulated in 1 level.

  Pass Criteria:
  Server MUST respond with RELAYREPLY message.
  Response MUST include option 18.
  Response MUST include option 9.
  Response option 9 MUST contain Relayed Message.
  Relayed Message MUST include option 1.
  Relayed Message MUST include option 2.
  Relayed Message MUST include option 3.
  Relayed Message option 3 MUST contain sub-option 5.

@v6 @kea_only @controlchannel @hook @network_cmds
  Scenario: hook.v6.network.cmds.add-on-relay-addr
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

  Using UNIX socket on server in path $(SOFTWARE_INSTALL_DIR)var/kea/control_socket send {"command":"network6-add","arguments":{"shared-networks":[{"name": "name-abc","relay":{"ip-address":"2001:db8::abcd"},"preferred-lifetime": 3000,"rebind-timer": 2000,"renew-timer": 1000,"valid-lifetime": 4000,"subnet6":[{"id":1,"pools": [{"pool": "2001:db8:1::1-2001:db8:1::10"}],"preferred-lifetime": 3000,"rebind-timer": 2000,"renew-timer": 1000,"reservation-mode": "all","subnet": "2001:db8:1::/64","valid-lifetime": 4000}]}]}}
  Using UNIX socket on server in path $(SOFTWARE_INSTALL_DIR)var/kea/control_socket send {"command":"network6-get","arguments":{"name": "name-abc"}}
  Sleep for 5 seconds.

  Test Procedure:
  Client sets DUID value to 00:03:00:01:f6:f5:f4:f3:f2:01.
  Client does include client-id.
  Client does include IA-NA.
  Client sends SOLICIT message.

  RelayAgent sets ifaceid value to interface-abc.
  RelayAgent does include interface-id.
  RelayAgent sets linkaddr value to 2001:db8::abcd.
  RelayAgent forwards message encapsulated in 1 level.

  Pass Criteria:
  Server MUST respond with RELAYREPLY message.
  Response MUST include option 18.
  Response MUST include option 9.
  Response option 9 MUST contain Relayed Message.
  Relayed Message MUST include option 1.
  Relayed Message MUST include option 2.
  Relayed Message MUST include option 3.
  Relayed Message option 3 MUST contain sub-option 5.

@v6 @kea_only @controlchannel @hook @network_cmds
  Scenario: hook.v6.network.cmds.add-conflict
  Test Setup:
  Server is configured with 2001:db8:a::/64 subnet with 2001:db8:a::1-2001:db8:a::1 pool.
  Server is configured with another subnet: 2001:db8:b::/64 with 2001:db8:b::1-2001:db8:b::1 pool.
  #first shared subnet
  Add subnet 0 to shared-subnet set 0.
  Add subnet 1 to shared-subnet set 0.
  Add configuration parameter name with value "name-xyz" to shared-subnet 0 configuration.
  Add configuration parameter interface with value "$(SERVER_IFACE)" to shared-subnet 0 configuration.
  Server has control channel on unix socket with name $(SOFTWARE_INSTALL_DIR)var/kea/control_socket.
  Add hooks library located $(SOFTWARE_INSTALL_DIR)lib/hooks/libdhcp_subnet_cmds.so.
  Send server configuration using SSH and config-file.

  DHCP server is started.

  Using UNIX socket on server in path $(SOFTWARE_INSTALL_DIR)var/kea/control_socket send {"command":"network6-list","arguments":{}}
  Using UNIX socket on server in path $(SOFTWARE_INSTALL_DIR)var/kea/control_socket send {"command":"network6-add","arguments":{"shared-networks": [{"interface": "$(SERVER_IFACE)","name": "name-xyz","option-data": [],"preferred-lifetime": 0,"rapid-commit": false,"rebind-timer": 0,"relay": {"ip-address": "::"},"renew-timer": 0,"reservation-mode": "all","subnet6": [{"id": 3,"interface": "$(SERVER_IFACE)","option-data": [],"pd-pools": [],"pools": [{"option-data": [],"pool": "2001:db8:c::1/128"}],"preferred-lifetime": 3000,"rapid-commit": false,"rebind-timer": 2000,"relay": {"ip-address": "::"},"renew-timer": 1000,"reservation-mode": "all","subnet": "2001:db8:c::/64","valid-lifetime": 4000},{"id": 4,"interface": "$(SERVER_IFACE)","option-data": [],"pd-pools": [],"pools": [{"option-data": [],"pool": "2001:db8:d::1/128"}],"preferred-lifetime": 3000,"rapid-commit": false,"rebind-timer": 2000,"relay": {"ip-address": "::"},"renew-timer": 1000,"reservation-mode": "all","subnet": "2001:db8:d::/64","valid-lifetime": 4000}],"valid-lifetime": 0}]}}

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

  Test Procedure:
  Client sets DUID value to 00:03:00:01:66:55:44:33:22:11.
  Client copies IA_NA option from received message.
  Client saves server-id option from received message.
  Client adds saved options. And DONT Erase.
  Client does include client-id.
  Client sends REQUEST message.

  Pass Criteria:
  Server MUST respond with REPLY message.
  Response MUST include option 1.
  Response MUST include option 2.
  Response MUST include option 3.
  Response option 3 MUST contain sub-option 5.

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

  Test Procedure:
  Client sets DUID value to 00:03:00:01:66:55:44:33:22:22.
  Client copies IA_NA option from received message.
  Client adds saved options. And DONT Erase.
  Client does include client-id.
  Client sends REQUEST message.

  Pass Criteria:
  Server MUST respond with REPLY message.
  Response MUST include option 1.
  Response MUST include option 2.
  Response MUST include option 3.
  Response option 3 MUST contain sub-option 5.

  Test Procedure:
  Client sets DUID value to 00:03:00:01:66:55:44:33:44:44.
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

@v6 @kea_only @controlchannel @hook @network_cmds
  Scenario: hook.v6.network.cmds.del
  Test Setup:
  Server is configured with 2001:db8:a::/64 subnet with 2001:db8:a::1-2001:db8:a::1 pool.
  Server is configured with another subnet: 2001:db8:b::/64 with 2001:db8:b::1-2001:db8:b::1 pool.
  Server is configured with another subnet: 2001:db8:c::/64 with 2001:db8:c::1-2001:db8:c::1 pool.
  Server is configured with another subnet: 2001:db8:d::/64 with 2001:db8:d::1-2001:db8:d::1 pool.
  Server is configured with another subnet: 2001:db8:e::/64 with 2001:db8:e::1-2001:db8:e::1 pool.
  Server is configured with another subnet: 2001:db8:f::/64 with 2001:db8:f::1-2001:db8:f::1 pool.
  Server is configured with dns-servers option in subnet 1 with value 2001:db8::1,2001:db8::2.
  #first shared subnet
  Add subnet 0 to shared-subnet set 0.
  Add subnet 1 to shared-subnet set 0.
  Add configuration parameter name with value "name-abc" to shared-subnet 0 configuration.
  Add configuration parameter interface-id with value "interface-abc" to shared-subnet 0 configuration.
  #second shared-subnet
  Add subnet 2 to shared-subnet set 1.
  Add subnet 3 to shared-subnet set 1.
  Add configuration parameter name with value "name-xyz" to shared-subnet 1 configuration.
  Add configuration parameter interface with value "$(SERVER_IFACE)" to shared-subnet 1 configuration.
  Add subnet 4 to shared-subnet set 2.
  Add subnet 5 to shared-subnet set 2.
  Add configuration parameter name with value "name-something" to shared-subnet 2 configuration.
  Add configuration parameter relay with value {"ip-address":"2001:db8::1234"} to shared-subnet 2 configuration.
  Add hooks library located $(SOFTWARE_INSTALL_DIR)lib/hooks/libdhcp_subnet_cmds.so.
  Server has control channel on unix socket with name $(SOFTWARE_INSTALL_DIR)var/kea/control_socket.
  Send server configuration using SSH and config-file.

  DHCP server is started.

  Using UNIX socket on server in path $(SOFTWARE_INSTALL_DIR)var/kea/control_socket send {"command":"network6-list","arguments":{}}
  Using UNIX socket on server in path $(SOFTWARE_INSTALL_DIR)var/kea/control_socket send {"command": "network6-del","arguments":{"name":"name-xyz","subnets-action": "delete"}}
  #Using UNIX socket on server in path $(SOFTWARE_INSTALL_DIR)var/kea/control_socket send {"command": "network6-add","arguments":{"subnet6":[{"id": 234,"interface":"$(SERVER_IFACE)","subnet": "2001:db8:1::/64","pools":[{"pool":"2001:db8:1::1-2001:db8:1::2"}]}]}}
  Using UNIX socket on server in path $(SOFTWARE_INSTALL_DIR)var/kea/control_socket send {"command":"network6-list","arguments":{}}

@v6 @kea_only @controlchannel @hook @network_cmds
  Scenario: hook.v6.network.cmds.del-2
  Test Setup:
  Server is configured with 2001:db8:a::/64 subnet with 2001:db8:a::1-2001:db8:a::1 pool.
  #first shared subnet
  Add subnet 0 to shared-subnet set 0.
  Add configuration parameter name with value "name-abc" to shared-subnet 0 configuration.
  Add configuration parameter interface with value "$(SERVER_IFACE)" to shared-subnet 0 configuration.
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

  Using UNIX socket on server in path $(SOFTWARE_INSTALL_DIR)var/kea/control_socket send {"command":"network6-list","arguments":{}}
  Using UNIX socket on server in path $(SOFTWARE_INSTALL_DIR)var/kea/control_socket send {"command": "network6-del","arguments":{"name":"name-abc","subnets-action": "delete"}}
  Using UNIX socket on server in path $(SOFTWARE_INSTALL_DIR)var/kea/control_socket send {"command":"network6-list","arguments":{}}

  Sleep for 5 seconds.
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

@v6 @kea_only @controlchannel @hook @network_cmds
  Scenario: hook.v6.network.cmds.del-non-existing
  Test Setup:
  Server is configured with 2001:db8:a::/64 subnet with 2001:db8:a::1-2001:db8:a::1 pool.
  Server is configured with another subnet: 2001:db8:b::/64 with 2001:db8:b::1-2001:db8:b::1 pool.
  Server is configured with another subnet: 2001:db8:c::/64 with 2001:db8:c::1-2001:db8:c::1 pool.
  Server is configured with another subnet: 2001:db8:d::/64 with 2001:db8:d::1-2001:db8:d::1 pool.
  Server is configured with another subnet: 2001:db8:e::/64 with 2001:db8:e::1-2001:db8:e::1 pool.
  Server is configured with another subnet: 2001:db8:f::/64 with 2001:db8:f::1-2001:db8:f::1 pool.
  Server is configured with dns-servers option in subnet 1 with value 2001:db8::1,2001:db8::2.
  #first shared subnet
  Add subnet 0 to shared-subnet set 0.
  Add subnet 1 to shared-subnet set 0.
  Add configuration parameter name with value "name-abc" to shared-subnet 0 configuration.
  Add configuration parameter interface-id with value "interface-abc" to shared-subnet 0 configuration.
  #second shared-subnet
  Add subnet 2 to shared-subnet set 1.
  Add subnet 3 to shared-subnet set 1.
  Add configuration parameter name with value "name-xyz" to shared-subnet 1 configuration.
  Add configuration parameter interface with value "$(SERVER_IFACE)" to shared-subnet 1 configuration.
  Add subnet 4 to shared-subnet set 2.
  Add subnet 5 to shared-subnet set 2.
  Add configuration parameter name with value "name-something" to shared-subnet 2 configuration.
  Add configuration parameter relay with value {"ip-address":"2001:db8::1234"} to shared-subnet 2 configuration.
  Add hooks library located $(SOFTWARE_INSTALL_DIR)lib/hooks/libdhcp_subnet_cmds.so.
  Server has control channel on unix socket with name $(SOFTWARE_INSTALL_DIR)var/kea/control_socket.
  Send server configuration using SSH and config-file.

  DHCP server is started.

  Using UNIX socket on server in path $(SOFTWARE_INSTALL_DIR)var/kea/control_socket send {"command":"network6-list","arguments":{}}
  Using UNIX socket on server in path $(SOFTWARE_INSTALL_DIR)var/kea/control_socket send {"command": "network6-del","arguments":{"name":"name-xyzc"}}
  Using UNIX socket on server in path $(SOFTWARE_INSTALL_DIR)var/kea/control_socket send {"command":"network6-list","arguments":{}}

@v6 @kea_only @controlchannel @hook @network_cmds
  Scenario: hook.v6.network.cmds.add-and-del
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

  Using UNIX socket on server in path $(SOFTWARE_INSTALL_DIR)var/kea/control_socket send {"command": "network6-add","arguments": {"shared-networks": [{"name": "name-abc","preferred-lifetime": 3000,"rebind-timer": 2000,"renew-timer": 1000,"valid-lifetime": 4000,"subnet6":[{"subnet":"2001:db8:a::/64","interface": "$(SERVER_IFACE)","pools":[{"pool":"2001:db8:a::1-2001:db8:a::1"}]}]}]}}

  Sleep for 5 seconds.
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
  Response sub-option 5 from option 3 MUST contain address 2001:db8:a::1.

  Using UNIX socket on server in path $(SOFTWARE_INSTALL_DIR)var/kea/control_socket send {"command": "network6-del","arguments":{"name":"name-abc","subnets-action": "delete"}}
  Using UNIX socket on server in path $(SOFTWARE_INSTALL_DIR)var/kea/control_socket send {"command":"network6-list","arguments":{}}

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