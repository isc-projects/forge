Feature: Kea subnet-id sanity-check
    Tests for sanity checks of a subnet-id.

@v6 @kea_only @subnet-id-sanity-check @abc
  Scenario: v6.sanity.check-subnet-id-fix-able
  Test Setup:
  Server is configured with 2001:db8::/64 subnet with 2001:db8::1-2001:db8::1 pool.
  Add configuration parameter id with value 666 to subnet 0 configuration.
  Add configuration parameter sanity-checks with value {"lease-checks":"fix"} to global configuration.
  Server has control channel on unix socket with name $(SOFTWARE_INSTALL_DIR)/var/kea/control_socket.

  Send server configuration using SSH and config-file.

  DHCP server is started.

  Test Procedure:
  Client sets DUID value to 00:03:00:01:f6:f5:f4:f3:f2:01.
  Client does include client-id.
  Client sets ia_id value to 1234567.
  Client does include IA-NA.
  Client sends SOLICIT message.

  Pass Criteria:
  Server MUST respond with ADVERTISE message.
  Response MUST include option 1.
  Response MUST include option 2.
  Response MUST include option 3.
  Response option 3 MUST contain sub-option 5.

  Test Procedure:
  Client sets DUID value to 00:03:00:01:f6:f5:f4:f3:f2:01.
  Client copies IA_NA option from received message.
  Client copies server-id option from received message.
  Client does include client-id.
  Client sends REQUEST message.

  Pass Criteria:
  Server MUST respond with REPLY message.
  Response MUST include option 1.
  Response MUST include option 2.
  Response MUST include option 3.
  Response option 3 MUST contain sub-option 5.
  Response sub-option 5 from option 3 MUST contain address 2001:db8::1.

  File stored in $(SOFTWARE_INSTALL_DIR)/var/kea/kea-leases6.csv MUST contain line or phrase: 2001:db8::1,00:03:00:01:f6:f5:f4:f3:f2:01
  File stored in $(SOFTWARE_INSTALL_DIR)/var/kea/kea-leases6.csv MUST contain line or phrase: 666,3000,0,1234567,128,0,0,,f6:f5:f4:f3:f2:01

  DHCP server is stopped.
  Clear logs.

  Test Setup:
  Server is configured with 2001:db8::/64 subnet with 2001:db8::1-2001:db8::1 pool.
  Add configuration parameter id with value 999 to subnet 0 configuration.
  Add configuration parameter sanity-checks with value {"lease-checks":"fix"} to global configuration.
  Server has control channel on unix socket with name $(SOFTWARE_INSTALL_DIR)/var/kea/control_socket.

  Send server configuration using SSH and config-file.
  DHCP server is started.

  File stored in $(SOFTWARE_INSTALL_DIR)/var/kea/kea.log MUST contain line or phrase: DHCPSRV_LEASE_SANITY_FIXED The lease 2001:db8::1 with subnet-id 666 failed subnet-id checks, but was corrected to subnet-id 999.

  Test Procedure:
  Client sets DUID value to 00:03:00:01:f6:f5:f4:f3:f2:22.
  Client does include client-id.
  Client sets ia_id value to 1234567.
  Client does include IA-NA.
  Client sends SOLICIT message.

  Pass Criteria:
  Server MUST respond with ADVERTISE message.
  Response MUST include option 1.
  Response MUST include option 2.
  Response MUST include option 3.
  Response option 3 MUST contain sub-option 5.

  Test Procedure:
  Client sets DUID value to 00:03:00:01:f6:f5:f4:f3:f2:22.
  Client copies IA_NA option from received message.
  Client copies server-id option from received message.
  Client does include client-id.
  Client sends REQUEST message.

  Pass Criteria:
  Server MUST respond with REPLY message.
  Response MUST include option 1.
  Response MUST include option 2.
  Response MUST include option 3.
  Response option 3 MUST contain sub-option 5.
  Response sub-option 5 from option 3 MUST contain address 2001:db8::1.

@v6 @kea_only @subnet-id-sanity-check @abc
  Scenario: v6.sanity.check-subnet-id-fix-able-double-restart
  Test Setup:
  Server is configured with 2001:db8::/64 subnet with 2001:db8::1-2001:db8::1 pool.
  Add configuration parameter id with value 666 to subnet 0 configuration.
  Add configuration parameter sanity-checks with value {"lease-checks":"fix"} to global configuration.
  Server has control channel on unix socket with name $(SOFTWARE_INSTALL_DIR)/var/kea/control_socket.

  Send server configuration using SSH and config-file.

  DHCP server is started.

  Test Procedure:
  Client sets DUID value to 00:03:00:01:f6:f5:f4:f3:f2:01.
  Client does include client-id.
  Client sets ia_id value to 1234567.
  Client does include IA-NA.
  Client sends SOLICIT message.

  Pass Criteria:
  Server MUST respond with ADVERTISE message.
  Response MUST include option 1.
  Response MUST include option 2.
  Response MUST include option 3.
  Response option 3 MUST contain sub-option 5.

  Test Procedure:
  Client sets DUID value to 00:03:00:01:f6:f5:f4:f3:f2:01.
  Client copies IA_NA option from received message.
  Client copies server-id option from received message.
  Client does include client-id.
  Client sends REQUEST message.

  Pass Criteria:
  Server MUST respond with REPLY message.
  Response MUST include option 1.
  Response MUST include option 2.
  Response MUST include option 3.
  Response option 3 MUST contain sub-option 5.
  Response sub-option 5 from option 3 MUST contain address 2001:db8::1.

  File stored in $(SOFTWARE_INSTALL_DIR)/var/kea/kea-leases6.csv MUST contain line or phrase: 2001:db8::1,00:03:00:01:f6:f5:f4:f3:f2:01
  File stored in $(SOFTWARE_INSTALL_DIR)/var/kea/kea-leases6.csv MUST contain line or phrase: 666,3000,0,1234567,128,0,0,,f6:f5:f4:f3:f2:01

  DHCP server is stopped.
  Clear logs.

  Test Setup:
  Server is configured with 2001:db8::/64 subnet with 2001:db8::1-2001:db8::1 pool.
  Add configuration parameter id with value 999 to subnet 0 configuration.
  Add configuration parameter sanity-checks with value {"lease-checks":"fix"} to global configuration.
  Server has control channel on unix socket with name $(SOFTWARE_INSTALL_DIR)/var/kea/control_socket.

  Send server configuration using SSH and config-file.
  DHCP server is started.

  File stored in $(SOFTWARE_INSTALL_DIR)/var/kea/kea.log MUST contain line or phrase: DHCPSRV_LEASE_SANITY_FIXED The lease 2001:db8::1 with subnet-id 666 failed subnet-id checks, but was corrected to subnet-id 999.

  Sleep for 13 seconds.

  DHCP server is stopped.

  Test Setup:
  Server is configured with 2001:db8::/64 subnet with 2001:db8::1-2001:db8::1 pool.
  Add configuration parameter id with value 999 to subnet 0 configuration.
  Add configuration parameter sanity-checks with value {"lease-checks":"fix"} to global configuration.
  Server has control channel on unix socket with name $(SOFTWARE_INSTALL_DIR)/var/kea/control_socket.

  Send server configuration using SSH and config-file.
  DHCP server is started.

  Test Procedure:
  Client sets DUID value to 00:03:00:01:f6:f5:f4:f3:f2:22.
  Client does include client-id.
  Client sets ia_id value to 987654321.
  Client does include IA-NA.
  Client sends SOLICIT message.

  Pass Criteria:
  Server MUST respond with ADVERTISE message.
  Response MUST include option 1.
  Response MUST include option 2.
  Response MUST include option 3.
  Response option 3 MUST contain sub-option 5.

  Test Procedure:
  Client sets DUID value to 00:03:00:01:f6:f5:f4:f3:f2:22.
  Client copies IA_NA option from received message.
  Client copies server-id option from received message.
  Client does include client-id.
  Client sends REQUEST message.

  Pass Criteria:
  Server MUST respond with REPLY message.
  Response MUST include option 1.
  Response MUST include option 2.
  Response MUST include option 3.
  Response option 3 MUST contain sub-option 5.
  Response sub-option 5 from option 3 MUST contain address 2001:db8::1.

#  Pause the Test.

@v6 @kea_only @subnet-id-sanity-check @abc
  Scenario: v6.sanity.check-subnet-id-fix-unable
  Test Setup:
  Server is configured with 2001:db8::/64 subnet with 2001:db8::1-2001:db8::1 pool.
  Add configuration parameter id with value 666 to subnet 0 configuration.
  Add configuration parameter sanity-checks with value {"lease-checks":"fix"} to global configuration.
  Server has control channel on unix socket with name $(SOFTWARE_INSTALL_DIR)/var/kea/control_socket.

  Send server configuration using SSH and config-file.

  DHCP server is started.

  Test Procedure:
  Client sets DUID value to 00:03:00:01:f6:f5:f4:f3:f2:01.
  Client does include client-id.
  Client sets ia_id value to 1234567.
  Client does include IA-NA.
  Client sends SOLICIT message.

  Pass Criteria:
  Server MUST respond with ADVERTISE message.
  Response MUST include option 1.
  Response MUST include option 2.
  Response MUST include option 3.
  Response option 3 MUST contain sub-option 5.

  Test Procedure:
  Client sets DUID value to 00:03:00:01:f6:f5:f4:f3:f2:01.
  Client copies IA_NA option from received message.
  Client copies server-id option from received message.
  Client does include client-id.
  Client sends REQUEST message.

  Pass Criteria:
  Server MUST respond with REPLY message.
  Response MUST include option 1.
  Response MUST include option 2.
  Response MUST include option 3.
  Response option 3 MUST contain sub-option 5.
  Response sub-option 5 from option 3 MUST contain address 2001:db8::1.

  File stored in $(SOFTWARE_INSTALL_DIR)/var/kea/kea-leases6.csv MUST contain line or phrase: 2001:db8::1,00:03:00:01:f6:f5:f4:f3:f2:01
  File stored in $(SOFTWARE_INSTALL_DIR)/var/kea/kea-leases6.csv MUST contain line or phrase: 666,3000,0,1234567,128,0,0,,f6:f5:f4:f3:f2:01

  DHCP server is stopped.

  Clear logs.

  Test Setup:
  Server is configured with 2001:db8::/64 subnet with 2001:db8::1-2001:db8::1 pool.
  Add configuration parameter id with value 999 to subnet 0 configuration.
  Add configuration parameter sanity-checks with value {"lease-checks":"fix"} to global configuration.
  Server has control channel on unix socket with name $(SOFTWARE_INSTALL_DIR)/var/kea/control_socket.

  Send server configuration using SSH and config-file.

  DHCP server is started.

  Test Procedure:
  Client sets DUID value to 00:03:00:01:f6:f5:f4:f3:f2:01.
  Client does include client-id.
  Client sets ia_id value to 1234567.
  Client does include IA-NA.
  Client sends SOLICIT message.

  Pass Criteria:
  Server MUST respond with ADVERTISE message.
  Response MUST include option 1.
  Response MUST include option 2.
  Response MUST include option 3.
  Response option 3 MUST contain sub-option 5.

  Test Procedure:
  Client sets DUID value to 00:03:00:01:f6:f5:f4:f3:f2:01.
  Client copies IA_NA option from received message.
  Client copies server-id option from received message.
  Client does include client-id.
  Client sends REQUEST message.

  Pass Criteria:
  Server MUST respond with REPLY message.
  Response MUST include option 1.
  Response MUST include option 2.
  Response MUST include option 3.
  Response option 3 MUST contain sub-option 5.
  Response sub-option 5 from option 3 MUST contain address 2001:db8::1.

@v6 @kea_only @subnet-id-sanity-check @abc
  Scenario: v6.sanity.check-subnet-id-fix-del-unable
  Test Setup:
  Server is configured with 2001:db8::/64 subnet with 2001:db8::1-2001:db8::1 pool.
  Add configuration parameter id with value 666 to subnet 0 configuration.
  Add configuration parameter sanity-checks with value {"lease-checks":"fix-del"} to global configuration.
  Server has control channel on unix socket with name $(SOFTWARE_INSTALL_DIR)/var/kea/control_socket.

  Send server configuration using SSH and config-file.

  DHCP server is started.

  Test Procedure:
  Client sets DUID value to 00:03:00:01:f6:f5:f4:f3:f2:01.
  Client does include client-id.
  Client sets ia_id value to 1234567.
  Client does include IA-NA.
  Client sends SOLICIT message.

  Pass Criteria:
  Server MUST respond with ADVERTISE message.
  Response MUST include option 1.
  Response MUST include option 2.
  Response MUST include option 3.
  Response option 3 MUST contain sub-option 5.

  Test Procedure:
  Client sets DUID value to 00:03:00:01:f6:f5:f4:f3:f2:01.
  Client copies IA_NA option from received message.
  Client copies server-id option from received message.
  Client does include client-id.
  Client sends REQUEST message.

  Pass Criteria:
  Server MUST respond with REPLY message.
  Response MUST include option 1.
  Response MUST include option 2.
  Response MUST include option 3.
  Response option 3 MUST contain sub-option 5.
  Response sub-option 5 from option 3 MUST contain address 2001:db8::1.

  File stored in $(SOFTWARE_INSTALL_DIR)/var/kea/kea-leases6.csv MUST contain line or phrase: 2001:db8::1,00:03:00:01:f6:f5:f4:f3:f2:01
  File stored in $(SOFTWARE_INSTALL_DIR)/var/kea/kea-leases6.csv MUST contain line or phrase: 666,3000,0,1234567,128,0,0,,f6:f5:f4:f3:f2:01

  DHCP server is stopped.

  Clear logs.

  Test Setup:
  Server is configured with 2001:db8::/64 subnet with 2001:db8::1-2001:db8::1 pool.
  Add configuration parameter id with value 999 to subnet 0 configuration.
  Add configuration parameter sanity-checks with value {"lease-checks":"fix-del"} to global configuration.
  Server has control channel on unix socket with name $(SOFTWARE_INSTALL_DIR)/var/kea/control_socket.

  Send server configuration using SSH and config-file.

  DHCP server is started.


@v6 @kea_only @subnet-id-sanity-check @abc
  Scenario: v6.sanity.check-subnet-id-fix-del-able
  Test Setup:
  Server is configured with 2001:db8::/64 subnet with 2001:db8::1-2001:db8::1 pool.
  Add configuration parameter id with value 666 to subnet 0 configuration.
  Add configuration parameter sanity-checks with value {"lease-checks":"fix-del"} to global configuration.
  Server has control channel on unix socket with name $(SOFTWARE_INSTALL_DIR)/var/kea/control_socket.

  Send server configuration using SSH and config-file.

  DHCP server is started.

  Test Procedure:
  Client sets DUID value to 00:03:00:01:f6:f5:f4:f3:f2:01.
  Client does include client-id.
  Client sets ia_id value to 1234567.
  Client does include IA-NA.
  Client sends SOLICIT message.

  Pass Criteria:
  Server MUST respond with ADVERTISE message.
  Response MUST include option 1.
  Response MUST include option 2.
  Response MUST include option 3.
  Response option 3 MUST contain sub-option 5.

  Test Procedure:
  Client sets DUID value to 00:03:00:01:f6:f5:f4:f3:f2:01.
  Client copies IA_NA option from received message.
  Client copies server-id option from received message.
  Client does include client-id.
  Client sends REQUEST message.

  Pass Criteria:
  Server MUST respond with REPLY message.
  Response MUST include option 1.
  Response MUST include option 2.
  Response MUST include option 3.
  Response option 3 MUST contain sub-option 5.
  Response sub-option 5 from option 3 MUST contain address 2001:db8::1.

  File stored in $(SOFTWARE_INSTALL_DIR)/var/kea/kea-leases6.csv MUST contain line or phrase: 2001:db8::1,00:03:00:01:f6:f5:f4:f3:f2:01
  File stored in $(SOFTWARE_INSTALL_DIR)/var/kea/kea-leases6.csv MUST contain line or phrase: 666,3000,0,1234567,128,0,0,,f6:f5:f4:f3:f2:01


  Test Setup:
  Server is configured with 2001:db8::/64 subnet with 2001:db8::1-2001:db8::1 pool.
  Add configuration parameter id with value 999 to subnet 0 configuration.
  Add configuration parameter sanity-checks with value {"lease-checks":"fix-del"} to global configuration.
  Server has control channel on unix socket with name $(SOFTWARE_INSTALL_DIR)/var/kea/control_socket.

  Send server configuration using SSH and config-file.

  DHCP server is reconfigured.

@v6 @kea_only @subnet-id-sanity-check @abc
  Scenario: v6.sanity.check-subnet-id-warn
  Test Setup:
  Server is configured with 2001:db8::/64 subnet with 2001:db8::1-2001:db8::1 pool.
  Add configuration parameter id with value 666 to subnet 0 configuration.
  Add configuration parameter sanity-checks with value {"lease-checks":"warn"} to global configuration.
  Server has control channel on unix socket with name $(SOFTWARE_INSTALL_DIR)/var/kea/control_socket.

  Send server configuration using SSH and config-file.

  DHCP server is started.

  Test Procedure:
  Client sets DUID value to 00:03:00:01:f6:f5:f4:f3:f2:01.
  Client does include client-id.
  Client sets ia_id value to 1234567.
  Client does include IA-NA.
  Client sends SOLICIT message.

  Pass Criteria:
  Server MUST respond with ADVERTISE message.
  Response MUST include option 1.
  Response MUST include option 2.
  Response MUST include option 3.
  Response option 3 MUST contain sub-option 5.

  Test Procedure:
  Client sets DUID value to 00:03:00:01:f6:f5:f4:f3:f2:01.
  Client copies IA_NA option from received message.
  Client copies server-id option from received message.
  Client does include client-id.
  Client sends REQUEST message.

  Pass Criteria:
  Server MUST respond with REPLY message.
  Response MUST include option 1.
  Response MUST include option 2.
  Response MUST include option 3.
  Response option 3 MUST contain sub-option 5.
  Response sub-option 5 from option 3 MUST contain address 2001:db8::1.

  File stored in $(SOFTWARE_INSTALL_DIR)/var/kea/kea-leases6.csv MUST contain line or phrase: 2001:db8::1,00:03:00:01:f6:f5:f4:f3:f2:01
  File stored in $(SOFTWARE_INSTALL_DIR)/var/kea/kea-leases6.csv MUST contain line or phrase: 666,3000,0,1234567,128,0,0,,f6:f5:f4:f3:f2:01

  Test Setup:
  Server is configured with 2001:db8::/64 subnet with 2001:db8::1-2001:db8::1 pool.
  Add configuration parameter id with value 999 to subnet 0 configuration.
  Add configuration parameter sanity-checks with value {"lease-checks":"warn"} to global configuration.
  Server has control channel on unix socket with name $(SOFTWARE_INSTALL_DIR)/var/kea/control_socket.

  Send server configuration using SSH and config-file.

  DHCP server is reconfigured.

  Sleep for 2 seconds.

  File stored in $(SOFTWARE_INSTALL_DIR)/var/kea/kea.log MUST contain line or phrase: DHCPSRV_LEASE_SANITY_FAIL The lease 2001:db8::1 with subnet-id 666 failed subnet-id checks.

  Test Procedure:
  Client sets DUID value to 00:03:00:01:f6:f5:f4:f3:f2:33.
  Client does include client-id.
  Client sets ia_id value to 1234567.
  Client does include IA-NA.
  Client sends SOLICIT message.

  Pass Criteria:
  Server MUST respond with ADVERTISE message.
  Response MUST include option 1.
  Response MUST include option 2.
	Response MUST include option 3.
	Response option 3 MUST contain sub-option 13.
	Response sub-option 13 from option 3 MUST contain statuscode 2.

@v6 @kea_only @subnet-id-sanity-check @abc
  Scenario: v6.sanity.check-subnet-id-del-renew
  Test Setup:
  Server is configured with 2001:db8::/64 subnet with 2001:db8::1-2001:db8::1 pool.
  Add configuration parameter id with value 666 to subnet 0 configuration.
  Add configuration parameter sanity-checks with value {"lease-checks":"del"} to global configuration.
  Server has control channel on unix socket with name $(SOFTWARE_INSTALL_DIR)/var/kea/control_socket.

  Send server configuration using SSH and config-file.

  DHCP server is started.

  Test Procedure:
  Client sets DUID value to 00:03:00:01:f6:f5:f4:f3:f2:01.
  Client does include client-id.
  Client sets ia_id value to 1234567.
  Client does include IA-NA.
  Client sends SOLICIT message.

  Pass Criteria:
  Server MUST respond with ADVERTISE message.
  Response MUST include option 1.
  Response MUST include option 2.
  Response MUST include option 3.
  Response option 3 MUST contain sub-option 5.

  Test Procedure:
  Client sets DUID value to 00:03:00:01:f6:f5:f4:f3:f2:01.
  Client copies IA_NA option from received message.
  Client copies server-id option from received message.
  Client does include client-id.
  Client sends REQUEST message.

  Pass Criteria:
  Server MUST respond with REPLY message.
  Response MUST include option 1.
  Response MUST include option 2.
  Response MUST include option 3.
  Response option 3 MUST contain sub-option 5.
  Response sub-option 5 from option 3 MUST contain address 2001:db8::1.

  File stored in $(SOFTWARE_INSTALL_DIR)/var/kea/kea-leases6.csv MUST contain line or phrase: 2001:db8::1,00:03:00:01:f6:f5:f4:f3:f2:01
  File stored in $(SOFTWARE_INSTALL_DIR)/var/kea/kea-leases6.csv MUST contain line or phrase: 666,3000,0,1234567,128,0,0,,f6:f5:f4:f3:f2:01

  DHCP server is stopped.

  Clear logs.

  Test Setup:
  Server is configured with 2001:db8::/64 subnet with 2001:db8::1-2001:db8::1 pool.
  Add configuration parameter id with value 999 to subnet 0 configuration.
  Add configuration parameter sanity-checks with value {"lease-checks":"del"} to global configuration.
  Server has control channel on unix socket with name $(SOFTWARE_INSTALL_DIR)/var/kea/control_socket.

  Send server configuration using SSH and config-file.

  DHCP server is started.
  Sleep for 2 seconds.

  File stored in $(SOFTWARE_INSTALL_DIR)/var/kea/kea.log MUST contain line or phrase: DHCPSRV_LEASE_SANITY_FAIL_DISCARD The lease 2001:db8::1 with subnet-id 666 failed subnet-id checks and was dropped.

	Test Procedure:
  Client sets DUID value to 00:03:00:01:f6:f5:f4:f3:f2:01.
	Client copies server-id option from received message.
	Client copies IA_NA option from received message.
	Client does include client-id.
  Client sends RENEW message.

	Pass Criteria:
	Server MUST respond with REPLY message.
	Response MUST include option 1.
	Response MUST include option 2.
  Response MUST include option 3.
  Response option 3 MUST contain sub-option 5.
  Response sub-option 5 from option 3 MUST contain address 2001:db8::1.

  Test Procedure:
  Client sets DUID value to 00:03:00:01:f6:f5:f4:f3:f2:22.
  Client does include client-id.
  Client sets ia_id value to 1234567.
  Client does include IA-NA.
  Client sends SOLICIT message.

  Pass Criteria:
  Server MUST respond with ADVERTISE message.
  Response MUST include option 1.
  Response MUST include option 2.
  Response MUST include option 3.
	Response option 3 MUST contain sub-option 13.
	Response sub-option 13 from option 3 MUST contain statuscode 2.

  File stored in $(SOFTWARE_INSTALL_DIR)/var/kea/kea-leases6.csv MUST contain line or phrase: 2001:db8::1,00:03:00:01:f6:f5:f4:f3:f2:01
  File stored in $(SOFTWARE_INSTALL_DIR)/var/kea/kea-leases6.csv MUST contain line or phrase: 666,3000,0,1234567,128,0,0,,f6:f5:f4:f3:f2:01

  File stored in $(SOFTWARE_INSTALL_DIR)/var/kea/kea-leases6.csv MUST contain line or phrase: 2001:db8::1,00:03:00:01:f6:f5:f4:f3:f2:01
  File stored in $(SOFTWARE_INSTALL_DIR)/var/kea/kea-leases6.csv MUST contain line or phrase: 999,3000,0,1234567,128,0,0,,f6:f5:f4:f3:f2:01

  File stored in $(SOFTWARE_INSTALL_DIR)/var/kea/kea-leases6.csv MUST NOT contain line or phrase: 2001:db8::1,00:03:00:01:f6:f5:f4:f3:f2:22
  File stored in $(SOFTWARE_INSTALL_DIR)/var/kea/kea-leases6.csv MUST NOT contain line or phrase: 999,3000,0,1234567,128,0,0,,f6:f5:f4:f3:f2:22


@v6 @kea_only @subnet-id-sanity-check @abc
  Scenario: v6.sanity.check-subnet-id-del
  Test Setup:
  Server is configured with 2001:db8::/64 subnet with 2001:db8::1-2001:db8::1 pool.
  Add configuration parameter id with value 666 to subnet 0 configuration.
  Add configuration parameter sanity-checks with value {"lease-checks":"del"} to global configuration.
  Server has control channel on unix socket with name $(SOFTWARE_INSTALL_DIR)/var/kea/control_socket.
  Add hooks library located $(SOFTWARE_INSTALL_DIR)/lib/kea/hooks/libdhcp_lease_cmds.so.
  Send server configuration using SSH and config-file.

  DHCP server is started.

  Test Procedure:
  Client sets DUID value to 00:03:00:01:f6:f5:f4:f3:f2:01.
  Client does include client-id.
  Client sets ia_id value to 1234567.
  Client does include IA-NA.
  Client sends SOLICIT message.

  Pass Criteria:
  Server MUST respond with ADVERTISE message.
  Response MUST include option 1.
  Response MUST include option 2.
  Response MUST include option 3.
  Response option 3 MUST contain sub-option 5.

  Test Procedure:
  Client sets DUID value to 00:03:00:01:f6:f5:f4:f3:f2:01.
  Client copies IA_NA option from received message.
  Client copies server-id option from received message.
  Client does include client-id.
  Client sends REQUEST message.

  Pass Criteria:
  Server MUST respond with REPLY message.
  Response MUST include option 1.
  Response MUST include option 2.
  Response MUST include option 3.
  Response option 3 MUST contain sub-option 5.
  Response sub-option 5 from option 3 MUST contain address 2001:db8::1.

  File stored in $(SOFTWARE_INSTALL_DIR)/var/kea/kea-leases6.csv MUST contain line or phrase: 2001:db8::1,00:03:00:01:f6:f5:f4:f3:f2:01
  File stored in $(SOFTWARE_INSTALL_DIR)/var/kea/kea-leases6.csv MUST contain line or phrase: 666,3000,0,1234567,128,0,0,,f6:f5:f4:f3:f2:01

  DHCP server is stopped.

  Clear logs.

  Test Setup:
  Server is configured with 2001:db8::/64 subnet with 2001:db8::1-2001:db8::1 pool.
  Add configuration parameter id with value 999 to subnet 0 configuration.
  Add configuration parameter sanity-checks with value {"lease-checks":"del"} to global configuration.
  Server has control channel on unix socket with name $(SOFTWARE_INSTALL_DIR)/var/kea/control_socket.
  Add hooks library located $(SOFTWARE_INSTALL_DIR)/lib/kea/hooks/libdhcp_lease_cmds.so.
  Send server configuration using SSH and config-file.

  DHCP server is started.
  Sleep for 2 seconds.

  File stored in $(SOFTWARE_INSTALL_DIR)/var/kea/kea.log MUST contain line or phrase: DHCPSRV_LEASE_SANITY_FAIL_DISCARD The lease 2001:db8::1 with subnet-id 666 failed subnet-id checks and was dropped.

  Test Procedure:
  Client sets DUID value to 00:03:00:01:f6:f5:f4:f3:f2:22.
  Client does include client-id.
  Client sets ia_id value to 7654321.
  Client does include IA-NA.
  Client sends SOLICIT message.

  Pass Criteria:
  Server MUST respond with ADVERTISE message.
  Response MUST include option 1.
  Response MUST include option 2.
  Response MUST include option 3.
  Response option 3 MUST contain sub-option 5.
  Response sub-option 5 from option 3 MUST contain address 2001:db8::1.

  Test Procedure:
  Client sets DUID value to 00:03:00:01:f6:f5:f4:f3:f2:22.
  Client copies IA_NA option from received message.
  Client copies server-id option from received message.
  Client does include client-id.
  Client sends REQUEST message.

  Pass Criteria:
  Server MUST respond with REPLY message.
  Response MUST include option 1.
  Response MUST include option 2.
  Response MUST include option 3.
  Response option 3 MUST contain sub-option 5.
  Response sub-option 5 from option 3 MUST contain address 2001:db8::1.
Using UNIX socket on server in path $(SOFTWARE_INSTALL_DIR)/var/kea/control_socket send {"command":"lease6-get","arguments":{"ip-address": "2001:db8::1"}}
Using UNIX socket on server in path $(SOFTWARE_INSTALL_DIR)/var/kea/control_socket send {"command":"lease6-get","arguments":{"subnet-id":666,"identifier-type":"duid", "identifier": "00:03:00:01:f6:f5:f4:f3:f2:01"}}
  File stored in $(SOFTWARE_INSTALL_DIR)/var/kea/kea-leases6.csv MUST contain line or phrase: 2001:db8::1,00:03:00:01:f6:f5:f4:f3:f2:01
  File stored in $(SOFTWARE_INSTALL_DIR)/var/kea/kea-leases6.csv MUST contain line or phrase: 666,3000,0,1234567,128,0,0,,f6:f5:f4:f3:f2:01
#  Pause the Test.

#  File stored in $(SOFTWARE_INSTALL_DIR)/var/kea/kea-leases6.csv MUST contain line or phrase: 2001:db8::1,00:03:00:01:f6:f5:f4:f3:f2:22
#  File stored in $(SOFTWARE_INSTALL_DIR)/var/kea/kea-leases6.csv MUST contain line or phrase: 999,3000,0,1234567,128,0,0,,f6:f5:f4:f3:f2:22


@v6 @kea_only @subnet-id-sanity-check @abc
  Scenario: v6.sanity.check-subnet-id-none
  Test Setup:
  Server is configured with 2001:db8::/64 subnet with 2001:db8::1-2001:db8::1 pool.
  Add configuration parameter id with value 666 to subnet 0 configuration.
  Add configuration parameter sanity-checks with value {"lease-checks":"none"} to global configuration.
  Server has control channel on unix socket with name $(SOFTWARE_INSTALL_DIR)/var/kea/control_socket.

  Send server configuration using SSH and config-file.

  DHCP server is started.

  Test Procedure:
  Client sets DUID value to 00:03:00:01:f6:f5:f4:f3:f2:01.
  Client does include client-id.
  Client sets ia_id value to 1234567.
  Client does include IA-NA.
  Client sends SOLICIT message.

  Pass Criteria:
  Server MUST respond with ADVERTISE message.
  Response MUST include option 1.
  Response MUST include option 2.
  Response MUST include option 3.
  Response option 3 MUST contain sub-option 5.

  Test Procedure:
  Client sets DUID value to 00:03:00:01:f6:f5:f4:f3:f2:01.
  Client copies IA_NA option from received message.
  Client copies server-id option from received message.
  Client does include client-id.
  Client sends REQUEST message.

  Pass Criteria:
  Server MUST respond with REPLY message.
  Response MUST include option 1.
  Response MUST include option 2.
  Response MUST include option 3.
  Response option 3 MUST contain sub-option 5.
  Response sub-option 5 from option 3 MUST contain address 2001:db8::1.

  File stored in $(SOFTWARE_INSTALL_DIR)/var/kea/kea-leases6.csv MUST contain line or phrase: 2001:db8::1,00:03:00:01:f6:f5:f4:f3:f2:01
  File stored in $(SOFTWARE_INSTALL_DIR)/var/kea/kea-leases6.csv MUST contain line or phrase: 666,3000,0,1234567,128,0,0,,f6:f5:f4:f3:f2:01

  Test Setup:
  Server is configured with 2001:db8::/64 subnet with 2001:db8::1-2001:db8::1 pool.
  Add configuration parameter id with value 999 to subnet 0 configuration.
  Add configuration parameter sanity-checks with value {"lease-checks":"none"} to global configuration.
  Server has control channel on unix socket with name $(SOFTWARE_INSTALL_DIR)/var/kea/control_socket.

  Send server configuration using SSH and config-file.

  DHCP server is reconfigured.
  Sleep for 2 seconds.
  File stored in $(SOFTWARE_INSTALL_DIR)/var/kea/kea-leases6.csv MUST contain line or phrase: 2001:db8::1,00:03:00:01:f6:f5:f4:f3:f2:01
  File stored in $(SOFTWARE_INSTALL_DIR)/var/kea/kea-leases6.csv MUST contain line or phrase: 666,3000,0,1234567,128,0,0,,f6:f5:f4:f3:f2:01

@v6 @kea_only
  Scenario: v6.sanitydsasdasd

#  Using UNIX socket on server in path $(SOFTWARE_INSTALL_DIR)/var/kea/control_socket send {"command": "config-get","arguments":  {} }
#  Using UNIX socket on server in path $(SOFTWARE_INSTALL_DIR)/var/kea/control_socket send {"command": "list-commands","arguments":  {} }

  Test Procedure:
  Client sets DUID value to 00:03:00:01:f6:f5:f4:f3:f2:01.
  Client does include client-id.
  Client sets ia_id value to 1234567.
  Client does include IA-NA.
  Client sends SOLICIT message.

  Pass Criteria:
  Server MUST respond with ADVERTISE message.
  Response MUST include option 1.
  Response MUST include option 2.
  Response MUST include option 3.
  Response option 3 MUST contain sub-option 5.

  Test Procedure:
  Client sets DUID value to 00:03:00:01:f6:f5:f4:f3:f2:01.
  Client copies IA_NA option from received message.
  Client copies server-id option from received message.
  Client does include client-id.
  Client sends REQUEST message.

  Pass Criteria:
  Server MUST respond with REPLY message.
  Response MUST include option 1.
  Response MUST include option 2.
  Response MUST include option 3.
  Response option 3 MUST contain sub-option 5.
  Response sub-option 5 from option 3 MUST contain address 2001:db8::1.

  Test Setup:
  Server is configured with 2001:db8::/64 subnet with 2001:db8::1-2001:db8::1 pool.
  Add configuration parameter id with value 888 to subnet 0 configuration.
  Add configuration parameter sanity-checks with value {"lease-checks":"fix"} to global configuration.
  Server has control channel on unix socket with name $(SOFTWARE_INSTALL_DIR)/var/kea/control_socket.

  Send server configuration using SSH and config-file.

  DHCP server is started.

  Sleep for 5 seconds.

  Test Procedure:
  Client sets DUID value to 00:03:00:01:f6:f5:f4:f3:f2:22.
  Client does include client-id.
  Client sets ia_id value to 1234567.
  Client does include IA-NA.
  Client sends SOLICIT message.

  Pass Criteria:
  Server MUST respond with ADVERTISE message.
  Response MUST include option 1.
  Response MUST include option 2.
  Response MUST include option 3.
  Response option 3 MUST contain sub-option 5.


@v6 @sharednetworks @sharedsubnets @kea_only
  Scenario: v6.sanity-check-subnet-id
  Test Setup:
  Server is configured with 2001:db8::/64 subnet with 2001:db8::1-2001:db8::1 pool.
  Add configuration parameter id with value 666 to subnet 0 configuration.
  Add configuration parameter sanity-checks with value {"lease-checks":"fix"} to global configuration.
  Server has control channel on unix socket with name $(SOFTWARE_INSTALL_DIR)/var/kea/control_socket.

  Send server configuration using SSH and config-file.

  DHCP server is started.

  Using UNIX socket on server in path $(SOFTWARE_INSTALL_DIR)/var/kea/control_socket send {"command": "config-get","arguments":  {} }
  Using UNIX socket on server in path $(SOFTWARE_INSTALL_DIR)/var/kea/control_socket send {"command": "list-commands","arguments":  {} }

  Test Procedure:
  Client sets DUID value to 00:03:00:01:f6:f5:f4:f3:f2:01.
  Client does include client-id.
  Client sets ia_id value to 1234567.
  Client does include IA-NA.
  Client sends SOLICIT message.

  Pass Criteria:
  Server MUST respond with ADVERTISE message.
  Response MUST include option 1.
  Response MUST include option 2.
  Response MUST include option 3.
  Response option 3 MUST contain sub-option 5.

  Test Procedure:
  Client sets DUID value to 00:03:00:01:f6:f5:f4:f3:f2:01.
  Client copies IA_NA option from received message.
  Client copies server-id option from received message.
  Client does include client-id.
  Client sends REQUEST message.

  Pass Criteria:
  Server MUST respond with REPLY message.
  Response MUST include option 1.
  Response MUST include option 2.
  Response MUST include option 3.
  Response option 3 MUST contain sub-option 5.
  Response sub-option 5 from option 3 MUST contain address 2001:db8::1.

  File stored in $(SOFTWARE_INSTALL_DIR)/var/kea/kea-leases6.csv MUST contain line or phrase: 2001:db8::1,00:03:00:01:f6:f5:f4:f3:f2:01
  File stored in $(SOFTWARE_INSTALL_DIR)/var/kea/kea-leases6.csv MUST contain line or phrase: 666,3000,0,1234567,128,0,0,,f6:f5:f4:f3:f2:01

  DHCP server is stopped.

  Test Setup:
  Server is configured with 2001:db8::/64 subnet with 2001:db8::1-2001:db8::2 pool.
  Add configuration parameter id with value 888 to subnet 0 configuration.
  Add configuration parameter sanity-checks with value {"lease-checks":"fix-del"} to global configuration.
  Server has control channel on unix socket with name $(SOFTWARE_INSTALL_DIR)/var/kea/control_socket.

  Send server configuration using SSH and config-file.

  DHCP server is started.

  Sleep for 12 seconds.

  Test Setup:
  Server is configured with 2001:db8::/64 subnet with 2001:db8::1-2001:db8::2 pool.
  Add configuration parameter id with value 999 to subnet 0 configuration.
  Add configuration parameter sanity-checks with value {"lease-checks":"fix-del"} to global configuration.
  Server has control channel on unix socket with name $(SOFTWARE_INSTALL_DIR)/var/kea/control_socket.

  Send server configuration using SSH and config-file.

  DHCP server is reconfigured.
  Sleep for 12 seconds.

#  Using UNIX socket on server in path $(SOFTWARE_INSTALL_DIR)/var/kea/control_socket send {"command": "config-get","arguments":  {} }

  Test Procedure:
  Client sets DUID value to 00:03:00:01:f6:f5:f4:f3:f2:22.
  Client does include client-id.
  Client sets ia_id value to 1234567.
  Client does include IA-NA.
  Client sends SOLICIT message.

  Pass Criteria:
  Server MUST respond with ADVERTISE message.
  Response MUST include option 1.
  Response MUST include option 2.
  Response MUST include option 3.
  Response option 3 MUST contain sub-option 5.

  Test Procedure:
  Client sets DUID value to 00:03:00:01:f6:f5:f4:f3:f2:22.
  Client copies IA_NA option from received message.
  Client copies server-id option from received message.
  Client does include client-id.
  Client sends REQUEST message.

  Pass Criteria:
  Server MUST respond with REPLY message.
  Response MUST include option 1.
  Response MUST include option 2.
  Response MUST include option 3.
  Response option 3 MUST contain sub-option 5.
  Response sub-option 5 from option 3 MUST contain address 2001:db8::2.
  Sleep for 10 seconds.

#  Using UNIX socket on server in path $(SOFTWARE_INSTALL_DIR)/var/kea/control_socket send {"command": "config-get","arguments":  {} }

  Test Procedure:
  Client sets DUID value to 00:03:00:01:f6:f5:f4:f3:f2:33.
  Client does include client-id.
  Client sets ia_id value to 1234567.
  Client does include IA-NA.
  Client sends SOLICIT message.

  Pass Criteria:
  Server MUST respond with ADVERTISE message.
  Response MUST include option 1.
  Response MUST include option 2.
	Response MUST include option 3.
	Response option 3 MUST contain sub-option 13.
	Response sub-option 13 from option 3 MUST contain statuscode 2.
#  Response option 3 MUST contain sub-option 5.
#  Response sub-option 5 from option 3 MUST contain address 2001:db8::2.

#Pause the Test.

@v6 @sharednetworks @sharedsubnets @kea_only
  Scenario: v6.sanity-check-shared-subnet-id
  Test Setup:
  Server is configured with 2001:db8:a::/64 subnet with 2001:db8:a::1-2001:db8:a::1 pool.
  Add configuration parameter id with value 666 to subnet 0 configuration.
  Server is configured with another subnet: 2001:db8:b::/64 with 2001:db8:b::1-2001:db8:b::1 pool.
  Add configuration parameter id with value 777 to subnet 1 configuration.
  Add subnet 0 to shared-subnet set 0.
  Add subnet 1 to shared-subnet set 0.
  Add configuration parameter name with value "name-abc" to shared-subnet 0 configuration.
  Add configuration parameter interface with value "$(SERVER_IFACE)" to shared-subnet 0 configuration.
  Add configuration parameter sanity-checks with value {"lease-checks":"fix-del"} to global configuration.
  Server has control channel on unix socket with name $(SOFTWARE_INSTALL_DIR)/var/kea/control_socket.
  Send server configuration using SSH and config-file.

  DHCP server is started.

  Using UNIX socket on server in path $(SOFTWARE_INSTALL_DIR)/var/kea/control_socket send {"command": "config-get","arguments":  {} }

  Test Procedure:
  Client sets DUID value to 00:03:00:01:f6:f5:f4:f3:f2:01.
  Client does include client-id.
  Client sets ia_id value to 1234567.
  Client does include IA-NA.
  Client sends SOLICIT message.

  Pass Criteria:
  Server MUST respond with ADVERTISE message.
  Response MUST include option 1.
  Response MUST include option 2.
  Response MUST include option 3.
  Response option 3 MUST contain sub-option 5.

  Test Procedure:
  Client sets DUID value to 00:03:00:01:f6:f5:f4:f3:f2:01.
  Client copies IA_NA option from received message.
  Client copies server-id option from received message.
  Client does include client-id.
  Client sends REQUEST message.

  Pass Criteria:
  Server MUST respond with REPLY message.
  Response MUST include option 1.
  Response MUST include option 2.
  Response MUST include option 3.
  Response option 3 MUST contain sub-option 5.
  #Response sub-option 5 from option 3 MUST contain address 2001:db8:a::1.

  Test Procedure:
  Client sets DUID value to 00:03:00:01:f6:f5:f4:f3:f2:02.
  Client sets ia_id value to 7654321.
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
  Client sets DUID value to 00:03:00:01:f6:f5:f4:f3:f2:02.
  Client copies IA_NA option from received message.
  Client copies server-id option from received message.
  Client does include client-id.
  Client sends REQUEST message.

  Pass Criteria:
  Server MUST respond with REPLY message.
  Response MUST include option 1.
  Response MUST include option 2.
  Response MUST include option 3.
  Response option 3 MUST contain sub-option 5.

  File stored in $(SOFTWARE_INSTALL_DIR)/var/kea/kea-leases6.csv MUST contain line or phrase: 2001:db8:a::1,00:03:00:01:f6:f5:f4:f3:f2:01
  File stored in $(SOFTWARE_INSTALL_DIR)/var/kea/kea-leases6.csv MUST contain line or phrase: 666,3000,0,1234567,128,0,0,,f6:f5:f4:f3:f2:01
  File stored in $(SOFTWARE_INSTALL_DIR)/var/kea/kea-leases6.csv MUST contain line or phrase: 2001:db8:b::1,00:03:00:01:f6:f5:f4:f3:f2:02
  File stored in $(SOFTWARE_INSTALL_DIR)/var/kea/kea-leases6.csv MUST contain line or phrase: 777,3000,0,7654321,128,0,0,,f6:f5:f4:f3:f2:02

  Test Setup:
  Server is configured with 2001:db8:a::/64 subnet with 2001:db8:a::1-2001:db8:a::1 pool.
  Add configuration parameter id with value 888 to subnet 0 configuration.
  Server is configured with another subnet: 2001:db8:b::/64 with 2001:db8:b::1-2001:db8:b::1 pool.
  Add configuration parameter id with value 999 to subnet 1 configuration.
  Add subnet 0 to shared-subnet set 0.
  Add subnet 1 to shared-subnet set 0.
  Add configuration parameter name with value "name-abc" to shared-subnet 0 configuration.
  Add configuration parameter interface with value "$(SERVER_IFACE)" to shared-subnet 0 configuration.
  Add configuration parameter sanity-checks with value {"lease-checks":"fix"} to global configuration.
  Server has control channel on unix socket with name $(SOFTWARE_INSTALL_DIR)/var/kea/control_socket.
  Send server configuration using SSH and config-file.

  DHCP server is reconfigured.

  Sleep for 10 seconds.










