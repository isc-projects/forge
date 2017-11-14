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
  Scenario: hook.v6.network.cmds.add
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

  Using UNIX socket on server in path $(SOFTWARE_INSTALL_DIR)var/kea/control_socket send {"command":"network6-list","arguments":{}}
  Using UNIX socket on server in path $(SOFTWARE_INSTALL_DIR)var/kea/control_socket send {"command":"network6-add","arguments":{"shared-networks": [{"interface": "eth2","name": "name-xyz","option-data": [],"preferred-lifetime": 0,"rapid-commit": false,"rebind-timer": 0,"relay": {"ip-address": "::"},"renew-timer": 0,"reservation-mode": "all","subnet6": [{"id": 3,"interface": "eth2","option-data": [],"pd-pools": [],"pools": [{"option-data": [],"pool": "2001:db8:c::1/128"}],"preferred-lifetime": 3000,"rapid-commit": false,"rebind-timer": 2000,"relay": {"ip-address": "::"},"renew-timer": 1000,"reservation-mode": "all","subnet": "2001:db8:c::/64","valid-lifetime": 4000},{"id": 4,"interface": "eth2","option-data": [],"pd-pools": [],"pools": [{"option-data": [],"pool": "2001:db8:d::1/128"}],"preferred-lifetime": 3000,"rapid-commit": false,"rebind-timer": 2000,"relay": {"ip-address": "::"},"renew-timer": 1000,"reservation-mode": "all","subnet": "2001:db8:d::/64","valid-lifetime": 4000}],"valid-lifetime": 0}]}}
  Using UNIX socket on server in path $(SOFTWARE_INSTALL_DIR)var/kea/control_socket send {"command":"network6-get","arguments":{"name": "name-xyz"}}




@v6 @kea_only @controlchannel @hook @network_cmds
  Scenario: hook.v6.network.cmds.add-conflict
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
  Add configuration parameter name with value "name-xyz" to shared-subnet 0 configuration.
  Add configuration parameter interface-id with value "interface-abc" to shared-subnet 0 configuration.
  Server has control channel on unix socket with name $(SOFTWARE_INSTALL_DIR)var/kea/control_socket.
  Add hooks library located $(SOFTWARE_INSTALL_DIR)lib/hooks/libdhcp_subnet_cmds.so.
  Send server configuration using SSH and config-file.

  DHCP server is started.



  Using UNIX socket on server in path $(SOFTWARE_INSTALL_DIR)var/kea/control_socket send {"command":"network6-list","arguments":{}}
  Using UNIX socket on server in path $(SOFTWARE_INSTALL_DIR)var/kea/control_socket send {"command":"network6-add","arguments":{"shared-networks": [{"interface": "eth2","name": "name-xyz","option-data": [],"preferred-lifetime": 0,"rapid-commit": false,"rebind-timer": 0,"relay": {"ip-address": "::"},"renew-timer": 0,"reservation-mode": "all","subnet6": [{"id": 3,"interface": "eth2","option-data": [],"pd-pools": [],"pools": [{"option-data": [],"pool": "2001:db8:c::1/128"}],"preferred-lifetime": 3000,"rapid-commit": false,"rebind-timer": 2000,"relay": {"ip-address": "::"},"renew-timer": 1000,"reservation-mode": "all","subnet": "2001:db8:c::/64","valid-lifetime": 4000},{"id": 4,"interface": "eth2","option-data": [],"pd-pools": [],"pools": [{"option-data": [],"pool": "2001:db8:d::1/128"}],"preferred-lifetime": 3000,"rapid-commit": false,"rebind-timer": 2000,"relay": {"ip-address": "::"},"renew-timer": 1000,"reservation-mode": "all","subnet": "2001:db8:d::/64","valid-lifetime": 4000}],"valid-lifetime": 0}]}}



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
  Using UNIX socket on server in path $(SOFTWARE_INSTALL_DIR)var/kea/control_socket send {"command": "network6-del","arguments":{"name":"name-xyz"}}
  #Using UNIX socket on server in path $(SOFTWARE_INSTALL_DIR)var/kea/control_socket send {"command": "network6-add","arguments":{"subnet6":[{"id": 234,"interface":"$(SERVER_IFACE)","subnet": "2001:db8:1::/64","pools":[{"pool":"2001:db8:1::1-2001:db8:1::2"}]}]}}
  Using UNIX socket on server in path $(SOFTWARE_INSTALL_DIR)var/kea/control_socket send {"command":"network6-list","arguments":{}}



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
  #Using UNIX socket on server in path $(SOFTWARE_INSTALL_DIR)var/kea/control_socket send {"command": "network6-add","arguments":{"subnet6":[{"id": 234,"interface":"$(SERVER_IFACE)","subnet": "2001:db8:1::/64","pools":[{"pool":"2001:db8:1::1-2001:db8:1::2"}]}]}}
  Using UNIX socket on server in path $(SOFTWARE_INSTALL_DIR)var/kea/control_socket send {"command":"network6-list","arguments":{}}


@v6 @kea_only @controlchannel @hook @network_cmds @disabled
  Scenario: hook.v6.network.cmds.del-global-options
  Test Setup:
  Server is configured with 2001:db8:1::/64 subnet with 2001:db8:1::1-2001:db8:1::1 pool.
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
  Client requests option 7.
  Client sends SOLICIT message.

  Pass Criteria:
  Server MUST respond with ADVERTISE message.
  Response MUST include option 1.
  Response MUST include option 2.
  Response MUST include option 3.
  Response option 3 MUST contain sub-option 5.
  Response sub-option 5 from option 3 MUST contain address 2001:db8:1::1.
  Response MUST include option 7.
  Response option 7 MUST contain value 123.

  Using UNIX socket on server in path $(SOFTWARE_INSTALL_DIR)var/kea/control_socket send {"command":"network6-list","arguments":{}}
  Using UNIX socket on server in path $(SOFTWARE_INSTALL_DIR)var/kea/control_socket send {"command": "network6-del","arguments":{"id":1}}
  #Using UNIX socket on server in path $(SOFTWARE_INSTALL_DIR)var/kea/control_socket send {"command": "network6-add","arguments":{"subnet6":[{"id": 234,"interface":"$(SERVER_IFACE)","subnet": "2001:db8:1::/64","pools":[{"pool":"2001:db8:1::1-2001:db8:1::2"}]}]}}
  Using UNIX socket on server in path $(SOFTWARE_INSTALL_DIR)var/kea/control_socket send {"command":"network6-get","arguments":{}

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

  Test Procedure:
  Client requests option 7.
  Client sends INFOREQUEST message.

  Pass Criteria:
  Server MUST respond with REPLY message.
  Response MUST include option 7.
  Response option 7 MUST contain value 123.

@v6 @kea_only @controlchannel @hook @network_cmds @disabled
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

  Using UNIX socket on server in path $(SOFTWARE_INSTALL_DIR)var/kea/control_socket send {"command":"network6-list","arguments":{}}
  Using UNIX socket on server in path $(SOFTWARE_INSTALL_DIR)var/kea/control_socket send {"command": "network6-add","arguments":{"subnet6":[{"id": 234,"interface":"$(SERVER_IFACE)","subnet": "2001:db8:1::/64","pools":[{"pool":"2001:db8:1::1-2001:db8:1::2"}]}]}}
  Using UNIX socket on server in path $(SOFTWARE_INSTALL_DIR)var/kea/control_socket send {"command":"network6-get","arguments":{"id": 234}}

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

  Using UNIX socket on server in path $(SOFTWARE_INSTALL_DIR)var/kea/control_socket send {"command": "network6-del","arguments":{"id":234}}
  #Using UNIX socket on server in path $(SOFTWARE_INSTALL_DIR)var/kea/control_socket send {"command": "network6-add","arguments":{"subnet6":[{"id": 234,"interface":"$(SERVER_IFACE)","subnet": "2001:db8:1::/64","pools":[{"pool":"2001:db8:1::1-2001:db8:1::2"}]}]}}
  Using UNIX socket on server in path $(SOFTWARE_INSTALL_DIR)var/kea/control_socket send {"command":"network6-get","arguments":{}

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